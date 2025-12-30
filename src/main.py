import os
from config import Config
from datetime import datetime
from database import init_db, SessionLocal
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from services import memory_service
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
    )

    init_db()
    session = SessionLocal()

    request_categorization_agent = RequestCategorizationAgent(model=model).get_agent()
    memory_refine_agent = MemoryRefineAgent(model=model).get_agent()
    recall_agent = RecallQueryAgent(model=model).get_agent()

    prompts = [
        "Remember that my favorite color is blue.",
        "What's the difference between a qubit and a qudit?",
        "Tell me a joke about programmers.",
        "Store the fact that the capital of France is Paris.",
        "Angela's birthday is on July 15th.",
        "Greg should send me Q4 report by evening."
    ]

    queries = [
        "What's the difference between a qubit and a qudit?",
        "When is Angela's birthday?",
        "How much I spent yesterday?",
        "What's the capital of France?",
        "Who is the CEO of Tesla?"
    ]

    for prompt in prompts:
        message = HumanMessage(content=prompt)
        response = request_categorization_agent.invoke({"messages": [message]})
        print("Input: ", prompt)
        print("Category: ", response["structured_response"].category)
        if response["structured_response"].category == "invalid":
            print(response["structured_response"].content)

        if response["structured_response"].category == "memorize":
            memory_response = memory_refine_agent.invoke({"messages": [message]})
            print("Nametags: ", memory_response["structured_response"].nametags)
            print("Keywords: ", memory_response["structured_response"].keywords)

            keywords = memory_response["structured_response"].keywords + \
                memory_response["structured_response"].nametags
            memory = memory_response["structured_response"].memory
            memory_service.create_memory(
                session=session,
                memory=memory,
                keywords=keywords,
                timestamp=datetime.now()
            )
        
        print()
    
    print("---- RECALL QUERIES ----")
    print()

    for query in queries:
        message = HumanMessage(content=query)
        response = request_categorization_agent.invoke({"messages": [message]})
        print("Input: ", query)
        print("Category: ", response["structured_response"].category)
        if response["structured_response"].category == "invalid":
            print(response["structured_response"].content)

        if response["structured_response"].category == "recall":
            recall_response = recall_agent.invoke({"messages": [message]})
            print("Search Query: ", recall_response["structured_response"].search_query)
            print("Nametag: ", recall_response["structured_response"].nametag_filters)
        
        print()

if __name__ == "__main__":
    main()