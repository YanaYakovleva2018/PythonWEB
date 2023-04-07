FROM python:3.11
ENV APP_HOME /app
WORKDIR $ABVAD
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "abvad//main.py"]
