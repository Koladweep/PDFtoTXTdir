from tkinter import Tk, filedialog
import os
import logging
from pypdf import PdfReader

# Suppress warnings
logging.basicConfig(level=logging.ERROR)

def browse_directory(title="Select a Directory"):  # Added a parameter for the title
    root = Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory(title=title)  # Use the title parameter
    root.destroy()
    return directory_path

def convert_pdf_to_txt(pdf_path, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            txt_file.write(page.extract_text())

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)
        output_root = os.path.join(output_dir, relative_path)
        
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                txt_path = os.path.join(output_root, os.path.splitext(file)[0] + '.txt')
                print(f"converting {pdf_path} to {txt_path}")
                convert_pdf_to_txt(pdf_path, txt_path)

if __name__ == "__main__":
    input_directory = browse_directory(title="select input directory")
    print(f'input directory: {input_directory}')
    output_directory = browse_directory("select output directory")
    print(f'output directory: {output_directory}')
    process_directory(input_directory, output_directory)
