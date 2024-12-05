-- Create the user table
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    registration_date DATE NOT NULL,
    user_id TEXT NOT NULL,
    password TEXT NOT NULL,
    org_id INTEGER NOT NULL,
    user_type TEXT NOT NULL,
    role_id TEXT,
    FOREIGN KEY (org_id) REFERENCES org(org_id)
    FOREIGN KEY (role_id) REFERENCES org(role_id)
);