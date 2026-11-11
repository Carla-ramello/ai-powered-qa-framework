from ai_analyzer.analyzer import classify_error


# TEST 1: Verificar que los errores de aserción se clasifican correctamente.
# Simulamos un AssertionError generado por Pytest.
# Esperamos que el clasificador devuelva ASSERTION ERROR.
def test_classify_assertion_error():
    error = "AssertionError: assert 200 == 201"

    result = classify_error(error)

    assert result == "ASSERTION ERROR"


# TEST 2: Evitar falsos positivos al encontrar timeout=10.
# El parámetro timeout=10 configura el tiempo máximo de espera.
# Su presencia no significa que haya ocurrido un timeout.
# Esperamos que el error se clasifique como ASSERTION ERROR.
def test_timeout_parameter_not_classified_as_timeout():
    error = """
    response = requests.get(url, timeout=10)
    AssertionError: assert 200 == 201
    """

    result = classify_error(error)

    assert result == "ASSERTION ERROR"


# TEST 3: Verificar la clasificación de un timeout real.
# Simulamos una excepción ReadTimeout.
# Esperamos que el clasificador devuelva TIMEOUT ERROR.
def test_classify_timeout_error():
    error = "requests.exceptions.ReadTimeout: Request timed out"

    result = classify_error(error)

    assert result == "TIMEOUT ERROR"


# TEST 4: Verificar la clasificación de errores de conexión.
# Simulamos una excepción ConnectionError.
# Esperamos que el clasificador devuelva CONNECTION ERROR.
def test_classify_connection_error():
    error = "requests.exceptions.ConnectionError: Connection refused"

    result = classify_error(error)

    assert result == "CONNECTION ERROR"


# TEST 5: Verificar el comportamiento ante errores desconocidos.
# Cuando no reconocemos ninguna excepción, esperamos UNKNOWN ERROR.
def test_classify_unknown_error():
    error = "Unexpected application behavior"

    result = classify_error(error)

    assert result == "UNKNOWN ERROR"