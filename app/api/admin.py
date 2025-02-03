from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from ..models import AdminUser
from .. import db

admin_bp = Blueprint('admin_api', __name__)
api = Api(admin_bp)

class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        admin = AdminUser.query.filter_by(email=email).first()

        if not admin or not check_password_hash(admin.password_hash, password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=admin.id)
        return {"access_token": access_token, "role": admin.role}, 200

api.add_resource(AdminLogin, "/admin/login")
