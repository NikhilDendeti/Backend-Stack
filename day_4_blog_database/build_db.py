import sqlite3
import os

DB_FILE = "blog.db"


def build():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE post_tags (
            post_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id)
        )
    """)

    users = [
        ("nikhil", "nikhil@example.com"),
        ("venu", "venu@example.com"),
        ("sravya", "sravya@example.com"),
        ("kiran", "kiran@example.com"),
    ]
    for user in users:
        cur.execute("INSERT INTO users (username, email) VALUES (?, ?)", user)

    posts = [
        (1, "Learning Python OOP", "Classes and objects are fun", "2026-01-05"),
        (1, "Exception Handling Tips", "try except else finally", "2026-01-10"),
        (2, "SQL Joins Explained", "Inner join vs left join", "2026-02-01"),
        (2, "Why Foreign Keys Matter", "Referential integrity basics", "2026-02-15"),
        (3, "Django Models 101", "Fields and migrations", "2026-03-01"),
        (4, "Getting Started With venv", "Isolating your project", "2026-03-20"),
    ]
    for post in posts:
        cur.execute(
            "INSERT INTO posts (user_id, title, body, created_at) VALUES (?, ?, ?, ?)",
            post,
        )

    comments = [
        (1, 2, "Nice explanation", "2026-01-06"),
        (1, 3, "This helped a lot", "2026-01-07"),
        (2, 4, "Finally is easy to forget", "2026-01-11"),
        (3, 1, "Left join clicked for me now", "2026-02-02"),
        (3, 4, "Great examples", "2026-02-03"),
        (5, 2, "Waiting for the ORM post", "2026-03-02"),
    ]
    for comment in comments:
        cur.execute(
            "INSERT INTO comments (post_id, user_id, body, created_at) VALUES (?, ?, ?, ?)",
            comment,
        )

    tags = ["python", "sql", "django", "beginner"]
    for tag in tags:
        cur.execute("INSERT INTO tags (name) VALUES (?)", (tag,))

    post_tags = [
        (1, 1), (1, 4),
        (2, 1), (2, 4),
        (3, 2),
        (4, 2),
        (5, 3),
        (6, 4),
    ]
    for post_tag in post_tags:
        cur.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", post_tag)

    conn.commit()
    conn.close()
    print("blog.db created with sample data")


if __name__ == "__main__":
    build()
