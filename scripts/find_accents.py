import os

french_accented_characters = [
     'À', 'Â', 'Ä', 'ç', 'Ç', 'É', 'È', 'Ê', 'Ë',
    "ï", 'Î', 'Ï', 'Ô', 'Ö', 'ù', 'Ù', 'Û', 'Ü', 'Ÿ'
]

folder = "../data/saved_texts_txt"

files = os.listdir(folder)
for file in files:
    if file.endswith(".txt"):
        continue
    else:
        files.remove(file)

for file in files:
    with open(f"{folder}/{file}", "r") as f:
        text = f.read()
        for char in text:
            if char in french_accented_characters:
                print(f"{char} : {file}")

