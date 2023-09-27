
from sqlalchemy import Integer, String, TIMESTAMP,TEXT
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True,)
    author_id: Mapped[str] = mapped_column(Integer,primary_key=True)
    created: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    title: Mapped[str] = mapped_column(TEXT,nullable=False)
    body: Mapped[str] = mapped_column(TEXT,nullable=False)
    topic_id: Mapped[str] = mapped_column(ForeignKey("Topic.topicid"))


class Topic(db.Model):
    topic_id: Mapped[int] = mapped_column(Integer,primary_key= True)
    topic_name: Mapped[str] = mapped_column(String)

class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    post_id: Mapped[int] = mapped_column(Integer,ForeignKey(Post.id))
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey(User.id))
    created: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    comment_body: Mapped[str] = mapped_column(TEXT,nullable=False) 





'''
import sqlite3
import click
from flask import current_app, g

def init_app(app):
    
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql','r') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

  '''