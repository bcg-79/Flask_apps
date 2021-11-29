from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(150), nullable=False)
	exp_account = db.relationship('ExpenceAccount')


class ExpenceAccount(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	account_name = db.Column(db.String(100), nullable=False)
	category = db.Column(db.String(50), nullable=False)
	initial_amount = db.Column(db.Float, nullable=False)
	remaining_amount = db.Column(db.Float, nullable=False, default=0.0)
	created = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
	current = db.Column(db.Integer, nullable=False, default=0)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	expence = db.relationship('Expence')

class Expence(db.Model):
	id  = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Float, nullable=False)
	payee = db.Column(db.String(150), nullable=False)
	category = db.Column(db.String(150), nullable=False)
	notes = db.Column(db.String(300), nullable=False)
	add_spend = db.Column(db.Integer, nullable=False, default=0)
	created = db.Column(db.DateTime(timezone=True), default=func.now())
	exp_acc_id = db.Column(db.Integer, db.ForeignKey('expence_account.id'))