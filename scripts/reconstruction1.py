
import pandas as pd

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def reconstruction(df):

    text = ""
    i = 0
    while i < len(df):
        print(text, "\n")
        string = df.iloc[i]["charBurst"].replace("␣", " ").replace("⇪", "")
        if i == 0:
            text = string
            i += 1
            continue
        else:
            current_string = df.iloc[i]["charBurst"].replace("␣", " ").replace("⇪", "")
            current_posStart = df.iloc[i]["posStart"]
            current_posEnd =  df.iloc[i]["posEnd"]

            if current_string != "⌫" and current_string != "⌦":
                print(current_posEnd)
                print(current_posStart)
                print(current_string)
                print(text[:current_posStart])
                print(text[current_posStart:])
                text = text[:current_posStart] + current_string + text[current_posStart:]
                if i <= len(df):
                    i += 1
                    continue
                else:
                    break
            elif current_string == "⌫":
                if current_posStart == (len(text) + 1):
                    text = text[:-1]
                else:
                    text = text[:current_posEnd] + text[current_posEnd + 1:]

                if i <= len(df):
                    i += 1
                    continue
                else:
                    break
             
    return text            

df = open_corpus_csv('../data/tables/test.csv')

        
grouped = df.groupby('ID')
for id, group in grouped:
    text = reconstruction(group)
    with open(f"../data/reconstructed_texts/{id}.txt", "w") as file:
        file.write(text)