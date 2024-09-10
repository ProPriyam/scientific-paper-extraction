import os
import subprocess
import re

def pdf_to_svg(input_pdf, output_svg):
    try:
        # Run Inkscape command to convert PDF to SVG
        subprocess.run(
            ['C:/Program Files/Inkscape/bin/inkscape.exe', input_pdf, '--export-type=svg', '--export-filename=' + output_svg],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Successfully converted {input_pdf} to {output_svg}")
        # Sanitize the SVG file to remove problematic characters
        #sanitize_svg(output_svg)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during conversion of {input_pdf}: {e}")
        return False

def sanitize_svg(svg_file):
    try:
        with open(svg_file, 'r', encoding='utf-8') as file:
            content = file.read()
        # Use regex to remove invalid XML characters
        sanitized_content = re.sub(r'[^\x09\x0A\x0D\x20-\x7F]', '', content)
        # Write back the sanitized content to the file
        with open(svg_file, 'w', encoding='utf-8') as file:
            file.write(sanitized_content)
        print(f"Sanitized {svg_file} and removed invalid characters.")
    except Exception as e:
        print(f"Error occurred during sanitization of {svg_file}: {e}")

def convert_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.svg')
            
            if pdf_to_svg(input_path, output_path):
                print(f"Converted {filename} to SVG")
            else:
                print(f"Skipped {filename} due to conversion error")

# Example usage
input_folder = 'data/cropped_pdfs'
output_folder = 'data/converted_svgs'
convert_folder(input_folder, output_folder)