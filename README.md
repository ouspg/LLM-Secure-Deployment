# <p align="center">Secure Deployment Practices for Large Language Model Applications</p>
This repository contains the codebase for Mikko Lempinen's Master's Thesis: [**Secure Deployment Practices for Large Language Model Applications**](https://urn.fi/URN:NBN:fi:oulu-202506124420).

## <p align="center">Table of Contents</p>

- [Deployment via Docker](#docker-deploymet)
- [Direct deployment](#direct-deploymet)
    - [Frontend deployment](#frontend-deployment)
    - [Backend deployment](#backend-deployment)
- [Docker Scout](#scout)
    - [Software Bill of Materials](#sbom)
    - [CVEs](#cves)

## <p align="center">Deployment via Docker</p><a name="docker-deployment"></a>

The application was deployed with Docker version 28.0.1.

To simplify the deployment process, we will be generating a self-signed SSL certificate for
enforcing TLS communications with the backend of the application that contains the LLM.

We will additionally include the certificate and its private key within the Docker image to ease reproducibility, 
which is a security risk if the plan is to allow non-restricted access to the image. 
A more robust alternative would be to, for example, mount a volume containing a valid signed
certificate onto the backend container after building it with Docker. 

> [!IMPORTANT] 
> The application is configured to be served at **https://86.50.253.176**. In order to deploy the application from other domains, the following variables need to be changed accordingly:
> - Change `server_name` variables *(two)* in `app/frontend/nginx.conf` to your public IP address or domain name.
> - Change `set_real_ip_from` in `app/frontend/nginx.conf` to the CIDR range of trusted addresses.
> - Change the IP address in `compose.yaml` **line 29**.
> - Change the URL in `app/frontend/src/Elements/ChatBot.jsx` **line 27**.
> - Your domain needs to be added to the list of allowed origins in `app/frontend/nginx.conf` **line 53**

1. In the root directory of the repository, generate a self-signed SSL certificate:
    ```console
    openssl req -x509 -newkey rsa:4096 -keyout app/backend/key.pem -out app/backend/cert.pem -days 365 -nodes
    ```

2. Copy the SSL certificate and its private key to `app/frontend` directory:
    ```console
    cp app/backend/cert.pem app/frontend/cert.pem
    ```
    ```console
    cp app/backend/key.pem app/frontend/key.pem
    ```

3. Build the Docker environment with:
    ```console
    docker compose up -d
    ```
4. Patiently wait for the build to finish *(can take more than an hour with slow internet connection)*. After the build is complete, the 
containers (`LLM-Secure-Deployment-Frontend` and `LLM-Secure-Deployment-Backend`) should be up and running.

5. Navigate to `https://<YOUR_DOMAIN_NAME>` via a browser and you can use the application.

> [!NOTE] 
> - Generation of the first response message of the chatbot may take a while as the input and output filters will be loaded after the server receives its first request after intialization.
> - You can monitor the backend container's logging with the command:
>   ```console
>    docker logs CONTAINER_ID -f
>    ```

## <p align="center">Direct deployment</p><a name="direct-deployment"></a>
The application can be deployed directly without sandboxing it with Docker. Note that the proxy server is only included in the Docker deployment. Direct deployment was 
done with Ubuntu 24.04 and Python 3.12.3.

In the root directory of the repository, create and activate a Python virtual environment:
```console
python -m venv .venv
```
```console
source .venv/bin/activate
```

### <p align="center">Backend deployment</p><a name="backend-deployment"></a>
> [!IMPORTANT] 
> If deploying the backend and frontend on the same machine *(locally)*, you need to adjust the configured CORS policy in `app/backend/app.py` accordingly: change the `allow_origins=origins` parameter on **line 21** to `allow_origins=[*]` to allow requests from the same origin.

1. In the root directory of the repository, install backend dependencies:
    ```console
    pip install -r app/backend/requirements.txt
    ```
    
2. Generate a self-signed SSL certificate:
    ```console
    openssl req -x509 -newkey rsa:4096 -keyout app/backend/key.pem -out app/backend/cert.pem -days 365 -nodes
    ```

3. Navigate to the `app/backend` directory with:
    ```console
    cd app/backend
    ```

4. Inside the `app/backend/` directory, you can now start the LLM-application with
    ```console
    python app.py
    ```
5. The backend should now be running with its endpoint being on port `8000`.


### <p align="center">Frontend deployment</p><a name="frontend-deployment"></a>
1. Change the URL in `app/frontend/src/Elements/ChatBot.jsx` on **line 27** to match the URL of the backend API *(`https://127.0.0.1:8000/chat` by default if deploying locally)*.

2. Install frontend dependencies with npm:
    ```console
    cd app/frontend
    ```
    ```console
    npm install
    ```
    ```console
    npm install -g serve
    ```

3. Inside the `app/frontend/` directory, you can now build and serve the React frontend with:
    ```console
    npm run build
    ```
    ```console
    serve -s build -l 3006
    ```
4. The frontend should now be running with its endpoint being on port `3006`. Navigate to 
`http://<YOUR_IP_ADDRESS>:3006` *(`http://localhost:3006` by default if deploying locally)* via a browser to use the application.



## <p align="center">Docker Scout</p><a name="scout"></a>

When the application is deployed with Docker, Docker Scout can be used to analyze the environment for known vulnerabilities and to suggest fixes to these vulnerabilities. Docker Scout can additionally be used generate a Software Bill of Materials (SBOM) of the environment on command. [These](https://medium.com/@charles.vissol/install-the-docker-scout-and-sbom-plugins-8b1744758b7e) instructions can be followed to install the required plugins for Docker CLI.


### <p align="center">CVEs</p><a name="cves"></a>
To analyze the built environment for vulnerabilities:

1. Install [Scout](https://docs.docker.com/scout/) plugin for Docker.

2. Use the following command to print the analysis to console (more instructions of usage can be found [here](https://docs.docker.com/reference/cli/docker/scout/cves/)):
    ```console
    docker scout cves IMAGE_ID
    ```

### <p align="center">Software Bill of Materials</p><a name="sbom"></a>
To generate an SBOM of the built environment:

1. Install [sbom](https://docs.docker.com/scout/how-tos/view-create-sboms/) plugin for Docker.

2. Use the following command to generate a human readable SBOM to the console (more instructions of usage can be found [here](https://docs.docker.com/scout/how-tos/view-create-sboms/)):
    ```console
    docker scout sbom --format list IMAGE_ID
    ```



