# Урок 14 — Cloud-driven Data Cleaning Pipeline

Проект обрабатывает Excel-файл из облака в цикле: находит входной файл по имени в папке Google Drive (или берет источник из Яндекс.Диска), переводит в CSV, чистит данные по 5 задачам и обновляет итоговый `xlsx`.

## Что уже реализовано

- Разделение на изолированные модули-«черные ящики»:
  - `cloud/*` - клиенты Яндекс.Диска и Google Drive.
  - `cloud_io/*` - download/prepare и upload модули.
  - `processing/*` - нормализация и 5 задач очистки.
  - `sync/*` - state store, детектор изменений, цикл обработки.
- Поиск входа Google по `GOOGLE_INPUT_NAME` + `GOOGLE_INPUT_FOLDER_ID`.
- Обновление выхода Google по `GOOGLE_OUTPUT_NAME` + `GOOGLE_OUTPUT_FOLDER_ID` (без дублей).
- Сборка итогового файла `lesson14_all_tasks_clean.xlsx` и загрузка в целевые хранилища.

## Запуск cloud-режима

```bash
python app.py
```

`app.py` автоматически читает переменные из `.env`, поэтому отдельный экспорт env перед запуском не нужен.

Перед запуском нужно задать переменные окружения из `config.py`:

- `GOOGLE_SERVICE_ACCOUNT_FILE`
- `GOOGLE_INPUT_NAME`
- `GOOGLE_INPUT_FOLDER_ID`
- `YANDEX_INPUT_PATH`
- `YANDEX_OUTPUT_PATH`
- `GOOGLE_OUTPUT_NAME`
- `GOOGLE_OUTPUT_FOLDER_ID`
- `POLLING_SECONDS`
- `STATE_FILE`
- `TEMP_ROOT`

Минимально обязательные для Google-потока:

- `GOOGLE_SERVICE_ACCOUNT_FILE`
- `GOOGLE_INPUT_NAME`
- `GOOGLE_INPUT_FOLDER_ID`

`YANDEX_*` можно оставить пустыми, если работаешь только с Google Drive.

## Зависимости

- Python 3.10+
- `pandas`
- `openpyxl`
- `requests`
- `google-api-python-client`
- `google-auth`

Установка:

```bash
pip install -r requirements.txt
```
