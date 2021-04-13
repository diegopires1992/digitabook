from . import db

class UserModel(db.Model):
    __tablename__ = "UserModel"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(30), nullable = False)
    cpf = db.Column(db.String(11), nullable = False, unique = True)
    phone = db.Column(db.Integer, nullable = False, unique = True)