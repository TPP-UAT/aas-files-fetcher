import os
import PyPDF2

# Function to search for content in a PDF file
def search_pdf_for_content(pdf_file_path, target_content, log_file_path):
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if target_content in page_text:
                    return True
        return False
    except Exception as e:
        print(f"Error reading {pdf_file_path}: {e}")
        filename = pdf_file_path.split("/")[-1].split(".pdf")[0]
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{filename}\n")
        return False

# Directory where the PDFs are located
pdfs_folder = "./webscraping"

# Content to search for in the PDFs
target_content = "We apologize for the inconvenience..."

# Log file to record exceptions
log_file_path = "files_with_error.txt"

# Loop through PDF files in the folder and search for content
for root, dirs, files in os.walk(pdfs_folder):
    for file_name in files:
        if file_name.endswith(".pdf"):
            pdf_file_path = os.path.join(root, file_name)
            print(f"Searching {pdf_file_path}...")
            if search_pdf_for_content(pdf_file_path, target_content, log_file_path):
                print(f"Content found in: {pdf_file_path}")

print("Search completed.")
