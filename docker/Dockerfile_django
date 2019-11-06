FROM python:3
ENV PYTHONBUFFERED 1
WORKDIR /srv
COPY requirements.txt /srv/
RUN pip install -r requirements.txt && rm requirements.txt