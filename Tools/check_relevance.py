from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

def check_query_relevance(natural_language_query: str) -> tuple[bool, str]:

    prompt = (
    "You are a SQL expert and strict database schema verifier. "
    "The available database schema contains only the following tables:\n"
    " - order_items: order_item_id, order_id, product_id, quantity.\n"
    " - orders: order_id, order_date, customer_name.\n"
    " - products: product_id, product_name, price.\n\n"
    "A user has asked the following question:\n"
    f"{natural_language_query}\n\n"
    "Determine if this question can be answered using only the above database. "
    "Your response must be exactly one of the following and nothing else (no extra text, commentary, or explanation):\n"
    " - yes\n"
    " - pls ask the proper query, this data is not available\n\n"
    "Respond with the exact word only."
)
    
    model = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)
    messages = [HumanMessage(content=prompt)]
    response = model(messages)
    output = response.content.strip().lower()
    
    # Choose the first non-empty line as the cleaned output.
    cleaned_output = ""
    for line in output.splitlines():
        if line.strip():
            cleaned_output = line.strip()
            break

    if cleaned_output == "yes":
        return (True, "yes")
    elif cleaned_output == "pls ask the proper query, this data is not available":
        return (False, "pls ask the proper query, this data is not available")
    else:
        return (False, "pls ask the proper query, this data is not available")
