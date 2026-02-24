FROM python:3.10

WORKDIR /app

COPY app.py .

RUN pip install flask prometheus_client

EXPOSE 80

CMD ["python", "app.py"]