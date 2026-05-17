from flask import Flask
from database.db import db
from routes.students import students_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(students_bp)

@app.route("/")
def home():
    return "API FUNCIONANDO"

if __name__ == "__main__":
    app.run(debug=True)