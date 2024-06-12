import faker
from models import User, Landlord, db
from app import app
from random import choice 

fake = faker.Faker()

with app.app_context():
    User.query.delete()
    Landlord.query.delete()

    db.session.commit()

    # Landlord
    landlords = []
    for _ in range(2):
        tenant = Landlord(name=fake.company())
        db.session.add(tenant)
        landlords.append(tenant)
    db.session.commit()

    # User 
    for _ in range(2):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            tenant_id=choice(landlords).id
        )
        db.session.add(user)
    db.session.commit()

