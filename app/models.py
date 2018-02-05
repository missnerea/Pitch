from . import db
from flask_login import UserMixin
from datetime import datetime

#User model
class User(UserMixin,db.Model):

    __tablename__='users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, index = True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship("Pitch", backref="user", lazy = "dynamic")
    comment = db.relationship("Comments", backref="user", lazy = "dynamic")
    vote = db.relationship("Votes", backref="user", lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

#PitchCategory model
class PitchCategory(db.Model):
    __tablename__ = 'categories'

    id= db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    #Submit new pitch
    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = PitchCategory.query.all()
        return categories

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id= db.Column(db.Integer,primary_key = True)
    details = db.Column(db.String(255))
    category_id= db.Column(db.Integer,db.ForeignKey("categories.id"))
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship("Comments", backref="pitches", lazy = "dynamic")
    vote = db.relationship("Votes", backref="pitches", lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def  clear_pitches(cls):
        Pitch.all_pitches.clear()

    def get_pitches(self):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches

class Comments(db.Model):
    __tablename__= 'comments'

    id = db.Column(db.Integer,primary_key = True)
    sentiment = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default= datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, ForeignKey("pitch.id"))

    def save_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comments.query.filter_by(Comments.time_posted.desc()).filter_by(pitches_id=id).all()
        return comments

class Votes(db.Model):
    __tablename__='votes'

    id = db.Column(db.Integer,primary_key= True)
    vote = db.Column(db.Integer)
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitch.id"))
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_votes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Votes.query.filter_by(user_id=user_id,pitches_id=pitches_id).all()
        return votes
