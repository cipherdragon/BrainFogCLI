from .Agent import Agent

from datetime import datetime
from langchain.messages import HumanMessage
from prompts import MemAssistantPrompt
from models.db import Memory

class MemAssistantAgent(Agent):
    def __init__(self, model):
        prompt = MemAssistantPrompt().get_prompt()
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=None
        )

    def invoke(self, query: str, memories: list[Memory]) -> str:
        memories_str = [f"{memory.timestamp:%Y-%m-%d %I:%M:%p} - {memory.memory}"
                        for memory in memories]
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M%p")
        prompt = f"Current Date/Time: {current_time}\nUser Query: {query}\nRetrieved Memories:\n---\n{'\n'.join(memories_str)}"
        response = self.agent.invoke({"messages": [HumanMessage(content=prompt)]})
        return response["messages"][-1].content