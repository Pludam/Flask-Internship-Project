from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from sqlalchemy import insert ,select, text
from db import db, User ,Post,Topic,Comments
import functools


bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = db.session.execute(select(Post,User).join(User,Post.author_id == User.id)).fetchall()
    topics = db.session.execute(select(Topic)).fetchall()
    
    return render_template('index.html', posts=posts, topics=topics)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    topics = db.session.execute(select(Topic)).fetchall()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        topic = request.form['topic']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            topicid = db.session.execute(select(Topic.topic_id).where(Topic.topic_name == topic)).fetchone()
            if not topicid:
                topicdb = Topic(topic_name = topic)
                db.session.add(topicdb)
            db.session.query(User).where(User.id == g.user[0].id).update({User.posts_created: User.posts_created + 1})
            db.session.execute(insert(Post).values(author_id = int(g.user[0].id),title=title,body=body,topic_id = topicid[0]))
            db.session.commit()
            postid = db.session.execute(select(Post.id).where(Post.title == title)).fetchone()
            return redirect(url_for('blog.post',post_id = postid[0]))

    return render_template('blog/create.html', topics = topics)


def get_post(id, check_author=True):
    post = db.session.execute(select(Post,User).join(User,Post.author_id == User.id).where(Post.id == id)).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post[0].author_id != g.user[0].id:
        abort(403)

    return post


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    
    db.session.query(Post).where(Post.id == id).delete()
    db.session.commit()

    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    topic = db.session.execute(select(Topic)).fetchall()
    if request.method == 'POST':
        title = request.form['title']
        topic = request.form['topic']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error) 
        else:
            topic_id =  db.session.execute(select(Topic.topic_id).where(Topic.topic_name == topic)).fetchone()
            db.session.query(Post).where(Post.id == id).update({Post.title: title,Post.body: body,Post.topic_id: topic_id[0]})
            db.session.query(User).where(User.id == g.user[0].id).update({User.posts_updated: User.posts_updated + 1})
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post,topics = topic)


@bp.route('/post/<int:post_id>', methods=["GET","POST"])
def post(post_id):
    post = db.session.execute(select(Post).join(User,Post.author_id == User.id).where(Post.id == post_id)).fetchone()
    post = get_post(post_id ,check_author=False)
    comments = db.session.execute(text("SELECT com.*, usr.* FROM comments com JOIN user usr ON com.user_id == usr.id WHERE com.post_id = :post_id"),{"post_id": post_id}).fetchall() 
    if request.method == 'POST':
        commentbody = request.form["commentbody"]
        db.session.execute(insert(Comments).values(user_id = g.user[0].id,comment_body = commentbody, post_id = post_id))
        db.session.commit()
        comments = db.session.execute(text("SELECT com.*, usr.* FROM comments com JOIN user usr ON com.user_id == usr.id WHERE com.post_id = :post_id"),{"post_id": post_id}).fetchall()
    return render_template("blog/post.html",post = post ,comments = comments)


@bp.route("/deletecomment/<int:comment_id>")
def deletecomment(comment_id):
    db.session.query(Comments).where(Comments.comment_id == comment_id).delete()
    db.session.commit()
    return redirect(request.referrer)


@bp.route("/newtopic",methods=["GET","POST"])
@login_required
def newtopic():
    if request.method == 'POST':
        topicname = request.form["topicname"]
        db.session.execute(insert(Topic).values(topic_name = topicname))
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("blog/newtopic.html")
