import os

import requests

TOGETHER_KEY = os.getenv("TOGETHER_KEY")

def set_api_key(key: str):
    TOGETHER_KEY=key

class Two():
    def __init__(self, model_name: str = "NousResearch/Nous-Capybara-7B-V1p9", api_key: str = None):
        self.model_name = model_name
        if api_key is None:
            api_key = TOGETHER_KEY
        self.api_key = api_key
    def prompt(prompt: str):
        return "USER: \n" + prompt + "\nASSISTANT:"        
    def __call__(self, prompt):
        hdr = {
            "Authorization": f"Bearer {self.api_key}"
        }
        jsn = {
            "model": self.model_name,
            "prompt": prompt,
            "top_p": 0.75,
            "top_k": 42,
            "max_tokens": 8192-len(prompt)
        }
        res = requests.post("https://api.together.xyz/v1/chat/completions", headers=hdr, json=jsn)
        return res.json()
    
if __name__ == "__main__":
    two = Two(api_key=os.getenv("TOGETHER_KEY"))
    print(two("Say hello, to me, bot. My name is Sam."))
        
        