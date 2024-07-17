
import pandas as pd

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def reconstruction(df):

    list_text = []
    deletions = 0
    for index, row in df.iterrows():
        print(list_text)
        string = row["charBurst"].replace("␣", " ").replace("⇪", "")
        if index == 0:
            list_text += list(string)
            continue
        else:
            current_string_list = list(row["charBurst"].replace("␣", " ").replace("⇪", ""))
            current_posStart = row["posStart"]
            current_posEnd =  row["posEnd"]

            if "⌫" in current_string_list or "⌦" in current_string_list:
                if current_posEnd >= (len(list_text) + 1):
                    list_text.pop(-1)
                else:
                    list_text.pop(current_posEnd)
                    deletions += 1

            elif current_string_list not in ["⌫", "⌦"]:
                print("insertion :", {string})
                for char in string:
                    print(char)
                    list_text.insert(current_posStart, char)
                    current_posStart += 1
                    print(list_text)
                    
        for i, indice in enumerate(list_text):
            print(i, indice)
        print(f"after processing row {index}")
    
    print("".join(list_text))
    return text            

df = open_corpus_csv('../data/tables/test.csv')

        
grouped = df.groupby('ID')
for id, group in grouped:
    text = reconstruction(group)
    with open(f"../data/reconstructed_texts/{id}.txt", "w") as file:
        file.write(text)