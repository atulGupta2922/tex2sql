-- Create the user table
CREATE TABLE role (
    role_id INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL,
    policy TEXT NOT NULL
);