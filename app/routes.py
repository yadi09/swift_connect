from flask import Blueprint, render_template, request, jsonify
from .models import BusinessRequest
from . import db
import uuid
from flask_login import login_required

bp = Blueprint('main', __name__)

# Home route for customer onboarding
@bp.route('/')
def index():
    return render_template('index.html')

# Check request status route
@bp.route('/get_request/<string:request_id>', methods=['GET'])
def get_request(request_id):
    request_record = BusinessRequest.get_by_request_id(request_id)
    if request_record:
        return jsonify({
            "company_name": request_record.company_name,
            "business_email": request_record.business_email,
            "swift_code": request_record.swift_code,
            "business_type": request_record.business_type,
            "request_reason": request_record.request_reason,
            "request_status": request_record.request_status,
            "request_id": request_record.request_id,
            "success": True
        }), 200
    else:
        return jsonify({"error": "Request ID not found", "success": False}), 404

# Submit request route
@bp.route('/submit_request', methods=['POST'])
def submit_request():
    data = request.json  # Get JSON data from frontend

    # Extract form data
    company_name = data.get('company_name')
    business_email = data.get('business_email')
    swift_code = data.get('swift_code')
    business_type = data.get('business_type')
    request_reason = data.get('request_reason')

    # Validate required fields
    if not all([company_name, business_email, swift_code, business_type, request_reason]):
        return jsonify({"message": "All fields are required", "success": False}), 400
    
    # Validate email not in use
    if BusinessRequest.query.filter(BusinessRequest.business_email == business_email, BusinessRequest.request_status != "Rejected").first():
        return jsonify({"message": "A request with this email already exists", "success": False}), 400

    # Create a new request record
    new_request = BusinessRequest(
        company_name=company_name,
        business_email=business_email,
        swift_code=swift_code,
        business_type=business_type,
        request_reason=request_reason,
        request_status="Pending",  # Default status
        request_id="BR" + str(uuid.uuid4())[:8]  # Generate a unique request ID
    )

    # Save to database
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Request submitted successfully!", "success": True, "request_id": new_request.request_id}), 201

# Admin route with login requirement
@bp.route('/admin', methods=['GET'])
@login_required
def admin():
    all_requests = BusinessRequest().all()
    return render_template('admin.html', requests=all_requests)

# Get all requests route