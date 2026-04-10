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
