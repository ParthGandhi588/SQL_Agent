from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

def create_query(natural_language_query: str) -> str:

    # Construct a prompt for generating a SQL query.
    prompt = (
    "Generate exactly one properly formatted SQL query with no additional commentary or explanation using the following database schema:\n"
    " - order_items: order_item_id, order_id, product_id, quantity.\n"
    " - orders: order_id, order_date, customer_name.\n"
    " - products: product_id, product_name, price.\n\n"
    "Ensure your SQL query does not include any backticks (`), single quotes ('), or double quotes (\") for string literals or identifiers. "
    "Return only the SQL query with no extra text.\n\n"
    "Make the query as easy and simple as possible. Avoid using joins frequently; only use joins when it is absolutely necessary to retrieve the required data.\n\n"
    f"{natural_language_query}\n\nSQL Query:"
    )

    
    model = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)
    messages = [HumanMessage(content=prompt)]
    response = model(messages)
    generated_query = response.content.strip()
    return generated_query
