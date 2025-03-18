'''
Input & Output filters for the model.
'''
from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import Anonymize, PromptInjection, TokenLimit, InvisibleText, Secrets
from llm_guard.input_scanners import Language as LanguageIn
from llm_guard.output_scanners import Deanonymize, Sensitive
from llm_guard.output_scanners import Language as LanguageOut
from llm_guard.vault import Vault

vault  = Vault()

def input_filter(prompt: str, filters: list=['all']):
    '''
    Scans the given prompt with selected filters and returns filtered prompt. Each filter
    adds a 0.1 - 4 ms latency to the model's response time in production.

    Args:
        prompt (str): User prompt to scan.
    Kwargs:
        filters (Sequence[str]): List of filters to use. Available filters: "anonymize", 
        "token_limit", "prompt_injection", "language", "invisible_text", "secrets".
    Return:
        (dict): Dictionary with the following keys - filtered_prompt, results_valid, and results_score.
    '''
    if len(filters) > 20:
        raise ValueError('Too many items in `filters`.')
    # Initialize scanners to use.
    # Note: scanners are ran in the same order they are added to `scanners`.
    scanners = []
    if 'all' in filters:
        # Enforces a strict token limit on user prompts.
        scanners.append(TokenLimit(limit=500))
        # Redacts PII from user prompts (very experimental).
        #scanners.append(Anonymize(vault))
        # Secrets include API tokens, Private Keys, High Entropy Strings, etc.
        scanners.append(Secrets(redact_mode="REDACT_PARTIAL"))
        # Only accepts English prompts.
        scanners.append(LanguageIn(valid_languages=['en']))
        # Scans the user prompt for known Prompt Injections.
        scanners.append(PromptInjection(threshold=0.92))
        # Removes invisible Unicode characters.
        scanners.append(InvisibleText())
    elif 'token_limit' in filters:
        scanners.append(TokenLimit(limit=500))
    elif 'anonymize' in filters:
        scanners.append(Anonymize(vault))
    elif 'secrets' in filters:
        # Secrets include API tokens, Private Keys, High Entropy Strings, etc.
        scanners.append(Secrets(redact_mode="REDACT_PARTIAL"))
    elif 'language' in filters:
        # Only accepts English prompts.
        scanners.append(LanguageIn(valid_languages=['en']))
    elif 'prompt_injection' in filters:
        scanners.append(PromptInjection(threshold=0.92))
    elif 'invisible_text' in filters:
        # Removes invisible Unicode characters.
        scanners.append(InvisibleText())

    # Run scanners on the prompt and return results
    filtered_prompt, results_valid, results_score = scan_prompt(scanners, prompt)
    return {"filtered_prompt": filtered_prompt, "results_valid": results_valid,
            "results_score": results_score}


def output_filter(output: str, filtered_prompt: str, filters: list=['all']):
    '''
    Scans the given output with selected filters and returns filtered response. Each filter
    adds a 0.1 - 4 ms latency to the model's response time in production.
    
    Args:
        output (str):   Model output to filter.
        filtered_prompt (str): Filtered prompt used to generate model response.
    Kwargs:
        filters (list): List of filters to use. Available filters: "deanonymize",
                        "sensitive", "language".
    Return:
        (dict):   Dictionary containing: filtered_response, results_valid, and results_score.
    '''
    if len(filters) > 20:
        raise ValueError('Too many items in `filters`.')
    # Initialize scanners to use
    scanners = []
    if 'all'in filters:
        # Adds redacted PII back to model response if applicable.
        #scanners.append(Deanonymize(vault))
        scanners.append(Sensitive())
        # Only accepts responses in English
        scanners.append(LanguageOut(valid_languages=['en']))
    elif 'deanonymize' in filters:
        try: # Not tested what happens if Deanonymize() is used, but Anonymize() is not.
            scanners.append(Deanonymize(vault))
        except Exception:
            pass
    elif 'sensitive' in filters:
        scanners.append(Sensitive())
    elif 'language' in filters:
        # Only accepts responses in English
        scanners.append(LanguageOut(valid_languages=['en']))
    # Run all on scanners on the output and return results
    filtered_response, results_valid, results_score = scan_output(scanners, filtered_prompt, output)
    filtered_response = language_score_filter(results_score["language"], filtered_response)
    return {"filtered_response": filtered_response, "results_valid": results_valid,
            "results_score": results_score}


def language_score_filter(score, response, score_threshold=1.0):
    """
    If score is equal or higher than the score_threshold, returns
    a filtered response.
    """
    if score >= score_threshold:
        response = "Unfortunately, I started thinking in a foreign language and" \
        " I am not allowed to do that. Please rephrase your question or statement."
    return response
