import sqlite3

DB_FILE = "blog.db"

queries = [
    ("posts joined with author name",
     """SELECT posts.title, users.username
        FROM posts
        INNER JOIN users ON posts.user_id = users.id"""),

    ("posts + users + comments, comment count per post",
     """SELECT posts.title, users.username, COUNT(comments.id) AS comment_count
        FROM posts
        INNER JOIN users ON posts.user_id = users.id
        LEFT JOIN comments ON comments.post_id = posts.id
        GROUP BY posts.id
        ORDER BY comment_count DESC"""),

    ("posts left joined with comments, including posts with no comments",
     """SELECT posts.title, comments.body
        FROM posts
        LEFT JOIN comments ON comments.post_id = posts.id"""),

    ("titles containing the word SQL (LIKE)",
     """SELECT title
        FROM posts
        WHERE title LIKE '%SQL%'"""),

    ("users with id in (1, 3) (IN)",
     """SELECT username, email
        FROM users
        WHERE id IN (1, 3)"""),

    ("posts created between two dates (BETWEEN)",
     """SELECT title, created_at
        FROM posts
        WHERE created_at BETWEEN '2026-02-01' AND '2026-03-01'"""),

    ("comment count per post (GROUP BY)",
     """SELECT posts.title, COUNT(comments.id) AS comment_count
        FROM posts
        LEFT JOIN comments ON comments.post_id = posts.id
        GROUP BY posts.id"""),

    ("posts with more than 1 comment (HAVING)",
     """SELECT posts.title, COUNT(comments.id) AS comment_count
        FROM posts
        LEFT JOIN comments ON comments.post_id = posts.id
        GROUP BY posts.id
        HAVING comment_count > 1"""),

    ("newest posts, page 2 (ORDER BY + LIMIT/OFFSET)",
     """SELECT title, created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT 3 OFFSET 1"""),

    ("posts tagged 'python' (many-to-many join)",
     """SELECT posts.title, tags.name
        FROM posts
        INNER JOIN post_tags ON post_tags.post_id = posts.id
        INNER JOIN tags ON tags.id = post_tags.tag_id
        WHERE tags.name = 'python'"""),
]


def run():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    for label, sql in queries:
        print(f"\n{label}")
        cur.execute(sql)
        for row in cur.fetchall():
            print(row)

    conn.close()


if __name__ == "__main__":
    run()
