import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Project, Education, Certification, ContactMessage

# 1. Initialize Flask Application Engine
app = Flask(__name__)

# 2. Configure Security & Database Settings
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production-kabul'  # Protects form submissions
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'portfolio.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Bind SQLAlchemy ORM to Flask App
db.init_app(app)

# 4. Auto-Create Database Tables inside /instance folder
with app.app_context():
    # Ensure the 'instance' directory exists
    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
    db.create_all()


# ==========================================
# 🌐 PUBLIC ROUTES
# ==========================================

@app.route('/')
def home():
    """Renders the main portfolio homepage fetching content dynamically from DB."""
    featured_projects = Project.query.filter_by(is_featured=True).all()
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    education_history = Education.query.order_by(Education.start_year.desc()).all()
    certifications = Certification.query.order_by(Certification.id.desc()).all()

    return render_template(
        'index.html',
        featured_projects=featured_projects,
        projects=all_projects,
        education=education_history,
        certifications=certifications
    )


@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Renders a dedicated case-study page for a single project."""
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)


@app.route('/contact', methods=['POST'])
def handle_contact():
    """Processes incoming contact form submissions and saves them to the DB."""
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if name and email and message:
        new_message = ContactMessage(
            sender_name=name,
            sender_email=email,
            subject=subject,
            message_body=message
        )
        db.session.add(new_message)
        db.session.commit()
        flash('Thank you! Your message has been sent successfully.', 'success')
    else:
        flash('Please fill in all required fields.', 'danger')

    return redirect(url_for('home'))


# ==========================================
# ⚙️ APPLICATION ENTRY POINT
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)