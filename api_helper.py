from language_detection import *
import os
import re


def get_user_language(msg, user_language):
    """
    API Helper Function, for Language Detection
    :param msg: User message/ string for which you want to detect languaeg
    :param user_language: In whic language user was making conversations. English is default. This parameter is required
    to make a fluent langauge switch in conversation, based on rules.
    :return: Return language name, currently: ["english", "roman-urdu"]
    """
    language = 'roman urdu'
    try:
        if len(msg.split(" ")) <= 2 or not re.sub(r" +", " ", re.sub(r"[^a-zA-Z]", " ", msg)):
            # messages containing less than three words/ containing only numbers will not switch language
            return user_language
        return get_language(msg)
    except Exception as e:
        print(e)
    return language


def log_user_conversation(sender, user_message, bot_response):
    """
    API Helper Function, for mainting conversation logs for each session ID
    :param sender: Unique session/ user ID
    :param user_message: Message sent from Human user to chatbot
    :param bot_response: Response Message from Chatbot to Human user
    :return: status [True/False] if converation is logged successfully
    """
    path_to_logs = "./conversation_log/"
    if not os.path.exists(path_to_logs):
        os.makedirs(path_to_logs)
    filename = "{user_id}.txt".format(user_id=sender)
    if bot_response:
        with open(path_to_logs + filename, "a") as file:
            file.write("\n\nUSER ---> {user_message}\nBOT ---> {bot_response}".format(
                user_message=user_message, bot_response=bot_response))
        return True
    return False


def get_action_names():
    """API Helper Function, to extract names of all user defined actions in chatbot domain"""
    with open("domain.yml", "r") as file:
        text = file.read()
    return [action.replace("- ", "") for action in text.split("actions:")[1].split(":")[0].split("\n")[:-1] if action]


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
