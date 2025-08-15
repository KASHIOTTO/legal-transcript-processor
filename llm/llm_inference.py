from transformers import AutoModelForCausalLm, AutoTokenizer

class LLMInference:
    def __init__(self, model_name='mistralai/mistral-7b-instruct-v0.1'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLm.from_pretrained(
            model_name, trust_remote_code=True
        )

    def extract_key_issues(self, transcript_text):
        prompt = (
            "Extract the key legal issues from the following transcripts:\n" + transcript_text + "\n\nIssues:"
        )
        inputs = self.tokenizer(prompt, return_tensors='pt', max_length=2048, truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
