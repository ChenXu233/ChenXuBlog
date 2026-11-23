"""Rotate weak development defaults in a server-side .env file.

Only weak or missing values are changed. Secret values are never printed.
"""

import os
import secrets
from pathlib import Path

WEAK_VALUES = {"", "123456", "admin", "password", "minioadmin", "changeme"}
ENV_PATH = Path(os.environ.get("ENV_FILE", "/work/.env"))


def main() -> None:
    if not ENV_PATH.is_file():
        raise SystemExit(f"Environment file not found: {ENV_PATH}")

    lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    indexes: dict[str, int] = {}
    values: dict[str, str] = {}
    changed: set[str] = set()

    for index, line in enumerate(lines):
        if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
            continue
        raw_key, raw_value = line.split("=", 1)
        key = raw_key.strip()
        if key.startswith("export "):
            key = key.removeprefix("export ").strip()
        indexes[key] = index
        values[key] = raw_value.strip().strip('"').strip("'")

    def put(key: str, value: str) -> None:
        if key in indexes:
            lines[indexes[key]] = f"{key}={value}"
        else:
            indexes[key] = len(lines)
            lines.append(f"{key}={value}")
        values[key] = value
        changed.add(key)

    if values.get("ADMIN_PASSWORD", "").lower() in WEAK_VALUES or len(
        values.get("ADMIN_PASSWORD", "")
    ) < 12:
        put("ADMIN_PASSWORD", secrets.token_urlsafe(36))

    for key in ("ACCESS_SECRET_KEY", "REFRESH_SECRET_KEY"):
        if values.get(key, "").lower() in WEAK_VALUES or len(values.get(key, "")) < 32:
            put(key, secrets.token_urlsafe(48))
    if values["ACCESS_SECRET_KEY"] == values["REFRESH_SECRET_KEY"]:
        put("REFRESH_SECRET_KEY", secrets.token_urlsafe(48))

    if values.get("MINIO_ACCESS_KEY", "").lower() in WEAK_VALUES:
        put("MINIO_ACCESS_KEY", f"minio_{secrets.token_hex(8)}")
    if values.get("MINIO_SECRET_KEY", "").lower() in WEAK_VALUES or len(
        values.get("MINIO_SECRET_KEY", "")
    ) < 12:
        put("MINIO_SECRET_KEY", secrets.token_urlsafe(36))

    if not changed:
        print("Production secrets already meet requirements; no values changed")
        return

    temporary = ENV_PATH.with_name(ENV_PATH.name + ".tmp")
    temporary.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
    os.chmod(temporary, 0o600)
    os.replace(temporary, ENV_PATH)
    print("Rotated weak production settings: " + ", ".join(sorted(changed)))


if __name__ == "__main__":
    main()
