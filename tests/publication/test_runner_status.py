"""Observer liveness regression tests; no scientific process is started or signalled."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/publication'))
import runner_status as status
import live


class DetectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'control.json'
        self.lock=Path(self.tmp.name)/'lock'
        self.control=dict(token='a'*32,active=True,started_at='2026-10-13T09:00:00+00:00',mode='continuous',requested=None,initial_end='100')
        self.started=datetime.fromisoformat(self.control['started_at']).timestamp()
        self.now=self.started+100
        self.owner=dict(pid=12345,ticks=int((self.started-0.1+11644473600)*1e7))
        self.save()

    def save(self):self.path.write_text(json.dumps(self.control),encoding='ascii')
    def tearDown(self):self.tmp.cleanup()
    def detect(self):return status.detect(self.now,self.path,self.lock)

    def test_hidden_command_line_does_not_matter(self):
        with patch.object(status,'lock_busy',return_value=True),patch.object(status,'lock_users',return_value=[self.owner]),patch.object(live,'active_runner',side_effect=AssertionError('no command-line query')):
            runner,source=self.detect()
        self.assertEqual(runner,source);self.assertEqual(source['initial_end'],'100')

    def test_stale_active_flag_without_lock_is_not_running(self):
        with patch.object(status,'lock_busy',return_value=False),patch.object(status,'lock_users') as users:
            runner,source=self.detect()
        self.assertIsNone(runner);self.assertTrue(source['stale_active']);users.assert_not_called()

    def test_publication_lock_holder_born_after_session_is_not_runner(self):
        newer=dict(self.owner,ticks=int((self.started+10+11644473600)*1e7))
        with patch.object(status,'lock_busy',return_value=True),patch.object(status,'lock_users',return_value=[newer]):self.assertIsNone(self.detect()[0])

    def test_pid_reuse_or_exit_between_queries_is_not_running(self):
        newer=dict(self.owner,ticks=self.owner['ticks']+100)
        for second in ([],[newer]):
            with patch.object(status,'lock_busy',return_value=True),patch.object(status,'lock_users',side_effect=[[self.owner],second]):self.assertIsNone(self.detect()[0])

    def test_uncertainty_is_never_stopped_or_idle(self):
        for owners in ([],[self.owner,self.owner],[dict(self.owner,ticks=self.owner['ticks']-1000*10**7)]):
            with patch.object(status,'lock_busy',return_value=True),patch.object(status,'lock_users',return_value=owners):
                with self.assertRaises(status.UnknownLiveness):self.detect()
        with patch.object(status,'lock_busy',return_value=True),patch.object(status,'lock_users',side_effect=PermissionError('private')):
            with self.assertRaises(status.UnknownLiveness):self.detect()

    def test_inactive_control_retains_session_without_liveness_query(self):
        self.control['active']=False;self.save()
        with patch.object(status,'lock_busy') as busy:runner,source=self.detect()
        self.assertIsNone(runner);self.assertFalse(source['stale_active']);busy.assert_not_called()

    def test_missing_control_with_busy_lock_is_unknown(self):
        self.path.unlink()
        with patch.object(status,'lock_busy',return_value=True):
            with self.assertRaises(status.UnknownLiveness):self.detect()
        with patch.object(status,'lock_busy',return_value=False):self.assertEqual(self.detect(),(None,None))

    def test_invalid_control_and_future_clock_refuse(self):
        for data in ('{torn','{}',json.dumps(dict(self.control,active=1)),json.dumps(dict(self.control,requested='12'))):
            self.path.write_text(data)
            with self.assertRaises(status.UnknownLiveness):self.detect()
        self.save()
        with self.assertRaises(status.UnknownLiveness):status.detect(self.started-10,self.path,self.lock)

    def test_control_change_retries_without_merging_sessions(self):
        changed=dict(self.control,token='b'*32,active=False)
        with patch.object(status,'read_control',side_effect=[self.control,changed,changed,changed]),patch.object(status,'lock_busy',return_value=False):runner,source=self.detect()
        self.assertIsNone(runner);self.assertFalse(source['stale_active'])

    def test_observe_preserves_details_when_liveness_unknown(self):
        observed=dict(state='stopped',schema_version=1,updated_at='x',session={'completed':4},recent_batches=[{'number':1}])
        with patch.object(live,'detect',side_effect=status.UnknownLiveness({'started':0})),patch.object(live,'snapshot',return_value=observed):value,_=live.observe(None)
        self.assertEqual(value['state'],'error');self.assertEqual(value['session']['completed'],4)

    @unittest.skipUnless(os.name=='nt','Windows kernel regression')
    def test_real_lock_holder_observation_never_signals_or_waits_for_lock(self):
        self.lock.write_bytes(b'0')
        program="import msvcrt,sys;f=open(sys.argv[1],'r+b');msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1);print('ready',flush=True);sys.stdin.readline()"
        process=subprocess.Popen([sys.executable,'-c',program,str(self.lock)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
        try:
            self.assertEqual(process.stdout.readline().strip(),'ready');self.assertTrue(status.lock_busy(self.lock))
            owners=status.lock_users(self.lock)
            self.assertEqual([owner['pid'] for owner in owners],[process.pid]);self.assertTrue(status.same_lock_user(owners[0],self.lock));self.assertIsNone(process.poll())
        finally:
            process.stdin.write('\n');process.stdin.flush();process.wait(timeout=5);process.stdin.close();process.stdout.close()
        self.assertFalse(status.lock_busy(self.lock));self.assertEqual(self.lock.read_bytes(),b'0')


if __name__=='__main__':unittest.main()
