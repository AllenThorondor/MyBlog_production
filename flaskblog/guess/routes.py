from flask import render_template, request, redirect, url_for, Blueprint
from flaskblog import db
from flaskblog.models import Friend
from flaskblog.guess.forms import GuessForm
import os
import secrets
from PIL import Image
from flask import url_for, current_app

guess = Blueprint('guess', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = form_picture.split('.')
    picture_fn = random_hex + str('.' + f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (600, 600)
    i = Image.open('/Users/liuqian/python/python3/Cloned-Repo/MyBlog_production/flaskblog/static/profile_pics/' + form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

@guess.route("/ask", methods=['GET', 'POST'])
def ask():
    form = GuessForm()
    if form.validate_on_submit():
        if form.validate_name(form.name):
            pass
        friend = Friend.query.filter_by(name=form.name.data).first()
        friend_name = friend.name
        # friend.picture = save_picture(friend.picture)
        # db.session.commit()

        return redirect(url_for('guess.who', name=friend_name))
    return render_template('ask.html', title='who are you', form=form)


@guess.route("/who/<string:name>", methods=['GET'])
def who(name):
    friend = Friend.query.filter_by(name=name).first()
    return render_template('who.html',friend=friend)
