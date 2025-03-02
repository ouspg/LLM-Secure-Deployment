#backend dockerfile
FROM python:3.12.3

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN useradd user
USER user

ENV HOME=/home/user\
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app
#COPY app.py app.py
#COPY cert.pem cert.pem
#COPY key.pem key.pem

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
    #"--ssl_certfile", "cert.pem",\
    #"--ssl_keyfile", "key.pem"]