# HEARD Frontend — Flask-ready starter

Purple/lavender responsive frontend, with a dashboard, step-by-step 3-stage symptom form, summary, review checklist, printable clinician brief, safety and privacy pages. Hindi/English toggle is included for UI labels.

## Run the preview on Windows
1. Extract the ZIP.
2. Open the `heard_frontend_flask_ready` folder in File Explorer.
3. Type `cmd` in the address bar and press Enter.
4. Run these commands one at a time:
```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```
5. Open `http://127.0.0.1:5000`.

## Move into your existing Flask + SQLite project
Back up your project first. Copy `templates` and `static` into your existing project, merging carefully. The included `app.py` is only a preview server and has no database logic. Merge its page routes into your existing app rather than replacing your existing `app.py`. Keep the SQLite code untouched for now; the form is demo-only and stores its sample answers in browser session storage, not SQLite.

## Limitations
This is frontend-first; no diagnosis, AI, clinical scoring, or test recommendations. Some long text remains English even after the language toggle. Use fictional data only until security, privacy and consent safeguards are implemented.
