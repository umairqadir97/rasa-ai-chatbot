#! /bin/sh

# start screen 'sample_screen'

screen -S chatbot_flask_api -d -m bash -c "python3 api.py"

screen -S chatbot_english_action_server -d -m bash -c "cd ./english_agent/; rasa run actions --port 5055;"

screen -S chatbot_english_chat_server -d -m bash -c "cd ./english_agent/;  rasa run -m models/ --enable-api --log-file out.log --cors "*" --endpoints endpoints.yml --port 8000;"

screen -S chatbot_roman_action_server -d -m bash -c "cd ./roman_urdu_agent/; rasa run actions --port 5056;"

screen -S chatbot_roman_chat_server -d -m bash -c "cd ./roman_urdu_agent/; rasa run -m models/ --enable-api --log-file out.log --cors "*" --endpoints endpoints.yml --port 8006;"

screen -S chatbot_redis_server -d -m bash -c "cd ~/redis-5.0.5; src/redis-server;"

# If you want to kill: screen -S name -X quit
# kill all linux screen: killall screen