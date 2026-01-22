class LLMRunner:
    def __init__(self, client):
        self.client = client

    def generate(self, prompt: str) -> str:
        return self.client.generate(prompt)
