# LLM Predictive Router Package

This package allows you to route chat requests between small and large LLM models based on prompt classification.

## Installation

You can install the package using pip:

```bash
pip install llm-predictive-router
```

## Example usage

```python
# Example Usage
from llm_predictive_router import LLMRouter

# Define model configuration
config = {
    "classifier": {
        "model_id": "DevQuasar/roberta-prompt_classifier-v0.1"
    },
    "small_llm": {
        "escalation_order": 0,
        "url": "http://localhost:1234/v1",
        "api_key": "lm-studio",
        "model_id": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
        "max_ctx": 4096
    },
    "large_llm": {
        "escalation_order": 1,
        "url": "http://localhost:1234/v1",
        "api_key": "lm-studio",
        "model_id": "lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF/Meta-Llama-3-70B-Instruct-Q4_K_M.gguf",
        "max_ctx": 8192
    }
}

router = LLMRouter(config)

# Example call with customized temperature and max_tokens
response, context, selected_model = router.chat(
    "Hello", 
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=100,    # Limit the response length
    verbose=True
)

response, context, selected_model = router.chat(
    "Tell me a story about a cat",
    curr_ctx=context,
    model_store_entry=selected_model,
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=512,    # Limit the response length
    verbose=True
)

response, context, selected_model = router.chat(
    "Now explain the biology of the cat",
    curr_ctx=context,
    model_store_entry=selected_model,
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=512,    # Limit the response length
    verbose=True
)

# this will escalate the model as we getting into specific domain details
response, context, selected_model = router.chat(
    "Get into the details of his matabolism, especially interested the detailed role of the liver",
    curr_ctx=context,
    model_store_entry=selected_model,
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=512,    # Limit the response length
    verbose=True
)
```
