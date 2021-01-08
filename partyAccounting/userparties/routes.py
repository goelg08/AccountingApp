from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from partyAccounting import db
from partyAccounting.models import UserParty
from partyAccounting.userparties.forms import UserPartyForm

userparties = Blueprint('userparties', __name__)


@userparties.route("/userparty/new", methods=['GET', 'POST'])
@login_required
def new_userparty():
	form = UserPartyForm()
	if form.validate_on_submit():
		userparty = UserParty(partyname=form.partyname.data, partymob=form.partymob.data, partyaddress=form.partyaddress.data, partydesc=form.partydesc.data, creator=current_user)
		db.session.add(userparty)
		db.session.commit()
		flash('Your party has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_user_party.html', title='New Party',
                           form=form, legend='New Party')


@userparties.route("/userparty/<int:userparty_id>")
def userparty(userparty_id):
	userparty = UserParty.query.get_or_404(userparty_id)
	return render_template('userparty.html', title=userparty.partyname, userparty=userparty)


@userparties.route("/userparty/<int:userparty_id>/update", methods=['GET', 'POST'])
@login_required
def update_userparty(userparty_id):
	userparty = UserParty.query.get_or_404(userparty_id)
	if userparty.creator != current_user:
		abort(403)
	form = UserPartyForm()
	if form.validate_on_submit():
		userparty.partyname = form.partyname.data
		userparty.partymob = form.partymob.data
		userparty.partyaddress = form.partyaddress.data
		userparty.partydesc = form.partydesc.data
		db.session.commit()
		flash('Your party has been updated!', 'success')
		return redirect(url_for('userparties.userparty', userparty_id=userparty.id))
	elif request.method == 'GET':
		form.partyname.data = userparty.partyname
		form.partymob.data = userparty.partymob
		form.partyaddress.data = userparty.partyaddress
		form.partydesc.data = userparty.partydesc
	return render_template('create_user_party.html', title='Update Party',
                           form=form, legend='Update Party')


@userparties.route("/userparty/<int:userparty_id>/delete", methods=['POST'])
@login_required
def delete_userparty(userparty_id):
	userparty = UserParty.query.get_or_404(userparty_id)
	if userparty.creator != current_user:
		abort(403)
	db.session.delete(userparty)
	db.session.commit()
	flash('Your party has been deleted!', 'success')
	return redirect(url_for('main.home'))