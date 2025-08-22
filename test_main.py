import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the parent directory to the path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db, Base

# Test database setup
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/library_test_db"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test data
test_user_data = {"name": "Test User", "email": "test@example.com"}

test_book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "description": "A test book description",
    "owner_id": 1,
}


class TestUsers:
    """Test cases for User CRUD operations"""

    def test_create_user(self):
        """Test creating a new user"""
        response = client.post("/users/", json=test_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_create_duplicate_user(self):
        """Test creating a user with duplicate email"""
        # First user should succeed
        client.post("/users/", json=test_user_data)

        # Second user with same email should fail
        response = client.post("/users/", json=test_user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_get_users(self):
        """Test getting all users"""
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_user_by_id(self):
        """Test getting a specific user"""
        # Create a user first
        create_response = client.post(
            "/users/", json={"name": "Specific User", "email": "specific@example.com"}
        )
        user_id = create_response.json()["id"]

        # Get the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Specific User"
        assert "books" in data

    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist"""
        response = client.get("/users/99999")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_update_user(self):
        """Test updating a user"""
        # Create a user first
        create_response = client.post(
            "/users/", json={"name": "Update User", "email": "update@example.com"}
        )
        user_id = create_response.json()["id"]

        # Update the user
        update_data = {"name": "Updated Name"}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "update@example.com"  # Email unchanged

    def test_delete_user(self):
        """Test deleting a user"""
        # Create a user first
        create_response = client.post(
            "/users/", json={"name": "Delete User", "email": "delete@example.com"}
        )
        user_id = create_response.json()["id"]

        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404


class TestBooks:
    """Test cases for Book CRUD operations"""

    def test_create_book(self):
        """Test creating a new book"""
        # Create a user first
        user_response = client.post(
            "/users/", json={"name": "Book Owner", "email": "bookowner@example.com"}
        )
        user_id = user_response.json()["id"]

        # Create a book
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "A test book",
            "owner_id": user_id,
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert data["owner_id"] == user_id

    def test_create_book_nonexistent_owner(self):
        """Test creating a book with non-existent owner"""
        book_data = {"title": "Orphan Book", "author": "No Author", "owner_id": 99999}
        response = client.post("/books/", json=book_data)
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_get_books(self):
        """Test getting all books"""
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_search_books(self):
        """Test searching books by title and author"""
        # Create a user and book first
        user_response = client.post(
            "/users/", json={"name": "Search Owner", "email": "searchowner@example.com"}
        )
        user_id = user_response.json()["id"]

        book_data = {
            "title": "Searchable Book",
            "author": "Searchable Author",
            "owner_id": user_id,
        }
        client.post("/books/", json=book_data)

        # Search by title
        response = client.get("/books/search/?title=Searchable")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "Searchable" in data[0]["title"]

        # Search by author
        response = client.get("/books/search/?author=Searchable")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "Searchable" in data[0]["author"]


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Library Management API is running" in response.json()["message"]


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
