# HELP — структура и сценарий работы проекта

## 1) Назначение папок проекта

- `cloud/`  
Слой API-клиентов облачных хранилищ. Здесь код, который умеет обращаться к Яндекс.Диску и Google Drive: получать метаданные файла, скачивать файл, загружать файл.
- `cloud_io/`  
Слой I/O-операций (черные ящики) вокруг облаков. Здесь модули, которые уже комбинируют действия: скачать файл + подготовить CSV, загрузить результат, очистить временные папки.
- `domain/`  
Доменные модели (dataclass), которыми обмениваются остальные слои: метаданные удаленного файла, решение детектора изменений и т.д.
- `processing/`  
Бизнес-логика очистки данных. Внутри:
  - `normalizers.py` — нормализация полей;
  - `tasks/` — 5 отдельных обработчиков заданий;
  - `pipeline.py` — оркестратор task1..task5;
  - `exporter.py` — сборка одного итогового `xlsx`.
- `sync/`  
Оркестрация циклической синхронизации: хранение state, определение изменений, запуск полного цикла download -> process -> upload.
- `processing/tasks/`  
Подпапка с задачами очистки:
  - `task1.py` — телефоны/даты,
  - `task2.py` — суммы/статусы,
  - `task3.py` — мусор/дубли,
  - `task4.py` — логика заказов и агрегация,
  - `task5.py` — комплексная очистка.
- `__pycache__/`  
Служебная папка Python с кэшированными `.pyc`, на логику проекта не влияет.

## 2) Назначение каждого файла в корне проекта

- `.env`  
Локальные реальные настройки окружения (секреты, пути, ID файлов). Используется при запуске `app.py`.
- `.env.example`  
Шаблон для `.env` с подробными комментариями, что и откуда брать.
- `.gitignore`  
Исключает из git временные файлы, кэши, state-файлы и локальные артефакты.
- `app.py`  
Главная точка входа cloud-режима. Проверяет обязательные env-переменные, создает клиентов облаков и запускает бесконечный sync-цикл.
- `config.py`  
Загружает конфигурацию из env в `AppConfig`.
- `lesson14_all_tasks_clean.xlsx`  
Итоговый очищенный файл (рабочий выходной артефакт обработки).
- `logging_setup.py`  
Единая настройка логирования.
- `README.md`  
Пользовательская документация проекта.
- `requirements.txt`  
Python-зависимости.

## 3) Назначение каждого файла в папках

### `cloud/`

- `cloud/base.py` — протокол `CloudStorageClient` (контракт методов `get_file_meta`, `download_file`, `upload_file`).
- `cloud/yandex_drive_client.py` — реализация клиента Яндекс.Диска.
- `cloud/google_drive_client.py` — реализация клиента Google Drive.
- `cloud/factory.py` — фабрика, создающая клиентов по `AppConfig`.

### `cloud_io/`

- `cloud_io/common.py` — конвертация входного `xlsx` в набор CSV по листам.
- `cloud_io/download_prepare_yandex.py` — скачать из Яндекс.Диска и подготовить CSV.
- `cloud_io/download_prepare_google.py` — скачать из Google Drive и подготовить CSV.
- `cloud_io/upload_result_yandex.py` — отправить итоговый `xlsx` на Яндекс.Диск.
- `cloud_io/upload_result_google.py` — отправить итоговый `xlsx` на Google Drive.
- `cloud_io/temp_files.py` — создание/очистка временных директорий.

### `domain/`

- `domain/models.py` — dataclass-модели (`RemoteFileMeta`, `PipelineResult`, `SyncDecision`).

### `processing/`

- `processing/normalizers.py` — функции `norm_phone`, `norm_date`, `norm_amount`, `norm_status`.
- `processing/pipeline.py` — запуск всех задач и формирование единого набора результатов.
- `processing/exporter.py` — запись нескольких DataFrame в один workbook.

### `processing/tasks/`

- `processing/tasks/task1.py` — очистка телефонов и дат.
- `processing/tasks/task2.py` — очистка сумм и статусов.
- `processing/tasks/task3.py` — фильтрация мусора, маркировка дублей/повторов.
- `processing/tasks/task4.py` — агрегация заказов до уровня `order_id`.
- `processing/tasks/task5.py` — комплексная очистка смешанных данных.

### `sync/`

- `sync/state_store.py` — чтение/запись JSON-состояния последних версий.
- `sync/change_detector.py` — определение, изменился ли файл и из какого источника брать.
- `sync/runner.py` — главный цикл синхронизации и обработки.

## 4) Последовательность работы скрипта (по файлам)

Ниже основной рабочий сценарий: cloud-режим.

---

### Сценарий B: cloud-режим (`python app.py`)

1. Стартует `app.py`.
2. `app.py` вызывает `logging_setup.py` -> настраивает логирование.
3. `app.py` вызывает `config.py` -> `load_config()` собирает `AppConfig`.
4. `app.py` делает preflight:
  - если нет `GOOGLE_SERVICE_ACCOUNT_FILE` / `GOOGLE_INPUT_NAME` -> завершение с понятным сообщением.
5. `app.py` вызывает `cloud/factory.py`:
  - создаются `YandexDriveClient` и `GoogleDriveClient`.
6. `app.py` создает `StateStore` из `sync/state_store.py`.
7. `app.py` запускает `sync/runner.py` -> `run_forever(...)`.

Дальше цикл в `sync/runner.py` повторяется:

