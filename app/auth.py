from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import AdminUser
from . import db

auth_bp = Blueprint("auth", __name__)

# Login route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bp.admin"))  # Redirect to admin dashboard

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = AdminUser.get_by_email(email)
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for("main.admin"))  # Redirect to admin dashboard
        else:
            flash("Invalid email or password", "error")
            return jsonify({"error": "Invalid email or password", "success": False}), 401

    return render_template("admin_login.html")

# Logout route
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# Register route (For initial admin setup)
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # full_name = request.form.get("full_name")
        # email = request.form.get("email")
        # password = request.form.get("password")
        # role = request.form.get("role")

        data = request.get_json()  # Parse the JSON data from the request body
        
        # Extract the fields from the JSON data
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        if AdminUser.get_by_email(email):
            flash("Email already registered", "error")
            # return redirect(url_for("auth.register"))
            return jsonify({"error": "Email already registered", "success": False}), 400

        new_admin = AdminUser(
            full_name=full_name, email=email, role=role
        )
        new_admin.set_password(password)

        db.session.add(new_admin)
        db.session.commit()

        flash("Admin account created successfully", "success")
        return redirect(url_for("auth.login"))

    # return render_template("register.html")
    return jsonify({"message": "Use PostMan to register new Admin", "success": True}), 201
