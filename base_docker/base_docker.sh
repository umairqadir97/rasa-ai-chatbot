#!/bin/bash

sudo docker rmi "chatbot_base"
sudo docker build -t "chatbot_base" .