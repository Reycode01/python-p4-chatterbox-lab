# seed.py

#!/usr/bin/env python3

from random import choice as rc
from faker import Faker

from app import app, db
from models import Message

fake = Faker()

def make_messages():
    with app.app_context():
        # Clear existing messages in the database
        Message.query.delete()

        # Generate a list of random usernames
        usernames = [fake.first_name() for _ in range(4)]
        if "Duane" not in usernames:
            usernames.append("Duane")

        messages = []

        # Create 20 random messages
        for _ in range(20):
            message = Message(
                body=fake.sentence(),
                username=rc(usernames),
            )
            messages.append(message)

        # Add all new messages to the session and commit to the database
        db.session.add_all(messages)
        db.session.commit()

if __name__ == '__main__':
    # Ensure the app context is active before running make_messages
    with app.app_context():
        make_messages()


