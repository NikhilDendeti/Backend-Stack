SELECT posts.title, users.username
FROM posts
INNER JOIN users ON posts.user_id = users.id;

SELECT posts.title, users.username, COUNT(comments.id) AS comment_count
FROM posts
INNER JOIN users ON posts.user_id = users.id
LEFT JOIN comments ON comments.post_id = posts.id
GROUP BY posts.id
ORDER BY comment_count DESC;

SELECT posts.title, comments.body
FROM posts
LEFT JOIN comments ON comments.post_id = posts.id;

SELECT title
FROM posts
WHERE title LIKE '%SQL%';

SELECT username, email
FROM users
WHERE id IN (1, 3);

SELECT title, created_at
FROM posts
WHERE created_at BETWEEN '2026-02-01' AND '2026-03-01';

SELECT posts.title, COUNT(comments.id) AS comment_count
FROM posts
LEFT JOIN comments ON comments.post_id = posts.id
GROUP BY posts.id;

SELECT posts.title, COUNT(comments.id) AS comment_count
FROM posts
LEFT JOIN comments ON comments.post_id = posts.id
GROUP BY posts.id
HAVING comment_count > 1;

SELECT title, created_at
FROM posts
ORDER BY created_at DESC
LIMIT 3 OFFSET 1;

SELECT posts.title, tags.name
FROM posts
INNER JOIN post_tags ON post_tags.post_id = posts.id
INNER JOIN tags ON tags.id = post_tags.tag_id
WHERE tags.name = 'python';
