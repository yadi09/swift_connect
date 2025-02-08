from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class BusinessRequest(db.Model):
    __tablename__ = "BusinessRequests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=False)
    business_email = db.Column(db.String(255), nullable=False, unique=True)
    swift_code = db.Column(db.String(20), nullable=False)
    business_type = db.Column(db.Enum("Bank", "Financial Institution", "Education", "Other"), nullable=False)
    request_reason = db.Column(db.Text, nullable=False)
    request_status = db.Column(db.Enum("Pending", "Approved", "Rejected"), server_default=db.text('Pending'))
    request_id = db.Column(db.String(50), nullable=False, unique=True)
    api_credentials = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def all(self):
        """Retrieve all business requests"""
        return BusinessRequest.query.all()

    def approve(self):
        """Mark the request as approved"""
        self.request_status = "Approved"
        db.session.commit()

    def reject(self):
        """Mark the request as rejected"""
        self.request_status = "Rejected"
        db.session.commit()

    @staticmethod
    def get_by_request_id(request_id):
        """Retrieve a business request by request_id"""
        return BusinessRequest.query.filter_by(request_id=request_id).first()

class AdminUser(db.Model):
    __tablename__ = "AdminUsers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("Admin", "Super Admin"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def set_password(self, password):
        """Hash the password and store it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the given password matches the stored hash"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        """Retrieve an admin user by email"""
        return AdminUser.query.filter_by(email=email).first()
