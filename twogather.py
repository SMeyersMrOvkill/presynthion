import os

import requests

class Two():
    def __init__(self, model_name: str =  "teknium/OpenHermes-2p5-Mistral-7B", api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key
    def prompt(self, prompt: str):
        return "<|im_start|>system\nYou are a verbally descriptive but otherwise silent SVG/JSON to English text description engine. You only care about positions and sizes. \n <|im_end|> \n <|im_start|>user \n " + prompt + " <|im_end|> \n <|im_start|>assistant"        
    def __call__(self, prompt):
        hdr = {
            "Authorization": f"Bearer {self.api_key}"
        }
        pr= prompt
        jsn = {
            "model": self.model_name,
            "prompt": pr,
            "temperature": 0.7,
            "top_p": 0.80,
            "top_k": 42,
            "max_tokens": 8192-len(prompt),
        }
        res = requests.post("https://api.together.xyz/v1/chat/completions", headers=hdr, json=jsn)
        return res.json(), prompt
    
if __name__ == "__main__":
    two = Two(api_key=os.getenv("TOGETHER_KEY"))
    print(two("Say hello, to me, bot. My name is Sam."))
        
        