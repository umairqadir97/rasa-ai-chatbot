echo "Creating docker container for chatbots(english + roman-urdu) & flask api"
sudo docker-compose build; sudo docker-compose up -d;

sudo docker rmi $(sudo docker images -f "dangling=true" -q)