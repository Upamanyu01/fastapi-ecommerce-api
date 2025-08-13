# FastAPI Ecommerce API

A fully functional Ecommerce API built using **FastAPI** with **SQLAlchemy**, **PostgreSQL**, **JWT-based authentication**, and full CRUD operations for Brands, Categories, Subcategories, and Products. Supports filtering, pagination, and role-based access control (Admin/User).

---

## Features

### User Authentication
- **Signup and Login:** Register and authenticate users.
- **JWT-based Authentication:** Secure endpoints with JSON Web Tokens.
- **Role-based Access:** Separate permissions for Admin and User roles.

### Brands
- Full CRUD operations (Create, Read, Update, Delete).
- Admin-only access for creating, updating, and deleting brands.

### Categories
- Full CRUD operations.
- Admin-only access for modifications.

### Subcategories
- Full CRUD operations.
- Linked to categories.
- Admin-only access for modifications.

### Products
- Full CRUD operations.
- Linked to Brand, Category, and Subcategory.
- Supports filtering by category, brand, and price range.
- Pagination and sorting capabilities.
- Admin-only access for modifications.

### Validation
- Pydantic schemas for robust field validation.
- Handles empty fields and invalid data gracefully.

### Logging
- All API requests and errors are logged to `app.log`.

---

## Tech Stack
- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Validation:** Pydantic
- **Server:** Uvicorn

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Upamanyu01/fastapi-ecommerce-api.git
cd fastapi-ecommerce-api

2. Create a Virtual Environment

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Set Up the Database


Create a PostgreSQL database named ecommerce_db.
Update database connection settings in database.py.

5. Run Migrations / Create Tables
python -m app.database

6. Run the Application
python run.py

Access API documentation: http://127.0.0.1:8000/docs
Alternative ReDoc: http://127.0.0.1:8000/redoc