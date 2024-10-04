import os
import subprocess
import re
from PyPDF2 import PdfReader

def extract_id(filename):
    match = re.search(r'(\d{4}\.\d{4,5})', filename)
    return match.group(1) if match else None

def check_pdf_for_vector_graphics(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        for page in pdf.pages:
            if '/Resources' in page and '/XObject' in page['/Resources']:
                for obj in page['/Resources']['/XObject'].values():
                    if isinstance(obj, dict):
                        if obj.get('/Subtype') == '/Form':
                            return True
                    elif hasattr(obj, 'get_object'):
                        resolved_obj = obj.get_object()
                        if isinstance(resolved_obj, dict) and resolved_obj.get('/Subtype') == '/Form':
                            return True
    return False

def convert_pdf_to_svg(pdf_path, svg_path):
    try:
        subprocess.run(["pdf2svg", pdf_path, svg_path], check=True)
        print(f"Converted {pdf_path} to {svg_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def process_pdfs(input_folder, output_folder, isline_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create a dictionary of IDs from isLine folder
    isline_ids = {}
    for filename in os.listdir(isline_folder):
        id = extract_id(filename)
        if id:
            isline_ids[id] = filename

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            pdf_id = extract_id(filename)
            
            if pdf_id and pdf_id in isline_ids:
                try:
                    if check_pdf_for_vector_graphics(pdf_path):
                        base_name = os.path.splitext(filename)[0]
                        svg_filename = f"{base_name}.svg"
                        svg_path = os.path.join(output_folder, svg_filename)
                        convert_pdf_to_svg(pdf_path, svg_path)
                    else:
                        print(f"Skipping {filename} as it doesn't contain vector graphics")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
            else:
                print(f"Skipping {filename} as no matching ID found in isLine folder")

# Usage
input_folder = "data/cropped_pdfs"
output_folder = "data/svgs"
isline_folder = "data/isLine"
process_pdfs(input_folder, output_folder, isline_folder)