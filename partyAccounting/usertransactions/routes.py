from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from partyAccounting import db
from partyAccounting.models import UserParty, UserPartyTransaction
from partyAccounting.usertransactions.forms import UserPartyTransactionForm

usertransactions = Blueprint('usertransactions', __name__)


@usertransactions.route("/userpartytransaction/<int:userparty_id>/new", methods=['GET', 'POST'])
@login_required
def new_userpartytransaction(userparty_id):
	form = UserPartyTransactionForm()
	userparty = UserParty.query.get(userparty_id)
	if form.validate_on_submit():
		userpartytransaction = UserPartyTransaction(user_id=userparty.user_id,userparty_id=userparty_id,debit=form.debit.data,credit=form.credit.data,balance=form.credit.data-form.debit.data,transactiondesc=form.transactiondesc.data)
		db.session.add(userpartytransaction)
		db.session.commit()
		flash('Transaction has been added!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_user_party_transaction.html', title='New Transaction',
                           form=form, legend='New Transaction')


