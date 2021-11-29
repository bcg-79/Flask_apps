import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'test.db'

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'dev'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
	app.config['PER_PAGE'] = 3

	db.init_app(app)

	from .auth import auth_bp
	from .views import views_bp

	app.register_blueprint(auth_bp, url_prefix='/auth')
	app.register_blueprint(views_bp, url_prefix='')

	create_database(app)

	from .models import User, ExpenceAccount, Expence

	login_manager = LoginManager()
	login_manager.login_view = 'auth_bp.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app

def create_database(app):
	if not os.path.exists('app1/' + DB_NAME):
		db.create_all(app=app)
		print("Database Created Successfully!")



