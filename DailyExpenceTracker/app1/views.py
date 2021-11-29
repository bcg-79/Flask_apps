from flask import (Blueprint, render_template, flash, redirect, url_for, request)
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import User, ExpenceAccount, Expence
from .forms import NewAccountForm, DefaultAcc, AddSpend
from . import db

views_bp = Blueprint('views_bp', __name__)

@views_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = AddSpend()
	user = User.query.filter_by(id=current_user.id).first()
	account = ExpenceAccount.query.filter_by(user_id=current_user.id).all()
	no_of_acc = len(account)

	active_acc = None	
	if account:
		for acc in account:
			if acc.current == 1:
				active_acc = acc

	if active_acc is not None:
		# last_5_exp = Expence.query.filter_by(exp_acc_id=active_acc.id).order_by(desc(active_acc.id)).limit(5).all()
		last_5_exp = Expence.query.filter_by(exp_acc_id=active_acc.id).order_by(desc(Expence.id)).limit(10).all()
	else:
		last_5_exp = None

	if form.validate_on_submit():
		add_spend = form.add_spend.data
		amount = form.amount.data
		payee = form.payee.data
		cat = form.category.data
		notes = form.notes.data
		exp_acc_id = form.exp_acc_id.data

		new_exp = Expence(amount=amount, payee=payee, category=cat, notes=notes, add_spend=add_spend, exp_acc_id=exp_acc_id)
		db.session.add(new_exp)

		if int(add_spend) == 0:
			if (active_acc.remaining_amount == 0.0) or (amount > active_acc.remaining_amount):
				flash(f"Not Enough amount to Spend", category='add_spend')
				return redirect(url_for('views_bp.dashboard'))
			else:
				active_acc.remaining_amount = active_acc.remaining_amount - amount
				db.session.commit()
				flash(f"{amount} Spend from current Account", category='add_spend')
				return redirect(url_for('views_bp.dashboard'))
		elif int(add_spend) == 1:
			active_acc.remaining_amount = active_acc.remaining_amount + amount
			db.session.commit()
			flash(f"{amount} Added to current Account", category='add_spend')
			return redirect(url_for('views_bp.dashboard'))

	return render_template('home_pages/dashboard.html', user=user, form=form, no_of_acc=no_of_acc, active_acc=active_acc, last_5_exp=last_5_exp)

@views_bp.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
	form1 = NewAccountForm()
	form2 = DefaultAcc()

	page = request.args.get('page', 1, type=int)

	acc_data = ExpenceAccount.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
	default_acc = ExpenceAccount.query.filter_by(user_id=current_user.id, current=1).first()

	if form1.submit1.data and form1.validate():
		acc_name = form1.acc_name.data
		cat = form1.category.data
		initial_amt = form1.initial_amt.data
		user_id = current_user.id

		account = ExpenceAccount(account_name=acc_name, category=cat, initial_amount=initial_amt, remaining_amount=initial_amt, user_id=user_id)
		db.session.add(account)
		db.session.commit()

		flash(f"{acc_name} Successfully added.", category='success')

		return redirect(url_for('views_bp.accounts'))

	if form2.submit2.data and form2.validate():
		acc_id = form2.acc_id.data

		old_acc = ExpenceAccount.query.filter_by(current=1).first()

		active_acc = ExpenceAccount.query.get(acc_id)
		active_acc.current = 1
		if old_acc:
			old_acc.current = 0

		db.session.commit()

		return redirect(url_for('views_bp.accounts'))

	return render_template('home_pages/accounts.html', form=form1, form2=form2, accounts=acc_data, default_acc=default_acc)


@views_bp.route('/transactions', methods=['GET', 'POST'])
def transactions():
	account = ExpenceAccount.query.all()
	exp_acc = ExpenceAccount.query.filter_by(current=1).first()
	exp_data = Expence.query.filter_by(exp_acc_id=exp_acc.id).all()

	add_tx = 0
	spend_tx = 0

	for tx in exp_data:
		if tx.add_spend == 1:
			add_tx += 1
		elif tx.add_spend == 0:
			spend_tx += 1
	all_tx = [len(exp_data), add_tx, spend_tx]

	if request.method == 'POST':
		acc_no = request.form['no_acc']
		exp_acc = ExpenceAccount.query.filter_by(id=acc_no).first()
		exp_data = Expence.query.filter_by(exp_acc_id=acc_no).all()

		add_tx = 0
		spend_tx = 0

		for tx in exp_data:
			if tx.add_spend == 1:
				add_tx += 1
			elif tx.add_spend == 0:
				spend_tx += 1

		all_tx = [len(exp_data), add_tx, spend_tx]


	return render_template('home_pages/all_transactions.html', account=account, exp_data=exp_data, exp_acc=exp_acc,all_tx=all_tx)