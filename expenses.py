from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        from models import Expense
        from app import db  
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        expense = Expense(
            user_id=current_user.id,
            category=category,
            amount=amount,
            description=description
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('expenses.dashboard'))

    return render_template('add_expense.html')

@expenses_bp.route('/budgets')
@login_required
def budgets():
    return render_template('budgets.html') 
