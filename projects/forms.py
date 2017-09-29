from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Regexp


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    activities = StringField('Activities', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    image = FileField('Project Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Only JPG and PNG images are allowed')
    ])
    tags = StringField('Tags', validators=[DataRequired(), Regexp(r'^[\w,:_\- ]*$',
                                                                      message="Allowed tag characters include letters spaces and , : _ -")])