import fitz  # PyMuPDF
import json
import os
from PIL import Image
import io

# Folder paths for JSONs and PDFs
json_folder = 'data/extracted_data/data/'  
pdf_folder = 'data/modified_pdfs/' 

# Create a directory for output JPGs
output_folder = 'data/cropped_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all JSON and PDF files
json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Function to match the correct PDF for each JSON based on file names
def find_matching_pdf(json_filename, pdf_files):
    for pdf_file in pdf_files:
        if pdf_file.replace('.pdf', '') in json_filename:
            return os.path.join(pdf_folder, pdf_file)
    return None

# Iterate through each JSON file
for json_file in json_files:
    json_file_path = os.path.join(json_folder, json_file)
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    matching_pdf_path = find_matching_pdf(json_file, pdf_files)
    
    if matching_pdf_path is None:
        print(f"No matching PDF found for {json_file}")
        continue
    
    pdf_document = fitz.open(matching_pdf_path)
    
    # Iterate through each item in the JSON
    for item in data:
        page_num = item['page']
        region = item['regionBoundary']
        name = item['name'] 

        # Load the specified page
        page = pdf_document[page_num]

        # Define the crop rectangle
        crop_rect = fitz.Rect(region['x1'], region['y1'], region['x2'], region['y2'])

        # Get the pixmap of the cropped region
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=crop_rect)

        # Convert pixmap to PIL Image
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Save the image as JPG
        jpg_path = os.path.join(output_folder, f'cropped_{name}.jpg')
        img.save(jpg_path, 'JPEG', quality=95)

        print(f'Cropped image saved as {jpg_path}')

    pdf_document.close()