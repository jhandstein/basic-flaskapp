from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OpenAIRequest(db.Model):
    __tablename__ = 'openai_requests'
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=True)
    entities = db.Column(db.String(200), nullable=True)
    answer = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Request {self.id}'

def store_request(type_: str, text: str, category: str=None, entities: str=None, answer: str=None) -> None:
    try:
        id = OpenAIRequest.query.count() + 1
    except:
        id = 1
    new_request = OpenAIRequest(id=id, request_type=type_, text=text)

    if type_ == 'text_classification':
        new_request.category = category
    elif type_ == 'entity_recognition':
        new_request.entities = entities
    elif type_ == 'question_answering':
        new_request.answer = answer
        
    db.session.add(new_request)
    db.session.commit()