from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError
from flaskblog.models import Friend


class GuessForm(FlaskForm):
    name =StringField('你的名字')
    submit = SubmitField('提交')

    def validate_name(self, name):
        friend_name = Friend.query.filter_by(name=name.data).first()
        if not friend_name:
            raise ValidationError('你的名字还没有被加入哦！')
