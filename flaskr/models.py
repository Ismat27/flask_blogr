from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Text, String, Integer, Boolean,DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

db = SQLAlchemy()
migrate = Migrate()

def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

class Variable(db.Model):
    __tablename__ = "variables"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    value = Column(Text, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    username = Column(String(200), server_default='unknown')
    first_name = Column(String(200))
    last_name = Column(String(200))
    email = Column(String(200))
    password = Column(Text)
    is_admin = Column(Boolean, server_default='f')
    is_superuser = Column(Boolean, server_default='f')
    signup_date = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now())
    cp = Column(Integer, nullable=False, default=0, server_default='0') # challenge points
    cap = Column(Integer, nullable=False, default=0, server_default='0') # course access points

    def __repr__(self):
        return f'<User id: {self.id} name: {self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def format(self):
        return {
            'id': self.public_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'challenge_points': self.cp,
            'course_access_points': self.cap
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Referral(db.Model):
    __tablename__ = 'referrals'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    commission = Column(Numeric(10, 2))
    status = Column(Boolean, server_default='f')
    date_created = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='referrals', foreign_keys=[user_id])
    refered_user_id = Column(Integer, ForeignKey('users.id'))
    refered_user = relationship('User', backref=backref("refered_in", uselist=False), foreign_keys=[refered_user_id])
    

    def format(self):
        return {
            'commission': self.commission,
            'referred_user': self.refered_user.fullname(),
            'status': self.status,
            'date_created': self.date_created
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    name = Column(String(200), nullable=False)
    access_points = Column(Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Question(db.Model):
    """Table for quiz questions
        cp: challenge points
        cap: course access points
    """
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    cp_wrong = Column(Integer, nullable=False)
    cp_right = Column(Integer, nullable=False)
    cap_wrong = Column(Integer, nullable=False)
    cap_right = Column(Integer, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def quiz_format(self):
        options = [
            self.option_a, self.option_b,
            self.option_c, self.option_d,
        ]
        return {
            'options': options,
            'question': self.text,
            'id': self.id,
        }
    
    def format(self):
        options = [
            self.option_a, self.option_b,
            self.option_c, self.option_d,
        ]
        opt = ['a', 'b', 'c', 'd']
        correct_option = ''
        for (key, value) in zip(opt, options):
            if value == self.answer:
                correct_option = key
                break
        return {
            'options': options,
            'question': self.text,
            'correct_option': correct_option,
            'id': self.id,
            'date_created': self.date_created
        }

class QuizSession(db.Model):
    """Table for quiz sessions users have taken
    """
    __tablename__ = 'quiz_sessions'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='quiz_taken', foreign_keys=[user_id])
    questions = Column(Text)
    score = Column(Integer, server_default='0')
    completed = Column(Boolean, server_default='f')
    date_created = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now())

    def __str__(self):
        return f'QuizSession taken by {self.user}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'taken_by': self.user.fullname(),
            'date': self.date_created,
            'score': self.score,
            'id': self.id,
            'completed': self.completed
        }
