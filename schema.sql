CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE routes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    length_km INTEGER,
    created_at TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    route_id INTEGER REFERENCES routes,
    user_id INTEGER REFERENCES users,
    content TEXT,
    rating INTEGER,
    created_at TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE route_classes (
    id INTEGER PRIMARY KEY,
    route_id INTEGER REFERENCES routes,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    route_id INTEGER REFERENCES routes,
    image BLOB
);

CREATE INDEX idx_user_routes ON routes (user_id);
CREATE INDEX idx_route_comments ON comments (route_id);
CREATE INDEX idx_user_comments ON comments (user_id);
CREATE INDEX idx_route_classes ON route_classes (route_id);
CREATE INDEX idx_route_images ON images (route_id);
