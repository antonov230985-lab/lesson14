"""Задача 1: нормализация телефонов и дат.

Файл обрабатывает CSV первого листа, оставляет идентификационные колонки и приводит
телефон/дату к стандартному формату.
"""

from pathlib import Path

import pandas as pd

from processing.normalizers import norm_date, norm_phone


def run(source_csv: Path, out_path: Path) -> pd.DataFrame:
    df = pd.read_csv(source_csv)
    result = df[["ID", "Клиент"]].copy()
    result["phone"] = df["Телефон (исходный)"].apply(norm_phone)
    result["date"] = df["Дата (исходная)"].apply(norm_date)
    result.to_excel(out_path, index=False)
    return result
