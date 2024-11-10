FROM python:3.11-slim

WORKDIR /main

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables for Flask (optional, but good practice)
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

EXPOSE 8080

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]
