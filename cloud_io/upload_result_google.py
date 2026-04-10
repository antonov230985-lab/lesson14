"""Черный ящик №4: выгрузка результата на Google Drive.

Файл принимает локальный итоговый xlsx и удаленный file_id (или пустое значение
для создания нового файла) и делегирует операцию клиенту Google Drive.
"""

from pathlib import Path

from cloud.google_drive_client import GoogleDriveClient


def upload_result_google(client: GoogleDriveClient, local_xlsx: Path, remote_file_id: str) -> None:
    client.upload_file(local_xlsx, remote_file_id)
