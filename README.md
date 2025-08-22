# Library Management API

A comprehensive CRUD API built with FastAPI and PostgreSQL for managing users and books. This API provides full CRUD operations, search functionality, and comprehensive Swagger documentation.

## Features

- **User Management**: Create, read, update, and delete users
- **Book Management**: Create, read, update, and delete books
- **Relationships**: Books are linked to users (owners)
- **Search**: Search books by title or author
- **Pagination**: Support for pagination on list endpoints
- **Validation**: Email validation and data validation using Pydantic
- **Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Testing**: Comprehensive test suite with pytest

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **Uvicorn**: ASGI server implementation
- **Pipenv**: Dependency management
- **Pytest**: Testing framework

## Project Structure

```
library_api/
│── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization
│   ├── database.py            # DB connection & session
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── crud.py                # DB operations (optional layer)
│   ├── deps.py                # Dependencies (e.g., get_db)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py           # User CRUD endpoints
│   │   ├── books.py           # Book CRUD endpoints
│   │   └── health.py          # Health check endpoint
│   └── core/
│       ├── config.py          # Config (env, constants)
│       └── __init__.py
│── .env
│── requirements.txt / Pipfile
│── run.py                     # Entry point (uvicorn)

```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Pipenv
- Docker and Docker Compose (for PostgreSQL)

### 2. Clone and Setup

```bash
# Create project directory
mkdir library-api
cd library-api

# Create virtual environment and install dependencies
pipenv install

# Activate virtual environment
pipenv shell
```

### 3. Database Setup

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL and pgAdmin
docker-compose up -d

# Wait for containers to start, then check status
docker-compose ps
```

This will start:

- PostgreSQL on `localhost:5432`
- pgAdmin on `localhost:8080` (admin@admin.com / admin)

#### Option B: Local PostgreSQL Installation

1. Install PostgreSQL locally
2. Create a database named `library_db`
3. Update the `DATABASE_URL` in `.env` file

### 4. Environment Configuration

Create a `.env` file with your database configuration:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/library_db
```

### 5. Run the Application

```bash
# Start the FastAPI server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Users

| Method | Endpoint                 | Description                     |
| ------ | ------------------------ | ------------------------------- |
| POST   | `/users/`                | Create a new user               |
| GET    | `/users/`                | Get all users (with pagination) |
| GET    | `/users/{user_id}`       | Get user by ID with their books |
| PUT    | `/users/{user_id}`       | Update a user                   |
| DELETE | `/users/{user_id}`       | Delete a user                   |
| GET    | `/users/{user_id}/books` | Get all books owned by a user   |

### Books

| Method | Endpoint           | Description                     |
| ------ | ------------------ | ------------------------------- |
| POST   | `/books/`          | Create a new book               |
| GET    | `/books/`          | Get all books (with pagination) |
| GET    | `/books/{book_id}` | Get book by ID with owner info  |
| PUT    | `/books/{book_id}` | Update a book                   |
| DELETE | `/books/{book_id}` | Delete a book                   |
| GET    | `/books/search/`   | Search books by title or author |

### Health Check

| Method | Endpoint | Description           |
| ------ | -------- | --------------------- |
| GET    | `/`      | Health check endpoint |

## Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com"
  }'
```

### Create a Book

```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "A classic American novel",
    "owner_id": 1
  }'
```

### Search Books

```bash
# Search by title
curl "http://localhost:8000/books/search/?title=Gatsby"

# Search by author
curl "http://localhost:8000/books/search/?author=Fitzgerald"
```

### Get User with Books

```bash
curl "http://localhost:8000/users/1"
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest test_main.py -v

# Run with coverage
pytest test_main.py --cov=main

# Run specific test class
pytest test_main.py::TestUsers -v
```

## Development

### Code Formatting

```bash
# Format code with black
black main.py test_main.py

# Lint code with flake8
flake8 main.py test_main.py
```

### Database Management

#### Reset Database

```bash
# Stop containers
docker-compose down

# Remove volumes (this will delete all data)
docker-compose down -v

# Start fresh
docker-compose up -d
```

#### Access PostgreSQL

```bash
# Using psql
docker exec -it library_postgres psql -U postgres -d library_db

# Or use pgAdmin at http://localhost:8080
```

## Environment Variables

| Variable       | Description                  | Default                                                    |
| -------------- | ---------------------------- | ---------------------------------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/library_db` |

|
