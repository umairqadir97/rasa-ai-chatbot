FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python3-dev python-dev libicu-dev libffi-dev libmysqlclient-dev python3-pip virtualenv\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip