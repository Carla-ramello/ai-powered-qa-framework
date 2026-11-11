import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"

def validate_http_status(method, expected, actual):
    if method.upper() == "GET" and expected == 201 and actual == 200:
        return (
            "QA VALIDATION: The test may have an incorrect expectation. "
            "A successful GET request normally returns HTTP 200. "
            "HTTP 201 is typically used when a resource is created. "
            "Review the API contract before changing the test."
        )

    return "QA VALIDATION: No specific rule matched."
# Envía el fallo a Qwen junto con el diagnóstico preliminar de QA.
# La validación es opcional para mantener compatibilidad con otros análisis.
def analyze_with_ai(error_message, qa_validation=None):
    prompt = f"""
You are a senior QA Automation Engineer.

Analyze ONLY the information provided below.

TEST FAILURE:
{error_message}
PRELIMINARY QA VALIDATION:
{qa_validation if qa_validation else "No deterministic validation available."}

IMPORTANT:
The QA validation provides a preliminary diagnosis.
Consider it when analyzing the failure.
Do not contradict the observed HTTP method or status codes.
If the evidence is insufficient, explain the uncertainty.

STRICT RULES:
1. Do not change the HTTP method.
2. Do not invent endpoints, logs, headers or backend behavior.
3. HTTP 200 means OK.
4. HTTP 201 means Created.
5. A successful GET request normally returns HTTP 200.
6. A GET request does not normally create resources.
7. If the test expects 201 for a successful GET,
   consider an incorrect test expectation first.
8. Clearly separate observed facts from possible causes.
9. Do not claim a backend defect without evidence.
10. If information is missing, explicitly say so.

RESPONSE FORMAT:

OBSERVED FAILURE:
Explain what actually happened.

MOST LIKELY CAUSE:
Explain the most likely reason based on the evidence.

RECOMMENDATION:
Suggest one specific action to investigate or fix the issue.

Keep the response under 120 words.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "1m",
            "options": {
                "temperature": 0.1
            }
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]


if __name__ == "__main__":
    error = """
    Test: test_get_posts
    HTTP Method: GET
    Expected status: 201
    Actual status: 200
    """
        # Ejecutamos nuestra regla de QA antes de consultar a la IA.
    qa_result = validate_http_status("GET", 201, 200)

    # Mostramos el diagnóstico generado por Python.
    print("\n===== QA VALIDATION =====")
    print(qa_result)

    # Enviamos a Qwen tanto el error como la validación preliminar.
    print("\n===== AI FAILURE ANALYSIS =====")
    print(analyze_with_ai(error, qa_result))