from pathlib import Path

import pandas as pd

from processing.tasks import task1, task2, task3, task4, task5

SHEET_TO_CSV = {
    "1_Телефоны_и_даты": "1_Телефоны_и_даты.csv",
    "2_Суммы_и_статусы": "2_Суммы_и_статусы.csv",
    "3_Мусор_и_дубли": "3_Мусор_и_дубли.csv",
    "4_Логика_заказов": "4_Логика_заказов.csv",
    "5_Комплексное": "5_Комплексное.csv",
}


def run_pipeline(csv_dir: Path, out_dir: Path) -> tuple[dict[str, pd.DataFrame], Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    task1_df = task1.run(csv_dir / SHEET_TO_CSV["1_Телефоны_и_даты"], out_dir / "task1_phones_dates_clean.xlsx")
    task2_df = task2.run(csv_dir / SHEET_TO_CSV["2_Суммы_и_статусы"], out_dir / "task2_amounts_statuses_clean.xlsx")
    task3_df = task3.run(
        csv_dir / SHEET_TO_CSV["3_Мусор_и_дубли"], out_dir / "task3_garbage_duplicates_clean.xlsx"
    )
    task4_df = task4.run(
        csv_dir / SHEET_TO_CSV["4_Логика_заказов"], out_dir / "task4_orders_aggregated_clean.xlsx"
    )
    task5_df = task5.run(csv_dir / SHEET_TO_CSV["5_Комплексное"], out_dir / "task5_full_pipeline_clean.xlsx")
    all_results = {
        "task1_phones_dates": task1_df,
        "task2_amounts_statuses": task2_df,
        "task3_garbage_duplicates": task3_df,
        "task4_orders_aggregated": task4_df,
        "task5_full_pipeline": task5_df,
    }
    return all_results, out_dir / "lesson13_all_tasks_clean.xlsx"
