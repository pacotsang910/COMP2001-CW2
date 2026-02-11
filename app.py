from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

# 1. Load Environment Variables (Security)
load_dotenv()

# 2. Initialize Flask App
app = Flask(__name__)

# 3. Database Configuration
# We fetch these from the .env file so they aren't hardcoded
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')

# Configure the connection string for ODBC Driver 18
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{user}:{password}@{server}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Initialize Plugins
db = SQLAlchemy(app)
ma = Marshmallow(app)

# 5. Base Route (Sanity Check)
@app.route('/')
def home():
    return {
        "message": "Trail Service API is running",
        "status": "Connected to Database"
    }

# 6. Start the Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)