import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI

client = OpenAI(ENV['OPENAI_API_KEY'])

events_df = pd.read_csv('files/event_info.csv')
companies_df = pd.read_csv('files/company_info.csv')
people_df = pd.read_csv('files/people_info.csv')

events_companies_df = events_df.merge(companies_df, on='event_url')
merged_df = events_companies_df.merge(people_df, on='homepage_base_url')

def tag_event_industry(event_name):
    response = client.completions.create(engine="text-davinci-003",
    prompt=f"Tag the following event with an industry: {event_name}",
    max_tokens=10)
    return response.choices[0].text.strip()

merged_df['event_industry'] = merged_df['event_name'].apply(tag_event_industry)

def generate_email(person_name, homepage_base_url):
    first_name, last_name = person_name.split()[:2]
    return f"{first_name.lower()}.{last_name.lower()}@{homepage_base_url}"

merged_df['email'] = merged_df.apply(lambda row: generate_email(row['person_name'], row['homepage_base_url']), axis=1)

engine = create_engine('postgresql://user:password@localhost:5432/ai_event')

merged_df.to_sql('merged_data', engine, if_exists='replace', index=False)
