"""Задача 3: удаление мусора и маркировка дублей.

Файл фильтрует невалидные строки, вычисляет точные дубли и помечает записи
как первичный/повторный визит или дубль с подготовкой итоговой таблицы.
"""

from pathlib import Path

import pandas as pd

from processing.normalizers import norm_amount, norm_date, norm_phone


def run(source_csv: Path, out_path: Path) -> pd.DataFrame:
    df = pd.read_csv(source_csv)
    work = df.copy()
    work["id_num"] = pd.to_numeric(work["#"], errors="coerce")
    work["amount_num"] = work["Сумма"].apply(norm_amount)
    work["phone_norm"] = work["Телефон"].apply(norm_phone)
    work["date_norm"] = work["Дата визита"].apply(norm_date)
    clean = work[
        work["id_num"].notna()
        & work["date_norm"].notna()
        & work["Клиент"].notna()
        & work["Услуга"].notna()
    ].copy()
    exact_key = ["Клиент", "phone_norm", "date_norm", "Услуга", "amount_num"]
    clean["is_exact_duplicate"] = clean.duplicated(subset=exact_key, keep="first")
    uniq = clean[~clean["is_exact_duplicate"]].copy()
    uniq["visit_number_for_client"] = (
        uniq.sort_values("date_norm").groupby(["Клиент", "phone_norm"]).cumcount() + 1
    )
    clean = clean.merge(uniq[exact_key + ["visit_number_for_client"]], on=exact_key, how="left")
    clean["duplicate_note"] = clean.apply(
        lambda row: (
            "дубль"
            if row["is_exact_duplicate"]
            else ("повторный визит" if row["visit_number_for_client"] > 1 else "первичный визит")
        ),
        axis=1,
    )
    clean["id_out"] = clean["#"]
    clean.loc[clean["is_exact_duplicate"], "id_out"] = None
    result = clean[
        ["id_out", "date_norm", "Клиент", "phone_norm", "Услуга", "amount_num", "duplicate_note"]
    ].rename(columns={"id_out": "#", "date_norm": "date", "phone_norm": "phone", "amount_num": "amount"})
    result.to_excel(out_path, index=False)
    return result
