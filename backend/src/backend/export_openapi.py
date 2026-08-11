"""Export OpenAPI schema to openapi.json (for frontend codegen).

Usage: python -m backend.export_openapi
"""
import json
from pathlib import Path

from backend import app
from backend.router import init_routers


def main() -> None:
    # init_routers normally runs inside lifespan; call it here so the
    # schema includes every router.
    init_routers(app)
    schema = app.openapi()
    out = Path(__file__).resolve().parent.parent.parent / "openapi.json"
    out.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"openapi.json written: {out} ({len(json.dumps(schema))} bytes)")


if __name__ == "__main__":
    main()
