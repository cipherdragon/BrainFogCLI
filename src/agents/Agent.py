from langchain.agents import create_agent

class Agent:
    def __init__(self, model, system_prompt, response_format):
        self.agent = create_agent(
            model=model,
            system_prompt=system_prompt,
            response_format=response_format
        )
    
    def get_agent(self):
        return self.agent