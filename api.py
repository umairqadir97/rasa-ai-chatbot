import ast
import os
from collections import defaultdict
import flask
from flask import *
from flask_cors import CORS
from random import random
import threading
import time
from configuration import *
from api_helper import *
from chat_endpoint import *


STATIC_DIR = os.path.abspath('./static')
app = Flask(__name__, static_folder=STATIC_DIR)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "demo-chat-bot"

# Load Inverted_Index, globally
file_handler = open(misspell_inverted_index_file, 'r', encoding="utf-8")
string_dict = file_handler.read()
user_language = "english"   # maintaining this variable at global scope or language switching decisions
inverted_index = defaultdict(lambda: [], ast.literal_eval(string_dict))

# conversation log
conversation_by_session = {}


@app.route('/', methods=['POST', 'GET'])
def server_health():
    """
    This endpoint is availabel to check server health
    :return: json object for server status [ON/OFF]
    """
    return jsonify({"server_status": "on"}), 200


@app.route('/chat', methods=['POST'])
def get_server_response():
    """
    Main Endpoint for making conversations with chatbot. Senda POST request with following json input:
    {"sender": Unique user ID,
    "message": Message you want to send to chatbot server
    }
    :return: Response from Chatbot Server
    """
    try:
        global conversation_by_session
        global user_language
        data = json.loads(flask.request.data)
        if "message" not in data or "sender" not in data:
            return jsonify({"Error": "Invalid Input!"}), 400
        sender = data["sender"]
        user_message = " ".join([inverted_index.get(key, key) for key in preprocessing(data['message']).split(" ")])
        language = get_user_language(user_message, user_language)
        print("Language: ", language)
        print("sender: {}, message: {}".format(sender, user_message))
        response_object, response_string = get_response_from_chatbot(sender=sender,
                                                                     message=user_message,
                                                                     language=language, debug=False)
        
        #
        # Conversation Logs -- start
        log_user_conversation(sender=sender, user_message=user_message, bot_response=response_string)
        # Conversation Logs -- end
        #

        return jsonify(response_object), 200
    except Exception as exe:
        import traceback
        print(traceback.format_exc(exe))
        return jsonify({"Error": str(exe)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
