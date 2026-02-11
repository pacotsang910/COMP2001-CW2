import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

#1. Load security variables from .env
load_dotenv()

# 2. Create the Connexion application instance 
# specification_dir tells it where to look for swagger.yml 
connex_app = connexion.App(__name__, specification_dir='./')

# 3. Get the underlying Flask app instance
app = connex_app.app

# 4. Database Configuration (ODBC Driver 18)
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{user}:{password}@{server}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Performance boost 

# 5. Initialize Plugins 
db = SQLAlchemy(app)
ma = Marshmallow(app)
import models

# 6. Load the Swagger definition 
connex_app.add_api("swagger.yml")

@app.route('/')
def home():
    return "<h1>Trail Service API</h1><p>Documentation available at /api/ui</p>"

if __name__ == '__main__':
    connex_app.run(host='0.0.0.0', port=5000, debug=True)