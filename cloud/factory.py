from config import AppConfig
from cloud.google_drive_client import GoogleDriveClient
from cloud.yandex_drive_client import YandexDriveClient


def build_clients(config: AppConfig) -> tuple[YandexDriveClient, GoogleDriveClient]:
    yandex = YandexDriveClient(config.yandex_token)
    google = GoogleDriveClient(config.google_service_account_file, config.google_drive_file_id)
    return yandex, google
