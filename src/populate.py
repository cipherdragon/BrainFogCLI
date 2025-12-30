import os
from config import Config
from datetime import datetime
from database import init_db, SessionLocal
from langchain.chat_models import init_chat_model
from services import memory_service
from agents import MemoryRefineAgent, RequestCategorizationAgent

def populate():
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
    memory_refine_agent = MemoryRefineAgent(model=model)

    prompts = [
        "I prefer my coffee black with no sugar.",
        "The 'Project Phoenix' launch date is set for October 12th.",
        "My sister's dog, Cooper, is a Golden Retriever.",
        "I'm allergic to shellfish and cashews.",
        "The guest Wi-Fi password is 'MountainView2024'.",
        "Mark's favorite wine is a dry Cabernet Sauvignon.",
        "I need to pay the property tax by the end of November.",
        "The office alarm code is 5582 followed by the hash key.",
        "I am currently reading 'Project Hail Mary' by Andy Weir.",
        "My car's last oil change was at 45,000 miles.",
        "Sarah mentioned she wants minimalist gold earrings for her birthday.",
        "The server maintenance window is every Sunday at 2 AM EST.",
        "I usually go to the gym on Mondays, Wednesdays, and Fridays.",
        "My library card number ends in 9931.",
        "The garden hose is stored in the shed behind the lawnmower.",
        "I'm learning the Actix-web framework for my new Rust project.",
        "The blue folder in the cabinet contains the house deed.",
        "My blood type is A-positive.",
        "Last night's dinner at 'The Blue Oyster' was excellent.",
        "The emergency shut-off valve for the water is in the basement crawlspace."
    ]

    for prompt in prompts:
        response = request_categorization_agent.invoke(prompt)
        print("Input: ", prompt)
        print("Category: ", response.category)
        if response.category == "invalid":
            print(response.content)

        if response.category == "memorize":
            memory_response = memory_refine_agent.invoke(prompt)
            print("Nametags: ", memory_response.nametags)
            print("Keywords: ", memory_response.keywords)

            keywords = memory_response.keywords + \
                memory_response.nametags
            memory = memory_response.memory
            memory_service.create_memory(
                session=session,
                memory=memory,
                keywords=keywords,
                timestamp=datetime.now()
            )
        
        print()

if __name__ == "__main__":
    populate()