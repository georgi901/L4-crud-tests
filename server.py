from flask import Flask, request, jsonify

app = Flask(__name__)

# Baza de date in memorie (lista de cursuri)
courses = [
    {"id": 1, "name": "Matematica", "professor": "Prof. Popescu", "credits": 5},
    {"id": 2, "name": "Informatica", "professor": "Prof. Ionescu", "credits": 6},
    {"id": 3, "name": "Fizica", "professor": "Prof. Georgescu", "credits": 4},
]

next_id = 4


# ---------- READ (GET) ----------

@app.route("/courses", methods=["GET"])
def get_courses():
    """Returneaza toate cursurile."""
    return jsonify(courses)


@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Returneaza un curs dupa ID."""
    course = next((c for c in courses if c["id"] == course_id), None)
    if course is None:
        return jsonify({"error": "Cursul nu a fost gasit"}), 404
    return jsonify(course)


# ---------- CREATE (POST) ----------

@app.route("/courses", methods=["POST"])
def create_course():
    """Creeaza un curs nou."""
    global next_id
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Campul 'name' este obligatoriu"}), 400

    course = {
        "id": next_id,
        "name": data["name"],
        "professor": data.get("professor", "Nespecificat"),
        "credits": data.get("credits", 0),
    }
    next_id += 1
    courses.append(course)
    return jsonify(course), 201


# ---------- UPDATE (PUT) ----------

@app.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Modifica un curs existent."""
    course = next((c for c in courses if c["id"] == course_id), None)
    if course is None:
        return jsonify({"error": "Cursul nu a fost gasit"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Body-ul requestului este gol"}), 400

    course["name"] = data.get("name", course["name"])
    course["professor"] = data.get("professor", course["professor"])
    course["credits"] = data.get("credits", course["credits"])

    return jsonify(course)


# ---------- DELETE ----------

@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Sterge un curs."""
    global courses
    original_len = len(courses)
    courses = [c for c in courses if c["id"] != course_id]

    if len(courses) == original_len:
        return jsonify({"error": "Cursul nu a fost gasit"}), 404

    return jsonify({"message": f"Cursul cu ID {course_id} a fost sters"}), 200


if __name__ == "__main__":
    print("Server pornit pe http://localhost:5000")
    print("Endpoints disponibile:")
    print("  GET    /courses          - Lista cursuri")
    print("  GET    /courses/<id>     - Un curs")
    print("  POST   /courses          - Adauga curs")
    print("  PUT    /courses/<id>     - Modifica curs")
    print("  DELETE /courses/<id>     - Sterge curs")
    print()
    app.run(debug=True, port=5000)
