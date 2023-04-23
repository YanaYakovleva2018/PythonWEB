FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p /data

COPY . .

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]
