from docx import Document
from pathlib import Path
import os
import re

# Define the input and output directories
dossier = Path("../data/saved_texts")
txt_output_dossier = Path("../data/saved_texts_txt")
txt_output_dossier.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

# Get all .docx files in the input directory
folder = list(dossier.glob('*.docx'))
folder_list = sorted(folder, key=lambda x: x.name)

# Function to rename the file based on the desired pattern
def rename_file(original_name):
    match = re.match(r'S(\d+)\s+(P[\+-])', original_name)
    if match:
        number = match.group(1)
        charge = match.group(2)
        new_name = f"{charge}S{number}.txt"
        return new_name
    else:
        return original_name + ".txt"

# Process each file
for file in folder_list:
    try:
        # Load the .docx document
        doc = Document(file)
        
        # Prepare a list to hold the text content
        full_text = []
        
        for para in doc.paragraphs:
            # Process the paragraph for line breaks
            lines = []
            for run in para.runs:
                text = run.text
                # Handle intentional line breaks (Shift+Enter) found as 'w:br'
                text = text.replace("\v", "\n")
                lines.append(text)
                
            # Combine all runs in the paragraph and append to full_text
            para_text = ''.join(lines)
            full_text.append(para_text)
        
        # Join all paragraphs with '\n\n' to separate them clearly
        full_text_str = '\n\n'.join(full_text)
        
        # Get the new file name and save as a .txt file
        new_file_name = rename_file(file.stem)
        output_path = txt_output_dossier / new_file_name
        with open(output_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(full_text_str)
        
    except Exception as e:
        print(f"Failed to process {file}: {e}")
