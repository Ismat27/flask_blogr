from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Text, String, Integer, Boolean,DateTime
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
