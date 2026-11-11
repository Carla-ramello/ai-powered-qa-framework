import json
from pathlib import Path
# Importamos el cliente que permite consultar nuestra IA local.
try:
    from ai_analyzer.ollama_client import analyze_with_ai
except ModuleNotFoundError:
    from ollama_client import analyze_with_ai

# Clasifica los errores detectados por Pytest.
# Buscamos nombres específicos de excepciones para evitar falsos positivos.
# Por ejemplo, timeout=10 no significa que haya ocurrido un TimeoutError.

def classify_error(error_message):
    error_message = str(error_message).lower()

    # Error de aserción: el resultado real no coincide con el esperado.
    if "assertionerror" in error_message:
        return "ASSERTION ERROR"

    # Error de tiempo de espera: la operación tardó demasiado.
    elif (
        "timeoutexception" in error_message
        or "readtimeout:" in error_message
        or "connecttimeout:" in error_message
        or "timeouterror:" in error_message
    ):
        return "TIMEOUT ERROR"

    # Error de conexión: no se pudo establecer comunicación.
    elif "connectionerror:" in error_message:
        return "CONNECTION ERROR"

    # Error HTTP del servidor.
    elif "500 internal server error" in error_message:
        return "SERVER ERROR"

    # No encontramos una excepción reconocida.
    else:
        return "UNKNOWN ERROR"


# Analiza los resultados de Pytest a partir de un reporte JSON.
# Por defecto utiliza report.json, pero permite indicar otro archivo.
def analyze_test_results(report_file="reports/report.json"):
    report_path = Path(report_file)

    if not report_path.exists():
        print("ERROR: Test report not found.")
        return

    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    tests = report.get("tests", [])

    print("\n===== QA TEST ANALYSIS =====")

    for test in tests:
        test_name = test.get("nodeid")
        outcome = test.get("outcome", "unknown")

        print(f"\nTest: {test_name}")
        print(f"Status: {outcome.upper()}")

        if outcome == "failed":
            print("Failure detected!")

            call = test.get("call", {})
            error = call.get(
                "longrepr",
                "No error details available."
            )

            print(f"Error details:\n{error}")

            error_type = classify_error(error)

            print(f"Error classification: {error_type}")

            # Enviamos el error a nuestra IA local para analizarlo.
            print("\n===== AI FAILURE ANALYSIS =====")

            try:
                ai_analysis = analyze_with_ai(
                    f"Error classification: {error_type}\n"
                    f"Test: {test_name}\n"
                    f"Failure details:\n{error}"
                )

                print(ai_analysis)

            except Exception as exc:
                # Si Ollama falla, mostramos el error sin detener el análisis.
                print(f"AI analysis unavailable: {exc}")

    print("\n===== ANALYSIS COMPLETED =====")
    


if __name__ == "__main__":
    import sys

    # Permite indicar la ruta del reporte desde PowerShell.
    # Si no se proporciona una ruta, utiliza el reporte principal.
    report_file = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "reports/report.json"
    )

    analyze_test_results(report_file)