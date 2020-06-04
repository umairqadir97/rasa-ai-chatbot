#!/usr/bin/python

import json
import re
import requests
from configuration import *

not_allowed_Slots = ["right now", "now", "the second", "on the 14th", "at this time"]
stopwords = ["(edited)"]+not_allowed_Slots
samples = ["check balance"]
RASA_API_SERVER_ROMAN = "http://localhost:8006/webhooks/rest/webhook"
RASA_API_SERVER_ENGLISH = "http://localhost:8000/webhooks/rest/webhook"


def preprocessing(text):
    """API Helper Function, for preprocessing the Human messages before forwarding to bot"""
    if text == "/restart":
        return text
    text = repr(text)
    text = text.strip(r'\n')
    if '\\n' in text:
        text = ' '.join(text.split("\\n")).replace('\\',"")
    elif '\n' in text:
        text = ' '.join(text.split("\n"))
    text = re.sub(r'[^0-9A-Za-z] *', ' ', text.lower().strip())
    text = re.sub(r' +', ' ', ' '.join(text.splitlines()).strip())
    text_tokens = text.split()
    text = " ".join([token for token in text_tokens if token not in stopwords])
    return str(text).strip("'").strip('"')


def get_response_from_chatbot(sender, message, language, debug=False):
    """
    API Helper Function, Intermediate function to pass message between Flask API &
        relevant Rasa servers [English/ Roman-Urdu]
    :param sender: Unique session/ user ID
    :param message: Text message of Human
    :param language: Language of human message
    :param debug: Debug mode [False by default]. Will print conversations to console if True
    :return:
        response: actual response from Rasa server
        response_string: response message as text for maintaining  conversation log
    """
    if debug:
        print("Sender: ", sender)
        print("Input Message: ", message)

    response = "Sorry, Something went wrong. Try again!"
    response_string = ""
    try:
        if not message or message == "None":
            message = "hi"
        elif message in ["/restart", "[__(__EXIT__)__]"]:
            response = reset_user_session(sender)
            return response, response_string
        message = preprocessing(message)

        #
        # language detection
        if language == "english":
            response = requests.post(RASA_API_SERVER_ENGLISH, json={"sender": sender, "message": message}).json()
        elif language == "roman urdu":
            response = requests.post(RASA_API_SERVER_ROMAN, json={"sender": sender, "message": message}).json()
        response_string = " \n  ".join([elt['text'] for elt in response if 'text' in elt]).lower()
        if "authentication fail" in response_string:
            reset_user_session(sender)
    except Exception as err:
        print("RASA Api Server Error: ", err)
    return response, response_string


def reset_user_session(sender):
    """
    API Helper Function, to reset a specific session tracker
    :param sender: Unique session/ user ID
    :return: Server response
    """
    server_response = requests.post(RASA_API_SERVER_ROMAN, json={"sender": sender, "message": "/restart"}).json()
    print("Resetting session against user_id: ", sender)
    return server_response


def test_samples():
    for pos, message in enumerate(samples):
        extraction = get_response_from_chatbot(sender="default", message=message, debug=True)['text']
        try:
            extraction = json.loads(extraction)
            print("\n", str(pos)+": ", message, extraction["intent"])
        except json.decoder.JSONDecodeError:
            print("Error!")
            print("\n", str(pos)+": ", message, extraction)


# if __name__ == "__main__":
#     sender_id = sys.argv[1:][0].strip()
#     input_message = sys.argv[1:][1].strip()
#     response = get_response_from_chatbot(sender_id, input_message, debug=True)
#     print("\n\nResponse: ", response)
