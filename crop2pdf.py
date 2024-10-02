import fitz  # PyMuPDF
import json
import os

# Folder paths for JSONs and PDFs
json_folder = 'data/stats_extraction/'  
pdf_folder = 'data/modified_pdfs/' 

# Create a directory for output PDFs and captions
output_folder = 'data/cropped_pdfs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all JSON and PDF files
json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Function to match the correct PDF for each JSON based on file names
def find_matching_pdf(json_filename, pdf_files):
    for pdf_file in pdf_files:
        if pdf_file.replace('.pdf', '') in json_filename:
            return os.path.join(pdf_folder, pdf_file), pdf_file.replace('.pdf', '')
    return None, None

# Iterate through each JSON file
for json_file in json_files:
    json_file_path = os.path.join(json_folder, json_file)
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    matching_pdf_path, pdf_id = find_matching_pdf(json_file, pdf_files)
    
    if matching_pdf_path is None:
        print(f"No matching PDF found for {json_file}")
        continue
    
    pdf_document = fitz.open(matching_pdf_path)
    
    # Iterate through each item in the JSON
    for item in data:
        caption = item['caption']
        page_num = item['page']
        region = item['regionBoundary']
        name = item['name'] 

        # Load the specified page
        page = pdf_document.load_page(page_num)

        # Convert the coordinates from points to fit the page's coordinate system
        crop_rect = fitz.Rect(region['x1'], region['y1'], region['x2'], region['y2'])
        # Crop the page to the defined region
        page.set_cropbox(crop_rect)

        # Save the cropped page as a new PDF, including the original PDF ID
        cropped_pdf_path = os.path.join(output_folder, f'cropped_{pdf_id}_{name}.pdf')
        with fitz.open() as new_pdf:
            new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            new_pdf.save(cropped_pdf_path)

        # Save the caption to a text file with UTF-8 encoding, including the original PDF ID
        caption_txt_path = os.path.join(output_folder, f'caption_{pdf_id}_{name}.txt')
        with open(caption_txt_path, 'w', encoding='utf-8') as caption_file:
            caption_file.write(caption)

        print(f'Cropped PDF saved as {cropped_pdf_path} and caption saved as {caption_txt_path}')

    pdf_document.close()