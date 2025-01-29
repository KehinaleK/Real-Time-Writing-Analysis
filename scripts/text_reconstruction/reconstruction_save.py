
import pandas as pd
import argparse
import os


def debug_print(debug, *args, **kwargs):
    if debug:
        print(*args, **kwargs)

def open_corpus_csv(csv_file):

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def mark_revisions_pipes(df):

    grouped = df.groupby("n_burst")

    df['start_brace'] = False
    df['end_brace'] = False
    df['first_row_in_burst'] = False

    for n_burst, group in grouped: #allows us to iterate through each burst

        df.loc[group.index[0], 'first_row_in_burst'] = True
        revision_rows = group[group["categ"] == "R"] # We get all of the rows with a revision category 
        if not revision_rows.empty:

            revision_rows['consecutive'] = (revision_rows.index.to_series().diff() == 1).cumsum()
           
            end = len(revision_rows) - 1

            for i, (index, row) in enumerate(revision_rows.iterrows()):
                    posStart = row["posStart"]
                    posEnd = row["posEnd"]
                    charBurst = row["charBurst"]

                    if i == 0:
                        df.loc[index, 'start_brace'] = True
                        if len(revision_rows) == 1:
                            df.loc[index, 'end_brace'] = True
                        continue

                    prev_index = revision_rows.index[i - 1]
                    prev_posEnd = df.loc[prev_index, 'posEnd']
                    prev_posStart = df.loc[prev_index, 'posStart']

                    if posStart != prev_posEnd:
                        df.loc[index, 'start_brace'] = True 
                        df.loc[prev_index, 'end_brace'] = True
                    if i == len(revision_rows) - 1:
                        df.loc[index, 'end_brace'] = True
        
    df.to_csv("heu.csv")
    return df



def reconstruction(df, debug):

    list_text = []

    for index, row in df.iterrows():
        string = row["charBurst"].replace("⇪", "").replace("␣", " ")
        category = row["categ"]
        start_brace = row["start_brace"]
        end_brace = row["end_brace"]
        first_row = row["first_row_in_burst"]

        debug_print(debug, f"ROW CURRENTLY BEING PROCESSED : {string}")
        if index == 0:
            debug_print(debug, f"THE ROW '{string}' IS THE FIRST ONE. WE CAN ADD IT TO THE LIST DIRECTLY.")
            list_text += [("", char, "") for char in string]
            debug_print(debug, f"OUR LIST CURRENTLY LOOKS LIKE THIS : {list_text}")
            continue
        else:
            debug_print(debug, f"THE ROW '{string}' IS NOT THE FIRST ONE.")
            current_string_list = list(string)
            debug_print(debug, f"WE CONVERT IT TO A LIST {current_string_list}")
            current_posStart = row["posStart"]
            debug_print(debug, f"WE DEFINE ITS POS_START : {current_posStart}")
            current_posEnd =  row["posEnd"]
            debug_print(debug, f"WE DEFINE ITS POS_END : {current_posEnd}")
            debug_print(debug, f"WE NOW CHECK THE ACTION.")

            if "⌫" in current_string_list or "⌦" in current_string_list:
                debug_print(debug, f"WE HAVE A DELETION AT POSITION : {current_posEnd}")
                if current_posEnd >= len(list_text) and len(list_text) != 0:
                    debug_print(debug, f"THE DELETION IS APPLIED BEYOND THE TEXT BOUNDARIES.\nWE IGNORE IT.")
                    continue
                elif len(list_text) == 0:
                    debug_print(debug, f"THE DELETION IS APPLIED WHEN NOTHING IS WRITTEN.\nWE IGNORE IT.")
                    continue
                else:
                    debug_print(debug, f"ELEMENT '{list_text[current_posEnd]}' IS DELETED AT POSITION '{current_posEnd}'.") # TU ESSAIES DE VOIR COMMENT FAIRE QUAND TU AS UN DEBUT OU UNE FIN D'INSERTION ELIMINÉ
                    deletions_string_insertions(current_posEnd, list_text)
                    list_text.pop(current_posEnd)
                    deletions(current_posEnd, category, list_text)

                    continue
                    
            elif "↺" in current_string_list:
                debug_print(debug, "WE HAVE A REPLACEMENT.")
                if len(current_string_list) == 1:
                    debug_print(debug, f"ELEMENT '{list_text[current_posStart]}' AT POSITION '{current_posStart}' IS REPLACED WITH NOTHING.")
                    debug_print(debug, "WE REMOVE IT FROM THE LIST.")
                    list_text.pop(current_posStart) # FAIRE ÇAAAA
                    deletions(current_posStart, category, list_text)
                    continue
                
                replaced_letters_number = (current_posEnd - current_posStart) + 1
                current_string_list.remove("↺")

                if len(current_string_list) > 1:
                    continue
                else:
                    debug_print(debug, f"WE WILL REPLACE {replaced_letters_number} ELEMENTS BY '{current_string_list[0]}'.")
                    list_text.insert(current_posStart, ("|", string[0], ""))
                    current_posStart += 1
                    for char in string[1:]:
                        debug_print(debug, f"WE REPLACE '{list_text[current_posStart]}' AT POSITION '{current_posStart}' BY '{char}'.")
                        list_text[current_posStart] = ("", char, "")
                        current_posStart += 1
                        replaced_letters_number -= 1
                    
                    while replaced_letters_number > 0:
                        list_text[current_posStart] = ("", " ", "")
                        current_posStart += 1
                        replaced_letters_number -= 1

            elif current_string_list not in ["⌫", "⌦"] and "↺" not in current_string_list:
                debug_print(debug, "WE HAVE TO ADD ELEMENTS TO THE LIST.")
                if current_posStart > len(list_text):
                    list_text.extend([(""," ", "")] * (current_posStart - len(list_text) + 1))

                debug_print(debug, f"WE ADD '{string}' FROM POSITION '{current_posStart}' TO '{current_posStart + len(string)}'")
                insertions(list_text, category, current_posStart, string, first_row)

        debug_print(debug, "HERE IS OUR UPTADED LIST AFTER MODIFICATION.")
        for index, char in enumerate(list_text):
            debug_print(debug, index, char)
                    
        debug_print(debug, "".join([pipe + char + _ for pipe, char, _ in list_text]))

    text = "".join([pipe + char + _ for pipe, char, _ in list_text])
    text = text.replace("↹", "\t").replace("⏎", "\n\n")
    
    return text            


