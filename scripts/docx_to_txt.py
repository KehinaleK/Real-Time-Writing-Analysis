import pypandoc
from pathlib import Path
import chardet
import re


dossier = Path("../data/saved_texts")
folder = list(dossier.glob('*.docx'))
folder_list = sorted(folder, key=lambda x: x.name)


for file in folder_list:
    try:
        name = file.name[:-5]
        number = re.search(f'S(\d+)', name).group(1)
        if "P" in file.name:
            corpus = "P"
        if "-" in file.name:
            charge = "-"
        else:
            charge = "+"
        new_name = corpus + charge + "S" + number
        output_path = Path(f"../data/saved_texts_txt/{new_name}.txt")
        output = pypandoc.convert_file(str(file), 'plain', outputfile=str(output_path))
        assert output == ""
        with open(output_path, "rb") as f:
            text = f.read()
            result = chardet.detect(text)
            encoding = result['encoding']
        with open(output_path, "r", encoding=encoding) as f:
            text = f.read()
        text = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text)
        with open(output_path, "w", encoding=encoding) as f:
            f.write(text)
    except Exception as e:
        print(f"Failed to convert {file}: {e}")

