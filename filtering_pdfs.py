import os
import fitz  # PyMuPDF
import pytesseract

# Input and output directories
input_dir = "data/pdfs"
output_dir = "data/modified_pdfs"
os.makedirs(output_dir, exist_ok=True)

# Function to check if a page contains images
def page_has_image(page):
    images = page.get_images(full=True)
    return len(images) > 0

# Function to check for time series keywords in figure descriptions
def figure_has_time_series_keywords(page_text):
    keywords = ["year", "years", "hour", "hours", "minute", "minutes", "second", "seconds", "time", "date", "month", "day", "week"]
    figure_descriptions = [desc.strip() for desc in page_text.split('\n') if desc.lower().startswith('figure')]
    
    for desc in figure_descriptions:
        if any(keyword in desc.lower() for keyword in keywords):
            return True, desc
    return False, ""

# Process PDFs from "arxiv_pdfs" directly to "trim_3"
def process_pdfs():
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Open the PDF file
            doc = fitz.open(input_path)
            
            # Create a new PDF for the output
            new_doc = fitz.open()
            
            # Loop through each page, and only add pages with images and relevant figure descriptions to the new PDF
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text("text")
                
                has_keywords, description = figure_has_time_series_keywords(page_text)
                
                if page_has_image(page) and has_keywords:
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                    print(f"File: {filename}, Page: {page_num + 1}, Keywords in Description: {description}")
            
            # Save the new PDF if it has any pages
            if len(new_doc) > 0:
                new_doc.save(output_path)
                print(f"Trimmed and saved: {output_path}")
            else:
                print(f"No relevant content found in: {input_path}")
            
            # Close the documents
            doc.close()
            new_doc.close()

    print("All PDFs processed and saved in trim_3.")

# Run the process
process_pdfs()

print("All PDFs processed.")
