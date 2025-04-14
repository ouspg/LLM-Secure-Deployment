# Backend Dockerfile


FROM python:3.12.3-slim

# For TLS
RUN apt-get install -y --no-install-recommends ca-certificates

RUN useradd user
USER user

ENV HOME=/home/user\
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy app/backend/ contents to working directory and install requirements.
COPY --chown=user . $HOME/app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Bake model download into image build to ease reproducibility. This is generally a bad practice 
# and the download should be done separately. E.g. by mounting a downloaded model onto a running container.
RUN python model_download.py

# Launch the backend on port 8000 on container start.
CMD ["uvicorn", "app:app",\
    "--host", "0.0.0.0",\
    "--port", "8000",\
    "--ssl-certfile", "cert.pem",\
    "--ssl-keyfile", "key.pem"]