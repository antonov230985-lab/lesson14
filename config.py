"""Централизованная конфигурация приложения.

Файл описывает dataclass AppConfig и собирает все настройки из переменных окружения:
токены/идентификаторы облаков, интервалы polling, пути к state-файлу и временной директории.
Все остальные модули получают параметры только через этот конфиг.
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    yandex_token: str
    google_service_account_file: str
    google_input_name: str
    google_input_folder_id: str
    remote_input_path_yandex: str
    remote_output_path_yandex: str
    remote_output_name_google: str
    remote_output_folder_id_google: str
    polling_seconds: int
    state_file: Path
    temp_root: Path


def load_config() -> AppConfig:
    return AppConfig(
        yandex_token=os.getenv("YANDEX_TOKEN", ""),
        google_service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", ""),
        google_input_name=os.getenv("GOOGLE_INPUT_NAME", "homework_lesson13.xlsx"),
        google_input_folder_id=os.getenv("GOOGLE_INPUT_FOLDER_ID", ""),
        remote_input_path_yandex=os.getenv("YANDEX_INPUT_PATH", "homework_lesson13.xlsx"),
        remote_output_path_yandex=os.getenv("YANDEX_OUTPUT_PATH", "lesson14_all_tasks_clean.xlsx"),
        remote_output_name_google=os.getenv("GOOGLE_OUTPUT_NAME", "lesson14_all_tasks_clean.xlsx"),
        remote_output_folder_id_google=os.getenv("GOOGLE_OUTPUT_FOLDER_ID", ""),
        polling_seconds=int(os.getenv("POLLING_SECONDS", "30")),
        state_file=Path(os.getenv("STATE_FILE", ".sync_state.json")),
        temp_root=Path(os.getenv("TEMP_ROOT", ".tmp_sync")),
    )
