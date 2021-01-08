from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from partyAccounting.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from partyAccounting.users.routes import users
	from partyAccounting.userparties.routes import userparties
	from partyAccounting.usertransactions.routes import usertransactions
	from partyAccounting.transactionreports.routes import transactionreports
	from partyAccounting.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(userparties)
	app.register_blueprint(usertransactions)
	app.register_blueprint(transactionreports)
	app.register_blueprint(main)


	#with app.app_context():
	#	db.create_all()

	return app