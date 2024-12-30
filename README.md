# KAM API - README

## Project Overview
The **Key Account Manager (KAM) API** is a system to manage leads, contacts, interactions, call planning, and performance tracking for account managers. Built with **FastAPI**, it provides a structured and scalable backend with features including secure authentication, robust lead and contact management, interaction tracking, and more.

---

## System Requirements

- **Python**: 3.10 or higher
- **PostgreSQL**: 13 or higher
- **Node.js**: (Optional, for frontend integration)
- **Pip**: Latest version
- **Operating System**: Linux, macOS, or Windows

---

## Installation Instructions

### Prerequisites
1. Install Python 3.10+.
2. Install PostgreSQL and ensure it is running.
3. Install pip and virtualenv (optional).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/kam-api.git
   cd kam-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a PostgreSQL database (e.g., `kam_db`).
   - Update the `DATABASE_URL` in the `config.py` file:
     ```python
     DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/kam_db"
     ```
---

## Running Instructions

### Start the Server
Run the following command to start the application:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### Access API Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

---

## API Documentation

### Authentication
- Access:  http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
---

## Sample Usage Examples

### Example 1: Register and Login
1. Register a new user:
   ```bash
   curl -X POST http://127.0.0.1:8000/auth/register \
       -H "Content-Type: application/json" \
       -d '{"username": "user@example.com", "password": "securepass"}'
   ```

2. Login to retrieve the token:
   ```bash
   curl -X POST http://127.0.0.1:8000/auth/login \
       -H "Content-Type: application/json" \
       -d '{"username": "user@example.com", "password": "securepass"}'
   ```

### Example 2: Create a KAM
1. Use the retrieved token to create a KAM:
   ```bash
   curl -X POST http://127.0.0.1:8000/kams \
       -H "Authorization: Bearer <TOKEN>" \
       -H "Content-Type: application/json" \
       -d '{"name": "John Manager", "email": "john.manager@example.com"}'
   ```

---