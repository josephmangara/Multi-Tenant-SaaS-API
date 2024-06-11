import faker
from models import User, Tenant 
from app import app, db

fake = faker.Faker()

with app.app_context():
    User.query.delete()
    Tenant.query.delete()

    db.session.commit()

    # User 
    names = []

    fake_name = User(
        username = fake.name(),
        password = fake.password(),
        tenant_id = fake.id()
    )

    db.session.add(fake_name)
    names.append(fake_name)

    db.session.commit()
