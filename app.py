from flask import Flask, render_template, redirect, url_for, flash  
from models import db, User, Budget, Expense
from flask_login import LoginManager
from flask_login import LoginManager, login_required, current_user

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'lkjhgfd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from routes.auth import auth_bp
    from routes.expenses import expenses_bp
    from routes.budget import budget_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(budget_bp)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Home route
    @app.route('/')
    @login_required
    def home():
        category_budgets = Budget.query.filter_by(user_id=current_user.id).all()

        # Get total spent per category
        expenses = Expense.query.filter_by(user_id=current_user.id).all()
        expenses_by_category = {}
        for exp in expenses:
            expenses_by_category[exp.category] = expenses_by_category.get(exp.category, 0) + exp.amount

        return render_template('index.html', category_budgets=category_budgets, expenses_by_category=expenses_by_category)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
