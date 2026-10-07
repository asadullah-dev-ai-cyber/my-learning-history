from main import app
from models import db, Project

def populate_database():
    with app.app_context():
        # Clean existing records and re-create
        db.drop_all()
        db.create_all()

        sample_projects = [
            Project(
                title="Flask Dynamic Blogging Platform",
                tagline="Full-stack blogging web app featuring multi-route routing and custom authentication.",
                description="Designed and deployed a full-stack Flask application equipped with dynamic routing, relational SQLite database storage, dynamic password hashing, administrative controls, and customized user interface styling.",
                tech_tags="Python, Flask, SQLite, HTML/CSS, Jinja2",
                category="Web Application",
                live_url="https://blog-website-2li9.onrender.com/",
                is_featured=True
            )
        ]

        db.session.bulk_save_objects(sample_projects)
        db.session.commit()
        print("✅ Database successfully updated with your hosted blog project!")

if __name__ == "__main__":
    populate_database()