from app.app import create_app
from app.models.base import db

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully!")
