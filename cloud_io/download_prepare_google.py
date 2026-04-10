from pathlib import Path

from cloud.google_drive_client import GoogleDriveClient
from cloud_io.common import xlsx_to_csv_bundle


def download_prepare_google(client: GoogleDriveClient, remote_file_id: str, work_dir: Path) -> tuple[Path, Path]:
    xlsx_path = work_dir / "homework_lesson13.xlsx"
    csv_dir = work_dir / "csv"
    client.download_file(remote_file_id, xlsx_path)
    xlsx_to_csv_bundle(xlsx_path, csv_dir)
    return xlsx_path, csv_dir
