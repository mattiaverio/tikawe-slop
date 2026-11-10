import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes

def add_route(title, description, length_km, user_id, classes):
    sql = """INSERT INTO routes (title, description, length_km, created_at, user_id)
             VALUES (?, ?, ?, datetime('now', 'localtime'), ?)"""
    db.execute(sql, [title, description, length_km, user_id])

    route_id = db.last_insert_id()

    sql = "INSERT INTO route_classes (route_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [route_id, class_title, class_value])

    return route_id

def get_route_count():
    sql = "SELECT COUNT(id) FROM routes"
    return db.query(sql)[0][0]

def get_routes(page, page_size):
    sql = """SELECT routes.id,
                    routes.title,
                    routes.length_km,
                    users.id user_id,
                    users.username,
                    COUNT(comments.id) comment_count,
                    ROUND(AVG(comments.rating), 1) average_rating
             FROM (SELECT id, title, length_km, user_id
                   FROM routes
                   ORDER BY id DESC
                   LIMIT ? OFFSET ?) routes
                  JOIN users ON routes.user_id = users.id
                  LEFT JOIN comments ON routes.id = comments.route_id
             GROUP BY routes.id
             ORDER BY routes.id DESC"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_route(route_id):
    sql = """SELECT routes.id,
                    routes.title,
                    routes.description,
                    routes.length_km,
                    routes.created_at,
                    users.id user_id,
                    users.username
             FROM routes JOIN users ON routes.user_id = users.id
             WHERE routes.id = ?"""
    result = db.query(sql, [route_id])
    return result[0] if result else None

def update_route(route_id, title, description, length_km, classes):
    sql = """UPDATE routes SET title = ?,
                               description = ?,
                               length_km = ?
                           WHERE id = ?"""
    db.execute(sql, [title, description, length_km, route_id])

    sql = "DELETE FROM route_classes WHERE route_id = ?"
    db.execute(sql, [route_id])

    sql = "INSERT INTO route_classes (route_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [route_id, class_title, class_value])

def remove_route(route_id):
    sql = "DELETE FROM comments WHERE route_id = ?"
    db.execute(sql, [route_id])
    sql = "DELETE FROM images WHERE route_id = ?"
    db.execute(sql, [route_id])
    sql = "DELETE FROM route_classes WHERE route_id = ?"
    db.execute(sql, [route_id])
    sql = "DELETE FROM routes WHERE id = ?"
    db.execute(sql, [route_id])

def get_classes(route_id):
    sql = "SELECT title, value FROM route_classes WHERE route_id = ? ORDER BY id"
    return db.query(sql, [route_id])

def get_search_condition(query, classes):
    like = "%" + query + "%"
    condition = "(routes.title LIKE ? OR routes.description LIKE ?)"
    params = [like, like]

    for class_title, class_value in classes:
        condition += """ AND routes.id IN (SELECT route_id
                                           FROM route_classes
                                           WHERE title = ? AND value = ?)"""
        params += [class_title, class_value]

    return condition, params

def get_result_count(query, classes):
    condition, params = get_search_condition(query, classes)
    sql = "SELECT COUNT(routes.id) FROM routes WHERE " + condition
    return db.query(sql, params)[0][0]

def find_routes(query, classes, page, page_size):
    condition, params = get_search_condition(query, classes)
    sql = """SELECT routes.id,
                    routes.title,
                    routes.length_km,
                    users.id user_id,
                    users.username
             FROM routes JOIN users ON routes.user_id = users.id
             WHERE """ + condition + """
             ORDER BY routes.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, params + [limit, offset])
