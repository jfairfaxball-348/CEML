"""Explicit successor session orchestration over the unchanged V2 arithmetic library.

Uses V2's existing _ledger_predecessors interface after a full startup replay.
No monkey-patching of any V2 function and no reusable on-disk verification cache.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import MappingProxyType

from .pinned import ReadLeases, IntegrityError
from .identity import ROOT, V2_BUILD, identity_paths, accepted, ACCEPTANCE


def require(condition, message):
    if not condition:
        raise IntegrityError(message)


def freeze(value):
    if isinstance(value, dict): return MappingProxyType({k:freeze(v) for k,v in value.items()})
    if isinstance(value, list): return tuple(map(freeze,value))
    return value


class Session:
    def __init__(self, chain, *, test=False, allow_empty=False):
        self.chain = Path(chain).absolute()
        self.test = test
        self.pins = ReadLeases(ROOT)
        self._verified = {}
        self._certificates = []
        self._layout = {}
        self.manifest_dir = None if test else self.chain.parent / (self.chain.name + '-manifests')
        self._manifest_names = set()
        self.active = None
        self.closed = False
        try:
            require(sys.version_info[:3]==(3,12,10),'Use the accepted Python 3.12.10')
            manifest = self.pins.pin(ROOT/'local/frontier/build/build_manifest.json')
            build = json.loads(manifest)
            bare = dict(build); reported = bare.pop('digest')
            canonical = json.dumps(bare,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
            require(reported == V2_BUILD == hashlib.sha3_256(b'CEML-FRONTIER-2/BUILD\0'+canonical).hexdigest(), 'Accepted V2 build manifest mismatch')
            for name, identity in build['inputs'].items():
                raw = self.pins.pin(ROOT/name).replace(b'\r\n',b'\n')
                require(hashlib.sha3_256(raw).hexdigest() == identity['lf']['sha3_256'], 'Frozen V2 input identity mismatch')
            for path in (ROOT/'local/frontier/build').iterdir():
                if path.is_file(): self.pins.pin(path)
            for path in identity_paths(): self.pins.pin(path)
            if not test and ACCEPTANCE.exists():
                self.pins.pin(ACCEPTANCE)
                require(accepted(),'Invalid I2 acceptance')
            self.pins.pin(ROOT/'PROGRAM_STATUS.md')
            # Execute only pinned, hash-checked frozen source bytes, not arbitrary import paths.
            for name in ('reference','f1_build','ceml_frontier'):
                path = ROOT/'tools/frontier'/f'{name}.py'
                spec=importlib.util.spec_from_file_location(name,path)
                module=importlib.util.module_from_spec(spec)
                sys.modules[name]=module
                exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
                if name=='ceml_frontier': self.f=module
            require(sys.modules['f1_build'].verify_build()['digest']==V2_BUILD,'V2 build verification mismatch')
            require(test or self.f.science_readable(False),'RUN1 read-only gate refused')
            paths=list(self.chain.glob('*/certificate.json'))
            require(paths or test and allow_empty,'Empty scientific ledger')

            paths.sort(key=lambda p:int(self.f.load_record(p,'certificate')['batch_start']))
            for number, path in enumerate(paths, 1):
                self._pin_batch(path.parent)
                if not test:
                    require(path.parent.name == f'batch-{number:04d}', 'Nonsequential batch directory')
                    manifest_path = self.manifest_dir / (path.parent.name + '.json')
                    require(self.pins.pin(manifest_path) == (path.parent / 'run.json').read_bytes(), 'Retained manifest differs from batch context')
                    self._manifest_names.add(manifest_path.name)
                cert=self.f.verify_batch(path,test,_ledger_predecessors=MappingProxyType(self._verified))
                self._promote(cert)
            self.guard()
            if not test:
                self.check_extension_anchor()
        except BaseException:
            self.close(); raise

    def check_extension_anchor(self):
        from .identity import PREFIX_BATCHES, PREFIX_DIGEST, PREFIX_END
        require(len(self._certificates) >= PREFIX_BATCHES, 'I2 requires the accepted 256-batch prefix')
        prefix = self._certificates[PREFIX_BATCHES-1]
        require(prefix['digest'] == PREFIX_DIGEST and prefix['batch_end'] == PREFIX_END,
                'I2 extension anchor mismatch')

    def ensure_chain_slot(self, directory, run):
        # The complete history was replayed, pinned, and checked for one contiguous
        # identity. Only the audited tip may be extended. No recursive depth policy.
        self.guard()
        self.predecessor(run)
        require(directory.parent == self.chain and not directory.exists(), 'Batch destination refused')
        if not self.test:
            expected = f'batch-{len(self._certificates)+1:04d}'
            require(directory.name == expected, 'New batch number must extend the audited tip')

    def _pin_batch(self, directory):
        names=set()
        allowed={'run.json','snapshot.json','certificate.json', 'acceptance.json' if self.test else 'authority.json',
                 'ckpt.0.json','ckpt.1.json','ckpt.2.json'}
        for path in directory.iterdir():
            require(path.is_file() and path.name in allowed,'Unexpected batch file or nested directory')
            data=self.pins.pin(path)
            require(len(data)<=self.f.MAX_RECORD,'Oversized batch record')
            names.add(path.name)
        self._layout[directory]=names

    def _promote(self, cert):
        require(cert['digest'] not in self._verified,'Duplicate/fork certificate')
        if self._certificates:
            prior=self._certificates[-1]
            require(cert['predecessor_digest']==prior['digest'] and cert['batch_start']==prior['batch_end'] and
                    all(cert[k]==prior[k] for k in self.f.IDENTITY),'Successor gap/identity mismatch')
        else:
            require(cert['batch_start']==cert['base_B'] and cert['predecessor_digest']==self.f.genesis(cert),'Missing genesis')
        self._verified[cert['digest']]=freeze(cert)
        self._certificates.append(copy.deepcopy(cert))

    def guard(self):
        require(not self.closed,'Closed verification session')
        actual={p for p in self.chain.iterdir() if p.is_dir()}
        expected=set(self._layout)
        if self.active is not None and self.active.exists(): expected.add(self.active)
        require(actual==expected,'Unexpected, missing or uncommitted batch directory')
        for directory,names in self._layout.items():
            require({p.name for p in directory.iterdir()}==names,'Historical batch layout changed')
        if self.manifest_dir is not None:
            require({p.name for p in self.manifest_dir.iterdir()} == self._manifest_names,
                    'Uncommitted or unexpected manifest')

    def ledger(self):
        self.guard();require(self._certificates,'Empty session ledger')
        first,last=self._certificates[0],self._certificates[-1]
        return dict(status='NONSCIENTIFIC_FIXTURE' if self.test else 'conditional_chain',batches=str(len(self._certificates)),
                    start=first['batch_start'],end=last['batch_end'],genesis_digest=first['predecessor_digest'],latest_certificate_digest=last['digest'])

    def predecessor(self, run):
        self.guard()
        if run['batch_start']==run['base_B']:
            require(not self._certificates and run['predecessor_digest']==self.f.genesis(run),'Unexpected genesis')
        else:
            require(self._certificates,'Missing authenticated predecessor')
            prior=self._certificates[-1]
            require(run['predecessor_digest']==prior['digest'] and run['batch_start']==prior['batch_end'] and
                    all(run[k]==prior[k] for k in self.f.IDENTITY),'Authenticated predecessor mismatch')

    def verify_existing(self, path):
        """Read-only benchmark/diagnostic: arithmetic replay of one pinned batch only."""
        self.guard();path=Path(path).absolute()
        require(path.parent in self._layout,'Certificate outside authenticated session')
        return self.f.verify_batch(path,self.test,_ledger_predecessors=MappingProxyType(self._verified))

    def cached_certificate(self, path):
        self.guard();path=Path(path).absolute()
        require(path.parent in self._layout,'Unverified certificate path')
        cert=self.f.load_record(path,'certificate')
        require(cert['digest'] in self._verified,'Unverified certificate digest')
        return cert

    def prepare_manifest(self, out, authority, acknowledge, max_t, max_total, prior_path, width):
        require(not self.test and accepted(),'Owner acceptance of SESSION-I2 required')
        prior=self.cached_certificate(prior_path)
        require(prior['digest']==self._certificates[-1]['digest'],'Manifest must extend session tip')
        out = self.f.local_path(out)
        require(out.parent == self.manifest_dir and out.name == f'batch-{len(self._certificates)+1:04d}.json'
                and not out.exists(), 'Manifest destination must extend the audited tip')
        snap,digest,expected=self.f.expected_acknowledgement(prior['base_kind'])
        require(acknowledge==expected,'Continuation acknowledgement mismatch')
        span=self.f.canonical_decimal(width,'width')
        run=dict(schema=self.f.SCHEMA_IDS['run'],run_id=prior['run_id'],run1_authority_id=authority,
                 snapshot_digest=digest,base_kind=prior['base_kind'],base_B=prior['base_B'],
                 accepted_assumption_ack=acknowledge,batch_start=prior['batch_end'],
                 batch_end=str(int(prior['batch_end'])+span),predecessor_digest=prior['digest'],
                 ruleset_id=self.f.RULESET,table_digest=self.f.reference.table_digest(),
                 native_build_digest=V2_BUILD,map_id='T-shortened-v1',max_t_per_explicit=max_t,max_total_t=max_total)
        self.f.run1_status();self.f.validate_manifest(run,snap);self.predecessor(run)
        self.f.write_atomic(out,self.f.canonical(run))
        self.pins.pin(self.f.local_path(out))
        self._manifest_names.add(out.name)
        return dict(status='MANIFEST_WRITTEN_NOT_EXECUTED',run_digest=self.f.H('RUN',self.f.canonical(run)),
                    batch_start=run['batch_start'],batch_end=run['batch_end'],predecessor_digest=run['predecessor_digest'])

    def execute(self, directory, run):
        try:
            return self._execute(directory, run)
        except BaseException:
            # A failed/incomplete attempt never leaves a reusable trusted session.
            self.close()
            raise

    def _execute(self, directory, run):
        """New-batch path; every arithmetic/checkpoint/record primitive stays frozen V2."""
        require(self.test or accepted(),'Owner acceptance of SESSION-I2 required')
        self.guard();directory=Path(directory).absolute()
        require(directory.parent==self.chain and not directory.exists(),'Batch destination refused')
        if not self.test: authority=self.f.run1_gate(run)
        self.f.validate_manifest(run,self.f.snapshot(),self.test)
        self.ensure_chain_slot(directory,run)
        if not self.test:
            require(self.f.load_record(self.manifest_dir / (directory.name + '.json'), 'run') == run,
                    'New batch differs from pinned admitted manifest')
        self.predecessor(run)
        self.active=directory
        if self.test:
            self.f.prepare_fixture(directory,run)
        else:
            directory.mkdir()
            for name,data in [('run.json',self.f.canonical(run)),('snapshot.json',self.f.canonical(self.f.snapshot())),('authority.json',authority)]:
                self.f.write_atomic(directory/name,data)
        for name in ('run.json', 'snapshot.json', 'acceptance.json' if self.test else 'authority.json'):
            self.pins.pin(directory/name)
        require(self.f.load_context(directory,self.test)[0]==run,'New batch context mismatch')
        self.predecessor(run)
        store=self.f.CheckpointStore(directory,run);store.initialize()
        summary=self.f.consume_native(int(run['batch_start']),int(run['batch_end']),int(run['max_t_per_explicit']),int(run['max_total_t']))
        store.write(summary)
        if summary['pending'] is not None:
            self.close()
            return dict(status='INCOMPLETE',next_n=summary['next_n'],pending=summary['pending'])
        require(summary['next_n']==run['batch_end'],'Incomplete batch cannot commit')
        self.predecessor(run)
        replay=self.f.summary_reference(int(run['batch_start']),int(run['batch_end']),int(run['max_t_per_explicit']),int(run['max_total_t']))
        require(summary==replay,'New batch independent replay mismatch')
        cert=self.f.seal(dict(schema=self.f.SCHEMA_IDS['certificate'],status='conditional_complete',run_digest=self.f.H('RUN',self.f.canonical(run)),
            **{k:run[k] for k in self.f.BINDING},checker_source_digest=self.f.checker_digest(),independent_replay_digest=replay['transcript_digest'],
            **{k:summary[k] for k in self.f.TOTALS},unresolved_count='0',pending=None),'CERTIFICATE')
        self.f.validate_shape(cert,'certificate')
        require(self.f.load_context(directory,self.test)[0]==run,'Commit context changed')
        self.predecessor(run)
        self.f.write_atomic(directory/'certificate.json',self.f.canonical(cert),False)
        self._pin_batch(directory)
        require(self.f.verify_batch(directory/'certificate.json',self.test,_ledger_predecessors=MappingProxyType(self._verified))==cert,'Final new-certificate verification mismatch')
        inspection=self.f.inspect_batch(directory)
        recovery=inspection['recovery']
        require(recovery.get('status')=='RECOVERABLE' and recovery.get('pending') is None and not recovery.get('warnings') and inspection['temporaries']=='0','New batch inspection refused')
        self._promote(cert);self.active=None;self.guard()
        return dict(status='NONSCIENTIFIC_FIXTURE' if self.test else 'COMMITTED',digest=cert['digest'],batch_end=run['batch_end'])

    def close(self):
        self.pins.close();self.closed=True

    def __enter__(self): return self
    def __exit__(self,*_): self.close()
