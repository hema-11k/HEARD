# HEARD — Your Story. Be Heard.

**A Women's Healthcare Appointment-Preparation Web App**

HEARD helps women prepare for healthcare appointments by organising their symptoms, highlighting patterns worth discussing, checking menstrual-cycle-related test timing and generating a concise, printable brief to share with a clinician.

> **HEARD does not diagnose.** It helps users prepare for a more informed conversation with a qualified healthcare professional.

**Team Rocket** · PS1: Women's Healthcare  
**Institution:** IPS Academy, Institute of Engineering & Science, Indore

---

## The Problem

Healthcare appointments are often short, making it difficult for patients to explain their symptoms, remember important details or communicate how their symptoms affect daily life. Information about symptom duration, menstrual cycle patterns and pain can be overlooked.

Delayed diagnosis is a documented challenge in women's healthcare. A multicentre study across ten countries reported an average diagnostic delay of approximately 6.7 years for endometriosis (Nnoaham et al., 2011).

HEARD aims to bridge this communication gap by turning unstructured symptom descriptions into organised, appointment-ready information.

## What HEARD Does

### 1. Describe Symptoms in Your Own Words

Users can describe their concerns in English, Hindi or Hinglish. Google Gemini helps interpret and structure natural-language descriptions into relevant fields while retaining the original description.

### 2. Highlight Patterns Worth Discussing

A transparent, rule-based engine identifies patterns that may warrant discussion, such as menstrual cycle lengths outside commonly used adult reference ranges or severe pain persisting for more than three months.

Missing information is not automatically treated as a confirmed symptom.

### 3. Cycle-Aware Test Timing

Users can select a planned hormone test and provide their last period date. HEARD calculates a suggested timing window where supported and flags potential timing mismatches.

These windows are informational guides, not personalised medical orders. Users should confirm test timing with their clinician.

### 4. Generate a Clinician Brief

HEARD generates a concise, printable brief containing:

- The user's original symptom description
- Relevant rule-based findings
- Test-timing information
- Suggested questions for the clinician
- An advocacy prompt to help users communicate their concerns

### 5. Independent Safety Checks

Rule-based checks identify configured warning signs, such as fainting or soaking a pad every hour, and display an urgent-care message.

These checks operate independently of Gemini parsing and do not rely solely on AI responses.

## Try the Demo

Use fictional information to explore the application.

| Field | Example |
|---|---|
| Description | `mera cycle 28 din ka hai aur bahut dard hota hai` |
| Duration | More than 3 months |
| Last period | 12 days ago |
| Planned test | FSH / LH / Estradiol |
| Pain | Severe |

Submit the form and review the generated findings, test-timing information and clinician brief.

To explore the safety-check workflow, try this fictional description:

`I fainted and I am soaking a pad every hour`

The application should display the corresponding configured safety warning.



## How It Works

```text
Browser
HTML / CSS / JavaScript
Served by Flask
        |
        | POST /assess
        v
FastAPI Backend
        |
        +-- Gemini Parser
        |   Natural-language interpretation
        |
        +-- Local Parser
        |   Fallback when Gemini is unavailable
        |
        +-- Safety Checks
        |   Independent keyword and rule checks
        |
        +-- Rules Engine
        |   Cycle patterns, duration and pain
        |
        +-- Test Timing
            Cycle dates and suggested windows
        |
        v
Structured Findings
Test-Timing Information
Suggested Questions
Printable Clinician Brief
```

### Design Principles

- **AI for language, rules for findings:** Gemini assists with interpreting and structuring language. Configured application rules determine findings, safety flags and timing calculations.
- **Fallback parsing:** A local parser provides a fallback when Gemini is unavailable or its response cannot be processed, subject to the implemented fallback logic.
- **Privacy-conscious design:** HEARD does not maintain its own user database or account system. Assessment results are held in browser session storage.
- **Transparent limitations:** Missing information is not assumed, and findings are not presented as a diagnosis.

## Tech Stack

