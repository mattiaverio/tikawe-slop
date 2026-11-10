from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_statistics(user_id):
    sql = """SELECT COUNT(routes.id) route_count,
                    IFNULL(SUM(routes.length_km), 0) total_km,
                    (SELECT COUNT(comments.id)
                     FROM comments
                     WHERE comments.user_id = ?) comment_count,
                    (SELECT ROUND(AVG(comments.rating), 1)
                     FROM comments JOIN routes ON comments.route_id = routes.id
                     WHERE routes.user_id = ?) average_rating
             FROM routes
             WHERE routes.user_id = ?"""
    return db.query(sql, [user_id, user_id, user_id])[0]

def get_routes(user_id, page, page_size):
    sql = """SELECT id, title, length_km, created_at
             FROM routes
             WHERE user_id = ?
             ORDER BY id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if password_hash and check_password_hash(password_hash, password):
        return user_id
    return None
