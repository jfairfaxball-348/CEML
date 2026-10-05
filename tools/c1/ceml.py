"""C1 orchestration commands of the I1 command surface (section 15).

  hardware-report   run the narrow audit collectors, then assemble and scan the reports
  calibrate         run one bounded CEML-CAL-1 family on the production executable
  decide            derive the decision log from retained evidence (no new evidence)
  build-profile     pinned offline engine build, then build manifest and machine profile

These commands are permitted only while PROGRAM_STATUS.md names C1 and denies
scientific execution. They accept no seed, start, size or work parameter.
self-test, status, verify, checkpoint, resume, validate, prepare and run are
commands of the engine executable itself and carry their own gates.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from gmp_setup import ROOT, Refusal, require_authorization

FAMILIES = ('route-crossover', 'small-block-sweep', 'hierarchical-sweep', 'backend-multiplication', 'representation',
            'allocation', 'compiler-build', 'terminal-handoff', 'audit-cost', 'memory-scaling')


def python(*arguments):
    return subprocess.run([sys.executable, '-B', *arguments], cwd=ROOT).returncode


def powershell(script, *arguments):
    return subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script, *arguments], cwd=ROOT).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    report = commands.add_parser('hardware-report')
    report.add_argument('--audit-run', required=True)
    calibrate = commands.add_parser('calibrate')
    calibrate.add_argument('--run-id', required=True)
    calibrate.add_argument('--family', required=True, choices=FAMILIES + ('checkpoint-durability', 'checkpoint-performance'))
    calibrate.add_argument('--resume-after-refusal', action='store_true')
    commands.add_parser('decide')
    commands.add_parser('build-profile')
    args = parser.parse_args()
    require_authorization()                     # C1 phase with scientific execution denied, or refuse
    if args.command == 'hardware-report':
        code = powershell('tools/c1/collect_windows.ps1', '-AuditRun', args.audit_run) or \
            powershell('tools/c1/collect_tools.ps1', '-AuditRun', args.audit_run)
        print('Collected. Assemble with: python tools/c1/c1_report.py --evidence final (audit run fixed in that tool).')
        return code
    if args.command == 'calibrate':
        if args.family == 'checkpoint-durability':
            return python('tools/c1/ckpt_suite.py', 'matrix', '--engine', '--run-id', args.run_id)
        if args.family == 'checkpoint-performance':
            return python('tools/c1/ckpt_suite.py', 'performance', '--engine', '--run-id', args.run_id)
        extra = ['--resume-after-refusal'] if args.resume_after_refusal else []
        return python('tools/c1/cal1_suite.py', '--engine', '--run-id', args.run_id, '--family', args.family, *extra)
    if args.command == 'decide':
        return python('tools/c1/c1_report.py', '--evidence', 'final')
    return python('tools/c1/engine_build.py') or python('tools/c1/c1_profile.py') or python('tools/c1/c1_profile.py', 'verify')


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Refusal as error:
        print('REFUSED:', error)
        sys.exit(1)
