# app.py

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Routes
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([message.serialize() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data.get('body'), username=data.get('username'))
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize()), 201

@app.route('/messages/<int:message_id>', methods=['PATCH'])
def update_message(message_id):
    message = Message.get_message_or_404(message_id)
    data = request.get_json()
    message.update(data)
    return jsonify(message.serialize())

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.get_message_or_404(message_id)
    message.delete()
    return '', 204

if __name__ == '__main__':
    app.run(port=4000)









