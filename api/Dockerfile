FROM python:3.12-slim

WORKDIR /app
COPY app.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh
CMD ["python", "app.py"]
