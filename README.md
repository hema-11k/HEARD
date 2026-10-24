# HEARD — AI-Powered Menstrual Health Assessment

HEARD is a menstrual health assessment prototype that helps users organize their reported symptoms and understand relevant assessment findings and safety information.

## Features

- **AI-Powered Symptom Parsing:** Uses Google Gemini to extract relevant information from natural-language symptom descriptions.
- **Menstrual Cycle Assessment:** Identifies cycle lengths outside the typical range.
- **Pain Information:** Preserves reported pain details without assuming an unreported numeric score.
- **Safety Guidance:** Highlights potential warning symptoms and when urgent medical care may be needed.
- **Assessment Interface:** Displays structured findings through a web-based interface.
- **Fallback Parsing:** Supports local parsing when AI parsing is unavailable.

## Technology Stack

- Python
- FastAPI
- Flask
- Google Gemini API
- Pydantic
- HTML, CSS and JavaScript
- Pytest

## Project Structure

```text
HEARD/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   ├── rules.py
│   ├── timing.py
│   ├── test_rules.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd HEARD
```

### 2. Start the backend

Open a terminal in the `backend` directory.

Create and activate a virtual environment on Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file inside `backend`:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace the placeholder with your own API key. Never commit API keys or other secrets.

Start FastAPI:

```powershell
uvicorn main:app --reload
```

Backend health check: http://127.0.0.1:8000/health

Interactive API documentation: http://127.0.0.1:8000/docs

### 3. Start the frontend

Open a second terminal in the `frontend` directory.

Create and activate a separate virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies and start the application:

```powershell
pip install -r requirements.txt
python app.py
```

Open the local URL printed by Flask, typically http://127.0.0.1:5000.

Keep both backend and frontend servers running while testing the integrated application.

## Testing

From the `backend` directory, run:

```powershell
pytest -q
```

The current automated backend test run completed with **5 tests passing**. Full integration and assessment-output validation should also be completed before release.

## Safety and Limitations

- HEARD is an informational prototype, not a diagnostic medical device.
- Assessment results depend on the information provided and the application's rules.
- Missing symptom values should not be treated as confirmed findings.
- Safety guidance does not replace professional medical advice.
- Clinical accuracy, privacy safeguards and end-to-end behaviour require further validation.

## Future Scope

- Multilingual interface and symptom input.
- Improved assessment validation.
- Menstrual history and cycle tracking.
- Additional testing and clinical review.

## Security

Do not upload `.env`, API keys, virtual environments, or cache directories to GitHub. Use fictional data during demonstrations and testing.

## Contributors

Add project team members and their GitHub profiles here.

---

**HEARD — Making menstrual health information easier to understand.**
