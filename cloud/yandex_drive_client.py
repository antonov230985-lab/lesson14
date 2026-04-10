from pathlib import Path

import requests

from domain.models import RemoteFileMeta


class YandexDriveClient:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token: str) -> None:
        self._headers = {"Authorization": f"OAuth {token}"}

    def get_file_meta(self, remote_path: str) -> RemoteFileMeta:
        response = requests.get(
            self.BASE_URL,
            headers=self._headers,
            params={"path": remote_path, "fields": "md5,modified"},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        version = payload.get("md5") or payload.get("modified") or "unknown"
        return RemoteFileMeta(version=version, modified=payload.get("modified"), source="yandex")

    def download_file(self, remote_path: str, local_path: Path) -> None:
        link_resp = requests.get(
            f"{self.BASE_URL}/download",
            headers=self._headers,
            params={"path": remote_path},
            timeout=30,
        )
        link_resp.raise_for_status()
        href = link_resp.json()["href"]
        file_resp = requests.get(href, timeout=120)
        file_resp.raise_for_status()
        local_path.write_bytes(file_resp.content)

    def upload_file(self, local_path: Path, remote_path: str) -> None:
        link_resp = requests.get(
            f"{self.BASE_URL}/upload",
            headers=self._headers,
            params={"path": remote_path, "overwrite": "true"},
            timeout=30,
        )
        link_resp.raise_for_status()
        href = link_resp.json()["href"]
        with local_path.open("rb") as input_file:
            upload_resp = requests.put(href, data=input_file, timeout=120)
            upload_resp.raise_for_status()
