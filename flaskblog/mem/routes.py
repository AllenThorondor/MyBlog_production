from flask import render_template, request, Blueprint
from flaskblog.models import Post

mem = Blueprint('mem', __name__)

@mem.route("/colt_steele")
def colt_steele():
    return render_template('colt_steele.html', title='colt_steele')
