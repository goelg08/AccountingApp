from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class UserPartyTransactionReportForm(FlaskForm):
	dateTo = DateField('dateTo', format='%Y-%m-%d')
	dateFrom = DateField('dateFrom', format='%Y-%m-%d')
	submit = SubmitField('Generate Report')