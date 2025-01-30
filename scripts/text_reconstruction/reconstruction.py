
import pandas as pd
import argparse
import os

"""
This script uses the csv file created thanks to retrieval.py.
For each user in the csv file, each row is processed to re-create every action.
These actions are then saved in a txt file in the saved_texts folder.
The saved text is the final version of the text as it was saved by the user during the experiment.
To run the script, one argument is required : the csv file you want to use.
You can also add the argument --debug to print additional information during execution. 
This can be useful to investigate problems during reconstruction.
"""


"""
This script may not work for every text. Some texts may need additional processing,
notably in the retrieval script, to be correctly reconstructed. Some variables are
not used but may be useful for futur analysis. If a text is not correctly
reconstructed, it will be removed from the reconstructed texts folder. These texts
will be printed at the end of the execution of the script.
"""

"""
To use or modify this script, I recommend you to read the MANUAL file.
"""


def debug_print(debug, *args, **kwargs):
    """This function allows to print additional information during execution if the --debug argument is used.
    The amount of information is quite important. It is recommended to use this function while investigating
    problems during reconstruction and using > test.txt to get the prints in a txt file."""

    if debug:
        print(*args, **kwargs)

def open_corpus_csv(csv_file):

    """This function allows to open the csv file created by retrieval.py.
    
    Parameters(s):
        csv_file = str : the csv file created by retrieval.py.
    Returns:
        df = pandas DataFrame : the csv file converted to a pandas DataFrame"""

    with open(csv_file, 'r') as file:
        df = pd.read_csv(file)

    return df


def mark_revisions_pipes(df):

    """This function allows to mark the beginning and the end of each revision burst in the DataFrame."""

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
        
    return df


