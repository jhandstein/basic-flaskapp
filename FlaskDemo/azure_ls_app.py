from flask import Flask, jsonify, request
from src.call_azure_endpoint import ls_prediction, ls_entity_recognition, ls_question_answering

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello fellow ChatGPT enthusiasts!'

@app.route('/textclass', methods=['POST'])
def text_classification():
    text_input = request.get_json()
    category, confidence = ls_prediction(text_input['text'])
    output = {'classification': f'Your input was classified as: *{category}* with confidence score: *{confidence}*'}
    return jsonify(output), 200

@app.route('/entityrecog/', methods=['POST'])
def entity_recognition():
    text_input = request.get_json()
    entities = ls_entity_recognition(text_input['text'])
    output = {'entities': entities}
    return jsonify(output), 200

@app.route('/questionanswering/', methods=['POST'])
def question_answering():
    text_input = request.get_json()
    answer = ls_question_answering(text_input['text'])
    output = {'answer': answer}
    return jsonify(output), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')