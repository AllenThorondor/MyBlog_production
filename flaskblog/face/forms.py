from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError
from flaskblog.models import Friend



class FaceForm(FlaskForm):
    picture1 = FileField("提交目标图像", validators=[FileAllowed(['jpg', 'png'])])
    picture2 = FileField("提交测试图像", validators=[FileAllowed(['jpg', 'png'])])
    path = ""
    submit = SubmitField("提交")
