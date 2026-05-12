from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class ChatRecord(db.Model):
    __tablename__ = "chat_records"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False, index=True)
    agent_name = db.Column(db.String(32), nullable=False)
    user_msg = db.Column(db.Text, nullable=False)
    agent_reply = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False)
    agent_name = db.Column(db.String(32), nullable=False)
    rating = db.Column(db.Integer)  # 1-5
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
