from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize these without an app first
db = SQLAlchemy()
ma = Marshmallow()