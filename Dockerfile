FROM python:3.8
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r ./requirements.txt
ADD . /app
ENV PYTHONPATH=/app
ENTRYPOINT python servel_scraper/main.py
