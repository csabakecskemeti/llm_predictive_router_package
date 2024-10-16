# LLM Predictive Router Package

This package allows you to route chat requests between small and large LLM models based on prompt classification. It dynamically selects the most suitable model depending on the complexity of the user input, ensuring optimal performance and maintaining conversation context.

## Installation

You can install the package using pip:

```bash
pip install llm-predictive-router
```

## Example Usage

```python
from llm_predictive_router import LLMRouter

# Define model configuration
config = {
    "classifier": {
        "model_id": "DevQuasar/roberta-prompt_classifier-v0.1"
    },
    # The entity name should match the predicted label from your prompt classifier
    "small_llm": {
        "escalation_order": 0,
        "url": "http://localhost:1234/v1",
        "api_key": "lm-studio",
        "model_id": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
        "max_ctx": 4096
    },
    # The entity name should match the predicted label from your prompt classifier
    "large_llm": {
        "escalation_order": 1,
        "url": "http://localhost:1234/v1",
        "api_key": "lm-studio",
        "model_id": "lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF/Meta-Llama-3-70B-Instruct-Q4_K_M.gguf",
        "max_ctx": 8192
    }
}

router = LLMRouter(config)

# Example call with simple prompt -> router to "small_llm"
response, context, selected_model = router.chat(
    "Hello", 
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=100,    # Limit the response length
    verbose=True
)

# Another simple prompt -> router to "small_llm"
response, context, selected_model = router.chat(
    "Tell me a story about a cat",
    curr_ctx=context,  # carry the chat history
    model_store_entry=selected_model,
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=512,    # Limit the response length
    verbose=True
)

# Default prompt classifier still considers this to a generic simple prompt -> router to "small_llm"
response, context, selected_model = router.chat(
    "Now explain the biology of the cat",
    curr_ctx=context,
    model_store_entry=selected_model,
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=512,    # Limit the response length
    verbose=True
)

# This will escalate the model -> router to "large_llm" as we are getting into specific domain details
response, context, selected_model = router.chat(
    "Get into the details of his metabolism, especially interested in the detailed role of the liver",
    curr_ctx=context,
    model_store_entry=selected_model,
    temperature=0.5,   # Lower temperature for more focused responses
    max_tokens=512,    # Limit the response length
    verbose=True
)
```

## Model Store JSON

The **model store** JSON defines the configuration of both the small and large LLM models that the router will switch between based on the prompt classification. Additionally, it includes a special **classifier** model entry used to predict the complexity of the user's prompt.

### Example Model Store Structure:

```json
{
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
```

### Explanation of Fields:

#### Classifier Entry:
- **classifier**: This special entry defines the model used to classify the complexity of the user's input. The `model_id` field specifies the model that is fine-tuned for prompt classification.
  - **model_id**: The identifier of the classifier model (e.g., Roberta-based classifier). This model predicts the complexity of the user prompt, allowing the router to choose the appropriate LLM for the response. It does not generate text but informs the routing logic.

#### LLM Entries:
- **escalation_order**: Defines the order in which models are escalated. Lower values are selected for less complex prompts, while higher values indicate more complex prompts.
- **url**: The URL of the API endpoint where the model is hosted.
- **api_key**: The API key required to authenticate with the model service.
- **model_id**: The specific model identifier (for example, from a model hub like Hugging Face or a local deployment).
- **max_ctx**: Maximum context size (in tokens) the model can handle.

---


## `router.chat` Method Documentation

### Overview

The `chat` method is responsible for handling user input, selecting the appropriate model based on the prompt classification, and managing the conversation context. It interacts with the model API to generate responses.

### Inputs

- **user_prompt** (`str`): The text prompt provided by the user for the model to respond to.
- **model_store_entry** (`dict`, optional): An entry from the model store representing the current model. If `None`, the function will classify the prompt and select the initial model.
- **curr_ctx** (`list`, optional): The current conversation context, a list of message objects between the user and the assistant.
- **system_prompt** (`str`, optional): A system prompt or directive that provides additional instructions for the model (default is an empty string).
- **temperature** (`float`, optional): Controls the randomness of the model’s output. A lower value (e.g., `0.1`) makes responses more deterministic, while a higher value (e.g., `0.9`) produces more random and creative outputs (default is `0.7`).
- **max_tokens** (`int`, optional): The maximum number of tokens to generate in the response (default: no explicit limit).
- **verbose** (`bool`, optional): If `True`, the function will print additional debugging information, such as the selected model and generated completion (default is `False`).

### Outputs

The method returns a tuple of three items:
1. **completion** (`str`): The text completion generated by the model.
2. **messages** (`list`): The updated conversation context, including the new user prompt and model response.
3. **model_store_entry** (`dict`): The model entry that was used for generating the response. This can be passed back into subsequent calls to ensure the same model is used unless escalation is needed.

### Example Usage

```python
# Start with a simple prompt
response, context, selected_model = router.chat(
    user_prompt="hello", 
    verbose=True
)

# Escalate to a more complex prompt
p = "Discuss the challenges and potential solutions for achieving sustainable development in the context of increasing global urbanization."
response, context, selected_model = router.chat(
    user_prompt=p, 
    curr_ctx=context, 
    model_store_entry=selected_model,
    temperature=0.5,
    max_tokens=200,
    verbose=True
)
```

---

## Solution Overview

The **llm-predictive-router** solution intelligently routes chat requests between models of different sizes based on the complexity of the prompt. By leveraging a pre-trained prompt classifier, the router can classify user inputs and escalate the model used for generating responses as needed.

Key components of the solution include:
- **Model Store**: Defines the configuration of multiple LLM models, including small and large variants.
- **Prompt Classifier**: A fine-tuned model (e.g., Roberta) that classifies user prompts to determine complexity.
- **Router**: Responsible for selecting and switching between models dynamically, depending on the classification result and current context.
- **Chat Handling**: Manages the conversation, tracks context, and interacts with the models to generate coherent responses.

This approach provides a balanced trade-off between model performance and response quality, allowing for optimal resource usage while maintaining high-quality conversational outputs.