def reconstruction(df, debug):

    """
    This function allows to reconstruct the text as it was saved by the user during the experiment.
    The function takes the DataFrame as input and returns the reconstructed text as a string.
    The function uses the mark_revisions_pipes function to mark the beginning and the end of each revision burst.
    The function uses the following functions : deletions, insertions, deletions_string_insertions.
    
    Parameters(s):
        df = pandas DataFrame : the DataFrame created by mark_revisions_pipes.
        debug = bool : if True, additional information will be printed during execution.
    Returns:
        text = str : the reconstructed text as a string.
    """

    # Each action is stored in a list for easier manipulation
    # Each action is trokenized in a tuple with 3 elements.
    # Thoses tuples allow us to associate an action (like ~ for a deletion) to a character.
    # By doing so, we keep the lenght of the list (and therefore the text) which allows us
    # to correctly add or delete elements with their positions found in the CSV file. The letters,
    # or the final text, is contained in the second element of the tuple. At the end of the process,
    # we can join the letters to get the final text. The first and the third elements of the tuple are
    # also concatenated to the letter to keep track of the actions that were done on the surrounding
    # characters.
    list_text = []

    # We iterate through each row of the DataFrame to reconstruct the text.
    for index, row in df.iterrows():
        string = row["charBurst"].replace("⇪", "").replace("␣", " ")
        category = row["categ"]
        start_brace = row["start_brace"]
        end_brace = row["end_brace"]
        first_row = row["first_row_in_burst"]

        debug_print(debug, f"ROW CURRENTLY BEING PROCESSED : {string}")
        # We check if the row is the first one. If it is, we can add it to the list directly.
        if index == 0:
            debug_print(debug, f"THE ROW '{string}' IS THE FIRST ONE. WE CAN ADD IT TO THE LIST DIRECTLY.")
            list_text += [("", char, "") for char in string]
            debug_print(debug, f"OUR LIST CURRENTLY LOOKS LIKE THIS : {list_text}")
            continue
        # If the row is not the first one, we have to check the action that was done.
        else:
            # We retrieve the list of characters from the string.
            # We also retrieve the start and the end position of the action.
            debug_print(debug, f"THE ROW '{string}' IS NOT THE FIRST ONE.")
            current_string_list = list(string)
            debug_print(debug, f"WE CONVERT IT TO A LIST {current_string_list}")
            current_posStart = row["posStart"]
            debug_print(debug, f"WE DEFINE ITS POS_START : {current_posStart}")
            current_posEnd =  row["posEnd"]
            debug_print(debug, f"WE DEFINE ITS POS_END : {current_posEnd}")
            debug_print(debug, f"WE NOW CHECK THE ACTION.")

            # We check the action that was done on the character.
            # For when the action is a deletion.
            if "⌫" in current_string_list or "⌦" in current_string_list:
                debug_print(debug, f"WE HAVE A DELETION AT POSITION : {current_posEnd}")
                # We check if the deletion is applied beyond the text boundaries.
                # Like at the very bottom of the text or at the very top.
                # If it is the case, we ignore it.
                if current_posEnd >= len(list_text) and len(list_text) != 0:
                    debug_print(debug, f"THE DELETION IS APPLIED BEYOND THE TEXT BOUNDARIES.\nWE IGNORE IT.")
                    continue
                # Same for when the text is empty.
                elif len(list_text) == 0:
                    debug_print(debug, f"THE DELETION IS APPLIED WHEN NOTHING IS WRITTEN.\nWE IGNORE IT.")
                    continue
                # If the deletion is applied within the text boundaries, we can process it.
                # We can call the deletions function to apply the deletion.
                # deletions_string_insertions is called first to check if the deletion is at the border of an insertion.
                # Since insertions are represented with curly brackets, a deletion at the border of one require shifting the brackets
                # left or right depending on the position of the deletion. 
                # If the deletion is not at the border of an insertion, the deletions function is called to apply the deletion.
                else:
                    debug_print(debug, f"ELEMENT '{list_text[current_posEnd]}' IS DELETED AT POSITION '{current_posEnd}'.") 
                    deletions_string_insertions(current_posEnd, list_text)
                    list_text.pop(current_posEnd)
                    deletions(current_posEnd, category, list_text)
                    # Since deletions are isolated actions, we can continue to the next row.
                    continue

            # For when the action is a replacement.
            # Replacement are represented by a left curved arrow.         
            elif "↺" in current_string_list:
                debug_print(debug, "WE HAVE A REPLACEMENT.")
                # If the replacement is not associated with any character, we remove the character at the position of the replacement.
                if len(current_string_list) == 1:
                    debug_print(debug, f"ELEMENT '{list_text[current_posStart]}' AT POSITION '{current_posStart}' IS REPLACED WITH NOTHING.")
                    debug_print(debug, "WE REMOVE IT FROM THE LIST.")
                    list_text.pop(current_posStart) 
                    deletions(current_posStart, category, list_text)
                    continue
                
                replaced_letters_number = (current_posEnd - current_posStart) + 1
                current_string_list.remove("↺")

                # If the replacement is associated with a character, we replace the character at the position of the replacement.
                # I have not found a way to correctly replace the character with the replacement character.
                # This part of the code may not work as intended.
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

            # For when the action is an insertion (spaces, or characters...).
            elif current_string_list not in ["⌫", "⌦"] and "↺" not in current_string_list:
                debug_print(debug, "WE HAVE TO ADD ELEMENTS TO THE LIST.")
                # If the start position of the insertion is beyond the text boundaries, we add empty elements to the list.
                if current_posStart > len(list_text):
                    list_text.extend([(""," ", "")] * (current_posStart - len(list_text) + 1))

                # We then simply add the characters to the list at the position of the insertion.
                # We call the insertions function to process the insertion.
                debug_print(debug, f"WE ADD '{string}' FROM POSITION '{current_posStart}' TO '{current_posStart + len(string)}'")
                insertions(list_text, category, current_posStart, string, first_row)

        # You'll see here an updated list after each row is processed.
        debug_print(debug, "HERE IS OUR UPTADED LIST AFTER MODIFICATION.")
        for index, char in enumerate(list_text):
            debug_print(debug, index, char)

        # We join the characters to get the text after each row is processed.          
        debug_print(debug, "".join([pipe + char + _ for pipe, char, _ in list_text]))

    # We join the characters to get the final text.
    # We replace some symbols.
    text = "".join([pipe + char + _ for pipe, char, _ in list_text])
    text = text.replace("↹", "\t").replace("⏎", "\n\n")
    
    return text            


