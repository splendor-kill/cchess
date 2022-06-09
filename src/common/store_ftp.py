from typing import Tuple, Sequence
import ftplib


class FTPHelper:
    def __init__(self, server, user, password, remote_dir) -> None:
        self._server = server
        self._user = user
        self._password = password
        self._remote_dir = remote_dir

    def load(self, whats: Sequence[Tuple[str, str]]) -> None:
        ftp_connection = ftplib.FTP(self._server, self._user, self._password)
        ftp_connection.cwd(self._remote_dir)
        for remote_name, local_path in whats:
            ftp_connection.retrbinary(f'RETR {remote_name}', open(local_path, 'wb').write)
        ftp_connection.quit()

    def save(self, whats: Sequence[Tuple[str, str]]) -> None:
        ftp_connection = ftplib.FTP(self._server, self._user, self._password)
        ftp_connection.cwd(self._remote_dir)
        for local_path, remote_name in whats:
            with open(local_path, 'rb') as fh:
                ftp_connection.storbinary(f'STOR {remote_name}', fh)
        ftp_connection.quit()
