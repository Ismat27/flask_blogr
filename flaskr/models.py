from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Text, String, Integer

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

