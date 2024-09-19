from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from bot import *

app =Flask(__name__)

CORS(app, resources={r"/*":{"origins": "*"}})

def get_chatbot_response(message, dealerId):
    chat = Chat(dealerId)
    # chat.add_training()
    response = chat.chatWithBot(message)
    return response

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chat", methods = ['POST'])
def chat():
    userMessage = request.form['message']
    # dealerId_dict = request.form['dealerId']
    dealerId = request.form['dealerId'] # dealerId_dict['dealer_id']
    botResponse = get_chatbot_response(userMessage, dealerId)
    return jsonify({"response": botResponse})

@app.route('/delete-file', methods=['POST'])
def delete_file():
    file_path = request.json.get('filePath')
    try:
        os.remove(file_path)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    app.run(debug = True, port = 5001, host = "0.0.0.0")