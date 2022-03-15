from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(100))

    def __init__(self, id, name):
        self.id = id
        self.name = name


    def to_dict(self):
        return dict(id=self.id, name=self.name)
