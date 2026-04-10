"""Настройка общего логирования проекта.

Файл содержит единый helper для инициализации базового логгера, чтобы сообщения
из всех модулей (sync/cloud/processing) имели одинаковый формат и уровень детализации.
"""

import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
