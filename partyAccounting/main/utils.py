import os
import secrets
from PIL import Image
from flask import url_for, current_app
from partyAccounting.models import UserPartyTransaction
from partyAccounting import db

def calculate_debt_cred_bal(userparty_for_txn):
	all_cred_debt_dic = {}
	if len(userparty_for_txn) > 0:
		for i in range(len(userparty_for_txn)):
			party_credit = 0
			party_debit = 0
			party_balance = 0
			cred_debt_dic = {}

			userpartytxn_credit = UserPartyTransaction.query.filter_by(user_id=userparty_for_txn[i].user_id, userparty_id=userparty_for_txn[i].id).all()
			if len(userpartytxn_credit) > 0:
				for j in range(len(userpartytxn_credit)):

					party_credit = party_credit + userpartytxn_credit[j].credit
					party_debit = party_debit + userpartytxn_credit[j].debit
					party_balance = party_balance + userpartytxn_credit[j].balance

					cred_debt_dic["tcredit"] = party_credit
					cred_debt_dic["tdebit"] = party_debit
					cred_debt_dic["tbalance"] = party_balance

				all_cred_debt_dic[userparty_for_txn[i].id] = cred_debt_dic
			else:
				cred_debt_dic["tcredit"] = 0
				cred_debt_dic["tdebit"] = 0
				cred_debt_dic["tbalance"] = 0
				all_cred_debt_dic[userparty_for_txn[i].id] = cred_debt_dic
	else:
		cred_debt_dic = {}

		cred_debt_dic["tcredit"] = 0
		cred_debt_dic["tdebit"] = 0
		cred_debt_dic["tbalance"] = 0
		all_cred_debt_dic[0] = cred_debt_dic


	return all_cred_debt_dic


def calculate_debt_cred_bal_report(userparty_for_txn, dt_to_fmt, dt_from_fmt):
	all_cred_debt_dic = {}
	if len(userparty_for_txn) > 0:
		for i in range(len(userparty_for_txn)):
			party_credit = 0
			party_debit = 0
			party_balance = 0
			cred_debt_dic = {}

			userpartytxn_credit = UserPartyTransaction.query.filter(UserPartyTransaction.user_id==userparty_for_txn[i].user_id, UserPartyTransaction.userparty_id==userparty_for_txn[i].id, db.between(UserPartyTransaction.transactiondte, dt_from_fmt, dt_to_fmt)).all()
			if len(userpartytxn_credit) > 0:
				for j in range(len(userpartytxn_credit)):

					party_credit = party_credit + userpartytxn_credit[j].credit
					party_debit = party_debit + userpartytxn_credit[j].debit
					party_balance = party_balance + userpartytxn_credit[j].balance

					cred_debt_dic["tcredit"] = party_credit
					cred_debt_dic["tdebit"] = party_debit
					cred_debt_dic["tbalance"] = party_balance

				all_cred_debt_dic[userparty_for_txn[i].id] = cred_debt_dic
			else:
				cred_debt_dic["tcredit"] = 0
				cred_debt_dic["tdebit"] = 0
				cred_debt_dic["tbalance"] = 0
				all_cred_debt_dic[userparty_for_txn[i].id] = cred_debt_dic
	else:
		cred_debt_dic = {}

		cred_debt_dic["tcredit"] = 0
		cred_debt_dic["tdebit"] = 0
		cred_debt_dic["tbalance"] = 0
		all_cred_debt_dic[0] = cred_debt_dic


	return all_cred_debt_dic


def calculate_debt_cred_bal_all(userparty_for_txn, user):
	all_cred_debt_dic_all = {}
	if len(userparty_for_txn) > 0:
		for i in range(len(userparty_for_txn)):
			party_credit = 0
			party_debit = 0
			party_balance = 0
			cred_debt_dic = {}

			userpartytxn_credit = UserPartyTransaction.query.filter_by(user_id=userparty_for_txn[i].user_id).all()
			if len(userpartytxn_credit) > 0:
				for j in range(len(userpartytxn_credit)):

					party_credit = party_credit + userpartytxn_credit[j].credit
					party_debit = party_debit + userpartytxn_credit[j].debit
					party_balance = party_balance + userpartytxn_credit[j].balance

					cred_debt_dic["tcredit"] = party_credit
					cred_debt_dic["tdebit"] = party_debit
					cred_debt_dic["tbalance"] = party_balance

				all_cred_debt_dic_all[userparty_for_txn[i].user_id] = cred_debt_dic
			else:
				cred_debt_dic["tcredit"] = 0
				cred_debt_dic["tdebit"] = 0
				cred_debt_dic["tbalance"] = 0
				all_cred_debt_dic_all[userparty_for_txn[i].user_id] = cred_debt_dic

	else:
		cred_debt_dic = {}

		cred_debt_dic["tcredit"] = 0
		cred_debt_dic["tdebit"] = 0
		cred_debt_dic["tbalance"] = 0
		all_cred_debt_dic_all[user.id] = cred_debt_dic

	return all_cred_debt_dic_all

