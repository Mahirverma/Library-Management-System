
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional
from wtforms import ValidationError
from my_project.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[EqualTo(
        'pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password')
    submit = SubmitField('Register!')

    def __init__(self, is_update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if is_update:  # For profile updates, make password optional
            self.password.validators = [Optional(), Length(min=8, max=80)]
        else:  # For registration, password is required
            self.password.validators = [InputRequired(), Length(min=8, max=80)]

    def validate_email(self,email, is_update=False):
        if is_update:
            if User.query.filter_by(email=self.email.data).first():
                raise ValidationError('Email has been registered')

    def validate_username(self,username, is_update=False):
        if is_update:
            if User.query.filter_by(username=self.username.data).first():
                raise ValidationError('Username has been registered')


class AddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    # dob=StringField('D.O.B',validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    Class = SelectField('Class', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    student_id = StringField("Student Id", validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_student(self, student_id):
        if User.query.filter_by(student_id=self.id.data).first():
            raise ValidationError('NO Student with this Id!')
