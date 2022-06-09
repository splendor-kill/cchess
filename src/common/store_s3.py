from typing import Tuple, Sequence
from minio import Minio
from minio.error import S3Error, ResponseError


class S3Helper:
    def __init__(self, server, access_key, secret_key, remote_dir) -> None:
        self._server = server
        self._access_key = access_key
        self._secret_key = secret_key
        self._remote_dir = remote_dir

    def load(self, whats: Sequence[Tuple[str, str]]) -> None:
        client = Minio(self._server, access_key=self._access_key, secret_key=self._secret_key, secure=False)
        for remote_name, local_path in whats:
            client.fget_object(self._remote_dir, remote_name, local_path)

    def save(self, whats: Sequence[Tuple[str, str]]) -> None:
        client = Minio(self._server, access_key=self._access_key, secret_key=self._secret_key, secure=False)

        found = client.bucket_exists(self._remote_dir)
        if not found:
            client.make_bucket(self._remote_dir)
        for local_path, remote_name in whats:
            client.fput_object(self._remote_dir, remote_name, local_path)
