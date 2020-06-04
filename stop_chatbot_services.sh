#! /bin/sh

# kill -9 $(pidof src/redis-server)

screen -r chatbot_flask_api -X quit
screen -r chatbot_english_action_server -X quit
screen -r chatbot_english_chat_server -X quit
screen -r chatbot_roman_action_server -X quit
screen -r chatbot_roman_chat_server -X quit
screen -r chatbot_redis_server -X quit
