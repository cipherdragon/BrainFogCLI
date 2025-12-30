import os
from config import Config
from database import init_db, SessionLocal
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from services import memory_service
from agents import RecallQueryAgent, RequestCategorizationAgent, MemAssistantAgent

def recall():
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

    request_categorization_agent = RequestCategorizationAgent(model=model)
    recall_agent = RecallQueryAgent(model=model)
    mem_assistant_agent = MemAssistantAgent(model=model)

    queries = [
        "What is the Wi-Fi password for guests?",
        "Where did I put the water shut-off valve in case of an emergency?",
        "When is the server maintenance scheduled?",
        "What kind of earrings does Sarah want for her birthday?",
        "What were my gym days again?"
    ]

    for query in queries:
        response = request_categorization_agent.invoke(query)
        print("Input: ", query)
        if response.category == "invalid":
            print(response.content)

        if response.category == "recall":
            recall_response = recall_agent.invoke(query)
            memories = memory_service.query_memory(
                session=session,
                query=recall_response.search_query
            )

            response = mem_assistant_agent.invoke(query, memories)
            print("Assistant Response: ", response)

        print()

if __name__ == "__main__":
    recall()