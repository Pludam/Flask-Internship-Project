-- database: blog/instance/blog.sqlite

CREATE TABLE "comments"(
comment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
post_id INTEGER NOT NULL REFERENCES "post"("id"),
user_id INTEGER NOT NULL REFERENCES "user"("id"),
created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
comment_body TEXT NOT NULL
);

CREATE TABLE "post" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL, topic_id INTENGER,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE topic (
  topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_name TEXT NOT NULL
);
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  posts_created INTEGER, posts_updated INTENGER
);