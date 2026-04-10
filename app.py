"""Точка входа cloud-режима урока 14.

Файл запускает бесконечный цикл синхронизации: читает конфигурацию из переменных окружения,
инициализирует клиентов Яндекс.Диска и Google Drive, проверяет корректность обязательных
настроек и передает управление модулю оркестрации sync.runner.
"""

from dotenv import load_dotenv

from cloud.factory import build_clients
from config import load_config
from logging_setup import setup_logging
from sync.runner import run_forever
from sync.state_store import StateStore


def _validate_required_settings() -> list[str]:
    config = load_config()
    missing: list[str] = []
    if not config.google_service_account_file:
        missing.append("GOOGLE_SERVICE_ACCOUNT_FILE")
    if not config.google_input_name:
        missing.append("GOOGLE_INPUT_NAME")
    return missing


def main() -> None:
    # Автоматически подгружаем переменные из .env из корня проекта.
    load_dotenv(override=True)
    setup_logging()
    missing = _validate_required_settings()
    if missing:
        print("Ошибка конфигурации: не заданы обязательные переменные окружения:")
        for key in missing:
            print(f"- {key}")
        print("Создай .env на основе .env.example и перезапусти app.py.")
        raise SystemExit(1)
    config = load_config()
    yandex_client, google_client = build_clients(config)
    state_store = StateStore(config.state_file)
    run_forever(config, yandex_client, google_client, state_store)


if __name__ == "__main__":
    main()
