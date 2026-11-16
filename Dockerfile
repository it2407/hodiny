FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Europe/Prague

COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]