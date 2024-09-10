import os
import subprocess
from PyPDF2 import PdfReader

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
        subprocess.run(["C:/Program Files/pdf2svg/pdf2svg.exe", pdf_path, svg_path], check=True)
        print(f"Converted {pdf_path} to {svg_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def process_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            try:
                if check_pdf_for_vector_graphics(pdf_path):
                    svg_filename = os.path.splitext(filename)[0] + '.svg'
                    svg_path = os.path.join(output_folder, svg_filename)
                    convert_pdf_to_svg(pdf_path, svg_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


# Usage
input_folder = "data/cropped_pdfs"  # Replace with your input folder path
output_folder = "data/svgs"  # Replace with your output folder path
process_pdfs(input_folder, output_folder)
