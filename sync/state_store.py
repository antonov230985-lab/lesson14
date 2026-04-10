"""Хранилище состояния синхронизации.

Файл отвечает за чтение и запись JSON-состояния последних обработанных версий файлов,
чтобы цикл мог обнаруживать реальные изменения и не запускаться лишний раз.
"""

import json
from pathlib import Path


class StateStore:
    def __init__(self, state_file: Path) -> None:
        self.state_file = state_file

    def load(self) -> dict[str, str]:
        if not self.state_file.exists():
            return {}
        return json.loads(self.state_file.read_text(encoding="utf-8"))

    def save(self, state: dict[str, str]) -> None:
        self.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
