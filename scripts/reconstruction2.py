
import pandas as pd

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def reconstruction(df):

    list_text = []
    deletions = 0
    for index, row in df.iterrows():
        string = row["charBurst"].replace("␣", " ").replace("⇪", "")
        if index == 0:
            list_text += list(string)
            continue
        else:
            current_string_list = list(row["charBurst"].replace("␣", " ").replace("⇪", ""))
            current_posStart = row["posStart"]
            current_posEnd =  row["posEnd"]

            if "⌫" in current_string_list or "⌦" in current_string_list:
                if current_posEnd >= len(list_text) and len(list_text) != 0:
                    list_text.pop(-1)
                elif len(list_text) == 0:
                    continue
                else:
                    list_text.pop(current_posEnd)

            elif current_string_list not in ["⌫", "⌦"]:
                for char in string:
                    list_text.insert(current_posStart, char)
                    current_posStart += 1
                    

    text = "".join(list_text)
    return text            

df = open_corpus_csv('../data/tables/planification.csv')

        
grouped = df.groupby('ID')
for id, group in grouped:
    print(id)
    text = reconstruction(group)
    print(text)
    with open(f"../data/reconstructed_texts/{id}.txt", "w") as file:
        file.write(text)