# Agentic Splunk SRE

An autonomous Site Reliability Engineering agent that leverages Google's Agent Development Kit (ADK) and the Gemini model to write SPL, query Splunk logs, and summarize system issues. 

This project can be run as a standalone FastAPI application, deployed via Docker, or integrated directly into Google Cloud as a Vertex AI Extension.

## Features
- **Autonomous Splunk Queries:** The agent writes and executes its own SPL based on natural language requests.
- **FastAPI Wrapper:** Exposes the ADK agent via a clean REST API.
- **Docker-Ready:** Easily deployable to Google Cloud Run.

## Local Setup
1. Clone the repository and navigate into it.
2. Copy `.env.example` to `.env` and fill in your Splunk (port 8089 access required) and GCP credentials.
3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Run API
```bash
uvicorn app.main:app --reload
```

