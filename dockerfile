FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python2.7 build-essential libssl-dev libffi-dev python-dev python-tk
RUN pip install nltk==3.2.2
RUN python -m nltk.downloader punkt

COPY . /spider/
WORKDIR /spider/
RUN pip install -r requirements.txt


WORKDIR /spider/491_Spider
CMD ["scrapy", "crawl", "news"]