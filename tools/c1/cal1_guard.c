/* Stage: hardware characterization. Resource guard for bounded CEML-CAL-1 cases
 * under the revised local ceilings (docs/C1_RESOURCE_CEILINGS_V2.md).
 *
 * The child is created suspended and joins a non-inherited kill-on-close Job
 * (256 MiB process and job memory, one active process, one logical processor)
 * before it runs. Memory, storage, AC and sleep-index checks run at every
 * polling boundary. Paging rates use intervals of at least one second.
 * Any page output, or page input above the ceiling in two consecutive
 * intervals, refuses or aborts; one isolated input excursion is recorded only.
 * A processor-performance reading below nominal at an interval invalidates. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <powrprof.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <psapi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CASE_MS 5000
#define INPUT_CEILING 100.0

typedef struct { ULONGLONG available, free_storage; double input, output, performance; } Observation;
static PDH_HQUERY query;
static PDH_HCOUNTER input_counter, output_counter, performance_counter;
static ULONGLONG pressure_sample_at;
static double sampled_input, sampled_output, sampled_performance = -1.0, maximum_input, minimum_performance = -1.0;
static int performance_available, consecutive_high, excursions, intervals;

static int counter_value(PDH_HCOUNTER counter, double *value) {
    PDH_FMT_COUNTERVALUE result;
    if (PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &result) != ERROR_SUCCESS ||
        (result.CStatus != PDH_CSTATUS_VALID_DATA && result.CStatus != PDH_CSTATUS_NEW_DATA)) return 0;
    *value = result.doubleValue;
    return *value >= 0;
}

static const char *observe(Observation *value) {
    MEMORYSTATUSEX memory = {0};
    SYSTEM_POWER_STATUS power;
    ULARGE_INTEGER free_bytes;
    GUID *scheme = NULL;
    DWORD standby_ac, standby_dc, hibernate_ac, hibernate_dc;
    DWORD status = ERROR_SUCCESS;
    memory.dwLength = sizeof(memory);
    if (!GlobalMemoryStatusEx(&memory) || !GetDiskFreeSpaceExW(L".", &free_bytes, NULL, NULL) ||
        !GetSystemPowerStatus(&power)) return "required-monitor-unavailable";
    value->available = memory.ullAvailPhys; value->free_storage = free_bytes.QuadPart;
    if (value->available < 4ULL*1024*1024*1024 || value->free_storage < 16ULL*1024*1024*1024)
        return "headroom-breach";
    if (power.ACLineStatus != 1) return "ac-power-unavailable";
    if (PowerGetActiveScheme(NULL, &scheme) != ERROR_SUCCESS || !scheme) return "power-policy-unavailable";
    status |= PowerReadACValueIndex(NULL, scheme, &GUID_SLEEP_SUBGROUP, &GUID_STANDBY_TIMEOUT, &standby_ac);
    status |= PowerReadDCValueIndex(NULL, scheme, &GUID_SLEEP_SUBGROUP, &GUID_STANDBY_TIMEOUT, &standby_dc);
    status |= PowerReadACValueIndex(NULL, scheme, &GUID_SLEEP_SUBGROUP, &GUID_HIBERNATE_TIMEOUT, &hibernate_ac);
    status |= PowerReadDCValueIndex(NULL, scheme, &GUID_SLEEP_SUBGROUP, &GUID_HIBERNATE_TIMEOUT, &hibernate_dc);
    LocalFree(scheme);
    if (status != ERROR_SUCCESS) return "power-policy-unavailable";
    if (standby_ac || standby_dc || hibernate_ac || hibernate_dc) return "sleep-policy-refusal";
    if (GetTickCount64() - pressure_sample_at >= 1000) {
        if (PdhCollectQueryData(query) != ERROR_SUCCESS || !counter_value(input_counter, &sampled_input) ||
            !counter_value(output_counter, &sampled_output)) return "pressure-monitor-unavailable";
        if (performance_available && !counter_value(performance_counter, &sampled_performance))
            return "performance-monitor-unavailable";
        pressure_sample_at = GetTickCount64();
        ++intervals;
        if (sampled_input > maximum_input) maximum_input = sampled_input;
        if (sampled_input > INPUT_CEILING) { ++consecutive_high; ++excursions; } else consecutive_high = 0;
        if (performance_available && (minimum_performance < 0 || sampled_performance < minimum_performance))
            minimum_performance = sampled_performance;
    }
    value->input = sampled_input; value->output = sampled_output; value->performance = sampled_performance;
    if (sampled_output != 0.0) return "paging-output";
    if (consecutive_high >= 2) return "paging-input-sustained";
    if (performance_available && intervals && sampled_performance < 100.0) return "processor-performance-below-nominal";
    return NULL;
}

static ULONGLONG time_value(FILETIME value) {
    return ((ULONGLONG)value.dwHighDateTime << 32) | value.dwLowDateTime;
}

static void performance_text(char *text, size_t size, double value) {
    if (value < 0) strcpy_s(text, size, "null"); else sprintf_s(text, size, "\"%.0f\"", value);
}

int main(int argc, char **argv) {
    HANDLE job = NULL;
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION limits = {0};
    STARTUPINFOA startup = {0};
    PROCESS_INFORMATION process = {0};
    PROCESS_MEMORY_COUNTERS memory = {0};
    Observation first = {0}, second = {0}, last = {0};
    DWORD_PTR process_affinity, system_affinity;
    char command[1024], application[32768], minimum_text[32], final_text[32];
    char *last_separator;
    const char *reason = NULL, *abort_code = "C1_RESOURCE_ABORT";
    LARGE_INTEGER frequency = {0}, begin = {0}, end = {0};
    FILETIME created = {0}, exited = {0}, kernel = {0}, user_time = {0};
    wchar_t path[96];
    DWORD exit_code = 0, waited;
    ULONGLONG elapsed_ms;
    size_t used;
    int aborted = 0, a;
    int pressure_only = argc == 2 && strcmp(argv[1], "--pressure-check") == 0;
    if (!pressure_only) {
        if (argc < 3 || argc > 14) return 2;
        if (strcmp(argv[1], "cal1_case.exe") && strcmp(argv[1], "cal1_case_checked.exe") &&
            strcmp(argv[1], "ckpt_case.exe")) return 2;
        used = (size_t)sprintf_s(command, sizeof(command), "%s --calibration-only", argv[1]);
        for (a = 2; a < argc; ++a) {
            const char *c;
            if (!argv[a][0] || strlen(argv[a]) > 40) return 2;
            for (c = argv[a]; *c; ++c) if (!((*c >= 'a' && *c <= 'z') || (*c >= '0' && *c <= '9') || *c == '-')) return 2;
            used += (size_t)sprintf_s(command + used, sizeof(command) - used, " %s", argv[a]);
        }
    }
    swprintf_s(path, 96, L"%cMemory%cPages Input%csec", 92, 92, 47);
    if (PdhOpenQueryW(NULL, 0, &query) != ERROR_SUCCESS ||
        PdhAddEnglishCounterW(query, path, 0, &input_counter) != ERROR_SUCCESS) reason = "pressure-monitor-unavailable";
    swprintf_s(path, 96, L"%cMemory%cPages Output%csec", 92, 92, 47);
    if (!reason && PdhAddEnglishCounterW(query, path, 0, &output_counter) != ERROR_SUCCESS) reason = "pressure-monitor-unavailable";
    swprintf_s(path, 96, L"%cProcessor Information(_Total)%c%% Processor Performance", 92, 92);
    if (!reason) performance_available = PdhAddEnglishCounterW(query, path, 0, &performance_counter) == ERROR_SUCCESS;
    if (!reason && PdhCollectQueryData(query) != ERROR_SUCCESS) reason = "pressure-monitor-unavailable";
    pressure_sample_at = GetTickCount64();
    if (!reason) { Sleep(1000); reason = observe(&first); last = first; }
    if (!reason) { Sleep(1000); reason = observe(&second); last = second; }
    if (reason) {
        printf("{\"kind\":\"guard\",\"abort_code\":\"C1_PREFLIGHT_REFUSAL\",\"reason\":\"%s\","
               "\"available_bytes\":\"%llu\",\"pages_input_rounded\":\"%.0f\",\"pages_output_rounded\":\"%.0f\"}\n",
               reason, last.available, last.input, last.output);
        if (query) PdhCloseQuery(query);
        return 10;
    }
    if (pressure_only) {
        performance_text(final_text, sizeof(final_text), second.performance);
        printf("{\"kind\":\"pressure_check\",\"ok\":true,\"samples\":\"2\","
               "\"first_pages_input_rounded\":\"%.0f\",\"second_pages_input_rounded\":\"%.0f\","
               "\"pages_output_rounded\":\"%.0f\",\"available_bytes\":\"%llu\",\"processor_performance_percent\":%s}\n",
               first.input, second.input, second.output, second.available, final_text);
        PdhCloseQuery(query); return 0;
    }
    job = CreateJobObjectW(NULL, NULL);
    if (!job || !GetProcessAffinityMask(GetCurrentProcess(), &process_affinity, &system_affinity)) return 11;
    limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | JOB_OBJECT_LIMIT_PROCESS_MEMORY |
        JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_AFFINITY;
    limits.BasicLimitInformation.ActiveProcessLimit = 1;
    limits.BasicLimitInformation.Affinity = process_affinity & (~process_affinity + 1);
    limits.ProcessMemoryLimit = 256*1024*1024; limits.JobMemoryLimit = 256*1024*1024;
    if (!SetInformationJobObject(job, JobObjectExtendedLimitInformation, &limits, sizeof(limits))) return 11;
    if (!GetModuleFileNameA(NULL, application, sizeof(application))) return 11;
    last_separator = strrchr(application, '\\');
    if (!last_separator) return 11;
    strcpy_s(last_separator + 1, sizeof(application) - (size_t)(last_separator + 1 - application), argv[1]);
    startup.cb = sizeof(startup);
    startup.dwFlags = STARTF_USESTDHANDLES;
    startup.hStdInput = GetStdHandle(STD_INPUT_HANDLE);
    startup.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    startup.hStdError = GetStdHandle(STD_ERROR_HANDLE);
    if (!QueryPerformanceFrequency(&frequency) || !QueryPerformanceCounter(&begin) ||
        !CreateProcessA(application, command, NULL, NULL, TRUE, CREATE_SUSPENDED | CREATE_NO_WINDOW,
                        NULL, NULL, &startup, &process)) return 11;
    if (!AssignProcessToJobObject(job, process.hProcess) || ResumeThread(process.hThread) == (DWORD)-1) {
        TerminateProcess(process.hProcess, 11); CloseHandle(process.hThread); CloseHandle(process.hProcess);
        CloseHandle(job); PdhCloseQuery(query); return 11;
    }
    CloseHandle(process.hThread);
    do {
        waited = WaitForSingleObject(process.hProcess, 100);
        if (!QueryPerformanceCounter(&end)) { reason = "timer-unavailable"; break; }
        elapsed_ms = (ULONGLONG)((end.QuadPart - begin.QuadPart)*1000/frequency.QuadPart);
        if (waited == WAIT_OBJECT_0) {
            ULONGLONG age = GetTickCount64() - pressure_sample_at;
            if (age < 1000) Sleep((DWORD)(1000 - age));
        }
        reason = observe(&last);
        if (reason || waited == WAIT_FAILED || (waited == WAIT_TIMEOUT && elapsed_ms >= CASE_MS)) {
            if (!reason) reason = waited == WAIT_FAILED ? "process-monitor-unavailable" : "case-timeout";
            break;
        }
    } while (waited == WAIT_TIMEOUT);
    if (reason) {
        aborted = 1; TerminateJobObject(job, 12); WaitForSingleObject(process.hProcess, 1000);
        if (strcmp(reason, "processor-performance-below-nominal") == 0) abort_code = "C1_ENVIRONMENT_INVALID";
        else if (strstr(reason, "unavailable")) abort_code = "C1_MEASUREMENT_INVALID";
    }
    if (!GetExitCodeProcess(process.hProcess, &exit_code) ||
        !GetProcessTimes(process.hProcess, &created, &exited, &kernel, &user_time) ||
        !GetProcessMemoryInfo(process.hProcess, &memory, sizeof(memory))) {
        aborted = 1; reason = "measurement-unavailable"; abort_code = "C1_MEASUREMENT_INVALID";
    }
    performance_text(minimum_text, sizeof(minimum_text), minimum_performance);
    performance_text(final_text, sizeof(final_text), last.performance);
    printf("{\"kind\":\"guard\",\"abort_code\":%s%s%s,\"reason\":\"%s\",\"exit_code\":\"%lu\","
           "\"process_wall_ticks\":\"%lld\",\"qpc_frequency\":\"%lld\",",
           aborted ? "\"" : "", aborted ? abort_code : "null", aborted ? "\"" : "", reason ? reason : "none", exit_code,
           (long long)(end.QuadPart - begin.QuadPart), (long long)frequency.QuadPart);
    if (aborted) printf("\"cpu_time_ns\":null,\"peak_rss_bytes\":null,");
    else printf("\"cpu_time_ns\":\"%llu\",\"peak_rss_bytes\":\"%llu\",",
                (time_value(kernel) + time_value(user_time))*100, (ULONGLONG)memory.PeakWorkingSetSize);
    printf("\"available_bytes\":\"%llu\",\"free_storage_bytes\":\"%llu\",\"pressure_intervals\":\"%d\","
           "\"pages_input_excursion_intervals\":\"%d\",\"maximum_pages_input_rounded\":\"%.0f\","
           "\"final_pages_input_rounded\":\"%.0f\",\"final_pages_output_rounded\":\"%.0f\","
           "\"minimum_processor_performance_percent\":%s,\"final_processor_performance_percent\":%s}\n",
           last.available, last.free_storage, intervals, excursions, maximum_input, last.input, last.output,
           minimum_text, final_text);
    CloseHandle(process.hProcess); CloseHandle(job); PdhCloseQuery(query);
    return aborted ? 12 : exit_code ? 13 : 0;
}
