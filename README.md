# safrs_pa

This project is a minimal runnable copy of the Northwind combined app.

It is intended to be started with `run_with_spa.py`, which:

- runs the FastAPI backend
- serves the built admin SPA at `/admin-app/`

Unlike `projects/northwind`, this project does not include the editable frontend
source tree or `node_modules`. It only ships the built frontend under
`frontend/dist/`.

## Run

From `backend/`:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cd ..
python run_with_spa.py
```

`backend/requirements.txt` installs the current SAFRS source directly from GitHub.

Default URLs:

- admin app: `http://127.0.0.1:5656/admin-app/`
- API: `http://127.0.0.1:5656/api`
- docs: `http://127.0.0.1:5656/docs`
- admin schema: `http://127.0.0.1:5656/ui/admin/admin.yaml`
