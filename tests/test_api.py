import requests

# TEST 1: Verificar que podemos consultar un recurso existente.
# Enviamos una petición GET y comprobamos:
# - Que el servidor responde con HTTP 200 (OK).
# - Que la respuesta contiene un JSON válido.
def test_get_posts():

    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "title" in data
    assert "body" in data

# TEST 2: Verificar el comportamiento ante un recurso inexistente.
# Solicitamos un post que no existe y comprobamos:
# - Que el servidor responde con HTTP 404 (Not Found).
# Esto permite validar el manejo de recursos no encontrados.
def test_get_nonexistent_post():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/999999",
        timeout=10
    )

    assert response.status_code == 404

# TEST 3: Validar la estructura y los tipos de datos de la respuesta.
# Consultamos un post existente y comprobamos:
# - Que la respuesta contiene los campos obligatorios.
# - Que los identificadores son números enteros.
# - Que el título y el contenido son cadenas de texto.
# Esto ayuda a detectar cambios inesperados en el contrato de la API.
def test_get_post_schema():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert isinstance(data["userId"], int)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)

# TEST 4: Verificar la creación simulada de un recurso mediante POST.
# Enviamos un nuevo post con título, contenido e identificador de usuario.
# Comprobamos:
# - Que el servidor devuelve HTTP 201 (Created).
# - Que la respuesta contiene los datos enviados.
# - Que el servidor asigna un identificador al nuevo recurso.
# JSONPlaceholder simula la creación, pero no guarda los datos.

def test_create_post():
    url = "https://jsonplaceholder.typicode.com/posts"

    payload = {
        "title": "AI-Powered QA Framework",
        "body": "Testing API automation with Python and Pytest",
        "userId": 1
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert isinstance(data["id"], int)

# TEST 5: Verificar la actualización simulada de un recurso mediante PUT.
# Enviamos nuevos datos para reemplazar el contenido de un post.
# Comprobamos:
# - Que el servidor devuelve HTTP 200 (OK).
# - Que el identificador del recurso se mantiene.
# - Que la respuesta contiene los datos actualizados.
# JSONPlaceholder simula la actualización, pero no guarda los cambios.

def test_update_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"

    payload = {
        "id": 1,
        "title": "Updated AI-Powered QA Framework",
        "body": "Testing PUT requests with Python and Pytest",
        "userId": 1
    }

    response = requests.put(
        url,
        json=payload,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == payload["id"]
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

    # TEST 6: Verificar la eliminación simulada de un recurso mediante DELETE.
# Enviamos una petición para eliminar un post existente.
# Comprobamos:
# - Que el servidor responde con HTTP 200 (OK).
# - Que la operación no genera un error HTTP.
# JSONPlaceholder simula la eliminación, pero no borra el recurso realmente.

def test_delete_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"

    response = requests.delete(
        url,
        timeout=10
    )

    assert response.status_code == 200