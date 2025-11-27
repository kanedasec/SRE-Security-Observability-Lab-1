from python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
run pip install --no-cache-dir -r requirements.txt

COPY app/ /app

EXPOSE 500

CMD ["python", "api.py"]