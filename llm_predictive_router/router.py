# router.py
from openai import OpenAI
from transformers import RobertaTokenizerFast, pipeline

class LLMRouter:
    def __init__(self, config):
        self.model_store = config
        self.tokenizer = RobertaTokenizerFast.from_pretrained(config['classifier']['model_id'])
        self.sentence_classifier = pipeline(
            "sentiment-analysis", 
            model=config['classifier']['model_id'], 
            tokenizer=self.tokenizer
        )

    def prompt_classifier(self, user_prompt):
        return self.sentence_classifier(user_prompt)[0]['label']

    def route(self, user_prompt):
        return self.model_store[self.prompt_classifier(user_prompt)]

    def chat(self, user_prompt, model_store_entry=None, curr_ctx=[], system_prompt=' ', verbose=False):
        if model_store_entry is None and not curr_ctx:
            model_store_entry = self.route(user_prompt)
            if verbose:
                print(f'Classified prompt - selected model: {model_store_entry["model_id"]}')
        else:
            model_store_candidate = self.route(user_prompt)
            if model_store_candidate["escalation_order"] > model_store_entry["escalation_order"]:
                model_store_entry = model_store_candidate
                if verbose:
                    print(f'Escalated model - selected model: {model_store_entry["model_id"]}')

        client = OpenAI(base_url=model_store_entry['url'], api_key=model_store_entry['api_key'])
        messages = curr_ctx + [{"role": "user", "content": user_prompt}]

        completion = client.chat.completions.create(
            model=model_store_entry['model_id'],
            messages=messages,
            temperature=0.7
        )
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})

        if verbose:
            print(f'Used model: {model_store_entry["model_id"]}')
            print(f'Completion: {completion}')

        client.close()
        return completion.choices[0].message.content, messages, model_store_entry

