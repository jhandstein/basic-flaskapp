from flask import Flask, request, jsonify
from src.call_azure_endpoint import ls_prediction, ls_entity_recognition, ls_question_answering
from src.mysql_database import db, store_request
from src import mysql_secrets

con_string = f'mysql://{mysql_secrets.dbuser}:{mysql_secrets.dbpass}@{mysql_secrets.dbhost}/{mysql_secrets.dbname}'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = con_string
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

app = create_app()

# create table before first request (if it doesn't exist)
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return 'Hello fellow SQL enthusiasts!'

@app.route('/db/textclass', methods=['POST'])
def text_classification():
    text_input = request.get_json()
    category, confidence = ls_prediction(text_input['text'])
    output = {'classification': f'Your input was classified as: *{category}* with confidence score: *{confidence}*'}
    store_request(type_='text_classification', text=text_input['text'], category=category)
    return jsonify(output), 200

@app.route('/db/entityrecog/', methods=['POST'])
def entity_recognition():
    text_input = request.get_json()
    entities = ls_entity_recognition(text_input['text'])
    output = {'entities': entities}
    store_request(type_='entity_recognition', text=text_input['text'], entities=entities.__repr__())
    return jsonify(output), 200

@app.route('/db/questionanswering/', methods=['POST'])
def question_answering():
    text_input = request.get_json()
    answer = ls_question_answering(text_input['text'])
    output = {'answer': answer}
    store_request(type_='question_answering', text=text_input['text'], answer=answer)
    return jsonify(output), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)