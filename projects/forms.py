from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, TextAreaField, FileField, SelectMultipleField, widgets, PasswordField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    activities = StringField('Activities', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    area = MultiCheckboxField('Area', validators=[DataRequired()],
                              choices=[('1', 'Project'), ('2', 'Bachelor'), ('3', 'Masters')])
    image = FileField('Project Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Only JPG and PNG images are allowed')
    ])
    tags = StringField('Tags', validators=[DataRequired(), Regexp(r'^[\w,:_\- ]*$',

                                                                  message="Allowed tag characters include letters spaces and , : _ -")])

class AuthRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address format'),
                                             Regexp(r'^.*@nbi\.ku\.dk$', message='Must be an @nbi.ku.dk email')])


class PasswordResetForm(AuthRequestForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8),
                                                     EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address format'),
                                             Regexp(r'^.*@nbi\.ku\.dk$', message='Must be an @nbi.ku.dk email')])
    password = PasswordField('Password', validators=[DataRequired()])
