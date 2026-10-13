"""Operator adapter for the isolated I2 worker; no network or shell interpolation."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from .identity import ROOT, PROFILE, digest


class Client:
    profile = PROFILE
    def __init__(self, chain):
        self.errors=tempfile.TemporaryFile(mode='w+t',encoding='utf-8')
        isolation={'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP} if os.name=='nt' else {'start_new_session':True}
        self.process=subprocess.Popen([sys.executable,'-m','tools.session_i2.worker',str(chain)],cwd=ROOT,
                                      stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.errors,
                                      text=True,encoding='utf-8',**isolation)
        try:
            ready=self.read()
            if ready.get('status')!='SESSION_READY' or ready.get('profile')!=PROFILE or ready.get('profile_digest')!=digest():
                raise ValueError('I2 startup refused: '+json.dumps(ready,sort_keys=True))
        except BaseException:
            self.close();raise

    def read(self):
        line=self.process.stdout.readline(131073)
        if not line or len(line)>131072 or not line.endswith('\n'):
            raise ValueError('I2 worker lost or invalid response; no automatic retry')
        value=json.loads(line)
        if not isinstance(value,dict): raise ValueError('Invalid I2 response')
        return value

    def call(self, arguments):
        self.process.stdin.write(json.dumps(list(map(str,arguments)))+'\n');self.process.stdin.flush()
        return self.read()

    def close(self):
        if self.process.stdin:
            try:self.process.stdin.close()
            except BrokenPipeError:pass
        try: self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.terminate();self.process.wait(timeout=10)
        self.process.stdout.close();self.errors.close()

    def __enter__(self): return self
    def __exit__(self,*_): self.close()
