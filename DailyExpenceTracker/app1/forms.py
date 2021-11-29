from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, FloatField,
					 SelectField, SubmitField, IntegerField, TextAreaField)
from wtforms.validators import DataRequired, Email, Length
from .models import ExpenceAccount, Expence

class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class NewAccountForm(FlaskForm):
	acc_name = StringField('Account Name', validators=[DataRequired(), Length(min=4, max=30)])
	category = SelectField('Categories', choices=[('personal', 'Personal'), ('commercial', 'Commercial')])
	initial_amt = FloatField('Initial Amount', validators=[DataRequired(message="Accept Only Numbers.")])
	submit1 = SubmitField('Create New Account')

class DefaultAcc(FlaskForm):
	acc_id = IntegerField()
	submit2 = SubmitField('Set Default')

class AddSpend(FlaskForm):
	add_spend = SelectField('Add/Spend', choices=[(0, 'Spend Money'), (1, 'Add Money')])
	amount = FloatField('Amount', validators=[DataRequired(message="Accept Numbers only.")])
	payee = StringField('Payee', validators=[DataRequired(), Length(min=5, max=30)])
	category = SelectField('Category', choices=[('home', 'Home'), ('personal', 'Personal'), ('hospital', 'Hospital'), ('post', 'Post Office'), ('other', 'Other')])
	notes = TextAreaField('Notes')
	exp_acc_id = IntegerField()




