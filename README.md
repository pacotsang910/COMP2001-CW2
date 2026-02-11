**Trail Service Micro-service (COMP2001)**
Project Overview
This micro-service provides a RESTful API for managing trail data, including metadata and geographic coordinates. It is built using Python, Flask, and Connexion, and it integrates with a remote Microsoft SQL Server for persistent storage and the University of Plymouth's authentication system for secure access control.

**Key Features**
Full CRUD Support: Create, Read, Update, and Delete trails.
Geo-Data Management: Handles nested LocationPoint data with sequence ordering.
Security: Header-based authentication (X-Email / X-Password) with ownership verification.
API Documentation: Interactive documentation via Swagger UI (OpenAPI 3.0).
Containerized: Fully portable via Docker.

**Prerequisites**
To run this project locally, you will need:
1. Python 3.11+
2. Docker Desktop (optional, for containerization)
3. ODBC Driver 18 for SQL Server
4. A .env file containing the following variables:
  The username, password, the server and database name

**Installation & Setup**
1. Local Setup
    a. Clone the repository:
       git clone <your-repo-url>
       cd COMP2001-CW2
2. Create and activate a virtual environment:
      python -m venv venv
     .\venv\Scripts\activate
3. Install dependencies:
     pip install -r requirements.txt
4. Run the application:
     python app.py

**API Usage & Documentation**
Once the server is running, access the interactive API documentation at: http://localhost:5000/ui

**System Architecture**
The micro-service follows a layered architecture to ensure separation of concerns:
API Layer (Connexion): Validates input against swagger.yml.
Logic Layer (trails.py): Handles authentication and ownership checks.
Data Layer (SQLAlchemy): Manages ORM mapping to MS SQL Server.

Author
Name: Tsang Pak Ho
Student ID: 10967029
University: University of Plymouth
Module: COMP2001 Information Management & Retrieval

