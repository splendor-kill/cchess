import os
import subprocess
from logging import getLogger
from typing import Tuple, Sequence

from minio import Minio

logger = getLogger(__name__)


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
        # found = client.bucket_exists(self._remote_dir)
        # if not found:
        #     client.make_bucket(self._remote_dir)
        for local_path, remote_name in whats:
            client.fput_object(self._remote_dir, remote_name, local_path)

    def download_dirobj_async(self, from_where, to_where):
        """ recursive download dir object to local folder as a sub dir

        :param from_where: remote dir object name
        :param to_where: local dir name hold the remote dir object name
        :return: a subprocess in order the caller can control the download progress
        """
        alias = f'http://{self._access_key}:{self._secret_key}@{self._server}'
        remote_path = os.path.join('mys3', self._remote_dir, from_where)
        local_path = to_where
        cmd = f'MC_HOST_mys3={alias} mc cp -r {remote_path} {local_path}'
        logger.debug(cmd)
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('server', help='the s3 server url')
    parser.add_argument('-a', help='s3 access key, or user name', required=True, metavar='ACCESS-KEY', dest='access')
    parser.add_argument('-s', help='s3 secret key, or password', required=True, metavar='SECRET-KEY', dest='secret')
    parser.add_argument('-b', help='s3 bucket', required=True, metavar='BUCKET', dest='bucket')
    args = parser.parse_args()

    client = Minio(args.server, access_key=args.access, secret_key=args.secret, secure=False)

    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)

    bucket = args.bucket
    print(f'\nobjects in {bucket}:')
    objects = client.list_objects(bucket)
    for obj in objects:
        print('  ', obj.object_name)
