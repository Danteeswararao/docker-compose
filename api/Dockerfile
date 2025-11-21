FROM python:3.12-slim

WORKDIR /app
COPY app.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# CMD must run Flask in foreground
CMD ["python", "app.py"]
