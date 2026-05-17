from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from models.student import Student
from database.db import db

students_bp = Blueprint("students", __name__)


# CREATE
@students_bp.route("/students", methods=["POST"])
def create_student():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    try:
        student = Student(
            dni=data["dni"],
            name=data["name"],
            age=data["age"],
            grade=data["grade"],
            is_approved=data["is_approved"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(student)
        db.session.commit()

        return jsonify(student.to_dict()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "DNI already exists"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


# GET ALL
@students_bp.route("/students", methods=["GET"])
def get_students():

    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


# GET BY ID
@students_bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "student not found"}), 404

    return jsonify(student.to_dict())


# UPDATE
@students_bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "student not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    student.dni = data.get("dni", student.dni)
    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)
    student.grade = data.get("grade", student.grade)
    student.is_approved = data.get("is_approved", student.is_approved)

    student.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify(student.to_dict())

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "DNI already exists"}), 400


# DELETE
@students_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "student deleted"})


# AVERAGE GRADE
@students_bp.route("/students/average", methods=["GET"])
def average_grade():

    students = Student.query.all()

    if len(students) == 0:
        return jsonify({"average": 0})

    total = sum(student.grade for student in students)
    average = total / len(students)

    return jsonify({"average": average})


# BULK INSERT
@students_bp.route("/students/bulk", methods=["POST"])
def bulk_students():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    students = []

    try:
        for item in data:

            student = Student(
                dni=item["dni"],
                name=item["name"],
                age=item["age"],
                grade=item["grade"],
                is_approved=item["is_approved"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            students.append(student)

        db.session.add_all(students)
        db.session.commit()

        return jsonify({"message": "students created"}), 201

    except KeyError as e:
        db.session.rollback()
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


# TABLE (HTML PARTIAL - HTMX)
@students_bp.route("/students/table", methods=["GET"])
def students_table():

    students = Student.query.all()

    return render_template(
        "partials/students_table.html",
        students=students
    )