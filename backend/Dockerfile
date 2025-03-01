#backend dockerfile
FROM python:3.12.3

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY app.py app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]