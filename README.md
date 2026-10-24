# HEARD — fixed working copy

This bundle contains the FastAPI backend and Flask frontend.

## 1. Backend (Terminal 1)
Open a terminal in `backend` and run:

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend health check: http://127.0.0.1:8000/health

## 2. Frontend (Terminal 2)
Open a second terminal in `frontend` and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000/chat.html or http://127.0.0.1:5000/.

## 3. Tests
From the `backend` folder:

```bash
python -m pip install pytest
python -m pytest -q
```

## Notes
- The core intake parser works locally and does not require a Gemini API key.
- Unknown pad/clot counts produce a missing bleeding score (`null`), not a misleading `0`.
- Qualitative descriptions such as “very painful” and “heavy bleeding” are preserved without inventing numeric scores.
- This is a symptom-organization prototype, not a diagnostic medical device. Safety guidance is conservative and does not replace professional care.
- The ZIP intentionally excludes `.env`, virtual environments, and secrets.
