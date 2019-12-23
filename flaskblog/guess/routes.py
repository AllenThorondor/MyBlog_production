from flask import render_template, request, redirect, url_for, Blueprint
from flaskblog.models import Friend
from flaskblog.guess.forms import GuessForm

guess = Blueprint('guess', __name__)

@guess.route("/ask", methods=['GET', 'POST'])
def ask():
    form = GuessForm()
    if form.validate_on_submit():
        if form.validate_name(form.name):
            pass
        name = form.name.data
        return redirect(url_for('guess.who', name=name))
    return render_template('ask.html', title='who are you', form=form)


@guess.route("/who/<string:name>", methods=['GET'])
def who(name):
    friend = Friend.query.filter_by(name=name).first()
    return render_template('who.html',friend=friend)
