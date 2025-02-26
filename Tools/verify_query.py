from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

def verify_query(natural_language_query: str, sql_query: str) -> bool:

    # Construct a prompt for verification.
    prompt = (
        "You are a SQL expert. A user asked the following question:\n\n"
        f"{natural_language_query}\n\n"
        "The following SQL query was generated to answer the question:\n\n"
        f"{sql_query}\n\n"
        "Is this SQL query correct and appropriate for answering the user's question? "
        "Answer 'yes' if it is correct, or 'no' if it is not.Strictly answer 'yes' or 'no'."
    )
    
    model = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)
    messages = [HumanMessage(content=prompt)]
    response = model(messages)
    output = response.content.strip().lower()
    
    # Take the first non-empty line
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
        return (False, "no")
