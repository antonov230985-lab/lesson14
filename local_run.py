from pathlib import Path

from cloud_io.common import xlsx_to_csv_bundle
from cloud_io.temp_files import cleanup_dir, ensure_dir
from processing.exporter import save_all_tasks_to_one_workbook
from processing.pipeline import run_pipeline


def main() -> None:
    source = Path("homework_lesson13.xlsx")
    temp_root = Path(".tmp_local_run")
    csv_dir = temp_root / "csv"
    outputs_dir = temp_root / "outputs"
    final_output = Path("lesson14_all_tasks_clean.xlsx")

    ensure_dir(temp_root)
    try:
        xlsx_to_csv_bundle(source, csv_dir)
        results, _ = run_pipeline(csv_dir, outputs_dir)
        save_all_tasks_to_one_workbook(results, final_output)
        print(f"Done: cleaned workbook saved to {final_output}")
    finally:
        cleanup_dir(temp_root)


if __name__ == "__main__":
    main()
