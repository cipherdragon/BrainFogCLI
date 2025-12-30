from .Agent import Agent

from langchain.messages import HumanMessage
from prompts import MemAssistantPrompt

class MemAssistantAgent(Agent):
    def __init__(self, model):
        prompt = MemAssistantPrompt().get_prompt()
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=None
        )

    def invoke(self, query: str, memories: list[str]) -> str:
        prompt = f"User Query: {query}\nRetrieved Memories:\n---\n{'\n'.join(memories)}"
        response = self.agent.invoke({"messages": [HumanMessage(content=prompt)]})
        return response["messages"][-1].content