"""Абстрактный контракт для cloud-клиентов.

Файл объявляет протокол CloudStorageClient: получение метаданных, скачивание и загрузка файла.
Реализации Яндекс/Google следуют этому интерфейсу, что упрощает оркестрацию и тестирование.
"""

from pathlib import Path
from typing import Protocol

from domain.models import RemoteFileMeta


class CloudStorageClient(Protocol):
    def get_file_meta(self, remote_path: str) -> RemoteFileMeta:
        ...

    def download_file(self, remote_path: str, local_path: Path) -> None:
        ...

    def upload_file(self, local_path: Path, remote_path: str) -> None:
        ...
