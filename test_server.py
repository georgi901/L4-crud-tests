import pytest
import json
from server import app


@pytest.fixture
def client():
    """Creeaza un client de test Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_courses():
    """Reseteaza lista de cursuri inainte de fiecare test."""
    import server
    server.courses = [
        {"id": 1, "name": "Matematica", "professor": "Prof. Popescu", "credits": 5},
        {"id": 2, "name": "Informatica", "professor": "Prof. Ionescu", "credits": 6},
        {"id": 3, "name": "Fizica", "professor": "Prof. Georgescu", "credits": 4},
    ]
    server.next_id = 4


# ==================== TESTE READ (GET) ====================

class TestGetCourses:
    def test_get_all_courses(self, client):
        """Verifica ca GET /courses returneaza toate cursurile."""
        response = client.get("/courses")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3

    def test_get_all_courses_content(self, client):
        """Verifica ca primul curs are campurile corecte."""
        response = client.get("/courses")
        data = response.get_json()
        assert data[0]["name"] == "Matematica"
        assert data[0]["professor"] == "Prof. Popescu"
        assert data[0]["credits"] == 5

    def test_get_single_course(self, client):
        """Verifica ca GET /courses/1 returneaza cursul corect."""
        response = client.get("/courses/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Matematica"
        assert data["id"] == 1

    def test_get_course_not_found(self, client):
        """Verifica ca GET /courses/999 returneaza 404."""
        response = client.get("/courses/999")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


# ==================== TESTE CREATE (POST) ====================

class TestCreateCourse:
    def test_create_course(self, client):
        """Verifica ca POST /courses creeaza un curs nou."""
        new_course = {
            "name": "Baze de Date",
            "professor": "Prof. Marinescu",
            "credits": 5
        }
        response = client.post("/courses", json=new_course)
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Baze de Date"
        assert data["id"] == 4

    def test_create_course_appears_in_list(self, client):
        """Verifica ca un curs nou apare in lista dupa creare."""
        client.post("/courses", json={"name": "Chimie", "credits": 3})
        response = client.get("/courses")
        data = response.get_json()
        assert len(data) == 4
        names = [c["name"] for c in data]
        assert "Chimie" in names

    def test_create_course_without_name(self, client):
        """Verifica ca POST fara 'name' returneaza 400."""
        response = client.post("/courses", json={"professor": "Prof. X"})
        assert response.status_code == 400

    def test_create_course_default_professor(self, client):
        """Verifica ca profesorul implicit este 'Nespecificat'."""
        response = client.post("/courses", json={"name": "Logica"})
        data = response.get_json()
        assert data["professor"] == "Nespecificat"


# ==================== TESTE UPDATE (PUT) ====================

class TestUpdateCourse:
    def test_update_course_name(self, client):
        """Verifica ca PUT modifica numele cursului."""
        response = client.put("/courses/1", json={"name": "Matematica Avansata"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Matematica Avansata"
        # Celelalte campuri raman neschimbate
        assert data["professor"] == "Prof. Popescu"

    def test_update_course_all_fields(self, client):
        """Verifica ca PUT modifica toate campurile."""
        update = {
            "name": "Fizica Cuantica",
            "professor": "Prof. Einstein",
            "credits": 7
        }
        response = client.put("/courses/3", json=update)
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Fizica Cuantica"
        assert data["professor"] == "Prof. Einstein"
        assert data["credits"] == 7

    def test_update_course_not_found(self, client):
        """Verifica ca PUT pe un curs inexistent returneaza 404."""
        response = client.put("/courses/999", json={"name": "Test"})
        assert response.status_code == 404


# ==================== TESTE DELETE ====================

class TestDeleteCourse:
    def test_delete_course(self, client):
        """Verifica ca DELETE sterge cursul."""
        response = client.delete("/courses/2")
        assert response.status_code == 200
        # Verificam ca nu mai exista
        response = client.get("/courses/2")
        assert response.status_code == 404

    def test_delete_course_reduces_count(self, client):
        """Verifica ca dupa stergere avem un curs mai putin."""
        client.delete("/courses/1")
        response = client.get("/courses")
        data = response.get_json()
        assert len(data) == 2

    def test_delete_course_not_found(self, client):
        """Verifica ca DELETE pe un curs inexistent returneaza 404."""
        response = client.delete("/courses/999")
        assert response.status_code == 404

    def test_delete_then_other_courses_intact(self, client):
        """Verifica ca stergerea unui curs nu afecteaza celelalte."""
        client.delete("/courses/2")
        response = client.get("/courses/1")
        assert response.status_code == 200
        assert response.get_json()["name"] == "Matematica"
        response = client.get("/courses/3")
        assert response.status_code == 200
        assert response.get_json()["name"] == "Fizica"
