from app import db

class BusinessRequest(db.Model):
    __tablename__ = "BusinessRequests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=False)
    business_email = db.Column(db.String(255), nullable=False, unique=True)
    swift_code = db.Column(db.String(20), nullable=False)
    business_type = db.Column(db.Enum("Bank", "Financial Institution", "Other"), nullable=False)
    request_reason = db.Column(db.Text, nullable=False)
    request_status = db.Column(db.Enum("Pending", "Approved", "Rejected"), server_default=db.text('Pending'))
    request_id = db.Column(db.String(50), nullable=False, unique=True)
    api_credentials = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class AdminUser(db.Model):
    __tablename__ = "AdminUsers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("Admin", "Super Admin"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
