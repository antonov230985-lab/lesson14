"""Основной цикл синхронизации и обработки.

Файл реализует orchestration: проверка изменений, скачивание обновленного источника,
обработка через pipeline, выгрузка результата в облака, обновление state и cleanup.
"""

import logging
import time

from cloud.google_drive_client import GoogleDriveClient
from cloud.yandex_drive_client import YandexDriveClient
from cloud_io.download_prepare_google import download_prepare_google
from cloud_io.download_prepare_yandex import download_prepare_yandex
from cloud_io.temp_files import cleanup_dir, ensure_dir
from cloud_io.upload_result_google import upload_result_google
from cloud_io.upload_result_yandex import upload_result_yandex
from config import AppConfig
from processing.exporter import save_all_tasks_to_one_workbook
from processing.pipeline import run_pipeline
from sync.change_detector import detect_change
from sync.state_store import StateStore

logger = logging.getLogger(__name__)


def run_once(config: AppConfig, yandex: YandexDriveClient, google: GoogleDriveClient, state_store: StateStore) -> None:
    state = state_store.load()
    yandex_meta = yandex.get_file_meta(config.remote_input_path_yandex)
    google_meta = google.get_file_meta(config.google_drive_file_id)
    decision = detect_change(yandex_meta.version, google_meta.version, state)
    if not decision.changed:
        logger.info("No changes detected in cloud sources.")
        return

    run_root = config.temp_root / f"run_{int(time.time())}"
    ensure_dir(run_root)
    try:
        if decision.source == "yandex":
            _, csv_dir = download_prepare_yandex(yandex, config.remote_input_path_yandex, run_root)
        else:
            _, csv_dir = download_prepare_google(google, config.google_drive_file_id, run_root)

        outputs, combined_path = run_pipeline(csv_dir, run_root / "outputs")
        save_all_tasks_to_one_workbook(outputs, combined_path)
        upload_result_yandex(yandex, combined_path, config.remote_output_path_yandex)
        upload_result_google(google, combined_path, "")

        state["yandex_version"] = yandex_meta.version
        state["google_version"] = google_meta.version
        state_store.save(state)
        logger.info("Processed and uploaded combined workbook from %s source.", decision.source)
    finally:
        cleanup_dir(run_root)


def run_forever(config: AppConfig, yandex: YandexDriveClient, google: GoogleDriveClient, state_store: StateStore) -> None:
    while True:
        try:
            run_once(config, yandex, google, state_store)
        except Exception as exc:
            logger.exception("Sync iteration failed: %s", exc)
        time.sleep(config.polling_seconds)
