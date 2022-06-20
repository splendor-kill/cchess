from typing import Tuple, Sequence
import subprocess
import os



class S3Helper:
    def __init__(self, server, access_key, secret_key, remote_dir) -> None:
        self._server = server
        self._access_key = access_key
        self._secret_key = secret_key
        self._remote_dir = remote_dir

    def load(self, whats: Sequence[Tuple[str, str]]) -> None:       
        for remote_name, local_path in whats:
            remote_path = os.path.join(self._remote_dir, remote_name)
            cmd =  f'python3 -m omnitool.omni_storage -f download_url -u {remote_path} -l {local_path}'
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            print(result)

    def save(self, whats: Sequence[Tuple[str, str]]) -> None:
        for local_path, remote_name in whats:
            remote_path = os.path.join(self._remote_dir, remote_name)
            cmd =  f'python3 -m omnitool.omni_storage -f upload_url -u {remote_path} -l {local_path}'
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            print(result)
