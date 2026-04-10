"""Общие операции cloud I/O-подготовки.

Файл содержит преобразование входного Excel в набор CSV по листам. Этот шаг делает
дальнейшую обработку независимой от формата источника и упрощает модульность задач.
"""

from pathlib import Path

import pandas as pd


def xlsx_to_csv_bundle(xlsx_path: Path, csv_dir: Path) -> Path:
    csv_dir.mkdir(parents=True, exist_ok=True)
    sheets = pd.read_excel(xlsx_path, sheet_name=None, header=2)
    for sheet_name, dataframe in sheets.items():
        dataframe.to_csv(csv_dir / f"{sheet_name}.csv", index=False)
    return csv_dir
