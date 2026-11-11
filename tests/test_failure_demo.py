import requests


# TEST DEMO 1: Generar un fallo controlado para probar nuestro analizador.
# Consultamos un recurso existente mediante GET.
# Intencionalmente esperamos HTTP 201, aunque la API normalmente devuelve 200.
# Objetivo:
# - Comprobar que Pytest detecta el fallo.
# - Generar un reporte JSON con información del error.
# - Utilizar ese reporte para evaluar el diagnóstico de nuestra IA.
#
# IMPORTANTE: Este test está diseñado para fallar.
# No debe incluirse en la ejecución normal de nuestra suite.

def test_incorrect_http_expectation():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10
    )

    assert response.status_code == 201