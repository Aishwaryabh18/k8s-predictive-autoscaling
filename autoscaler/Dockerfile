FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install kubernetes requests

CMD ["python", "main.py"]