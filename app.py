from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.agent import SQLAgent
import os
from dotenv import load_dotenv

load_dotenv()

DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# Configure your PostgreSQL database connection details.
db_config = {
    "dbname": DBNAME,
    "user": USER,
    "password": PASSWORD,
    "host": HOST,
    "port": PORT
}

# Create an instance of SQLAgent. This will load the model and be reused for each request.
agent = SQLAgent(db_config)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def process_query(request: QueryRequest):
    natural_language_query = request.query
    try:
        sql_query, results = agent.run(natural_language_query)
        return {
            "sql_query": sql_query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
