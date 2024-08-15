from docx import Document
from pathlib import Path
import os
import re


dossier = Path("../data/saved_texts")
txt_output_dossier = Path("../data/saved_texts_txt")
txt_output_dossier.mkdir(exist_ok=True)  

folder = list(dossier.glob('*.docx'))
folder_list = sorted(folder, key=lambda x: x.name)

def rename_file(original_name):
    match = re.match(r'S(\d+)\s+(P[\+-])', original_name)
    if match:
        number = match.group(1)
        charge = match.group(2)
        new_name = f"{charge}S{number}.txt"
        return new_name
    else:
        return original_name + ".txt"

for file in folder_list:
    try:
 
        doc = Document(file)
        
      
        full_text = []
        
        for para in doc.paragraphs:
            lines = []
            for run in para.runs:
                text = run.text
                text = text.replace("\v", "\n")
                lines.append(text)
     
            para_text = ''.join(lines)
            full_text.append(para_text)
       
        full_text_str = '\n\n'.join(full_text)

        new_file_name = rename_file(file.stem)
        output_path = txt_output_dossier / new_file_name
        with open(output_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(full_text_str)
        
    except Exception as e:
        print(f"Failed to process {file}: {e}")
