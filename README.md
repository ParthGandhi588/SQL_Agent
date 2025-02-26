# SQL Agent 

This project implements a FastAPI application that uses an LLM-powered SQL agent to convert natural language queries into SQL statements and execute them against a PostgreSQL database.

## Features

- Natural language to SQL conversion using Groq LLM
- Query relevance checking based on available database schema
- SQL query verification
- PostgreSQL database integration
- REST API endpoint for processing queries

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Groq API key

## Project Structure

```
├── app.py                 # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (to be created)
├── Agent
│   └── agent.py           # Main SQL agent implementation
└── Tools
    ├── check_relevance.py # Checks if a query is relevant to the database schema
    ├── create_query.py    # Generates SQL from natural language
    ├── execute_query.py   # Executes SQL against PostgreSQL
    └── verify_query.py    # Verifies generated SQL is appropriate
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ParthGandhi588/SQL_Agent.git
   cd SQL_Agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root directory with the following variables:
   ```
   # PostgreSQL Configuration
   DBNAME=your_database_name
   USER=your_database_user
   PASSWORD=your_database_password
   HOST=localhost
   PORT=5432

   # Groq API Configuration
   GROQ_API_KEY=your_groq_api_key
   MODEL_NAME=llama-3.1-8b-instant  # or your preferred Groq model
   ```

## Database Setup

Ensure your PostgreSQL database has the following schema(This is just for Demo purpose):

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_name VARCHAR(255) NOT NULL
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL
);
```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

2. The API will be available at `http://localhost:8000`

## API Usage

### Query Endpoint

- **URL**: `/query`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "query": "What are the top 5 most expensive products?"
  }
  ```
- **Success Response**:
(This is demo output not the actual output)
  ```json
  {
    "sql_query": "SELECT product_name, price FROM products ORDER BY price DESC LIMIT 5",
    "results": [
      ["Premium Widget", 199.99],
      ["Deluxe Gadget", 149.99],
      ["Advanced Tool", 129.99],
      ["Professional Kit", 99.99],
      ["Standard Device", 79.99]
    ]
  }
  ```

## Error Handling

The API will return appropriate HTTP status codes for different errors:
- `500`: Internal server error (details provided in response)
- `400`: Bad request (when the query cannot be processed)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request
