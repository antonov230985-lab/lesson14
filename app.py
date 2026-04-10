from cloud.factory import build_clients
from config import load_config
from logging_setup import setup_logging
from sync.runner import run_forever
from sync.state_store import StateStore


def main() -> None:
    setup_logging()
    config = load_config()
    yandex_client, google_client = build_clients(config)
    state_store = StateStore(config.state_file)
    run_forever(config, yandex_client, google_client, state_store)


if __name__ == "__main__":
    main()
