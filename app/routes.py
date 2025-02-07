from flask import Blueprint, render_template, request, jsonify
from .models import BusinessRequest
from . import db
import uuid

bp = Blueprint('main', __name__)

# Home route for customer onboarding
@bp.route('/')
def index():
    return render_template('index.html')

# Check request status route
@bp.route('/check_status/<int:request_id>', methods=['GET'])
def check_status(request_id):
    request_record = BusinessRequest.query.get(request_id)
    if request_record:
        return jsonify({"status": request_record.request_status})
    else:
        return jsonify({"error": "Request ID not found"}), 404

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
