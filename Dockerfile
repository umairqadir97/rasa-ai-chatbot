FROM chatbot_base

RUN apt-get update \
	&& apt-get install -y locales \
	&& rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

WORKDIR /code

COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt

COPY scripts/run_action_server_english.sh scripts/run_action_server_english.sh
RUN chmod +x scripts/run_action_server_english.sh

COPY scripts/run_chat_server_english.sh scripts/run_chat_server_english.sh
RUN chmod +x scripts/run_chat_server_english.sh

COPY scripts/run_action_server_roman.sh scripts/run_action_server_roman.sh
RUN chmod +x scripts/run_action_server_roman.sh

COPY scripts/run_chat_server_roman.sh scripts/run_chat_server_roman.sh
RUN chmod +x scripts/run_chat_server_roman.sh

COPY . .

ENTRYPOINT []