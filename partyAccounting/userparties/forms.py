from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class UserPartyForm(FlaskForm):
	partyname = StringField('Party Name', validators=[DataRequired()])
	partymob = IntegerField('Party Mobile', validators=[DataRequired()])
	partyaddress = TextAreaField('Party Address', validators=[DataRequired()])
	partydesc = TextAreaField('Party Description', validators=[DataRequired()])
	submit = SubmitField('Add Party')