def deletions(current_posEnd, category, list_text):
    if current_posEnd == 0:
        if len(list_text) != 0:
            history = "~" + list_text[0][0]
            new_tuple = (history, list_text[0][1], "")
            list_text[0] = new_tuple
    else:
        if category == "R":
            history = list_text[current_posEnd - 1][2] + "<~>"
        else:
            history = list_text[current_posEnd - 1][2] + "~"

        new_tuple = ("", list_text[current_posEnd - 1][1], history)
        list_text[current_posEnd - 1] = new_tuple

def insertions(list_text, category, current_posStart, string, first_row):

    pipe = "|" if first_row == True else ""
    if category == "R":
        if len(string) <= 1:
            symbol_l = "<"
            symbol_r = ">"
            list_text.insert(current_posStart, (f"{symbol_l}{pipe}", string[0], symbol_r))
        else:
            symbol_l = "{"
            symbol_r = "}"

            list_text.insert(current_posStart, (f"{symbol_l}{pipe}", string[0], ""))
            current_posStart += 1
            for char in string[1:-1]:
                list_text.insert(current_posStart, ("", char, ""))
                current_posStart += 1
            list_text.insert(current_posStart, ("", string[-1], symbol_r))
    else:
        symbol_l = ""
        symbol_r = ""
        if len(string) <= 1:
            list_text.insert(current_posStart, (f"{symbol_l}{pipe}", string[0], symbol_r))
        else:
            list_text.insert(current_posStart, (f"{symbol_l}{pipe}", string[0], ""))
            current_posStart += 1
            for char in string[1:-1]:
                list_text.insert(current_posStart, ("", char, ""))
                current_posStart += 1
            list_text.insert(current_posStart, ("", string[-1], symbol_r))


