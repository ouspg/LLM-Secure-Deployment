# <p align="center">Secure Deployment of Large Language Models</p>
This repository contains the codebase for Mikko Lempinen's Master's Thesis titled "Secure Deployment of Large Language Models"

## <p align="center">Table of Contents</p>

- [Deployment via Docker](#docker-deploymet)
- [Direct deployment](#direct-deploymet)
    - [Frontend deployment](#frontend-deployment)
    - [Backend deployment](#backend-deployment)

## <p align="center">Deployment via Docker</p><a name="docker-deployment"></a>

The application was deployed with Docker version 28.0.1.

To simplify the deployment process, we will be generating a self-signed SSL certificate for
enforcing TLS communications with the backend of the application that contains the LLM.

We will additionally include the certificate and its private key within the Docker image, 
which is a security risk if the plan is to allow non-restricted access to the image.

1. Generate a self-signed SSL certificate:
    ```console
    openssl req -x509 -newkey rsa:4096 -keyout app/backend/key.pem -out app/backend/cert.pem -days 365 -nodes
    ```

2. In the root directory of the repository, build the Docker environment with:
    ```console
    docker compose up -d
    ```
3. Patiently wait for the build to finish *(can take an hour)*. After the build is complete, the 
containers (`llm-secure-deployment-backend` and `llm-secure-deployment-frontend`) should be up and running.

4. Navigate to `https://localhost:3006` via a browser and you can use the application.

## <p align="center">Direct deployment</p><a name="direct-deployment"></a>
The application can be deployed directly without sandboxing it with Docker. Direct deployment was 
done with Ubuntu 24.04 and Python 3.12.3.

In the root directory of the repository, create and activate a Python virtual environment:
```console
python -m venv .venv
```
```console
source .venv/bin/activate
```

### <p align="center">Frontend deployment</p><a name="frontend-deployment"></a>
1. Install frontend dependencies with npm:
    ```console
    cd app/frontend
    ```
    ```console
    npm install
    ```
    ```console
    npm install -g serve
    ```

2. Inside the `app/frontend/` directory, you can now build and serve the React frontend with:
    ```console
    npm run build
    ```
    ```console
    serve -s build -l 3006
    ```
3. The frontend should now be running with its endpoint being on port `3006`. Navigate to 
`https://localhost:3006` via a browser to use the application.

### <p align="center">Backend deployment</p><a name="backend-deployment"></a>
1. Install backend dependencies:
    ```console
    pip install -r app/backend/requirements.txt
    ```
2. Download the Hugging Face Language Model:
    ```console
    cd app/backend
    ```
    ```console
    python download_model.py
    ```

3. Inside the `app/backend/` directory, you can now start the LLM-application with
    ```console
    python app.py
    ```
4. The backend should now be running with its endpoint being on port `8000`.



## Generating and Using SSL Certificates

1. Navigate to `./ProductionReadyChatbot` and generate a self-signed certificate with the following command:

    ```bash
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    ```

2. Save the **`cert.pem`** and **`key.pem`** files in the `./ProductionReadyChatbot` directory.

3. Ensure that your system **trusts** the certificate, as self-signed certificates are not trusted by default. You can do this in one of two ways:

    **Option 1: Add the certificate to root certificates (Linux/Ubuntu)**
    - Copy the certificate to the appropriate directory:
        ```bash
        sudo cp cert.pem /usr/local/share/ca-certificates/cert.crt
        sudo update-ca-certificates
        ```

    **Option 2: Manually trust the certificate in your browser**
    - Open [https://127.0.0.1:8000/](https://127.0.0.1:8000/) in your browser.
    - Accept the certificate warning and manually trust it. This will allow the frontend to connect to the backend.

---
