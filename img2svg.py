import os
import subprocess

inkscape_path = "C:/Program Files/Inkscape/bin/inkscape.exe"

def convert_png_to_svg(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Walk through the input directory recursively
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.png'):
                input_file_path = os.path.join(root, file)
                
                # Define the output SVG file path directly in the output folder
                output_file_name = os.path.splitext(file)[0] + '.svg'
                output_file_path = os.path.join(output_dir, output_file_name)

                # Run the Inkscape command to convert PNG to SVG
                command = [inkscape_path, input_file_path, '--export-filename', output_file_path]
                
                # Execute the command
                subprocess.run(command, check=True)

                print(f'Converted: {input_file_path} -> {output_file_path}')

# Example usage:
input_folder = 'data/extracted_data'  # Replace with your input folder path
output_folder = 'data/svg_data'  # Replace with your output folder path
convert_png_to_svg(input_folder, output_folder)
