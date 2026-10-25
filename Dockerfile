FROM python:3.14-slim
COPY app.py /app.py
CMD ["python", "/app.py"]
