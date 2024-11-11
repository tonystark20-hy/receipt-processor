FROM python:3.11-slim

WORKDIR /main

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

EXPOSE 8080

RUN python -m unittest discover -s tests

CMD ["flask", "run"]
