import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM images")
db.execute("DELETE FROM route_classes")
db.execute("DELETE FROM comments")
db.execute("DELETE FROM routes")
db.execute("DELETE FROM users")

USER_COUNT = 1000
ROUTE_COUNT = 10**5
COMMENT_COUNT = 10**6

classes = {}
for class_title, class_value in db.execute("SELECT title, value FROM classes"):
    if class_title not in classes:
        classes[class_title] = []
    classes[class_title].append(class_value)

for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, ROUTE_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    length_km = random.randint(1, 100)
    db.execute("""INSERT INTO routes (title, description, length_km, created_at, user_id)
                  VALUES (?, ?, ?, datetime('now', 'localtime'), ?)""",
               ["route" + str(i), "description" + str(i), length_km, user_id])
    for class_title, class_values in classes.items():
        db.execute("""INSERT INTO route_classes (route_id, title, value)
                      VALUES (?, ?, ?)""",
                   [i, class_title, random.choice(class_values)])

for i in range(1, COMMENT_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    route_id = random.randint(1, ROUTE_COUNT)
    rating = random.randint(1, 5)
    db.execute("""INSERT INTO comments (route_id, user_id, content, rating, created_at)
                  VALUES (?, ?, ?, ?, datetime('now', 'localtime'))""",
               [route_id, user_id, "comment" + str(i), rating])

db.commit()
db.close()
