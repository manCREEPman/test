from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return dict(id=self.id, name=self.name)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(160), nullable=False, unique=True)
    password = db.Column(db.String(260), nullable=False)
    vk_user_id = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return f"<user {self.user_id}>"

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    vk_group_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<group {self.group_id}>"

class User_group(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), primary_key=True)

    def __repr__(self):
        return f"<user_group {self.user_id}: {self.group_id}>"

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    author_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    state = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    changed = db.Column(db.DateTime)
    changed_by = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)
    text = db.Column(db.Text)

    def __repr__(self):
        return f"<post {self.post_id}: {self.author_user_id}>"

class Post_attachement_image(db.Model):
    attachement_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    image = db.Column(db.LargeBinary, nullable=False)
    tag = db.Column(db.String(64))

    def __repr__(self):
        return f"<post {self.attachement_id}: {self.post_id}>"

class Post_attachement(db.Model):
    attachement_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    vk_object = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<post {self.attachement_id}: {self.post_id}>"

class Uploaded_image_gtt(db.Model):
    __table_args__ = {'prefixes': ['TEMPORARY']}
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    tag = db.Column(db.String(64))

    def __repr__(self):
        return f"<post {self.num}>"

class Post_gtt(db.Model):
    __table_args__ = {'prefixes': ['TEMPORARY']}
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.DateTime)
    text = db.Column(db.Text)

    def __repr__(self):
        return f"<post {self.order}>"

class Post_attachement_image_gtt(db.Model):
    __table_args__ = {'prefixes': ['TEMPORARY']}
    id = db.Column(db.Integer, primary_key=True)
    post_gtt_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    tag = db.Column(db.String(64))

    def __repr__(self):
        return f"<post {self.order}>"

class Post_attachement_gtt(db.Model):
    __table_args__ = {'prefixes': ['TEMPORARY']}
    id = db.Column(db.Integer, primary_key=True)
    post_gtt_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    vk_object = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<post {self.order}>"

