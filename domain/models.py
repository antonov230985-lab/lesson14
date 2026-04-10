"""Доменные модели и контракты обмена данными.

Файл описывает dataclass-структуры для метаданных удаленного файла, результата пайплайна
и решения детектора изменений. Эти модели используются для явного и типобезопасного
взаимодействия между модулями.
"""

from dataclasses import dataclass


@dataclass
class RemoteFileMeta:
    version: str
    modified: str | None
    source: str


@dataclass
class PipelineResult:
    output_xlsx_path: str
    source: str


@dataclass
class SyncDecision:
    changed: bool
    source: str | None
