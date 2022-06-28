import os
import subprocess
from typing import Tuple, Sequence


class S3Helper:
    def __init__(self, server, access_key, secret_key, remote_dir) -> None:
        self._server = server
        self._access_key = access_key
        self._secret_key = secret_key
        self._remote_dir = remote_dir

    def load(self, whats: Sequence[Tuple[str, str]]) -> None:
        for remote_name, local_path in whats:
            remote_path = os.path.join(self._server, self._remote_dir, remote_name)
            cmd = f'python3 -m omnitool.omni_storage -f download_url -u {remote_path} -l {local_path}'
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            print(result)

    def save(self, whats: Sequence[Tuple[str, str]]) -> None:
        for local_path, remote_name in whats:
            remote_path = os.path.join(self._server, self._remote_dir, remote_name)
            cmd = f'python3 -m omnitool.omni_storage -f upload_url -u {remote_path} -l {local_path}'
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            print(result)

    def download_dirobj_async(self, from_where, to_where):
        """ the omnitool only has function of downloading the entire dir object, and cannot save as a new name

        :param from_where: remote dir object name, MUST end with '/'
        :param to_where: local dir name hold the remote dir object name
        :return: a subprocess in order the caller can control the download progress
        """
        remote_path = os.path.join(self._server, from_where)
        local_path = to_where
        cmd = f'python3 -m omnitool.omni_storage -f download_url -u {remote_path} -l {local_path}'
        print(cmd)
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
