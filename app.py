import connexion
from flask import render_template
import os
from dotenv import load_dotenv
from pathlib import Path
from extensions import db, ma

# 1. Setup Environment Loading
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# 2. Get variables with hardcoded fallbacks for your specific setup
# This ensures it works NOW, even if your .env is still being tricky
user = os.getenv('DB_USER') or 'HK_PTsang'
server = os.getenv('DB_SERVER') or 'dist-6-505.uopnet.plymouth.ac.uk'
database = os.getenv('DB_NAME') or 'COMP2001_HK_PTsang'
# Replace 'YOUR_REAL_PASSWORD' with the actual password from your screenshot
password = os.getenv('DB_PASSWORD') or 'YOUR_REAL_PASSWORD' 

print(f"--- DEBUG: Connecting as User: {user} to Server: {server} ---")

# 3. Create the Connexion application
connex_app = connexion.App(__name__, specification_dir='./')
app = connex_app.app

# 4. Configure the Database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{user}:{password}@{server}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 5. Initialize extensions
db.init_app(app)
ma.init_app(app)

# 6. Add API and Routes
connex_app.add_api("swagger.yml", options={"swagger_url": "/ui"})

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    connex_app.run(host='0.0.0.0', port=5000)