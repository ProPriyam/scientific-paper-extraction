import random
import json
import dotenv
import os
import requests

dotenv.load_dotenv()

def save_random_lines(input_file_path, output_file_path, num_lines=100):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        # Filter lines for those that are in the selected category - (econonmics in this case)
        econ_lines = [line for line in lines if '"categories":' in line and ('"econ' in line or '"q-fin' in line)]

        if len(econ_lines) < num_lines:
            print(f"The file contains only {len(econ_lines)} economics lines, which is less than the requested {num_lines} lines.")
            selected_lines = econ_lines
        else:
            selected_lines = random.sample(econ_lines, num_lines)

        # Convert selected lines to JSON
        json_objects = [json.loads(line) for line in selected_lines]

        with open(output_file_path, 'w') as output_file:
            json.dump(json_objects, output_file, indent=4)

        print(f"Random {num_lines} economics lines saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Save usage
input_file_path = os.getenv("path_arxiv")
output_file_path = 'data/random100_econ.json'
save_random_lines(input_file_path, output_file_path, num_lines=100)

# Open the file and read its contents
with open("data/random100_econ.json", "r") as file:
    data = json.load(file)

# Extract 'id' field from each entry and store in a list
id_list = [entry['id'] for entry in data]

# Create a new directory to store PDFs
output_dir = "data/pdfs"
os.makedirs(output_dir, exist_ok=True)

# Base URL for downloading PDFs
base_url = "https://www.arxiv.org/pdf/"

# Loop through each ID and download the PDF
for paper_id in id_list:
    pdf_url = f"{base_url}{paper_id}"
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        pdf_path = os.path.join(output_dir, f"{paper_id.replace('/', '_')}.pdf")
        with open(pdf_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {pdf_path}")
    else:
        print(f"Failed to download: {pdf_url}")

print("All downloads completed.")