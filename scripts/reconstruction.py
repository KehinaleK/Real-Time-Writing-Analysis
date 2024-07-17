
import pandas as pd

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df
df = open_corpus_csv('../data/tables/test.csv')


def reconstruction(df):

    text = ""
    i = 0
    while i < len(df)-1:
        print(text, "\n")
        if i == 0:
            text = df.iloc[i]["charBurst"].replace("␣", " ").replace("⇪", "")
            i += 1
            continue
        else:
            previous_row = df.iloc[i - 1] 
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            posStart = current_row["posStart"]
            posEnd = current_row["posEnd"]
            running_text = current_row["charBurst"].replace("␣", " ").replace("⇪", "")
            if posStart == 0:
                text = running_text + text
                i += 1
                continue
            if running_text != "⌫":
                text = text[:posStart] + running_text + text[posStart:]
                i += 1
                continue
            elif running_text == "⌫" and previous_row["posEnd"] == posStart:
                if next_row["charBurst"] != "⌫":
                    text = text[:-1]
                    i += 1
                    continue
                if next_row["charBurst"] == "⌫" and next_row["posStart"] != posEnd:
                    text = text[:-1]
                    i += 1
                    continue
                if next_row["charBurst"] == "⌫" and next_row["posStart"] == posEnd:
                    deletions = 0
                    print(f"oui, {next_row['charBurst']}")
                    for j in range(i, len(df)):
                        current_row = df.iloc[j]
                        print(current_row["posStart"])
                        next_row = df.iloc[j + 1]
                        print(next_row["posStart"])
                        posEnd = current_row["posEnd"]
                        running_text = current_row["charBurst"].replace("␣", " ").replace("⇪", "")
                        if running_text == "⌫" and next_row["posStart"] == posEnd:
                            deletions += 1
                        else:
                            break
                    print("number of deletions" ,deletions)
                    text = text[:posStart - deletions] + text[posStart:]
                    print(f"i : {i}")
                    i += deletions
                    continue
            
            
            elif running_text == "⌫" and previous_row["posEnd"] != posStart:
                deletions = 1
                if next_row["charBurst"] != "⌫":
                    text = text[:posStart] + text[posStart + 1:]
                    i += 1
                    continue       
                if next_row["charBurst"] == "⌫" and next_row["posStart"] == posEnd:
                    #print("here")
                    #print(text)
                    #print(previous_row["charBurst"])
                    #print(current_row["charBurst"])
                    #print(next_row["charBurst"])
                    deletions = 1
                    for j in range(i, len(df)):
                        current_row = df.iloc[j]
                        #print(current_row["charBurst"])
                        next_row = df.iloc[j + 1]
                        posEnd = current_row["posEnd"]
                        #print(posEnd)
                        running_text = current_row["charBurst"].replace("␣", " ").replace("⇪", "")
                        if running_text == "⌫" and next_row["posStart"] == posEnd:
                            #print(f"Donc le notre c'est ça : {running_text} avec la end {posEnd}")
                            #print(f"Donc voici le start du prochain {next_row['posStart']} et le prochain {next_row['charBurst']}")
                            deletions += 1
                        else:
                            break
                    text = text[:posStart - deletions] + text[posStart:]
                    i += deletions
                    continue
                    
                    


reconstruction(df)

        