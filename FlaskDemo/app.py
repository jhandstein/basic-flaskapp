from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/') # prevents 404
def index():
    return 'Hello World!'

# best practices:
#  - don't use dashes
# - use telling names

text = {'text': 'This is your useful chatbot!'}
@app.route('/return-string', methods=['GET'])
def return_string():
    return jsonify(text)

# example for endpoint in controller
@app.route('/text-input', methods=['POST'])
def manual_text_input():
    text_input = request.get_json()

    output = {'text': f'You said: *{text_input["text"]}*'}
    return jsonify(output), 200



if __name__ == '__main__':
    app.run(debug=True, port=5001) # debug has to be False for actual deployment

# http://127.0.0.1:5000/