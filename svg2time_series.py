import os
import matplotlib.pyplot as plt
from svgpathtools import svg2paths
import numpy as np

def extract_plot_data(svg_file):
    paths, attributes = svg2paths(svg_file)
    
    x_data = []
    y_data = []
    
    for path in paths:
        if len(path) > 1:  # Ignore paths with less than 2 points
            try:
                # Use a list comprehension instead of np.linspace
                t_values = [i/99 for i in range(100)]
                points = [path.point(t) for t in t_values]
                x_data.extend([p.real for p in points])
                y_data.extend([p.imag for p in points])
            except Exception as e:
                print(f"Error processing path: {e}")
                continue
    
    if not x_data or not y_data:
        raise ValueError("No valid data extracted from the SVG file")
    
    return x_data, y_data

def plot_extracted_data(x_data, y_data, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data)
    plt.title("Extracted Time Series Plot")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.savefig(output_file)
    plt.close()

def process_svg_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".svg"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
            
            try:
                x_data, y_data = extract_plot_data(input_file)
                plot_extracted_data(x_data, y_data, output_file)
                print(f"Processed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Usage
input_folder = "data/svgs"
output_folder = "data/final_data"
process_svg_folder(input_folder, output_folder)