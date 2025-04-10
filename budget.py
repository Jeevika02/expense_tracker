from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Budget

budget_bp = Blueprint('budget', __name__, url_prefix='/budget')

@budget_bp.route('/set_category_budget', methods=['POST'])
@login_required
def set_category_budget():
    category = request.form['category']
    amount = float(request.form['amount'])

    existing = Budget.query.filter_by(user_id=current_user.id, category=category).first()
    if existing:
        existing.amount = amount  
    else:
        new_budget = Budget(category=category, amount=amount, user_id=current_user.id)
        db.session.add(new_budget)

    db.session.commit()
    flash(f"{category} budget set to ₹{amount}", "success")
    return redirect(url_for('home'))
