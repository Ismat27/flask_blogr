from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
