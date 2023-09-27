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
    #user[0].posts_created = db.session.execute(select(User.posts_created).where(User.id == usr_id))
    #user[0].posts_updated = db.session.execute(select(User.posts_created).where(User.id == usr_id))
    posts = db.session.execute(select(Post,User).where(Post.author_id == usr_id).join(User,Post.author_id == User.id).order_by(Post.created)).fetchall()
    return render_template("user/profile.html", user=user,post=posts)


#db.session.query(Post).where(usr_id == Post.author_id).count()
#db.session.query(User.posts_created).where(User.id== usr_id)





        















    """ def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()
        user = db.session.execute(select(User).where(User.username==request.form["username"])).fetchone()
        session['user_id'] = user[0].id

        return redirect(url_for("index")) """
    


    """ def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        user = db.session.execute(select(User).where(User.username==username)).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[0].password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0].id
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html') """
    return redirect(url_for("index"))