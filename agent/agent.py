from typing import Tuple, Any
from Tools.create_query import create_query
from Tools.verify_query import verify_query
from Tools.execute_query import execute_query
from Tools.check_relevance import check_query_relevance

class SQLAgent:
    def __init__(self, db_config: dict):

        self.db_config = db_config

    def run(self, natural_language_query: str) -> Tuple[str, Any]:

        # First, check if the query is related to the available database.
        print("Checking the question is relevant or not...")
        relevant, relevance_message = check_query_relevance(natural_language_query)
        if not relevant:
            print("The user's question is not answerable using the available database.")
            return relevance_message
        
        # The query is related; proceed with generating and verifying the SQL query.
        max_iterations = 5
        sql_query = None

        for iteration in range(1, max_iterations + 1):
            print(f"\nIteration {iteration} of {max_iterations}: Generating query...")
            sql_query = create_query(natural_language_query)
            print("Generated SQL Query:")
            print(sql_query)
            valid= verify_query(natural_language_query, sql_query)
            if valid:
                print("Query verification succeeded.")
                break
            else:
                print("Query verification failed. Retrying...")
        else:
            raise Exception("Failed to generate a correct SQL query after 5 attempts.")

        print("Executing the verified query on the database...")
        results = execute_query(sql_query, self.db_config)
        return sql_query, results