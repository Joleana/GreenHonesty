import csv
from bs4 import BeautifulSoup
import openai

# OpenAI API key initialization
openai.api_key = "YOUR_OPENAI_API_KEY"

def clean_data(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def classify_claim(claim):
    response = openai.Completion.create(
      model="gpt-4.0-turbo",
      prompt=f"Classify the following claim as environmental (E), social (S), or governance (G): \"{claim}\".",
      max_tokens=10
    )
    return response.choices[0].text.strip()

def calculate_honesty_score(claim):
    response = openai.Completion.create(
      model="gpt-4.0-turbo",
      prompt=f"Rate the honesty of the following claim from 1 to 10, based on established criteria: \"{claim}\".",
      max_tokens=10
    )
    return int(response.choices[0].text.strip())

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        data = [row for row in reader]

    # Clean and process data
    for row in data:
        row['clean_data'] = clean_data(row['raw_data'])
        row['classification'] = classify_claim(row['clean_data'])
        row['honesty_score'] = calculate_honesty_score(row['clean_data'])

    # Write the processed data back to a new CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['company', 'raw_data', 'clean_data', 'classification', 'honesty_score']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    openai.api_key = input("Enter your API KEY: ")
    input_csv = input("Enter the path to your input CSV: ")
    output_csv = input("Enter the path to your output CSV: ")
    process_csv(input_csv, output_csv)
