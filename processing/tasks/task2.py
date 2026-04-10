"""Задача 2: нормализация сумм и статусов.

Файл очищает суммы и статусы, оставляя только целевые значения,
подходящие для дальнейшей аналитики и контроля качества.
"""

from pathlib import Path

import pandas as pd

from processing.normalizers import norm_amount, norm_status


def run(source_csv: Path, out_path: Path) -> pd.DataFrame:
    df = pd.read_csv(source_csv)
    result = df[["ID", "Услуга"]].copy()
    result["amount"] = df["Сумма (исходная)"].apply(norm_amount)
    result["status"] = df["Статус (исходный)"].apply(norm_status)
    result.to_excel(out_path, index=False)
    return result
