
import pandas as pd

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def reconstruction(df):

    list_text = []
    deletions = 0
    for index, row in df.iterrows():
    
        string = row["charBurst"].replace("⇪", "")
        print("on fait :", string)
        if index == 0:
            list_text += list(string)
            print(list_text)
            continue
        else:
            current_string_list = list(row["charBurst"].replace("⇪", ""))
            current_posStart = row["posStart"]
            current_posEnd =  row["posEnd"]

            if "⌫" in current_string_list or "⌦" in current_string_list:
                print(f"Nous avons un effacement en position {current_posEnd}")
                if current_posEnd >= len(list_text) and len(list_text) != 0:
                    list_text.pop(-1)
                elif len(list_text) == 0:
                    continue
                else:
                    print(list_text[current_posEnd])
                    list_text.pop(current_posEnd)
                    

            elif current_string_list not in ["⌫", "⌦"]:

                if current_posStart == (len(list_text) - 1):
                    for char in string:
                        list_text.append
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
    text = "".join(["\t" if ch == "↹" else "\n" if ch == "⏎" else ch for ch in list_text])
    print(text)
    return text            

df = open_corpus_csv('../data/tables/test.csv')

        
grouped = df.groupby('ID')
for id, group in grouped:
    text = reconstruction(group)
    with open(f"../data/reconstructed_texts/{id}.txt", "w") as file:
        file.write(text)