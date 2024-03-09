from flask import Blueprint,render_template
from db import db, Post ,User
from sqlalchemy import select 

from flask import (
 Blueprint,redirect, render_template, url_for
)
from db import User,Post, db
from sqlalchemy import select 


bp = Blueprint('user', __name__)

@bp.route('/<int:usr_id>/profile')
def profile(usr_id):
    user = db.session.execute(select(User).where(User.id == usr_id)).fetchone()
    
    user[0].posted_posts = db.session.query(Post).where(Post.author_id==usr_id).count()
    posts = db.session.execute(select(Post,User).where(Post.author_id == usr_id).join(User,Post.author_id == User.id).order_by(Post.created)).fetchall()
    return render_template("user/profile.html", user=user,post=posts)
