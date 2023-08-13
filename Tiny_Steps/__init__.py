from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'hello-bandor'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    app.app_context().push()

    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KtZvNSD2iC3vN8t0mffTjAsISgKHb1wIA9cErnPJQBTMeewiwrWLEjUArNiTwcTWkUBhK3QwofLcRMqm8npnh1Y00jELT29jV'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KtZvNSD2iC3vN8tyK2CHOynvPcfFJM2LBLGLAAEcIaJE01XfGTucjfVkNOiTQ90SK5ovGd3De7suo7O8huc2QB1004VEXFTLl'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Tourist
    @login_manager.user_loader
    def load_user(user_id):
        return Tourist.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

db.create_all(app=create_app())