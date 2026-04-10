from domain.models import SyncDecision


def detect_change(
    yandex_version: str | None, google_version: str | None, state: dict[str, str]
) -> SyncDecision:
    prev_yandex = state.get("yandex_version")
    prev_google = state.get("google_version")
    if yandex_version and yandex_version != prev_yandex:
        return SyncDecision(changed=True, source="yandex")
    if google_version and google_version != prev_google:
        return SyncDecision(changed=True, source="google")
    return SyncDecision(changed=False, source=None)
