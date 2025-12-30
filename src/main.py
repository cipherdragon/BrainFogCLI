import os
from config import Config
from database import init_db, SessionLocal
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from services import memory_service
from agents import RecallQueryAgent, RequestCategorizationAgent, MemAssistantAgent

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

    request_categorization_agent = RequestCategorizationAgent(model=model).get_agent()
    recall_agent = RecallQueryAgent(model=model).get_agent()
    mem_assistant_agent = MemAssistantAgent(model=model).get_agent()

    print("Not implemented yet")

if __name__ == "__main__":
    main()