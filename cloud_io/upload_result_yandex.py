from pathlib import Path

from cloud.yandex_drive_client import YandexDriveClient


def upload_result_yandex(client: YandexDriveClient, local_xlsx: Path, remote_path: str) -> None:
    client.upload_file(local_xlsx, remote_path)
