"""Publication boundaries and observer fixtures; no scientific execution or network."""
import importlib.util
from contextlib import nullcontext
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/publication'))
import live
import publish


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.contents = {p: (ROOT / p).read_text(encoding='utf-8') for p in publish.FILES}
        self.data = publish.website_progress.build(self.contents['docs/RUN1_PROGRESS.md'])
        self.certificates = [dict(batch_start=b['start'], batch_end=b['end'], digest=b['certificate_digest'],
                                  counts={k: '0' for k in publish.KEYS}, explicit_t_steps='0',
                                  explicit_odd_steps='0', explicit_standard_steps='0') for b in self.data['batches']]
        self.certificates[0]['counts'] = dict(zip(publish.KEYS, (str(v) for v in self.data['rule_counts'].values())))
        self.ledger = dict(batches=str(len(self.certificates)), end=self.data['coverage']['end'],
                           latest_certificate_digest=self.data['latest_certificate_digest'])

    def derive(self):
        return publish.derive_files(self.contents, self.certificates, self.ledger, 'a'*40, '2026-10-12T18:00:00Z')

    def test_already_published_does_not_make_a_new_commit(self):
        self.assertEqual(self.derive(), {})

    def test_preview_emits_its_own_status_without_network_or_publishing(self):
        ledger={**self.ledger, 'status':'conditional_chain'}
        output=StringIO()
        with patch.object(sys,'argv',['publish.py','--preview']), patch.object(publish,'git',return_value=''), patch.object(publish.operator,'operator_lock',return_value=nullcontext()), patch.object(publish,'verify_chain',return_value=(ledger,self.certificates)), patch.object(publish,'stamp',return_value='2026-10-12T00:00:00Z'), patch.object(publish,'api') as api, patch.object(publish,'publish') as uploader, patch('sys.stdout',output):
            self.assertEqual(publish.main(),0)
        self.assertEqual(json.loads(output.getvalue())['status'],'PUBLICATION_PREVIEW')
        api.assert_not_called(); uploader.assert_not_called()

    def test_rollback_and_changed_published_prefix_are_refused(self):
        self.certificates.pop()
        with self.assertRaises(publish.PublicationError): self.derive()
        self.setUp()
        self.certificates[0]['digest'] = 'a'*64
        with self.assertRaises(publish.PublicationError): self.derive()

    def test_new_publication_preserves_history_and_updates_feed(self):
        old_end = self.ledger['end']
        c = dict(self.certificates[-1], batch_start=old_end, batch_end=str(int(old_end)+4), digest='a'*64,
                 counts=dict(zip(publish.KEYS, ('2','1','0','0','0','1'))))
        self.certificates.append(c)
        self.ledger.update(batches=str(len(self.certificates)), end=c['batch_end'], latest_certificate_digest=c['digest'])
        files = self.derive()
        self.assertEqual(set(files), set(publish.FILES))
        data = json.loads(files['frontier_progress_for_website.json'])
        self.assertEqual(data['batches'][:-1], self.data['batches'])
        self.assertEqual(int(data['coverage']['integers']), int(self.data['coverage']['integers'])+4)
        self.assertIn("The owner's 1000000-integer continuation", files['docs/RUN1_PROGRESS.md'])
        self.assertNotIn('local/frontier/run1/', json.dumps(data))

    def test_gap_in_new_batch_is_refused(self):
        old_end = self.ledger['end']
        self.certificates.append(dict(self.certificates[-1], batch_start=str(int(old_end)+1), batch_end=str(int(old_end)+5), digest='a'*64))
        self.ledger.update(batches=str(len(self.certificates)), end=str(int(old_end)+5), latest_certificate_digest='a'*64)
        with self.assertRaises(publish.website_progress.PublicationError): self.derive()

    def test_github_never_bypasses_a_failed_check(self):
        calls=[]
        def api(endpoint, method='GET', body=None):
            calls.append((endpoint, method))
            if '/git/commits/' in endpoint: return {'tree': {'sha': 'base'}}
            if endpoint.endswith('/pulls'): return {'html_url':'https://github.com/example/pull/1','number':1}
            if endpoint.endswith('/pulls/1'): return {'mergeable':True, 'head':{'sha':'head'}}
            if endpoint.endswith('/status'): return {'total_count':1, 'state':'failure'}
            if endpoint.endswith('/check-runs'): return {'check_runs':[]}
            return {}
        with tempfile.TemporaryDirectory() as tmp, patch.object(publish, 'ROOT', Path(tmp)), patch.object(publish, 'api', api), patch.object(publish, 'commit_files', return_value='head'):
            (Path(tmp)/'local/frontier').mkdir(parents=True)
            with self.assertRaises(publish.PublicationError): publish.publish({'x':'y'}, 'base', self.ledger)
        self.assertFalse(any(e.endswith('/merge') for e,_ in calls))


