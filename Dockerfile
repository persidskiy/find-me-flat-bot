from python:2.7

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD . /

VOLUME [ "/data" ]

CMD ["python", "bot.py"]