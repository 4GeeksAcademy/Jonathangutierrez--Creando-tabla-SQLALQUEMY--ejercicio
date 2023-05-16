from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_student = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    programming_skills = db.Column(db.Boolean(), unique=False, nullable=False)

    


    # En la función repr le decimos cómo debemos representar en pantalla los datos que nos piden. Self se refiere a si mismo, en la tabla Student. Podemos añadir todos los datos que queramos mostrar.       
    def __repr__(self):
        return f'<Student {self.name_student} - {self.email}>'
    
class Project(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     project_name = db.Column(db.String(120), unique=True, nullable=False)   
     topics = db.Column(db.String(120), unique=False, nullable=False)  

     def __repr__(self):
         return f'<Project {self.project_name}>'
      
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    submited_date = db.Column(db.Date, nullable=False)


     # En backref ponemos el nombre de la tabla, en minúsculas y en plural
    student = relationship('Student', backref='submissions')
    project = relationship('Project', backref='submissions')

    def __repr__(self):
        return f'{self.student.name_student} - <Project {self.submited_date}>'

   


