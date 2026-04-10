"""Задача 4: агрегация заказов в одну строку на order_id.

Файл объединяет строки клиента, работ и товаров в агрегированный результат:
дата, клиент, телефон, общая сумма и количество позиций заказа.
"""

from pathlib import Path

import pandas as pd

from processing.normalizers import norm_date, norm_phone


def run(source_csv: Path, out_path: Path) -> pd.DataFrame:
    df = pd.read_csv(source_csv)
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df["price_num"] = pd.to_numeric(df["Цена"], errors="coerce")
    df["qty_num"] = pd.to_numeric(df["Кол-во"], errors="coerce")
    rows: list[dict] = []
    for order_id, part in df.groupby("order_id", dropna=True):
        client_row = part[part["Тип строки"] == "Клиент"].head(1)
        date = norm_date(client_row["Дата"].iloc[0]) if not client_row.empty else None
        client = client_row["Клиент"].iloc[0] if not client_row.empty else None
        phone = norm_phone(client_row["Телефон"].iloc[0]) if not client_row.empty else None
        item_rows = part[part["Тип строки"].isin(["Работа", "Товар"])].copy()
        item_rows["line_total"] = item_rows["qty_num"].fillna(0) * item_rows["price_num"].fillna(0)
        rows.append(
            {
                "order_id": int(order_id),
                "date": date,
                "client": client,
                "phone": phone,
                "total_amount": float(item_rows["line_total"].sum()),
                "items_count": int(item_rows.shape[0]),
            }
        )
    result = pd.DataFrame(rows).sort_values("order_id")
    result.to_excel(out_path, index=False)
    return result
