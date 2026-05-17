from database.db import db
from datetime import datetime

class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    dni = db.Column(
        db.String(8),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    grade = db.Column(
        db.Float,
        nullable=False
    )

    is_approved = db.Column(
        db.Boolean,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):

        return {
            "id": self.id,
            "dni": self.dni,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "is_approved": self.is_approved,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }