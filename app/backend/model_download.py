"""
Downloads a configured Hugging Face model and saves it into ./backend/models directory.
"""

import os
import traceback
from transformers import AutoModelForCausalLM, AutoTokenizer

def model_download(model_path="models/phi-3/", model_name="microsoft/Phi-3-mini-4k-instruct"):
    """
    Downloads a HF model and saves in to chosen path.
    
    Kwargs:
        model_path (str): Where to save the model.
        model_name (str): Name of the Hugging Face model. 
    """
    # Check if path exists
    if not os.path.exists(model_path):
        # Create the directory
        os.makedirs(model_path)
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True)

        # Save the model and tokenizer to the specified directory
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)

    except Exception:
        traceback.format_exc()



if __name__ == "__main__":
    model_download("models/phi-3/", "microsoft/Phi-3-mini-4k-instruct")
