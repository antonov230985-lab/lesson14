from pathlib import Path

from cloud.google_drive_client import GoogleDriveClient


def upload_result_google(client: GoogleDriveClient, local_xlsx: Path, remote_file_id: str) -> None:
    client.upload_file(local_xlsx, remote_file_id)
