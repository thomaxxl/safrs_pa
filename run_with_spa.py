from __future__ import annotations

import argparse
import sys
from pathlib import Path

import uvicorn
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

PROJECT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_DIR / "backend"
SRC_DIR = BACKEND_DIR / "src"
FRONTEND_DIST_DIR = PROJECT_DIR / "frontend" / "dist"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from northwind_backend import create_fastapi_app
from northwind_backend.config import get_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Northwind FastAPI backend and serve the built SPA at /admin-app/.",
    )
    parser.add_argument("--host", help="Bind host override.")
    parser.add_argument("--port", type=int, help="Bind port override.")
    return parser.parse_args()


def create_app():
    if not FRONTEND_DIST_DIR.is_dir():
        raise FileNotFoundError(
            f"Missing frontend build at {FRONTEND_DIST_DIR}. Run `npm run build` in frontend/ first."
        )

    frontend_index = FRONTEND_DIST_DIR / "index.html"
    if not frontend_index.is_file():
        raise FileNotFoundError(
            f"Missing built frontend entrypoint at {frontend_index}. Run `npm run build` in frontend/ first."
        )

    app = create_fastapi_app()

    assets_dir = FRONTEND_DIST_DIR / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="northwind-spa-assets")
        app.mount("/admin-app/assets", StaticFiles(directory=str(assets_dir)), name="northwind-spa-admin-assets")

    @app.get("/admin-app", include_in_schema=False)
    @app.get("/admin-app/", include_in_schema=False)
    def admin_app() -> FileResponse:
        return FileResponse(frontend_index)

    @app.get("/admin-app/{_path:path}", include_in_schema=False)
    def admin_app_fallback(_path: str) -> FileResponse:
        return FileResponse(frontend_index)

    return app


def main() -> None:
    args = parse_args()
    settings = get_settings()
    host = args.host or settings.host
    port = args.port or settings.port
    uvicorn.run(create_app(), host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
