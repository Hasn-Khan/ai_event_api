# ai_event_api

## Data Processing Steps
1. Loaded CSV files.
2. Merged datasets using `event_url` and `homepage_base_url`.
3. Standardized columns and enriched data using an LLM.

## Main Functionalities
- Parse user queries in natural language.
- Construct and execute SQL queries.
- Return results based on the query.

## Challenges
- Parsing complex natural language queries.
- Constructing accurate SQL queries from parsed attributes.

## Future Improvements
- Enhance LLM parsing accuracy.
- Optimize SQL query construction for complex queries.
