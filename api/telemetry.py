"""Privacy-preserving Supabase telemetry for beta usage and feedback."""
import hashlib
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class TelemetryUnavailable(RuntimeError):
    pass


def _configuration() -> tuple[str, str, str]:
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    salt = os.getenv("ANALYTICS_HASH_SALT", "") or key
    if not url or not key:
        raise TelemetryUnavailable("Supabase telemetry is not configured")
    return url, key, salt


def anonymous_hash(value: str) -> str:
    _, _, salt = _configuration()
    return hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()


def insert_row(table: str, payload: dict) -> None:
    url, key, _ = _configuration()
    request = Request(
        f"{url}/rest/v1/{table}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    try:
        with urlopen(request, timeout=8) as response:
            if not 200 <= response.status < 300:
                raise TelemetryUnavailable(f"Supabase returned {response.status}")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise TelemetryUnavailable("Supabase request failed") from exc
