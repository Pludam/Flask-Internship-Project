from flask import Flask,make_response,redirect,request, send_file
import auth
import blog
from db import db
from time import *
from datetime import *
import user
from flask_avatars import Avatars


def create_app(test_config=None):
    
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    avatars = Avatars(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///C:\\Users\\Damian.Plura\\Desktop\\Webseite\\blog\\instance\\blog.sqlite",
        APPNAME="Blog",
        AVATARS_SAVE_PATH = "C:\\Users\\Damian.Plura\\Desktop\\Webseite\\blog\\avatars")
    db.init_app(app)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    #register the blog blueprint
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    #setting the app secret key and registering the user and authentication blueprint
    app.secret_key = b'@Rm`#*}FU9Wf2J;A#He"]}O(c^#gc'
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)

    #setting up the color scheme route 
    @app.route("/set/<theme>")
    def set(theme):
        res = make_response(redirect(request.referrer))
        res.set_cookie("theme", theme)
        return res

    
    @app.template_filter()
    def zeitformat(value):
        try:
            value2 = value.timetuple()
        except:
            value2 = strptime(value, "%Y-%m-%d %H:%M:%S")
        value3 = strftime('%d.%m.%Y at %H:%M UTC', value2)
        return value3
    
    #avatar icon endpoint
    @app.route('/avatar/<string:usrnme>')
    def avatar(usrnme):
        filename = r'\\' + usrnme +"_s.png"
        filename2 = app.config['AVATARS_SAVE_PATH'] + filename
        print(filename2)
        return send_file(filename2)
    return app
