FROM python:3.8

WORKDIR /app

EXPOSE 8000

ENV db_user root
ENV db_pass tyM0fQatqKam7Jr
ENV db_ip localhost
ENV db_port 27017

COPY . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD python main.py