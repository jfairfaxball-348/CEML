"""Run the launcher's whole elevated path against stand-ins for the firewall and scheduler.

The first real elevated attempt (2026-10-12) failed, safely, on a bug that no
unelevated test could reach. This file closes that gap as far as it can be closed
without administrator rights: the real launcher text is executed unchanged except
that the administrator check is forced true and every firewall and scheduler
cmdlet is shadowed by a function that keeps its state in a temporary folder. The
helper it calls is a small fake as well. Nothing here touches the real firewall,
the real scheduler or the network, with or without elevation.

A simulation shows that the script's own logic, names, ordering and failure
handling are right. It does not show how Windows itself behaves; only the real
OS-blocked run does that.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools/l1/run_offline_acceptance.ps1"
ADMIN = ("$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(\n"
         "    [Security.Principal.WindowsBuiltInRole]::Administrator)\n")
ANCHOR = "Set-StrictMode -Version Latest\n$ErrorActionPreference = 'Stop'\n"
SOURCE = "5" * 64
# Every command in the launcher whose verb can change state. The four that would
# touch the firewall or the scheduler are exactly the ones the prelude shadows.
ALLOWED = {"New-Item", "New-NetFirewallRule", "New-ScheduledTaskAction", "New-ScheduledTaskPrincipal",
           "New-ScheduledTaskSettingsSet", "New-ScheduledTaskTrigger", "New-TimeSpan", "Out-Null",
           "Register-ScheduledTask", "Remove-NetFirewallRule", "Set-StrictMode", "Start-Process",
           "Start-Sleep", "Unregister-ScheduledTask", "Write-Output"}
SHADOWED = ("Get-NetFirewallProfile", "Get-NetFirewallRule", "Get-NetFirewallSecurityFilter",
            "Get-NetFirewallApplicationFilter", "Get-NetFirewallAddressFilter", "Get-NetFirewallPortFilter",
            "New-NetFirewallRule", "Remove-NetFirewallRule", "Register-ScheduledTask", "Get-ScheduledTask",
            "Unregister-ScheduledTask")

PRELUDE = r'''
# ---- simulation prelude: stand-ins for the firewall and scheduler cmdlets ----
# Both real modules are imported FIRST. Their commands are module functions, and a
# module that auto-loads later would replace same-named functions defined here, so
# the real Register-ScheduledTask would run. Importing now makes that impossible,
# and Sim-AssertShadow proves each stand-in is what the name resolves to.
Import-Module NetSecurity -ErrorAction Stop
Import-Module ScheduledTasks -ErrorAction Stop
$SimDir = Join-Path $PSScriptRoot '../../sim'
function Sim-AssertShadow {
    foreach ($name in @('Get-NetFirewallProfile', 'Get-NetFirewallRule', 'Get-NetFirewallSecurityFilter',
            'Get-NetFirewallApplicationFilter', 'Get-NetFirewallAddressFilter', 'Get-NetFirewallPortFilter',
            'New-NetFirewallRule', 'Remove-NetFirewallRule', 'Register-ScheduledTask', 'Get-ScheduledTask',
            'Unregister-ScheduledTask')) {
        $command = Get-Command -Name $name -ErrorAction Stop
        if ([string]$command.CommandType -ne 'Function' -or $command.ModuleName) {
            throw ('simulation stand-in is not in effect for ' + $name)
        }
    }
}
function Sim-Log([string]$Text) { Add-Content -LiteralPath (Join-Path $SimDir 'log.txt') -Value $Text -Encoding ASCII }
function Sim-Flag([string]$Name) { return (Test-Path -LiteralPath (Join-Path $SimDir ('flag-' + $Name))) }
function Sim-Rules {
    $items = @(Get-ChildItem -LiteralPath (Join-Path $SimDir 'rules') -Filter '*.json')
    foreach ($item in $items) { Get-Content -LiteralPath $item.FullName -Raw | ConvertFrom-Json }
}
function Get-NetFirewallProfile {
    [CmdletBinding()] param([string]$PolicyStore)
    # First call of every prerequisite and isolation check: re-prove the stand-ins each time.
    Sim-AssertShadow
    foreach ($index in 1..3) { [pscustomobject]@{ Enabled = 1; AllowLocalFirewallRules = 1 } }
}
function Get-NetFirewallRule {
    [CmdletBinding()] param([string]$PolicyStore, [string]$Name, [string]$Enabled, [string]$Action, [string]$Group)
    if (Sim-Flag 'enumeration-fails') { throw 'simulated firewall query failure' }
    if ($Action -eq 'Allow') { return }
    $rules = @(Sim-Rules)
    if ($Name) {
        $rules = @($rules | Where-Object { $_.Name -eq $Name })
        if ($rules.Count -eq 0) { throw 'simulated: no rule with that name' }
    }
    $rules
}
function Get-NetFirewallSecurityFilter {
    [CmdletBinding()] param([Parameter(ValueFromPipeline = $true)]$InputObject)
    process { }
}
function Get-NetFirewallApplicationFilter {
    [CmdletBinding()] param([Parameter(ValueFromPipeline = $true)]$InputObject)
    process { [pscustomobject]@{ Program = $InputObject.Program } }
}
function Get-NetFirewallAddressFilter {
    [CmdletBinding()] param([Parameter(ValueFromPipeline = $true)]$InputObject)
    process { [pscustomobject]@{ LocalAddress = $InputObject.LocalAddress; RemoteAddress = $InputObject.RemoteAddress } }
}
function Get-NetFirewallPortFilter {
    [CmdletBinding()] param([Parameter(ValueFromPipeline = $true)]$InputObject)
    process { [pscustomobject]@{ Protocol = $InputObject.Protocol } }
}
function New-NetFirewallRule {
    [CmdletBinding()] param([string]$PolicyStore, [string]$Name, [string]$DisplayName, [string]$Group,
        [string]$Enabled, [string]$Profile, [string]$Direction, [string]$Action, [string]$Program,
        [string]$Protocol, [string]$LocalAddress, [string]$RemoteAddress)
    if ($Name -notmatch '^CEML-L1Offline-[0-9a-f]{32}-(Inbound|Outbound)$') { throw ('simulated: unexpected rule name ' + $Name) }
    $path = Join-Path (Join-Path $SimDir 'rules') ($Name + '.json')
    if (Test-Path -LiteralPath $path) { throw 'simulated: duplicate rule' }
    $rule = [pscustomobject]@{ Name = $Name; DisplayName = $DisplayName; Group = $Group; Enabled = 1;
        Profile = $Profile; Direction = $Direction; Action = $Action; PrimaryStatus = 'OK'; Program = $Program;
        Protocol = $Protocol; LocalAddress = $LocalAddress; RemoteAddress = $RemoteAddress; PolicyStore = $PolicyStore }
    $rule | ConvertTo-Json | Set-Content -LiteralPath $path -Encoding ASCII
    Sim-Log ('new-rule ' + $Name)
    $rule
}
function Remove-NetFirewallRule {
    [CmdletBinding()] param([string]$PolicyStore, [string]$Name, [Parameter(ValueFromPipeline = $true)]$InputObject)
    process {
        if (Sim-Flag 'removal-fails') { throw 'simulated removal failure' }
        $target = if ($null -ne $InputObject) { $InputObject.Name } else { $Name }
        $path = Join-Path (Join-Path $SimDir 'rules') ($target + '.json')
        if (!(Test-Path -LiteralPath $path)) { throw 'simulated: no rule with that name' }
        Remove-Item -LiteralPath $path
        Sim-Log ('remove-rule ' + $target)
    }
}
function Register-ScheduledTask {
    [CmdletBinding()] param([string]$TaskName, $Action, $Trigger, $Principal, $Settings)
    if ($TaskName -notmatch '^CEML-L1Offline-[0-9a-f]{32}-Restore$') { throw 'simulated: unexpected task name' }
    $path = Join-Path (Join-Path $SimDir 'tasks') ($TaskName + '.txt')
    Set-Content -LiteralPath $path -Value $Action.Arguments -Encoding ASCII
    Sim-Log ('register-task ' + $TaskName + ' triggers=' + @($Trigger).Count + ' user=' + $Principal.UserId)
    [pscustomobject]@{ TaskName = $TaskName }
}
function Get-ScheduledTask {
    [CmdletBinding()] param([string]$TaskName)
    if (Sim-Flag 'task-query-fails') { throw 'simulated scheduler query failure' }
    $tasks = @(Get-ChildItem -LiteralPath (Join-Path $SimDir 'tasks') -Filter '*.txt' |
        ForEach-Object { [pscustomobject]@{ TaskName = $_.BaseName } })
    if ($TaskName) {
        $tasks = @($tasks | Where-Object { $_.TaskName -eq $TaskName })
        if ($tasks.Count -eq 0) { throw 'simulated: no such task' }
    }
    $tasks
}
function Unregister-ScheduledTask {
    [CmdletBinding(SupportsShouldProcess = $true)] param([string]$TaskName)
    $path = Join-Path (Join-Path $SimDir 'tasks') ($TaskName + '.txt')
    if (!(Test-Path -LiteralPath $path)) { throw 'simulated: no such task' }
    Remove-Item -LiteralPath $path
    Sim-Log ('unregister-task ' + $TaskName)
}
Sim-AssertShadow
# ---- end of simulation prelude ----
'''

FAKE_HELPER = r'''
"""Stand-in for offline_acceptance.py inside the launcher simulation. It runs nothing real."""
import json
from pathlib import Path
import sys

sim = Path(__file__).resolve().parents[2] / "sim"
scenario = json.loads((sim / "scenario.json").read_text(encoding="ascii"))
mode = sys.argv[1]


def flag(name):
    return (sim / ("flag-" + name)).exists()


if mode == "--plan":
    print(json.dumps({"scope": "SIMULATION", "source_sha256": scenario["source"], "python_version": "3.12.10"}))
    sys.exit(0)
if mode == "--probe":
    with (sim / "log.txt").open("a", encoding="ascii") as log:
        log.write("probe\n")
    blocked = any(json.loads(path.read_text(encoding="utf-8-sig"))["Direction"] == "Outbound"
                  for path in (sim / "rules").glob("*.json"))
    connected = not flag("network-down") and (not blocked or flag("blocking-ineffective"))
    print(json.dumps({"connected": connected}))
    sys.exit(0 if connected else 2)
if mode == "--run":
    out = Path(sys.argv[sys.argv.index("--output-dir") + 1])
    source = sys.argv[sys.argv.index("--expected-source") + 1]
    with (sim / "log.txt").open("a", encoding="ascii") as log:
        log.write("child-run\n")
    for name in scenario["flags_at_child"]:
        (sim / ("flag-" + name)).write_bytes(b"")
    (out / "checks.json").write_text(json.dumps({"status": scenario["checks_status"], "source_sha256": source}),
                                     encoding="ascii")
    sys.exit(scenario["child_exit"])
sys.exit(9)
'''


@unittest.skipUnless(os.name == "nt", "Windows launcher")
class LauncherSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = LAUNCHER.read_bytes().decode("ascii").replace("\r\n", "\n")

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(dir=ROOT / "local/frontier", prefix="launcher-sim-")
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.sim = self.root / "sim"
        for name in ("sim/rules", "sim/tasks", "tools/l1", "local/frontier"):
            (self.root / name).mkdir(parents=True)
        (self.sim / "log.txt").write_bytes(b"")
        self.assertEqual((1, 1), (self.text.count(ADMIN), self.text.count(ANCHOR)))
        simulated = self.text.replace(ADMIN, "$admin = $true\n").replace(ANCHOR, ANCHOR + PRELUDE)
        self.script = self.root / "tools/l1/run_offline_acceptance.ps1"
        self.script.write_bytes(simulated.encode("ascii"))
        (self.root / "tools/l1/offline_acceptance.py").write_bytes(FAKE_HELPER.encode("ascii"))
        self.scenario()

    def scenario(self, child_exit=0, checks_status="ENGINEERING-CHECKS-PASS", flags_at_child=()):
        (self.sim / "scenario.json").write_text(json.dumps(dict(
            source=SOURCE, child_exit=child_exit, checks_status=checks_status,
            flags_at_child=list(flags_at_child))), encoding="ascii")

    def flag(self, name, present=True):
        path = self.sim / ("flag-" + name)
        if present:
            path.write_bytes(b"")
        elif path.exists():
            path.unlink()

    def powershell(self, script, *arguments):
        shell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
        return subprocess.run([str(shell), "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                               "-File", str(script), *arguments], capture_output=True, timeout=300)

    def launch(self, mode="Run", source=SOURCE, launcher=None):
        arguments = ["-Mode", mode, "-PythonPath", sys.executable]
        if mode == "Run":
            arguments += ["-ExpectedSourceSha256", source, "-ExpectedLauncherSha256",
                          launcher or hashlib.sha256(self.script.read_bytes()).hexdigest()]
        result = self.powershell(self.script, *arguments)
        lines = [line for line in result.stdout.decode("ascii", "replace").splitlines() if line.startswith("{")]
        record = json.loads(lines[-1]) if lines else None
        return result.returncode, record, result.stderr.decode("ascii", "replace")

    def log(self):
        return (self.sim / "log.txt").read_text(encoding="ascii").split()

    def events(self):
        return [line for line in (self.sim / "log.txt").read_text(encoding="ascii").splitlines() if line]

    def rules(self):
        return sorted(path.stem for path in (self.sim / "rules").glob("*.json"))

    def tasks(self):
        return sorted(path.stem for path in (self.sim / "tasks").glob("*.txt"))

    def evidence(self):
        folder = self.root / "local/frontier/os-offline"
        return sorted(folder.iterdir()) if folder.is_dir() else []

    def watchdog(self, task):
        """Decode the registered watchdog command and run it against the same stand-ins."""
        arguments = (self.sim / "tasks" / (task + ".txt")).read_text(encoding="ascii").strip()
        self.assertTrue(arguments.startswith("-NoProfile -NonInteractive -EncodedCommand "))
        text = base64.b64decode(arguments.split()[-1]).decode("utf-16-le")
        path = self.root / "tools/l1/watchdog_sim.ps1"
        path.write_bytes((PRELUDE + text).encode("ascii"))
        return self.powershell(path).returncode, text

    def test_only_shadowed_commands_can_change_firewall_or_scheduler_state(self):
        verbs = "New|Remove|Set|Register|Unregister|Enable|Disable|Start|Stop|Add|Clear|Invoke|Restart|Rename|Move|Copy|Out|Write"
        used = set(re.findall(r"\b(?:%s)-[A-Za-z]+" % verbs, self.text))
        self.assertEqual(ALLOWED, used)
        for name in SHADOWED:
            self.assertEqual(1, PRELUDE.count("function " + name + " {"), name)
        for name in used & {"New-NetFirewallRule", "Remove-NetFirewallRule", "Register-ScheduledTask",
                            "Unregister-ScheduledTask"}:
            self.assertIn(name, SHADOWED)
        self.assertNotIn("\\", PRELUDE)

    def real_state(self):
        """Names of real CEML rules and tasks, read with the real cmdlets. Read-only."""
        path = self.root / "real_state.ps1"
        path.write_bytes(
            b"$ErrorActionPreference = 'Stop'\n"
            b"$rules = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop |\n"
            b"    Where-Object { $_.Name -like 'CEML-L1Offline-*' } | ForEach-Object { 'rule ' + $_.Name })\n"
            b"$tasks = @(Get-ScheduledTask -ErrorAction Stop |\n"
            b"    Where-Object { $_.TaskName -like 'CEML-L1Offline-*' } | ForEach-Object { 'task ' + $_.TaskName })\n"
            b"'checked'\n@($rules + $tasks) | Sort-Object\n")
        result = self.powershell(path)
        self.assertEqual(0, result.returncode, result.stderr.decode("ascii", "replace"))
        lines = result.stdout.decode("ascii").split("\n")
        self.assertEqual("checked", lines[0].strip())
        return [line.strip() for line in lines[1:] if line.strip()]

    def test_complete_run_blocks_verifies_restores_and_reports_pass(self):
        # The stand-ins must be the only thing the simulation touches: the real stores are
        # read before and after and must be identical (during the real OS-blocked run they
        # hold the outer launcher's own two rules and task, unchanged by this test).
        real_before = self.real_state()
        code, record, stderr = self.launch()
        self.assertEqual(real_before, self.real_state())
        self.assertEqual(0, code, stderr)
        self.assertEqual(("OS-BLOCKED-ENGINEERING-CHECKS-PASS", "completed", "0", "", "NOT_RUN", SOURCE),
                         (record["status"], record["last_stage"], record["child_exit_code"],
                          record["failure_kind"], record["scientific_execution"], record["source_sha256"]))
        for key in ("connected_baseline", "os_rules_verified", "rules_removed", "watchdog_removed",
                    "connected_after_restore", "checks_passed"):
            self.assertIs(True, record[key], key)
        events = self.events()
        created = [line.split()[1] for line in events if line.startswith("new-rule ")]
        # The defect of the first elevated attempt: these must be two names, not one joined string.
        self.assertEqual(2, len(created))
        prefix = created[0][:-len("-Inbound")]
        self.assertRegex(prefix, r"^CEML-L1Offline-[0-9a-f]{32}$")
        self.assertEqual([prefix + "-Inbound", prefix + "-Outbound"], created)
        order = [events.index(line) for line in (
            "probe", "register-task " + prefix + "-Restore triggers=2 user=SYSTEM", "new-rule " + created[0],
            "new-rule " + created[1], "child-run", "remove-rule " + created[0], "remove-rule " + created[1],
            "unregister-task " + prefix + "-Restore")]
        self.assertEqual(sorted(order), order)
        # Probes: baseline, blocked, blocked again after the child, reconnected after restoration.
        self.assertEqual(4, events.count("probe"))
        self.assertLess(events.index("remove-rule " + created[1]),
                        len(events) - 1 - events[::-1].index("probe"))
        self.assertEqual(([], []), (self.rules(), self.tasks()))
        folder, = self.evidence()
        self.assertEqual(prefix, "CEML-L1Offline-" + folder.name)
        self.assertEqual(record, json.loads((folder / "isolation.json").read_text(encoding="ascii")))
        self.assertTrue((folder / "checks.json").is_file())

    def test_preflight_changes_nothing_and_wrong_hashes_or_leftovers_refuse_first(self):
        code, record, _ = self.launch("Preflight")
        self.assertEqual((0, "PREPARED-NOT-EXECUTED", "NOT_RUN"),
                         (code, record["status"], record["os_isolated_acceptance"]))
        for arguments in (dict(source="0" * 64), dict(launcher="0" * 64)):
            code, record, _ = self.launch(**arguments)
            self.assertNotEqual(0, code)
            self.assertIsNone(record)
        self.assertEqual([], self.events())
        leftover = "CEML-L1Offline-" + "a" * 32 + "-Outbound"
        (self.sim / "rules" / (leftover + ".json")).write_text(json.dumps(dict(
            Name=leftover, Direction="Inbound")), encoding="ascii")
        code, record, stderr = self.launch()
        self.assertNotEqual(0, code)
        self.assertIn("earlier run", stderr)
        self.assertEqual(([], [leftover], [], []), (self.events(), self.rules(), self.tasks(), self.evidence()))

    def test_failed_baseline_refuses_before_any_change(self):
        self.flag("network-down")
        code, record, stderr = self.launch()
        self.assertNotEqual(0, code)
        self.assertIsNone(record)
        self.assertIn("baseline", stderr)
        self.assertEqual((["probe"], [], [], []), (self.events(), self.rules(), self.tasks(), self.evidence()))

    def assert_failed_but_restored(self, stage, **expected):
        code, record, stderr = self.launch()
        self.assertEqual(2, code, stderr)
        self.assertEqual(("FAIL", stage), (record["status"], record["last_stage"]))
        for key in ("connected_baseline", "rules_removed", "watchdog_removed", "connected_after_restore"):
            self.assertIs(True, record[key], key)
        self.assertIs(False, record["checks_passed"])
        for key, value in expected.items():
            self.assertEqual(value, record[key], key)
        self.assertEqual(([], []), (self.rules(), self.tasks()))
        self.assertEqual(2, sum(line.startswith("remove-rule ") for line in self.events()))
        return record

    def test_ineffective_blocking_is_a_failure_and_is_cleaned_up(self):
        self.flag("blocking-ineffective")
        self.assert_failed_but_restored("blocked-probe", os_rules_verified=False, child_exit_code="")
        self.assertNotIn("child-run", self.events())

    def test_failing_child_or_incomplete_evidence_is_a_failure_and_is_cleaned_up(self):
        self.scenario(child_exit=2)
        self.assert_failed_but_restored("child-exit-code", os_rules_verified=True, child_exit_code="2")
        (self.sim / "log.txt").write_bytes(b"")
        self.scenario(checks_status="FAIL")
        self.assert_failed_but_restored("evidence-check", os_rules_verified=True, child_exit_code="0")

    def test_removal_failure_keeps_the_watchdog_which_then_finishes_the_job(self):
        self.scenario(flags_at_child=["removal-fails"])
        code, record, stderr = self.launch()
        self.assertEqual(2, code, stderr)
        self.assertEqual(("FAIL", "CleanupFailed-WatchdogRetained", False, False, False),
                         (record["status"], record["failure_kind"], record["rules_removed"],
                          record["watchdog_removed"], record["connected_after_restore"]))
        self.assertEqual(2, len(self.rules()))
        task, = self.tasks()
        code, text = self.watchdog(task)
        self.assertEqual((1, 2, [task]), (code, len(self.rules()), self.tasks()))
        for name in self.rules():
            self.assertIn("'" + name + "'", text)
        self.flag("removal-fails", False)
        code, _ = self.watchdog(task)
        self.assertEqual((0, [], []), (code, self.rules(), self.tasks()))

    def test_failed_enumeration_still_removes_rules_by_name_and_keeps_the_watchdog(self):
        self.scenario(flags_at_child=["enumeration-fails"])
        code, record, stderr = self.launch()
        self.assertEqual(2, code, stderr)
        self.assertEqual(("FAIL", "final-isolation-verification", "CleanupFailed-WatchdogRetained", False, False),
                         (record["status"], record["last_stage"], record["failure_kind"],
                          record["rules_removed"], record["watchdog_removed"]))
        # The rules are gone although absence could not be verified, so nothing was claimed.
        self.assertEqual([], self.rules())
        task, = self.tasks()
        code, _ = self.watchdog(task)
        self.assertEqual((1, [task]), (code, self.tasks()))
        self.flag("enumeration-fails", False)
        code, _ = self.watchdog(task)
        self.assertEqual((0, [], []), (code, self.rules(), self.tasks()))

    def test_no_reconnection_keeps_the_watchdog_although_rules_are_verified_absent(self):
        self.scenario(flags_at_child=["network-down"])
        code, record, stderr = self.launch()
        self.assertEqual(2, code, stderr)
        self.assertEqual(("FAIL", "completed", True, True, False, False),
                         (record["status"], record["last_stage"], record["checks_passed"],
                          record["rules_removed"], record["connected_after_restore"], record["watchdog_removed"]))
        self.assertEqual([], self.rules())
        task, = self.tasks()
        code, _ = self.watchdog(task)
        self.assertEqual((0, []), (code, self.tasks()))


if __name__ == "__main__":
    unittest.main()
