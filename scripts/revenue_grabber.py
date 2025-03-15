import csv
import requests
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

API_BASE_URL = "http://www.omdbapi.com/?apikey=[key here]&" # TODO: use env file for key

def get_box_office(imdb_id):
    url = f"{API_BASE_URL}i={imdb_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("BoxOffice", "Not Available")
        except ValueError:
            return "Invalid JSON response"
    else:
        return "Error fetching data"

def process_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames = reader.fieldnames + ["boxOffice"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            writer.writeheader()

            for row in rows:
                imdb_id = row.get("fixedImdbId", "")
                print(f'Processing {imdb_id}')
                if imdb_id:
                    box_office = get_box_office(imdb_id).replace('$', '').replace(',', '')
                    row["boxOffice"] = box_office
                else:
                    row["boxOffice"] = "Error"

                writer.writerow(row)
                time.sleep(3)

input_file = 'input.csv'
output_file = 'output.csv'

process_csv(input_file, output_file)
