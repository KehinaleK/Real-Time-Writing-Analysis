
import pandas as pd
import re

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def reconstruction(df):

    list_text = []
    deletions = 0
    for index, row in df.iterrows():
    
        string = row["charBurst"].replace("⇪", "").replace("␣", " ")
        print("on fait :", string)
        if index == 0:
            list_text += list(string)
            print(list_text)
            continue
        else:
            current_string_list = list(row["charBurst"].replace("⇪", "").replace("␣", " "))
            current_posStart = row["posStart"]
            current_posEnd =  row["posEnd"]

            if "⌫" in current_string_list or "⌦" in current_string_list:
                print(f"Nous avons un effacement en position {current_posEnd}")
                if current_posEnd >= len(list_text) and len(list_text) != 0:
                    continue
                elif len(list_text) == 0:
                    continue
                else:
                    print(list_text[current_posEnd])
                    print(list_text[current_posEnd])
                    if list_text[current_posEnd] != "⏎":
                        list_text.pop(current_posEnd)
                    else:
                        continue
                    
            elif "↺" in current_string_list:
                print("HELOOOOOOO", current_string_list)
                if len(current_string_list) == 1:
                    print("longeur == 1 donc on remplace avec rien")
                    print(current_posStart)
                    list_text.pop(current_posStart)
                    for index, char in enumerate(list_text):
                        print(index, char)
                    continue
                
                replaced_letters_number = (current_posEnd - current_posStart) + 1
                current_string_list.remove("↺")

                if len(current_string_list) > 1:
                    continue
                
                else:
                    print(f"On doit remplacer {replaced_letters_number} lettres par {current_string_list[0]}")
                    for char in current_string_list:
                        print(f"liste avant {list_text}")
                        print(f"on remplace {list_text[current_posStart]} par {char}")
                        list_text[current_posStart] = char
                        current_posStart += 1
                        replaced_letters_number -= 1
                    
                    while replaced_letters_number > 0:
                        list_text[current_posStart] = " "
                        current_posStart += 1
                        replaced_letters_number -= 1


            elif current_string_list not in ["⌫", "⌦"] and "↺" not in current_string_list:
                if current_posStart > len(list_text):
                    list_text.extend([" "] * (current_posStart - len(list_text) +1))
                print(f"Nous n'avons pas d'effacement")
                print(f"On ajoute {string} de position {current_posStart} à {current_posStart + len(string)}")
                for char in string:
                    print(char)
                    print(current_posStart)
                    list_text.insert(current_posStart, char)
                    current_posStart += 1

        for index, char in enumerate(list_text):
            print(index, char)
                    
        print("".join(list_text))
    text = "".join(["\t" if ch == "↹" else "\n\n" if ch == "⏎" else ch for ch in list_text])
    print(text)
    return text            

df = open_corpus_csv('../data/tables/test.csv')

        
grouped = df.groupby('ID')
for id, group in grouped:
    text = reconstruction(group)
    with open(f"../data/reconstructed_texts/{id}.txt", "w") as file:
        file.write(text)