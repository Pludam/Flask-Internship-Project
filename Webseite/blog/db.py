from sqlalchemy import Integer, String, TIMESTAMP, TEXT
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    posts_created: Mapped[int] = mapped_column(Integer)
    posts_updated: Mapped[int] = mapped_column(Integer)


class Post(db.Model):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    author_id: Mapped[str] = mapped_column(Integer, primary_key=True)
    created: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    title: Mapped[str] = mapped_column(TEXT, nullable=False)
    body: Mapped[str] = mapped_column(TEXT, nullable=False)
    topic_id: Mapped[str] = mapped_column(ForeignKey("Topic.topicid"))


class Topic(db.Model):
    topic_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_name: Mapped[str] = mapped_column(String)


class Comments(db.Model):
    __tablename__ = "comments"
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey(Post.id))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    created: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    comment_body: Mapped[str] = mapped_column(TEXT, nullable=False)
