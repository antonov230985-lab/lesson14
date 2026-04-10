"""Черный ящик №3: выгрузка результата на Яндекс.Диск.

Файл принимает локальный итоговый xlsx и удаленный путь назначения,
после чего делегирует загрузку клиенту Яндекс.Диска.
"""

from pathlib import Path

from cloud.yandex_drive_client import YandexDriveClient


def upload_result_yandex(client: YandexDriveClient, local_xlsx: Path, remote_path: str) -> None:
    client.upload_file(local_xlsx, remote_path)
