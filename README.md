# Secure Deployment of Large Language Models
Contains the codebase for Mikko Lempinen's Master's Thesis titled "Secure Deployment of Large Language Models"

## Deployment via Docker

## Direct deployment
The application can be deployed directly without sandboxing it with Docker. Direct deployment was done with Ubuntu 24.04 and Python 3.12.3.

In the repository root directory, create and activate a Python virtual environment:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
### Frontend deployment
1. Install frontend dependencies with npm:
   - `cd app/frontend`
   - `npm install`
   - `npm install -g serve`
2. Inside the `frontend` directory, you can now build and serve the React frontend with:
   - npm run build
   - serve -s build -l 3006
### Backend deployment
1. Install backend dependencies:
   - `pip install -r app/backend/requirements.txt`
2. Download the Hugging Face Language Model:
   `cd app/backend`
   `python download_model.py`
3. Inside the `backend` directory, you can now start the LLM-application with
   - `python app.py`

## Requirements

### For LLM (Backend)
1. **Python 3.9+** (Required for Python, PyTorch, and LLM Transformers)
2. Install the necessary dependencies using pip:
    ```bash
    pip install fastapi uvicorn transformers
    ```

3. Install the correct version of **PyTorch** for your environment. Visit the official PyTorch website for installation instructions:
    - [PyTorch Installation](https://pytorch.org/get-started/locally/)

---

### For Frontend
1. Install **requests** and **certifi**:
    ```bash
    pip install requests certifi
    ```

2. Install **axios** for HTTP requests in the frontend:
    ```bash
    npm install axios
    ```

---

## Running the LLM and HTTPS Server/API

1. Navigate to `./ProductionReadyChatbot` in your terminal.

2. Run the LLM and the HTTPS server/API by executing:
    ```bash
    python llm.py
    ```
    Or:
    ```bash
    python3 llm.py
    ```

---

## Running the ChatBot Frontend

1. Navigate to `./ProductionReadyChatbot/chat-frontend` in your terminal.

2. Run the frontend application:
    ```bash
    npm start
    ```

3. If the app doesn't open in the browser automatically, go to [http://localhost:3000/](http://localhost:3000/).

4. If NPM packages are missing, install them by running:
    ```bash
    npm install
    ```

---

## Running the Terminal ChatBot

1. Navigate to `./ProductionReadyChatbot` in your terminal.

2. Run the terminal-based chatbot:
    ```bash
    python ChatBot.py
    ```

---

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
