from flask import render_template, request, Blueprint
from partyAccounting.models import User, UserParty, UserPartyTransaction
from flask_login import current_user
from partyAccounting.main.utils import calculate_debt_cred_bal, calculate_debt_cred_bal_all

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	all_cred_debt_dic = {}
	all_cred_debt_dic_all = {}
	query = request.args.get('query')
	page = request.args.get('page', 1, type=int)
	if current_user.is_authenticated:
		user = User.query.filter_by(username=current_user.username).first_or_404()
		if query:
			userparty = UserParty.query.filter(UserParty.creator==user, UserParty.partyname.contains(query))\
			.order_by(UserParty.partyadddate.desc())\
			.paginate(page=page, per_page=5)
		else:
			userparty = UserParty.query.filter_by(creator=user)\
			.order_by(UserParty.partyadddate.desc())\
			.paginate(page=page, per_page=5)
		userparty_for_txn = UserParty.query.filter_by(user_id=user.id).all()
		all_cred_debt_dic = calculate_debt_cred_bal(userparty_for_txn)
		all_cred_debt_dic_all = calculate_debt_cred_bal_all(userparty_for_txn, user)
		no_of_party = len(userparty_for_txn)
		userflag = 1
	else:
		user = User.query.first_or_404()
		if query:
			userparty = UserParty.query.order_by(UserParty.partyadddate.desc()).paginate(page=page, per_page=5)
		else:
			userparty = UserParty.query.order_by(UserParty.partyadddate.desc()).paginate(page=page, per_page=5)
		userparty_for_txn = UserParty.query.all()
		all_cred_debt_dic = calculate_debt_cred_bal(userparty_for_txn)
		all_cred_debt_dic_all = calculate_debt_cred_bal_all(userparty_for_txn, user)
		no_of_party = len(userparty_for_txn)
		userflag = 0
	return render_template('home.html', userparty=userparty, all_cred_debt_dic=all_cred_debt_dic, all_cred_debt_dic_all=all_cred_debt_dic_all, user=user, no_of_party=no_of_party, userflag=userflag)


@main.route("/about")
def about():
	return render_template('about.html', title='About')