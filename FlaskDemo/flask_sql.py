from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///openai-db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class LabelledText(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(200), nullable=False)
#     category = db.Column(db.String(20), nullable=False)

#     def __repr__(self):
#         return f'Text {self.id} - {self.category}'

# class OpenAIRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(20), nullable=False)
#     text = db.Column(db.String(200), nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def __repr__(self):
#         return f'Request {self.id}'

if __name__ == '__main__':
    app.run(debug=True, port=5001)