def deletions(current_posEnd, category, list_text):
    """
    This function allows to process deletions in the list_text.
    The function takes the current position of the deletion, the category of the action and the list_text as input.
    Different cases are processed to correctly delete the character and the surrounding actions.
    The function does not return anything but modifies the list_text in place.
    """
    # If the deletion is at the very beginning of the text.
    if current_posEnd == 0:
        # We change the first element of the list to keep track of the deletion.
        if len(list_text) != 0:
            history = "~" + list_text[0][0]
            new_tuple = (history, list_text[0][1], "")
            list_text[0] = new_tuple

    # If the deletion is somewhere in the text.
    else:
        # We check the category of the action.
        # If it is in a revision burst, then the element
        # at the position of the deletion is modified to include
        # the deletion symbol surrounded by chevrons.
        if category == "R":
            history = list_text[current_posEnd - 1][2] + "<~>"
        # If it is not in a revision burst, chevrons are not added.
        # Only the ~ symbol is added to the element.
        else:
            history = list_text[current_posEnd - 1][2] + "~"

        new_tuple = ("", list_text[current_posEnd - 1][1], history)
        list_text[current_posEnd - 1] = new_tuple

def insertions(list_text, category, current_posStart, string, first_row):

    """
    This function allows to process insertions in the list_text.
    The function takes the list_text, the category of the action, the current position of the insertion, the string to insert and a boolean as input.
    Different cases are processed to correctly insert the characters and the surrounding actions.
    The function does not return anything but modifies the list_text in place.
    """

    # A pipe is added to the first element of the tuple if it is the first row of the burst.
    # A pipe represents a pause, so a boundary between two bursts.
    pipe = "|" if first_row == True else ""
    if category == "R":
        # If the insertion is in a revision burst, curly brackets are added to the element at the position of the insertion.
        # Chevrons are added to the boudaries of single letter insertions.
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
        # If the processed burst is not a revision burst, characters are simply added to the list.
        # If there is no pipe or revision actions, nothing is added to the first and third elements of the tuple.
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

    """
    This function allows to process deletions that are at the border of an insertion in the list_text.
    The function takes the current position of the deletion and the list_text as input.
    Different cases are processed to correctly delete the character and the surrounding actions.
    The function does not return anything but modifies the list_text in place.
    """

    # If the deletion is at the boundary of an insertion, we have to shift the curly brackets left or right.
    # We therefore need to delete the existing tuple (the one that is at the position of the deletion) and modify
    # the surrounding tuples to correctly shift the curly brackets.

    tuple_to_delete = list_text[current_posEnd]
  
    # When a curly bracket is at the end of the tuple we want to delete.
    if "}" in tuple_to_delete[2]:
        # if the previous element has a curly bracket at the beginning.
        # We remove the curly bracket at the beginning of the previous element.
        if "{" in list_text[current_posEnd - 1][0]:
            history = list_text[current_posEnd - 1][0].replace("{", "")
            new_tuple = (history, list_text[current_posEnd - 1][1], list_text[current_posEnd - 1][2])
            list_text[current_posEnd - 1] = new_tuple
        else:
            # if the previous element does not have a curly bracket at the beginning.
            # We add a curly bracket at its end.
            # We therefore shifted the position of the ending of an insertion to not
            # loose its frontier when deleting a character.
            history = list_text[current_posEnd - 1][2] + "}"
            new_tuple = (list_text[current_posEnd - 1][0], list_text[current_posEnd - 1][1], history)
            list_text[current_posEnd - 1] = new_tuple           

    # The same logic is applied when a curly bracket is at the beginning of the tuple we want to delete.
    elif "{" in tuple_to_delete[0]:
        if "}" in list_text[current_posEnd + 1][2]:
            history = list_text[current_posEnd + 1][2].replace("}", "")
            new_tuple = (list_text[current_posEnd + 1][0], list_text[current_posEnd + 1][1], history)
            list_text[current_posEnd + 1] = new_tuple
        else:
            history = "{" + list_text[current_posEnd + 1][0]
            new_tuple = (history, list_text[current_posEnd + 1][1], list_text[current_posEnd + 1][2])
            list_text[current_posEnd + 1] = new_tuple 


def validation(folder):

    """
    This function allows to validate the reconstructed texts.
    The function takes the folder where the reconstructed texts are stored as input.
    The function compares the reconstructed texts with the saved texts by removing
    the symbols used to mark the actions. If the reconstructed text is the same as the saved text,
    the text is kept. If it is not, the text is removed from the reconstructed folder.

    Parameters(s):
        folder = str : the folder where the reconstructed texts are stored.
    Returns:
        not_validated_texts = list : the list of the texts that were not correctly reconstructed.
    """

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
    
    
    args = parser.parse_args()
    debug = args.debug
    corpus = args.file
    df = open_corpus_csv(f'../../data/tables/{corpus}.csv')
    grouped = df.groupby('ID')
    folder = "../../data/reconstructed_texts"
    # The reconstruction process is done for each user in the csv file.
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
