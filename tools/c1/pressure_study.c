/* Stage: hardware characterization. Bounded monitor-method observation only.
 * No arithmetic, calibration case or trajectory. It samples the same PDH
 * paging-rate proxy as cal_guard over one-second intervals: first with no
 * child, then with one arithmetic-free child launch per interval. The child
 * is cal_candidate.exe given a refused argument list, so it loads its image
 * and dependency and exits before any GMP call. Output is numeric only. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <stdio.h>
#include <string.h>

#define IDLE_SAMPLES 20
#define LAUNCH_SAMPLES 10

static PDH_HQUERY query;
static PDH_HCOUNTER input_counter, output_counter, reads_counter, performance_counter;
static int performance_available;

static int read_counter(PDH_HCOUNTER counter, double *value) {
    PDH_FMT_COUNTERVALUE result;
    if (PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &result) != ERROR_SUCCESS ||
        (result.CStatus != PDH_CSTATUS_VALID_DATA && result.CStatus != PDH_CSTATUS_NEW_DATA)) return 0;
    *value = result.doubleValue;
    return 1;
}

static int sample(const char *phase, int index, unsigned long launches) {
    MEMORYSTATUSEX memory = {0};
    double input, output, reads, performance = -1.0;
    memory.dwLength = sizeof(memory);
    if (PdhCollectQueryData(query) != ERROR_SUCCESS || !read_counter(input_counter, &input) ||
        !read_counter(output_counter, &output) || !read_counter(reads_counter, &reads) ||
        !GlobalMemoryStatusEx(&memory)) return 0;
    if (performance_available && !read_counter(performance_counter, &performance)) performance = -1.0;
    printf("{\"kind\":\"sample\",\"phase\":\"%s\",\"index\":\"%d\",\"launches\":\"%lu\","
           "\"pages_input_milli\":\"%.0f\",\"pages_output_milli\":\"%.0f\",\"page_reads_milli\":\"%.0f\","
           "\"available_bytes\":\"%llu\",\"processor_performance_milli\":%s%.0f%s}\n",
           phase, index, launches, input*1000.0, output*1000.0, reads*1000.0, memory.ullAvailPhys,
           performance < 0 ? "" : "\"", performance < 0 ? 0.0 : performance*1000.0,
           performance < 0 ? "" : "\"");
    return 1;
}

static int null_launch(const char *application) {
    STARTUPINFOA startup = {0};
    PROCESS_INFORMATION process = {0};
    char command[] = "cal_candidate.exe --arithmetic-free-launch";
    DWORD code = 0;
    startup.cb = sizeof(startup);
    if (!CreateProcessA(application, command, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &startup, &process))
        return 0;
    CloseHandle(process.hThread);
    if (WaitForSingleObject(process.hProcess, 5000) != WAIT_OBJECT_0) {
        TerminateProcess(process.hProcess, 9); CloseHandle(process.hProcess); return 0;
    }
    GetExitCodeProcess(process.hProcess, &code);
    CloseHandle(process.hProcess);
    return code == 2; /* the candidate's fixed argument refusal, before any arithmetic */
}

int main(void) {
    wchar_t path[96];
    char application[32768], *separator;
    int i;
    if (PdhOpenQueryW(NULL, 0, &query) != ERROR_SUCCESS) return 3;
    swprintf_s(path, 96, L"%cMemory%cPages Input%csec", 92, 92, 47);
    if (PdhAddEnglishCounterW(query, path, 0, &input_counter) != ERROR_SUCCESS) return 3;
    swprintf_s(path, 96, L"%cMemory%cPages Output%csec", 92, 92, 47);
    if (PdhAddEnglishCounterW(query, path, 0, &output_counter) != ERROR_SUCCESS) return 3;
    swprintf_s(path, 96, L"%cMemory%cPage Reads%csec", 92, 92, 47);
    if (PdhAddEnglishCounterW(query, path, 0, &reads_counter) != ERROR_SUCCESS) return 3;
    swprintf_s(path, 96, L"%cProcessor Information(_Total)%c%% Processor Performance", 92, 92);
    performance_available = PdhAddEnglishCounterW(query, path, 0, &performance_counter) == ERROR_SUCCESS;
    if (!GetModuleFileNameA(NULL, application, sizeof(application))) return 3;
    separator = strrchr(application, '\\');
    if (!separator) return 3;
    strcpy_s(separator+1, sizeof(application)-(size_t)(separator+1-application), "cal_candidate.exe");
    if (PdhCollectQueryData(query) != ERROR_SUCCESS) return 3;
    printf("{\"kind\":\"study\",\"idle_samples\":\"%d\",\"launch_samples\":\"%d\",\"interval_ms\":\"1000\","
           "\"processor_performance_counter\":%s}\n", IDLE_SAMPLES, LAUNCH_SAMPLES,
           performance_available ? "true" : "false");
    for (i = 0; i < IDLE_SAMPLES; ++i) { Sleep(1000); if (!sample("idle", i, 0)) return 4; }
    for (i = 0; i < LAUNCH_SAMPLES; ++i) {
        Sleep(500);
        if (!null_launch(application)) return 5;
        Sleep(500);
        if (!sample("arithmetic-free-launch", i, 1)) return 4;
    }
    for (i = 0; i < 5; ++i) { Sleep(1000); if (!sample("idle-after", i, 0)) return 4; }
    PdhCloseQuery(query);
    return 0;
}
