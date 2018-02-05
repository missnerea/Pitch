from . import db


#User model
class User(UserMixin,db.Model):

    __tablename__='users'
    id = db.Column(db.Interger,primary_key = True)
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

    id= db.Column(db.Interger, primary_key = True)
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

    id= db.Column(db.Interger,primary_key = True)
    details = db.Column(db.String(255))
    category_id= db.Column(db.Interger,db.ForeignKey("categories.id"))
    user_id= db.Column(db.Interger,db.ForeignKey("users.id"))
    comment = db.relationship("Comments", backref="pitches", lazy = "dynamic")
    vote = db.relationship("Votes", backref="pitches", lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self)
        db.session.commit
