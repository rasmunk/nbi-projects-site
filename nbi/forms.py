from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Regexp
from projects.forms import MultiCheckboxField
from nbi.conf import config


class NBIProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    activities = StringField('Activities', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    area = MultiCheckboxField('Area', validators=[DataRequired()],
                              choices=[('1', 'Project'),
                                       ('2', 'Bachelor'),
                                       ('3', 'Masters')])
    image = FileField('Project Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Only JPG and PNG images are allowed')])
    tags = StringField('Tags', validators=[
        DataRequired(),
        Regexp(r'' + config.get('NBI', 'tags_regex'),
               message=config.get('NBI', 'tags_regex_msg'))])

