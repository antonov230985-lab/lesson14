"""Утилиты работы с временными директориями.

Файл содержит безопасные функции создания и полной очистки временных каталогов,
которые используются в локальном и cloud-режиме после каждого цикла обработки.
"""

import shutil
from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def cleanup_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
