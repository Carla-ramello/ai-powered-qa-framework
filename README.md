# AI-Powered QA Framework

An API testing framework built with Python and Pytest, featuring automated failure classification and AI-assisted analysis using a locally hosted language model.

The project explores how artificial intelligence can support QA engineers by providing additional context when automated tests fail.

## Features

- **API Test Automation:** Automated REST API tests using Pytest and Requests.
- **HTTP Validation:** Verification of status codes, response bodies, and JSON structures.
- **Failure Classification:** Rule-based identification of assertion errors, timeouts, connection errors, and server errors.
- **AI-Assisted Analysis:** Integration with Ollama to analyze test failures using a local language model.
- **JSON Test Reports:** Generation and processing of structured Pytest reports.
- **Local AI Execution:** AI analysis runs locally without requiring a paid cloud API.

## Tech Stack

- Python
- Pytest
- Requests
- Ollama
- Qwen2.5-Coder 1.5B
- pytest-json-report
- Allure Pytest

## Project Structure

```text
ai-powered-qa-framework/
├── ai_analyzer/
│   ├── analyzer.py
│   └── ollama_client.py
├── config/
├── reports/
├── tests/
│   ├── test_api.py
│   ├── test_analyzer.py
│   └── test_failure_demo.py
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

## Running Tests

Run the standard test suite:

```powershell
python -m pytest -v
```

The standard suite currently contains **11 tests**.

An intentionally failing demonstration test is excluded from the default execution through `pytest.ini`.

Generate a JSON report:

```powershell
python -m pytest -v --json-report --json-report-file=reports/report.json
```

## AI Failure Analysis

This project uses Ollama with the `qwen2.5-coder:1.5b` model.

Install Ollama and download the model:

```powershell
ollama pull qwen2.5-coder:1.5b
```

Run the intentionally failing demonstration test and generate its report:

```powershell
python -m pytest tests/test_failure_demo.py -v -o addopts="" --json-report --json-report-file=reports/failure_demo.json
```

**Note:** The demonstration test is expected to fail.

Analyze the generated report:

```powershell
python ai_analyzer/analyzer.py reports/failure_demo.json
```

The analyzer identifies the failure, classifies the error, and requests an AI-generated explanation from the local Ollama model.

## Limitations

AI-generated explanations may be inaccurate or incomplete. The model can occasionally suggest incorrect causes or recommendations.

The AI analysis should be treated as supporting information rather than a definitive diagnosis. QA engineers must validate the conclusions against the observed results and API specifications.

## Future Improvements

- Validate AI-generated explanations against deterministic QA rules.
- Improve error classification and diagnostic accuracy.
- Generate structured analysis reports.
- Expand automated test coverage.
- Integrate the framework into CI/CD pipelines.

## Author

Carla Ramello

QA Automation | Python | API Testing | AI-Assisted Quality Engineering