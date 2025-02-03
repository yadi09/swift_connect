from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from ..models import BusinessRequest
from .. import db

business_requests_bp = Blueprint('business_requests_api', __name__)
api = Api(business_requests_bp)

class BusinessRequests(Resource):
    @jwt_required()
    def get(self):
        requests = BusinessRequest.query.all()
        return jsonify([{
            "id": req.id,
            "company_name": req.company_name,
            "business_email": req.business_email,
            "swift_code": req.swift_code,
            "business_type": req.business_type,
            "request_status": req.request_status,
            "created_at": req.created_at
        } for req in requests])

    def post(self):
        data = request.get_json()
        new_request = BusinessRequest(
            company_name=data["company_name"],
            business_email=data["business_email"],
            swift_code=data["swift_code"],
            business_type=data["business_type"],
            request_reason=data["request_reason"]
        )
        db.session.add(new_request)
        db.session.commit()
        return {"message": "Request submitted successfully"}, 201

api.add_resource(BusinessRequests, "/business_requests")


class UpdateRequestStatus(Resource):
    @jwt_required()
    def put(self, request_id):
        data = request.get_json()
        request_record = BusinessRequest.query.get(request_id)

        if not request_record:
            return {"message": "Request not found"}, 404

        request_record.request_status = data.get("status")
        request_record.rejection_reason = data.get("rejection_reason", None)

        db.session.commit()
        return {"message": "Request status updated"}, 200

api.add_resource(UpdateRequestStatus, "/business_requests/<int:request_id>")