def deletions_string_insertions(current_posEnd, list_text): # dans les cas ou on supprime un caractère qui est la frontière d'une insertion ! 

    tuple_to_delete = list_text[current_posEnd]
    #print(tuple_to_delete)
    if "}" in tuple_to_delete[2]:
        #print("on a un }", tuple_to_delete)
        if "{" in list_text[current_posEnd - 1][0]:
            #print("on veut supp un } et il y a un { dans l'élément d'avant", list_text[current_posEnd - 1])
            history = list_text[current_posEnd - 1][0].replace("{", "")
            new_tuple = (history, list_text[current_posEnd - 1][1], list_text[current_posEnd - 1][2])
            #print("on le remplace par ça ", new_tuple)
            list_text[current_posEnd - 1] = new_tuple
        else:
            #print("on a pas de { dans l'élément précédent", list_text[current_posEnd - 1])
            history = list_text[current_posEnd - 1][2] + "}"
            new_tuple = (list_text[current_posEnd - 1][0], list_text[current_posEnd - 1][1], history)
            #print("on le remplace par ça : ", new_tuple)
            list_text[current_posEnd - 1] = new_tuple           

    elif "{" in tuple_to_delete[0]:
        #print("on a un {", tuple_to_delete)
        if "}" in list_text[current_posEnd + 1][2]:
            #print("on veut supp un { et on a un } dans l'elem d'après", list_text[current_posEnd + 1])
            history = list_text[current_posEnd + 1][2].replace("}", "")
            new_tuple = (list_text[current_posEnd + 1][0], list_text[current_posEnd + 1][1], history)
            #print("on le remplace par ça", new_tuple)
            list_text[current_posEnd + 1] = new_tuple
        else:
            #print("on a pas de } dans l'élem d'après", list_text[current_posEnd + 1])
            history = "{" + list_text[current_posEnd + 1][0]
            new_tuple = (history, list_text[current_posEnd + 1][1], list_text[current_posEnd + 1][2])
            #print("on le remplace par ça :", new_tuple)
            list_text[current_posEnd + 1] = new_tuple 


def validation(folder):

    files = os.listdir(folder)
    not_validated_texts = []
    for file in files:
        with open(f"{folder}/{file}", "r") as f_behaviours:
            text_behaviours = f_behaviours.read()
            text_behaviours = text_behaviours.replace("|", "").replace("{", "").replace("}", "").replace("<", "").replace(">", "").replace("~", "")
            with open(f"../../data/saved_texts_txt/{file}", "r") as f_saved:
                text = f_saved.read()
                if text == text_behaviours:
                    continue
                else:
                    print(text)

                    print(text_behaviours)
                    not_validated_texts.append(file)
                    os.remove(f"{folder}/{file}")
                    
    return not_validated_texts

def main():


    parser = argparse.ArgumentParser(
    description="""This script uses the csv file created thanks to retrieval.py.
                For each user in the csv file, each row is processed to re-create
                in real time what was written or deleted by the user.
                For each text/user in the csv file, a txt file is created in the 
                saved_texts folder. The saved text is the final version of the text as
                it was saved by the user during the experiment"""
    )
    parser.add_argument("-f", "--file", required=True, type=str, choices=["planification", "formulation","revision", "test"],
                        help="""You can choose among the csv files created by retrieval.py.
                        Choices can be expanded based on your needs.""")
    parser.add_argument("--debug", action="store_true",
                        help="""Enable debugging mode to print additional information during execution.
                        If you want to further investigate problems during reconstruction, you can enable this
                        argument and have access to each step of the reconstruction. This process should be saved by adding "> test.txt"
                        after the command line so that everything is printed in a file.""" )
    parser.add_argument("--validation", action="store_true",
                        help="""Enable debugging mode to print additional information during execution.
                        If you want to further investigate problems during reconstruction, you can enable this
                        argument and have access to each step of the reconstruction. This process should be saved by adding "> test.txt"
                        after the command line so that everything is printed in a file.""" )
    
    
    
    args = parser.parse_args()
    debug = args.debug
    corpus = args.file
    df = open_corpus_csv(f'../../data/tables/{corpus}.csv')
    grouped = df.groupby('ID')
    folder = "../../data/reconstructed_texts_behaviours"
    for id, group in grouped:
        print(f"Text {id} is being constructed...")
        df_updated = mark_revisions_pipes(group)
        text = reconstruction(df_updated, debug)
        debug_print(debug, f"TEXT {id} AFTER RECONSTRUCTION :\n{text}")
        with open(f"{folder}/{id}.txt", "w") as file:
            file.write(text)

    not_valided_texts = validation(folder)
    print(f"{len(not_valided_texts)} texts were badly reconstructed, they will be removed from the reconstructed texts repertory.")
    print("Here is the list of the badly reconstructed texts :")
    for text in not_valided_texts:
        print(text)



if __name__ == "__main__":
    main()


    # if "⌫" in current_string_list or "⌦" in current_string_list:
    #             print(f"Nous avons un effacement en position {current_posEnd}")
    #             if current_posEnd >= len(list_text) and len(list_text) != 0:
    #                 continue
    #             elif len(list_text) == 0:
    #                 continue
    #             else:
    #                 print(list_text[current_posEnd])
    #                 print(list_text[current_posEnd])
    #                 if list_text[current_posEnd] != "⏎":
    #                     list_text.pop(current_posEnd)
    #                 else:
    #                     continue
                    