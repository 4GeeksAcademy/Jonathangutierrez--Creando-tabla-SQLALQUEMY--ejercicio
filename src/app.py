"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Student, Project, Submission
from datetime import datetime
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# FUNCIONES QUE VAMOS A IR UTILIZANDO EN with app.app_contexty():


# Creo estudiante en la tabla
def create_student():
    student = Student(name_student="Alex", email="alex@gmail.es", programming_skills=True) 
    # encolo el producto que quiero crear en base de datos
    db.session.add(student)
    # Confirmo los cambios para que haga los INSERT
    db.session.commit()

# Recuperar 1 estudiante
def get_student(id):
    student = Student.query.get(id)
    print(student)

# Recuperar a todos los estudientes
def get_all_students():
    student = Student.query.all()
    for s in student:
        print(s)   

# Filtar por campos. Por ejemplo: El estudiante con el ID más alto
def student_id_higher():
    student = Student.query.order_by(Student.id.desc()).first()
    print(student)

# Filtrar por campos. Por ejemplo: los estudiantes con conocimientos de programación previa
def students_with_programming_skills():
    students = Student.query.filter(Student.programming_skills == True).all()
    for student in students:
        print(student)

# Crear un nuevo proyecto en la tabla Project
def create_project():
    project = Project(project_name="Fetch API", topics="JavaScript, Fetch, DOM")
    db.session.add(project)
    db.session.commit()

# Recuperar todos los proyectos y mostrarlos en el terminal
def get_all_projects():
    projects = Project.query.all()
    for project in projects:
        print(project) 

# Recupera todos los proyectos que tratan sobre el topic “JavaScript”.
def get_all_projects_with_topic(topic):
    projects = Project.query.filter(Project.topics.like(f'%{topic}%')).all()
    print(projects)

# Estudiantes entregan proyectos
def delivered_project(s_id, p_id, date):
    # student_id es el nombre de la columna de submission
    # s_id simplemente es el valor del parámetro de la función, abreviatura de student_id. Valdría igual sin abreviar (student_id = student_id) pero lo pongo así para acordarme de donde viene.
    projects_done = Submission(student_id = s_id, project_id = p_id, submited_date=date) 
    db.session.add(projects_done)
    db.session.commit() 

# Recupera todos los proyectos entregados por un studiante (usa su Id para recuperar el estudiante de la base de datos). Para cada proyecto que ha entregado, muestra su nombre y sus topics.
def get_projects_delivered_by_student(s_id):
    student = Student.query.get(s_id)
    for project in student.submissions:
        print(project)

#  Recupera todos los proyectos de todos lo estudiantes cuya fecha de entrega ha sido antes del 17 de Abril de 2023.
#  Para cada proyecto, muestra el nombre del estudiante que lo entregó y la fecha exacta de entrega.

def get_projects_before_date(date):
    submissions = Submission.query.filter(Submission.submited_date < date).all()
    for submission in submissions:
        print(submission)






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
   # app.run(host='0.0.0.0', port=PORT, debug=False)

    # Lo necesitamos para pdoer ejecutar código Python normal fuera del entorno de Flask
    with app.app_context():
        # create_student()
        # get_student(3)
        # get_all_students()
        # student_id_higher()
        # students_with_programming_skills()
        # create_project()
        # get_all_projects()
        # get_all_projects_with_topic("JavaScript")
        # delivered_project(3, 2, datetime(2023, 4, 18))
        # get_projects_delivered_by_student(3)
        get_projects_before_date(datetime(2023, 4, 17))

