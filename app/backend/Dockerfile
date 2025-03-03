#backend dockerfile
FROM python:3.12.3-slim

WORKDIR /backend

#COPY requirements.txt requirements.txt
#RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN useradd user
USER user

ENV HOME=/home/user\
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN python model_download.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
    #"--ssl_certfile", "cert.pem",\
    #"--ssl_keyfile", "key.pem"]