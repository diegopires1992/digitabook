from . import db


class AuthorsModel(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullabe=False)
    birthplace = db.Column(db.String, nullable=False)
