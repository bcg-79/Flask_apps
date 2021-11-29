from flask import (Blueprint, render_template,
	redirect, url_for, flash)
from .forms import SignupForm, LoginForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()

		if user:
			if check_password_hash(user.password, password):
				login_user(user, remember=True)
				flash('Successfully Login!')
				return redirect(url_for('views_bp.dashboard'))
			else:
				flash("Check Username or Password!", category='error')
				return redirect(url_for('auth_bp.login'))
		else:
			flash('There is NO Account registered with this Email Address.', category='warning')
			return redirect(url_for('auth_bp.login'))

	return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		password = form.password.data

		u = User.query.filter_by(username=username).first()
		e = User.query.filter_by(email=email).first()
		if u:
			flash(f"Username {username} is already registered", category='username_error')
			return redirect(url_for('auth_bp.signup'))
		elif e:
			flash(f"Email {email} is already registered", category='email_error')
			return redirect(url_for('auth_bp.signup'))
		else:
			new_user = User(username=username, email=email, password=generate_password_hash(password))
			db.session.add(new_user)
			db.session.commit()

			flash(f'Account Created Successfully for {email}', category='success')
			return redirect(url_for('auth_bp.login'))

	return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth_bp.login'))

