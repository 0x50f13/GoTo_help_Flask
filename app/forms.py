from wtforms import StringField, Form
from wtforms.validators import Required,Length

class LoginForm(Form):
    username =StringField('username',validators=[Length(min=4,max=25)])
    password =StringField('password',validators=[Length(min=4,max=64)])