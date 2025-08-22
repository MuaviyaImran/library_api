-- Initialize the database with some sample data
-- This file is executed when the PostgreSQL container starts for the first time
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    author TEXT,
    owner_id INT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_name ON users(name);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);
CREATE INDEX IF NOT EXISTS idx_books_owner_id ON books(owner_id);

-- Insert sample users
INSERT INTO users (name, email, created_at) VALUES
('John Doe', 'john.doe@example.com', NOW()),
('Jane Smith', 'jane.smith@example.com', NOW()),
('Bob Johnson', 'bob.johnson@example.com', NOW())
ON CONFLICT (email) DO NOTHING;

-- Insert sample books (this will run after the tables are created by SQLAlchemy)
-- Note: The actual insertion of books should be done after users table is populated
-- This is handled by the application's startup