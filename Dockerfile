FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
COPY ./src/ /app

ENTRYPOINT ["python"]
CMD ["main.py"]
