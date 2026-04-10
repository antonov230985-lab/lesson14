"""Задача 5: комплексная очистка смешанных данных.

Файл применяет полный набор нормализаций, фильтрует невалидные записи,
убирает полные дубли и формирует финальную таблицу для листа 5.
"""

from pathlib import Path

import pandas as pd

from processing.normalizers import norm_amount, norm_date, norm_phone, norm_status


def run(source_csv: Path, out_path: Path) -> pd.DataFrame:
    df = pd.read_csv(source_csv)
    work = df.copy()
    work["id_num"] = pd.to_numeric(work["#"], errors="coerce")
    work = work[work["id_num"].notna()].copy()
    work["date"] = work["Дата"].apply(norm_date)
    work["client"] = work["Клиент"].astype(str).str.strip().str.title()
    work["phone"] = work["Телефон"].apply(norm_phone)
    work["vin"] = work["VIN"].astype(str).str.strip()
    work["service"] = work["Услуга"].astype(str).str.strip()
    work["amount"] = work["Сумма"].apply(norm_amount)
    work["status"] = work["Статус"].apply(norm_status)
    work.loc[work["vin"].isin(["nan", "None"]), "vin"] = None
    work.loc[work["service"].isin(["nan", "None"]), "service"] = None
    clean = work[
        work["date"].notna() & work["client"].notna() & work["phone"].notna() & work["service"].notna()
    ].copy()
    clean = clean.drop_duplicates(
        subset=["date", "client", "phone", "vin", "service", "amount", "status"],
        keep="first",
    )
    result = clean[["#", "date", "client", "phone", "vin", "service", "amount", "status"]]
    result.to_excel(out_path, index=False)
    return result
