from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy ORM instance
db = SQLAlchemy()


class Project(db.Model):
    """Stores showcased software applications and engineering projects."""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    tagline = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_tags = db.Column(db.String(200), nullable=False)  # Comma-separated: e.g. "Python, Flask, Tailwind"
    category = db.Column(db.String(80), nullable=False, default="Full-Stack")  # e.g. "Full-Stack", "AI / ML", "Automation"
    github_url = db.Column(db.String(255), nullable=True)
    live_url = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Project {self.title}>"


class Education(db.Model):
    """Stores academic background and university achievements."""
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(120), nullable=False)          # e.g. "B.S. in Computer Science"
    institution = db.Column(db.String(120), nullable=False)     # e.g. "Kabul University"
    concentration = db.Column(db.String(150), nullable=True)    # e.g. "Artificial Intelligence & Information Systems"
    start_year = db.Column(db.String(20), nullable=False)       # e.g. "2024"
    end_year = db.Column(db.String(20), nullable=False)         # e.g. "Present"
    relevant_coursework = db.Column(db.Text, nullable=True)    # e.g. "Discrete Math, OOP, Database Systems"

    def __repr__(self):
        return f"<Education {self.degree}>"


class Certification(db.Model):
    """Stores verified industry certifications and course accomplishments."""
    __tablename__ = 'certifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)          # e.g. "Working with APIs in Python"
    issuer = db.Column(db.String(100), nullable=False)         # e.g. "DataCamp"
    issue_date = db.Column(db.String(50), nullable=False)      # e.g. "June 2026"
    credential_url = db.Column(db.String(255), nullable=True)
    badge_icon = db.Column(db.String(100), nullable=True)       # e.g. "python_api_badge.png"

    def __repr__(self):
        return f"<Certification {self.title}>"


class ContactMessage(db.Model):
    """Stores messages received from recruiters and site visitors."""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message_body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<ContactMessage from {self.sender_email}>"