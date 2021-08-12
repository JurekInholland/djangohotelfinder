FROM python:3.9.6
RUN apt-get update && apt-get install -y cron
RUN chmod 644 /etc/crontab

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
