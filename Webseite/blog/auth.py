
from flask import (
 Blueprint, flash, g, redirect, render_template, request, url_for,make_response
)
from db import User,Post, db
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
import os
from os.path import isfile, join
from flask_avatars import Identicon
from os import listdir
from flask import current_app,url_for,g





bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/login', methods=('GET', 'POST'))
def login():
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
            
            res = make_response(redirect(url_for("index")))
            res.set_cookie("user_id","None")
            res.set_cookie("user_id",str(user[0].id))
            return res

        flash(error)

    return render_template('auth/login.html')
@bp.route('/logout')
def logout():
    res = make_response(redirect(url_for("index")))
    res.set_cookie("user_id","None")
    return res


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"]))
            db.session.add(user)
            db.session.commit()
            user = db.session.execute(select(User).where(User.username==request.form["username"])).fetchone()
            res = make_response(redirect(url_for("index")))
            res.set_cookie("user_id",str(user[0].id))
            
        except :
            flash("Username already exists")
            return redirect(url_for("auth.register"))
        return res
        

    return render_template("auth/register.html")


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    db.session.query(Post).where(Post.author_id == id).update({Post.author_id:0})
    db.session.query(Post).where(Post.author_id == id).update({Post.author_id:0})
    db.session.query(User).where(User.id == id).delete()
    
    db.session.commit()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view 




@bp.route('/changelogin',methods=["GET", "POST"])
def changelogin():
    if not g.user:
        return redirect(url_for("auth.login"))
    error = None
    if request.method == 'POST':
        error = None
        oldpassworddb =  db.session.execute(select(User).where(User.id==g.user[0].id)).fetchone()

        OldPassword = request.form['oldpassword']
        Newpassword1 = request.form['password1']
        Newpassword2 = request.form['password2']
        if not Newpassword1 == Newpassword2:
            error = "newpassword not the same"
          
        elif not check_password_hash(oldpassworddb[0].password, OldPassword):
             error = 'Incorrect password.'    
        

        if error is None:
            db.session.query(User).where(User.id==g.user[0].id).update({User.password: generate_password_hash(Newpassword1)})
            db.session.commit()
            return redirect(url_for("index"))

    if error:
        flash(error)

    return render_template("auth/changelogin.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = request.cookies.get("user_id")   
    try:
        g.user = db.session.execute(select(User).where(int(user_id) == User.id)).fetchone()
    except:
        g.user = None
    generate_identicon()



""" 
    if user_id is 'None':
        g.user = None
    else:
        g.user = db.session.execute(select(User).where(int(user_id) == User.id)).fetchone() """
    

""" 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))"""
def generate_identicon():
    if g.user:
        if not os.path.isfile(current_app.config['AVATARS_SAVE_PATH'] + r"\\" + g.user[0].username +"_s.png"):
            avatar = Identicon()
            filenames = avatar.generate(text=g.user[0].username)
        PATH_CONST = current_app.config["AVATARS_SAVE_PATH"]
        myFiles = [f for f in listdir(PATH_CONST) if isfile(join(PATH_CONST, f))]
        for file in myFiles:
            if '_m' in file:
                os.remove(PATH_CONST+r"\\"+file)
            elif '_l' in file:
                os.remove(PATH_CONST+r"\\"+file)

#text('SELECT * FROM user WHERE username = ?;'),params={username}