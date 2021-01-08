from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class UserPartyTransactionForm(FlaskForm):
	debit = IntegerField('DEBIT')
	credit = IntegerField('CREDIT')
	transactiondesc = TextAreaField('Comment')
	submit = SubmitField('Add Transaction')