"""Клиент Google Drive через официальный SDK.

Файл создает авторизованный сервис Google Drive по service account и реализует базовые
операции: получение метаданных, скачивание файла и обновление/создание итогового xlsx.
"""

from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from domain.models import RemoteFileMeta


class GoogleDriveClient:
    def __init__(self, service_account_file: str, source_file_id: str) -> None:
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=["https://www.googleapis.com/auth/drive"]
        )
        self.service = build("drive", "v3", credentials=creds, cache_discovery=False)
        self.source_file_id = source_file_id

    def get_file_meta(self, remote_path: str) -> RemoteFileMeta:
        file_id = remote_path or self.source_file_id
        meta = self.service.files().get(fileId=file_id, fields="id,name,md5Checksum,modifiedTime").execute()
        version = meta.get("md5Checksum") or meta.get("modifiedTime") or "unknown"
        return RemoteFileMeta(version=version, modified=meta.get("modifiedTime"), source="google")

    def download_file(self, remote_path: str, local_path: Path) -> None:
        file_id = remote_path or self.source_file_id
        request = self.service.files().get_media(fileId=file_id)
        with local_path.open("wb") as file_handle:
            downloader = MediaIoBaseDownload(file_handle, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    def upload_file(self, local_path: Path, remote_path: str) -> None:
        media = MediaFileUpload(str(local_path), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        if remote_path:
            self.service.files().update(fileId=remote_path, media_body=media).execute()
            return
        self.service.files().create(
            body={"name": local_path.name},
            media_body=media,
            fields="id",
        ).execute()
