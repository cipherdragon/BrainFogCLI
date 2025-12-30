import os
from config import Config
from datetime import datetime
from database import init_db, SessionLocal
from langchain.chat_models import init_chat_model
from services import memory_service

from agents import (
    RecallQueryAgent, RequestCategorizationAgent,
    MemAssistantAgent, MemoryRefineAgent
)

def help_msg():
    return "Help"

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
    )

    init_db()
    session = SessionLocal()

    memory_refine_agent = MemoryRefineAgent(model=model)
    request_categorization_agent = RequestCategorizationAgent(model=model)
    recall_agent = RecallQueryAgent(model=model)
    mem_assistant_agent = MemAssistantAgent(model=model)

    while True:
        print()
        user_input = input(">>> ")
        user_input = user_input.strip()
        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            break
        
        if user_input.lower() == "help":
            print(help_msg())
            continue

        print()

        response = request_categorization_agent.invoke(user_input)
        if response.category == "invalid":
            print(response.content)
            continue
        elif response.category == "recall":
            recall_response = recall_agent.invoke(user_input)
            memories = memory_service.query_memory(
                session=session,
                query=recall_response.search_query
            )

            response = mem_assistant_agent.invoke(user_input, memories)
            print(response)
        elif response.category == "memorize":
            memory_response = memory_refine_agent.invoke(response.content)

            keywords = memory_response.keywords + \
                memory_response.nametags
            memory = memory_response.memory
            memory_service.create_memory(
                session=session,
                memory=memory,
                keywords=keywords,
                timestamp=datetime.now()
            )

            print("Memorized!")
        else:
            print("Hmmm... I am not sure how to respond to that.")

if __name__ == "__main__":
    main()