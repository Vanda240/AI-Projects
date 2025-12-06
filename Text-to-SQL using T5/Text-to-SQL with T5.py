import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sqlparse

# Load the model and tokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSeq2SeqLM.from_pretrained("./fine_tuned_t5").to(device)
tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_t5")

# Function to translate natural language to SQL
def translate_to_sql(english_query):
    input_text = f"translate English to SQL: {english_query}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    outputs = model.generate(input_ids, max_new_tokens=100, do_sample=False)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql_query

# Function to explain SQL queries in plain English
def explain_sql(query):
    sql_to_plain = {
        "SELECT": "Retrieve",
        "FROM": "from the table",
        "WHERE": "where the condition is met",
        "AND": "and also",
        "OR": "or",
        "GROUP BY": "grouped by",
        "ORDER BY": "ordered by",
        "LIMIT": "limited to",
        "JOIN": "join with the table",
        "INNER JOIN": "join where both tables have matching values",
        "LEFT JOIN": "include all rows from the left table and matching rows from the right table",
        "RIGHT JOIN": "include all rows from the right table and matching rows from the left table",
        "FULL JOIN": "include all rows from both tables",
        "ON": "on the condition",
        "HAVING": "filter grouped results where",
        "DISTINCT": "only unique values of",
        "AS": "aliased as",
        "UNION": "combine results with",
        "EXCEPT": "exclude results that appear in",
        "INTERSECT": "find results common to",
        "CASE": "when a condition is met, return",
        "WHEN": "when the condition is",
        "THEN": "then return",
        "ELSE": "otherwise return",
        "END": "end the conditional expression",
        "LIKE": "matches the pattern",
        "IN": "is in the list of values",
        "NOT": "is not",
        "IS NULL": "has no value",
        "IS NOT NULL": "has a value",
        "COUNT": "count the number of",
        "SUM": "sum the values of",
        "AVG": "find the average of",
        "MIN": "find the minimum value of",
        "MAX": "find the maximum value of"
    }
    tokens = sqlparse.parse(query)[0].tokens
    explanation = []
    for token in tokens:
        explanation.append(sql_to_plain.get(token.value.upper(), token.value))
    return " ".join(explanation)

# Function to generate query suggestions
def generate_suggestions(query_info):
    suggestions = [
        "Do you want to filter by another column?",
        "Would you like to group the data by a column (e.g., department)?",
        "Do you want to sort the data in ascending or descending order?",
        "Would you like to add a condition (e.g., WHERE clause)?",
        "Do you want to include only distinct values?",
        "Would you like to join another table to fetch more details?",
        "Do you want to calculate aggregates like COUNT, SUM, or AVG?",
        "Would you like to add a LIMIT to restrict the number of rows returned?",
        "Do you want to exclude certain rows (e.g., using NOT or EXCEPT)?",
        "Would you like to add a CASE statement for conditional logic?",
        "Do you need results grouped by multiple columns?",
        "Would you like to add an ORDER BY clause with multiple columns?",
        "Do you want to use a pattern match (e.g., LIKE '%value%')?"
    ]
    return suggestions

# Extract columns or other info from SQL queries
def extract_query_info(sql_query):
    columns = []
    if "SELECT" in sql_query:
        columns = sql_query.split("FROM")[0].replace("SELECT", "").strip().split(",")
    return {"columns": columns}

# Main interactive function
def interactive_cli():
    print("Welcome to the Text-to-SQL CLI!")
    print("You can translate natural language to SQL, explain SQL queries, and get suggestions.")
    print("Type 'exit' to quit.\n")
    
    while True:
        print("Options:")
        print("1. Translate English to SQL")
        print("2. Explain an SQL Query")
        print("3. Generate Query Suggestions")
        choice = input("\nEnter your choice (1/2/3 or 'exit' to quit): ").strip()
        
        if choice == "exit":
            print("Exiting... Goodbye!")
            break
        
        if choice == "1":
            english_query = input("\nEnter your English query: ").strip()
            sql_query = translate_to_sql(english_query)
            print(f"\nGenerated SQL Query: {sql_query}\n")
        
        elif choice == "2":
            sql_query = input("\nEnter your SQL query: ").strip()
            explanation = explain_sql(sql_query)
            print(f"\nExplanation: {explanation}\n")
        
        elif choice == "3":
            sql_query = input("\nEnter your SQL query: ").strip()
            query_info = extract_query_info(sql_query)
            suggestions = generate_suggestions(query_info)
            print("\nSuggestions:")
            for suggestion in suggestions:
                print(f"- {suggestion}")
            print()
        
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    interactive_cli()
