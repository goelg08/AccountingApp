from datetime import datetime
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, make_response)
import pdfkit
from flask_login import current_user, login_required
from partyAccounting import db
from partyAccounting.models import User, UserParty, UserPartyTransaction
from partyAccounting.transactionreports.forms import UserPartyTransactionReportForm
from partyAccounting.main.utils import calculate_debt_cred_bal, calculate_debt_cred_bal_report

transactionreports = Blueprint('transactionreports', __name__)


@transactionreports.route("/userpartytransactionreport/<int:userparty_id>/report", methods=['GET', 'POST'])
@login_required
def report_userpartytransactionreport(userparty_id):
	form = UserPartyTransactionReportForm()
	userparty = UserParty.query.get(userparty_id)
	all_cred_debt_dic = {}
	if form.validate_on_submit():

		dt_to = form.dateTo.data
		dt_from = form.dateFrom.data

		dt_to_fmt = datetime(year=dt_to.year, month=dt_to.month, day=dt_to.day)
		dt_from_fmt = datetime(year=dt_from.year, month=dt_from.month, day=dt_from.day)

		userpartyreport = UserPartyTransaction.query.filter(UserPartyTransaction.user_id==userparty.user_id, UserPartyTransaction.userparty_id==userparty.id, db.between(UserPartyTransaction.transactiondte, dt_from_fmt, dt_to_fmt))
		user = User.query.filter_by(username=current_user.username).first_or_404()
		userparty_for_txn = UserParty.query.filter_by(user_id=user.id, id=userparty_id).all()
		all_cred_debt_dic = calculate_debt_cred_bal_report(userparty_for_txn, dt_to_fmt, dt_from_fmt)
		
		dt_to = form.dateTo.data
		dt_from = form.dateFrom.data

		print(userpartyreport)
		print(userparty_for_txn)
		print(all_cred_debt_dic)
		print(datetime(year=dt_to.year, month=dt_to.month, day=dt_to.day))
		print(datetime(year=dt_from.year, month=dt_from.month, day=dt_from.day))

		rendered = render_template('pdf_template.html', userpartyreport=userpartyreport, all_cred_debt_dic=all_cred_debt_dic, userparty=userparty, form=form )
		config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
		
		pdf = pdfkit.from_string(rendered, False, configuration=config)

		response = make_response(pdf)
		response.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

		return response
	return render_template('create_user_party_txn_report.html', title='Generate Reports',
                           form=form, legend='Generate Reports')


