from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

from huggingface_hub import login

login(token=api_token)
print("loggedIn ...")


class LLM:
    def __init__(self, model, tokenizer):
        self.tokenizer = tokenizer
        self.model = model

    @classmethod
    def load_model(cls):
        tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
        model = AutoModelForSeq2SeqLM.from_pretrained(
            "facebook/blenderbot-400M-distill"
        )
        return cls(model, tokenizer)

    def generate_response(self, input_text):
        input = self.tokenizer(input_text, return_tensors="pt")
        outputs = self.model.generate(
            input["input_ids"],
            temperature=0.8,
        )
        logging.info("Output...")
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_output
