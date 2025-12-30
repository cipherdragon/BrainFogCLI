import os
from config import Config
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

from agents import MemoryRefineAgent, RecallQueryAgent, RequestCategorizationAgent

def main():
    config = Config()
    if not os.environ.get("OPENAI_API_KEY"):
        if config.OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY is not set in environment variables or config file.")
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

    model = init_chat_model(
        model="gpt-3.5-turbo",
        temperature=0.0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # structured_output=True
    )

    request_categorization_agent = RequestCategorizationAgent(model=model).get_agent()
    memory_refine_agent = MemoryRefineAgent(model=model).get_agent()
    recall_agent = RecallQueryAgent(model=model).get_agent()

    prompts = [
        "Remember that my favorite color is blue.",
    ]

    queries = [

    ]

    for prompt in prompts:
        message = HumanMessage(content=prompt)
        response = request_categorization_agent.invoke({"messages": [message]})
        print("Request Categorization Response:", response["structured_response"].category)

        if response["structured_response"].category == "memorize":
            memory_response = memory_refine_agent.invoke({"messages": [message]})
            print("Memory Refine Response:", memory_response["structured_response"])

if __name__ == "__main__":
    main()