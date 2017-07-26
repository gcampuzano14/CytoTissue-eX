# all the imports
from flask_wtf import Form
from wtforms import StringField, validators, SelectField, SelectMultipleField, FileField
from flask_wtf.file import  *
# from flaskext.uploads import UploadSet, TEXT


# txtfile = UploadSet("text", TEXT)
class FileInputForm(Form):
    # DATA
    openfile = FileField('Input txt file', validators=[FileAllowed(['txt'], 'Only text files are valid input!'), FileRequired()])


class InputForm(Form):
    # DATA SYNTH
    site_codes = [('',''), ('UM', 'UM Copath'), ('JHS', 'JHS Copath')]
    # DATA
    out_dir = StringField('Name of project', validators=[validators.DataRequired()])
    choice_site = SelectField(label='Site', choices=site_codes, validators=[validators.Length(min=1)])