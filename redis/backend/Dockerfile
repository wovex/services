FROM python:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./app /app
ENV PYTHONPATH=/app

WORKDIR /app/

ENTRYPOINT ["/start.sh"]
