/* Stage: hardware characterization. Resource guard for the fixed native subset.
 * A suspended child joins a non-inherited kill-on-close Job before execution. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <powrprof.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <psapi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { ULONGLONG available, free_storage; double input, output; } Observation;
static PDH_HQUERY query;
static PDH_HCOUNTER input_counter, output_counter;
static ULONGLONG pressure_sample_at;
static double sampled_input, sampled_output;

static int pressure_counter(PDH_HCOUNTER counter, double *value) {
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
    /* Rate comparisons use intervals of at least one second throughout. */
    if (GetTickCount64()-pressure_sample_at >= 1000) {
        if (PdhCollectQueryData(query) != ERROR_SUCCESS || !pressure_counter(input_counter, &sampled_input) ||
            !pressure_counter(output_counter, &sampled_output)) return "pressure-monitor-unavailable";
        pressure_sample_at = GetTickCount64();
    }
    value->input = sampled_input; value->output = sampled_output;
    if (!(value->input <= 100.0 && value->output == 0.0)) return "paging-pressure";
    return NULL;
}

static ULONGLONG time_value(FILETIME value) {
    return ((ULONGLONG)value.dwHighDateTime << 32) | value.dwLowDateTime;
}

int main(int argc, char **argv) {
    HANDLE job = NULL;
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION limits = {0};
    STARTUPINFOA startup = {0};
    PROCESS_INFORMATION process = {0};
    PROCESS_MEMORY_COUNTERS memory = {0};
    Observation first = {0}, second = {0}, last = {0};
    DWORD_PTR process_affinity, system_affinity;
    char command[1400], application[32768];
    char *last_separator;
    const char *reason = NULL;
    LARGE_INTEGER frequency = {0}, begin = {0}, end = {0};
    FILETIME created = {0}, exited = {0}, kernel = {0}, user_time = {0};
    wchar_t input_path[80], output_path[80];
    DWORD exit_code = 0, waited;
    ULONGLONG elapsed_ms;
    size_t i, length;
    int aborted = 0;
    int pressure_only = argc == 2 && strcmp(argv[1], "--pressure-check") == 0;
    if (!pressure_only && (argc != 3 || (strcmp(argv[1], "t-direct") && strcmp(argv[1], "affine-small-public")))) return 2;
    length = pressure_only ? 256 : strlen(argv[2]);
    if (length != 256 && length != 1024) return 2;
    for (i=0; !pressure_only && i<length; ++i) if (!((argv[2][i]>='0' && argv[2][i]<='9') ||
        (argv[2][i]>='a' && argv[2][i]<='f'))) return 2;
    swprintf_s(input_path, 80, L"%cMemory%cPages Input%csec", 92, 92, 47);
    swprintf_s(output_path, 80, L"%cMemory%cPages Output%csec", 92, 92, 47);
    if (PdhOpenQueryW(NULL, 0, &query) != ERROR_SUCCESS ||
        PdhAddEnglishCounterW(query, input_path, 0, &input_counter) != ERROR_SUCCESS ||
        PdhAddEnglishCounterW(query, output_path, 0, &output_counter) != ERROR_SUCCESS ||
        PdhCollectQueryData(query) != ERROR_SUCCESS) reason = "pressure-monitor-unavailable";
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
        printf("{\"kind\":\"pressure_check\",\"ok\":true,\"samples\":\"2\","
               "\"first_pages_input\":\"%.3f\",\"second_pages_input\":\"%.3f\","
               "\"pages_output\":\"%.3f\",\"available_bytes\":\"%llu\"}\n",
               first.input, second.input, second.output, second.available);
        PdhCloseQuery(query); return 0;
    }
    job = CreateJobObjectW(NULL, NULL);
    if (!job || !GetProcessAffinityMask(GetCurrentProcess(), &process_affinity, &system_affinity)) return 11;
    limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | JOB_OBJECT_LIMIT_PROCESS_MEMORY |
        JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_ACTIVE_PROCESS | JOB_OBJECT_LIMIT_AFFINITY;
    limits.BasicLimitInformation.ActiveProcessLimit = 1;
    limits.BasicLimitInformation.Affinity = process_affinity & (~process_affinity+1);
    limits.ProcessMemoryLimit = 256*1024*1024; limits.JobMemoryLimit = 256*1024*1024;
    if (!SetInformationJobObject(job, JobObjectExtendedLimitInformation, &limits, sizeof(limits))) return 11;
    if (!GetModuleFileNameA(NULL, application, sizeof(application))) return 11;
    last_separator = strrchr(application, '\\');
    if (!last_separator || strlen(last_separator) < strlen("\\cal_guard.exe")) return 11;
    strcpy_s(last_separator+1, sizeof(application)-(size_t)(last_separator+1-application), "cal_candidate.exe");
    if (sprintf_s(command, sizeof(command), "cal_candidate.exe --calibration-only %s %s", argv[1], argv[2]) < 0) return 11;
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
        elapsed_ms = (ULONGLONG)((end.QuadPart-begin.QuadPart)*1000/frequency.QuadPart);
        if (waited == WAIT_OBJECT_0) {
            ULONGLONG age = GetTickCount64()-pressure_sample_at;
            if (age < 1000) Sleep((DWORD)(1000-age));
        }
        reason = observe(&last);
        if (reason || waited == WAIT_FAILED || elapsed_ms >= 5000) {
            if (!reason) reason = elapsed_ms >= 5000 ? "case-timeout" : "process-monitor-unavailable";
            break;
        }
    } while (waited == WAIT_TIMEOUT);
    if (reason) { aborted = 1; TerminateJobObject(job, 12); WaitForSingleObject(process.hProcess, 1000); }
    if (!GetExitCodeProcess(process.hProcess, &exit_code) ||
        !GetProcessTimes(process.hProcess, &created, &exited, &kernel, &user_time) ||
        !GetProcessMemoryInfo(process.hProcess, &memory, sizeof(memory))) {
        aborted = 1; reason = "measurement-unavailable";
    }
    printf("{\"kind\":\"guard\",\"abort_code\":%s,\"reason\":\"%s\",\"exit_code\":\"%lu\","
           "\"process_wall_ticks\":\"%lld\",\"qpc_frequency\":\"%lld\",\"cpu_time_ns\":\"%llu\","
           "\"peak_rss_bytes\":\"%llu\",\"available_bytes\":\"%llu\",\"free_storage_bytes\":\"%llu\","
           "\"preflight_pages_input_rounded\":\"%.0f\",\"final_pages_input_rounded\":\"%.0f\","
           "\"final_pages_output_rounded\":\"%.0f\",\"preflight_samples\":\"2\",\"scratch_bytes\":\"0\"}\n",
           aborted ? "\"C1_RESOURCE_ABORT\"" : "null", reason ? reason : "none", exit_code,
           (long long)(end.QuadPart-begin.QuadPart), (long long)frequency.QuadPart,
           aborted ? 0 : (time_value(kernel)+time_value(user_time))*100,
           aborted ? 0 : (ULONGLONG)memory.PeakWorkingSetSize, last.available, last.free_storage,
           second.input, last.input, last.output);
    CloseHandle(process.hProcess); CloseHandle(job); PdhCloseQuery(query);
    return aborted ? 12 : exit_code ? 13 : 0;
}