1. `runner.py` читает state через `sync/state_store.py`.
2. `runner.py` ищет входной Google-файл по имени в папке:
  - `GOOGLE_INPUT_NAME` + `GOOGLE_INPUT_FOLDER_ID`,
  - затем берет метаданные через `cloud/google_drive_client.py`.
3. `runner.py` вызывает `sync/change_detector.py`:
  - если изменений нет -> sleep и возврат к п.8;
    - если изменения есть -> выбирается источник (Яндекс/Google).
4. Если источник Яндекс:
  - `cloud_io/download_prepare_yandex.py` скачивает `xlsx` и делает CSV.
5. Если источник Google:
  - `cloud_io/download_prepare_google.py` скачивает найденный входной `xlsx` и делает CSV.
6. `runner.py` вызывает `processing/pipeline.py` (task1..task5).
7. `runner.py` вызывает `processing/exporter.py` и получает итоговый workbook.
8. `runner.py` загружает результат:
  - `cloud_io/upload_result_yandex.py`,
  - `cloud_io/upload_result_google.py` (обновляет/создает файл по имени в целевой папке).
9. `runner.py` обновляет state через `sync/state_store.py`.
10. `runner.py` вызывает `cloud_io/temp_files.py` для cleanup.
11. Цикл повторяется через интервал `POLLING_SECONDS`.

## 5) Логика ветвлений в одном месте

- Точка старта:
  - облако -> `app.py`
- В cloud-цикле:
  - нет изменений -> пропуск обработки;
  - изменения в Яндекс -> download через `download_prepare_yandex.py`;
  - изменения в Google -> download через `download_prepare_google.py`;
  - после любой обработки -> upload в оба облака + обновление state.

## 6) Краткая таблица: файл -> кто вызывает -> что делает


| Файл                                  | Кто вызывает                                       | Что делает / что отдает                                                |
| ------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| `app.py`                              | Пользователь (`python app.py`)                     | Старт cloud-режима, preflight, запуск бесконечного цикла синхронизации |
| `config.py`                           | `app.py`, `sync/*`                                 | Читает env и возвращает `AppConfig`                                    |
| `logging_setup.py`                    | `app.py`                                           | Настраивает формат и уровень логирования                               |
| `cloud/factory.py`                    | `app.py`                                           | Создает клиентов Яндекс/Google                                         |
| `cloud/base.py`                       | `cloud/*`, `sync/*`                                | Контракт cloud-клиента (meta/download/upload)                          |
| `cloud/yandex_drive_client.py`        | `cloud/factory.py`, `sync/runner.py`, `cloud_io/*` | Работа с API Яндекс.Диска                                              |
| `cloud/google_drive_client.py`        | `cloud/factory.py`, `sync/runner.py`, `cloud_io/*` | Работа с API Google Drive                                              |
| `domain/models.py`                    | `cloud/*`, `sync/*`                                | Типы данных (`RemoteFileMeta`, `SyncDecision` и т.д.)                  |
| `sync/runner.py`                      | `app.py`                                           | Главный цикл `detect -> download -> process -> upload -> cleanup`      |
| `sync/change_detector.py`             | `sync/runner.py`                                   | Определяет, есть ли изменение и какой источник активен                 |
| `sync/state_store.py`                 | `sync/runner.py`                                   | Читает/пишет JSON state версий                                         |
| `cloud_io/download_prepare_yandex.py` | `sync/runner.py`                                   | Скачивает xlsx из Яндекс и готовит CSV                                 |
| `cloud_io/download_prepare_google.py` | `sync/runner.py`                                   | Скачивает xlsx из Google и готовит CSV                                 |
| `cloud_io/common.py`                  | `cloud_io/download_prepare_*`                      | Конвертирует xlsx в CSV-набор по листам                                |
| `cloud_io/upload_result_yandex.py`    | `sync/runner.py`                                   | Загружает итоговый xlsx на Яндекс                                      |
| `cloud_io/upload_result_google.py`    | `sync/runner.py`                                   | Загружает итоговый xlsx в Google                                       |
| `cloud_io/temp_files.py`              | `sync/runner.py`                                   | Создает/чистит временные директории                                    |
| `processing/pipeline.py`              | `sync/runner.py`                                   | Запускает task1..task5 и возвращает результаты                         |
| `processing/exporter.py`              | `sync/runner.py`                                   | Собирает единый `xlsx` из DataFrame                                    |
| `processing/normalizers.py`           | `processing/tasks/*`                               | Нормализует телефон, дату, сумму, статус                               |
| `processing/tasks/task1.py`           | `processing/pipeline.py`                           | Чистит телефоны/даты                                                   |
| `processing/tasks/task2.py`           | `processing/pipeline.py`                           | Чистит суммы/статусы                                                   |
| `processing/tasks/task3.py`           | `processing/pipeline.py`                           | Удаляет мусор, помечает дубли/повторы                                  |
| `processing/tasks/task4.py`           | `processing/pipeline.py`                           | Агрегирует заказы до 1 строки на `order_id`                            |
| `processing/tasks/task5.py`           | `processing/pipeline.py`                           | Выполняет комплексную очистку                                          |
| `.env`                                | `config.py`                                        | Локальные реальные значения env                                        |
| `.env.example`                        | Пользователь                                       | Шаблон для заполнения `.env`                                           |
| `requirements.txt`                    | Пользователь/pip                                   | Список зависимостей                                                    |


