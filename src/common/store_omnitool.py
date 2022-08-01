import os
import subprocess
from logging import getLogger
from typing import Tuple, Sequence

logger = getLogger(__name__)


class S3Helper:
    def __init__(self, server, access_key, secret_key, remote_dir) -> None:
        self._server = server
        self._access_key = access_key
        self._secret_key = secret_key
        self._remote_dir = remote_dir

    def load(self, whats: Sequence[Tuple[str, str]]) -> None:
        for remote_name, local_path in whats:
            local_path = os.path.abspath(local_path)
            cmd = f'python3 -m omnitool.omni_storage dl {self._remote_dir} {remote_name} {local_path}'
            logger.debug(cmd)
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            logger.debug(result)

    def save(self, whats: Sequence[Tuple[str, str]]) -> None:
        for local_path, remote_name in whats:
            local_path = os.path.abspath(local_path)
            cmd = f'python3 -m omnitool.omni_storage ul {self._remote_dir} {local_path} {remote_name}'
            logger.debug(cmd)
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            logger.debug(result)

    def download_dirobj_async(self, from_where, to_where):
        """ the omnitool only has function of downloading the entire dir object, and cannot save as a new name

        :param from_where: remote dir object name, MUST end with '/'
        :param to_where: local dir name hold the remote dir object name
        :return: a subprocess in order the caller can control the download progress
        """
        local_path = to_where
        local_path = os.path.abspath(local_path)
        cmd = f'python3 -m omnitool.omni_storage dl {self._remote_dir} {from_where} {local_path}'
        logger.debug(cmd)
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