class LiveObserverTests(unittest.TestCase):
    def test_start_and_stop_manage_only_the_dedicated_watcher_task(self):
        with patch.object(live,'run') as run:
            live.control_task('Start')
            live.control_task('Stop')
        start = run.call_args_list[0].args[0]
        stop = run.call_args_list[1].args[0]
        self.assertIn('Start',start); self.assertIn('Stop',stop)
        self.assertTrue(any(arg.endswith('watch_task.ps1') for arg in start))
        self.assertNotIn('run_frontier.py',' '.join(start+stop))

    def fixture(self, path, *, complete=False, next_n=102, private=None):
        d=path/'batch-0001'; d.mkdir()
        run=dict(schema='CEML-FRONTIER-2-RUN', run_id='RUN1-operational-0001', base_B=live.BASE,
                 base_kind='operational', native_build_digest=live.BUILD, batch_start='100', batch_end='104')
        (d/'run.json').write_bytes(live.canonical(run))
        if complete:
            cert=dict(run, schema='CEML-FRONTIER-2-CERTIFICATE', status='conditional_complete', unresolved_count='0', pending=None)
            if private: cert['private_extra']=private
            cert['digest']=live.hashlib.sha3_256(b'CEML-FRONTIER-2/CERTIFICATE\0'+live.canonical(cert)).hexdigest()
            (d/'certificate.json').write_bytes(live.canonical(cert))
        else:
            checkpoint=dict(run, schema='CEML-FRONTIER-CKPT-2', next_n=str(next_n), generation='1',
                            run_digest=live.hashlib.sha3_256(b'CEML-FRONTIER-2/RUN\0'+live.canonical(run)).hexdigest())
            checkpoint['digest']=live.hashlib.sha3_256(b'CEML-FRONTIER-2/CHECKPOINT\0'+live.canonical(checkpoint)).hexdigest()
            (d/'ckpt.1.json').write_bytes(live.canonical(checkpoint))
        return d

    def test_checkpoint_is_provisional_and_crashed_runner_is_stopped(self):
        with tempfile.TemporaryDirectory() as tmp:
            chain=Path(tmp); self.fixture(chain)
            value=live.snapshot(chain,None,10)
        self.assertEqual(value['state'],'stopped')
        self.assertEqual(value['current_batch']['processed'],2)
        self.assertEqual(value['recent_batches'],[])

    def test_active_session_and_no_private_fields_leave_machine(self):
        with tempfile.TemporaryDirectory() as tmp:
            chain=Path(tmp); self.fixture(chain,complete=True,private='PRIVATE-HOST-ADDRESS-SECRET')
            value=live.snapshot(chain,dict(requested=4,started=0,started_at='2026-10-12T00:00:00Z'),10)
        self.assertEqual(value['session']['completed'],4)
        self.assertEqual(value['state'],'running')
        self.assertNotIn('PRIVATE',json.dumps(value))
        self.assertNotIn('digest',json.dumps(value))

    def test_torn_checkpoint_does_not_advance_cursor(self):
        with tempfile.TemporaryDirectory() as tmp:
            chain=Path(tmp); d=self.fixture(chain)
            (d/'ckpt.1.json').write_bytes(b'{torn')
            value=live.snapshot(chain,None,10)
        self.assertEqual(value['current_batch']['processed'],0)

    def test_invalid_certificate_is_not_reported_committed(self):
        with tempfile.TemporaryDirectory() as tmp:
            chain=Path(tmp); d=self.fixture(chain,complete=True)
            value=json.loads((d/'certificate.json').read_text());value['batch_end']='105'
            (d/'certificate.json').write_bytes(live.canonical(value))
            with self.assertRaises(ValueError):live.snapshot(chain,None,10)

    def test_transport_error_only_retries_live_upload(self):
        with patch.object(live,'active_runner',side_effect=ValueError('PRIVATE ERROR')):
            value,_=live.observe(None)
        self.assertEqual(value['state'],'error')
        self.assertNotIn('PRIVATE',json.dumps(value))

    def test_live_branch_update_is_non_force_and_never_main(self):
        calls=[]
        def api(endpoint,method='GET',body=None):
            calls.append((endpoint,method,body))
            return [{'ref':'refs/heads/live-status','object':{'sha':'parent'}}] if method=='GET' else {}
        with patch.object(live,'api',api),patch.object(live,'commit_files',return_value='new'):
            live.upload({'schema_version':1})
        self.assertEqual(calls[-1][2],{'sha':'new','force':False})
        self.assertTrue(calls[-1][0].endswith('/live-status'))


if __name__=='__main__': unittest.main()
