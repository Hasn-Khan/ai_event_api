from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
import openai

app = Flask(__name__)
engine = create_engine('postgresql://user:password@localhost:5432/mydatabase')

openai.api_key = ENV['OPENAI_API_KEY']

@app.route('/api/query', methods=['POST'])
def query():
    user_query = request.json.get('query')

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Parse the following query: {user_query}",
        max_tokens=100
    )
    parsed_query = response.choices[0].text.strip()

    sql_query = construct_sql(parsed_query)

    with engine.connect() as connection:
        result = connection.execute(text(sql_query))
        data = [dict(row) for row in result]
    
    return jsonify(data)

def construct_sql(parsed_query):
    return f"SELECT * FROM merged_data WHERE event_industry = '{parsed_query}'"

if __name__ == '__main__':
    app.run(debug=True)
