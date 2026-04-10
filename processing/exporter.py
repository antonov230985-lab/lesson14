from pathlib import Path

import pandas as pd


def save_all_tasks_to_one_workbook(results: dict[str, pd.DataFrame], out_path: Path) -> None:
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for sheet_name, dataframe in results.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
