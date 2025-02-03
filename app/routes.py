from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import BusinessRequest, AdminUser
from . import db
from flask_login import login_user, logout_user, login_required

bp = Blueprint('main', __name__)

# Home route for customer onboarding
@bp.route('/')
def index():
    return render_template('index.html')

# Admin login page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Implement admin login here
    return render_template('login.html')

# Admin dashboard route
@bp.route('/dashboard')
@login_required
def dashboard():
    requests = BusinessRequest.query.all()
    return render_template('dashboard.html', requests=requests)

# Approve request route
@bp.route('/approve/<int:request_id>')
@login_required
def approve_request(request_id):
    request = BusinessRequest.query.get(request_id)
    if request:
        request.request_status = 'Approved'
        db.session.commit()
        flash('Request approved successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# Reject request route
@bp.route('/reject/<int:request_id>', methods=['GET', 'POST'])
@login_required
def reject_request(request_id):
    request = BusinessRequest.query.get(request_id)
    if request:
        # Handle rejection reason and update request status
        rejection_reason = request.form['reason']
        request.request_status = 'Rejected'
        request.rejection_reason = rejection_reason
        db.session.commit()
        flash('Request rejected!', 'danger')
    return redirect(url_for('main.dashboard'))