| Component | Technology |
|---|---|
| Backend API | Python, FastAPI |
| Data validation | Pydantic |
| Frontend server | Flask |
| User interface | HTML, CSS, JavaScript |
| AI-assisted parsing | Google Gemini API |
| Fallback parsing | Local parser |
| Testing | Pytest |

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
│   ├── templates/
│   ├── static/
│   └── requirements.txt
├── .gitignore
└── README.md
```

### Key Files

- `backend/main.py` — FastAPI application and API endpoints
- `backend/models.py` — Pydantic data models
- `backend/parser.py` — Gemini parsing and local fallback logic
- `backend/rules.py` — Rule-based findings and suggested questions
- `backend/timing.py` — Test-timing calculations
- `backend/test_rules.py` — Automated tests
- `frontend/app.py` — Flask application
- `frontend/templates/` — HTML pages
- `frontend/static/` — CSS, JavaScript and other static assets



## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip
- Git
- A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/hema-11k/HEARD.git
cd HEARD
```

### 2. Configure Gemini API

Obtain an API key through [Google AI Studio](https://aistudio.google.com/).

Create a `.env` file inside the `backend/` directory with the environment variable names expected by the application:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_supported_model_name
```

- `GEMINI_API_KEY` — Your Google Gemini API key.
- `GEMINI_MODEL` — The supported Gemini model configured for the application.(gemini-3.8-flash used)

Use a model that is available to your API key and supported by the current implementation.

**Security:** Never commit your `.env` file or expose your API key in frontend JavaScript, public screenshots or GitHub.

### 3. Set Up and Run the Backend

Open a terminal in the repository root:

```bash
cd backend
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

The backend should be available at:

- **Health check:** http://127.0.0.1:8000/health
- **API documentation:** http://127.0.0.1:8000/docs

Keep this terminal running.

### 4. Set Up and Run the Frontend

Open a second terminal in the repository root:

```bash
cd frontend
python -m venv venv
```

Activate the frontend environment.

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Flask:

```bash
python app.py
```

Open the application at:

http://127.0.0.1:5000

Keep both servers running while testing the application locally.

**Important:** The frontend must be configured to call the correct backend URL. Local development typically uses `http://127.0.0.1:8000`; a deployed frontend must use the deployed backend URL.

### 5. Run the Tests

Open a terminal in the backend directory, activate its virtual environment and run:

```bash
pytest -q
```

Review the output to confirm whether the tests pass.

## Safety, Privacy and Limitations

- **Not a medical device:** HEARD supports appointment preparation. It does not diagnose medical conditions, prescribe treatment or replace professional medical advice.
- **Informational test windows:** Suggested hormone-test windows reflect commonly used timing guidance. Appropriate timing depends on the specific test, its purpose and individual circumstances. Users should confirm timing with their clinician.
- **Adult-focused design:** HEARD is intended for adults aged 18 and older. Menstrual patterns may differ during adolescence.
- **Irregular cycles:** Some timing calculations may be unreliable when cycles are irregular or information is incomplete. The application should communicate these limitations rather than imply certainty.
- **External AI processing:** When Gemini parsing is enabled, relevant user-entered text is sent to Google's Gemini API for processing. Avoid entering unnecessary identifying information.
- **Application storage:** HEARD does not maintain its own database or user accounts. Results held in browser session storage may remain accessible within the browser session. This does not guarantee that no data is processed or retained elsewhere.
- **Further validation required:** Clinical review of the rules, verification of test-timing guidance, accessibility testing and a privacy review are necessary before real-world clinical use.

## Future Scope

- Clinical review and validation of the rule engine
- Longitudinal symptom tracking with informed consent
- Expanded Hindi and multilingual interface support
- Secure, consent-based storage for returning users
- More detailed bleeding and pain tracking
- Expanded automated testing and accessibility improvements

## References

1. Nnoaham KE, et al. Impact of endometriosis on quality of life and work productivity: a multicenter study across ten countries. *Fertility and Sterility.* 2011;96(2):366–373.
2. American College of Obstetricians and Gynecologists. Committee Opinion No. 651: Menstruation in Girls and Adolescents: Using the Menstrual Cycle as a Vital Sign. *Obstetrics & Gynecology.* 2015;126:e143–e146.

## Team

**Team Rocket**

- **Member 1:** Hemandri Khanduja
- **Member 2:** Himanshi Suryavanshi

**Institution:** IPS Academy, Institute of Engineering & Science, Indore

---

**HEARD — Better Preparation. Better Conversations. Better Care.**
