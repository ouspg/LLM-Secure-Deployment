'''
Backend for LLM-application with PyTorch & FastAPI.
'''
import traceback
import time
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from model_download import model_download
import model_filters

app = fastapi.FastAPI()

# The Backend only allows communications from these origins.
origins = ["https://localhost", "https://86.50.253.176"]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"], # Not tested what specific headers are needed - should be restriced to only those.
)

max_memory_mapping = {0: "10GIB"} # GPU memory allocation optimization - optimized value(s) depend on your hardware.

print("Loading PHI-3 Mini model...")
try: # Does this throw some exception if model is not in "models/phi3" or can transformers handle it?
    model = AutoModelForCausalLM.from_pretrained("models/phi-3/", max_memory=max_memory_mapping)
    tokenizer = AutoTokenizer.from_pretrained("models/phi-3/", max_memory=max_memory_mapping)
except Exception:
    traceback.format_exc()
    model_download("models/phi-3/", "microsoft/Phi-3-mini-4k-instruct")
    model = AutoModelForCausalLM.from_pretrained("models/phi-3/", max_memory=max_memory_mapping)
    tokenizer = AutoTokenizer.from_pretrained("models/phi-3/", max_memory=max_memory_mapping)

# Initialize a text gen pipeline
pipe = pipeline(
    "text-generation", 
    model=model,
    tokenizer=tokenizer,
    device=0 # Cuda device ordinal, -1 for CPU
)

generation_args = {
    "max_new_tokens": 500, # Maximum number of tokens to generate.
    "return_full_text": False, 
    "do_sample": False, 
}


# POST path
@app.post('/chat')
async def chat(request: fastapi.Request):
    '''
    Generates and returns a response to user's prompt.
    '''
    body = await request.json()
    user_input = body.get("input", "")

    if not user_input:
        return {"error": "No input provided."}

    # Scan & filter the user's prompt
    filtered_prompt = model_filters.input_filter(user_input)
    user_input = filtered_prompt["filtered_prompt"]
    # Print filtered_results to console
    print("---------------------------------------")
    print(f"FILTERED PROMPT:\n")
    for key in filtered_prompt.keys():
        print(f"{key}: {filtered_prompt[key]}")
    print("---------------------------------------")


    generation_start_time = time.time()
    # Generate a model response
    message = [{"role": "user", "content": user_input}]
    output = pipe(message, **generation_args)
    generation_end_time = time.time()

    # Scan & filter the model's response
    filtered_response = model_filters.output_filter(output[0]["generated_text"], user_input)
    # Print filtered_response to console
    print("---------------------------------------")
    print(f"FILTERED RESPONSE:\n")
    for key in filtered_response.keys():
        print(f"{key}: {filtered_response[key]}")
    print("---------------------------------------")

    generation_elapsed_time = generation_end_time - generation_start_time

    return {
        "response": filtered_response["filtered_response"],
        "time_taken": generation_elapsed_time,
    }


#Server will start when the script is executed
if __name__ == "__main__":
    print("Starting a HTTPS server...")

    # Uvicorn server settings
    uvicorn.run(app,
                host="0.0.0.0",
                port=8000,
                ssl_certfile="cert.pem",  # SSL Certificate
                ssl_keyfile="key.pem",    # SSL Certificate Key
    )
