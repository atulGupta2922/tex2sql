-- Create the user table
CREATE TABLE user_db (
    user_db_id INTEGER PRIMARY KEY,
    connection TEXT NOT NULL,
    db_schema TEXT NOT NULL,
    org_id INTEGER NOT NULL,
    FOREIGN KEY (org_id) REFERENCES org(org_id)
);