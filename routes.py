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

def get_classes(route_id):
    sql = "SELECT title, value FROM route_classes WHERE route_id = ? ORDER BY id"
    return db.query(sql, [route_id])
