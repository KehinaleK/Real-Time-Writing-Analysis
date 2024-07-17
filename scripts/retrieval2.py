import os
import bs4
from bs4 import BeautifulSoup
import csv
from dataclasses import dataclass, field
from typing import List
import argparse


## Burst = liste de bursts
# Un élément de list quand le burst est linéaire
# Une liste de plusieurs bursts quand le burst a des élément qui se déplacent ! Donc seules les positions et les charBurst, Burst changent d'un élément à un autre


@dataclass
class Row:
    """ 
    This class allows to process the data extracted from the idfx files. Each object corresponds to a row in our resulting
    csv file. A single burst can have multiple rows depending on if it contains control characters and deletions.
    Therefore, positions and burst columns (charBurst and burst) change for every row, the remaining ones concern the entire burst
    and do not change from one row to another within a singular burst.
    Those rows are reunited in burst objects.

    id: str
        id of the user
    control : str
        level of expertise (- = expert, + = non-expert)
    tool : str
        ???
    n_burst : int
        id of each burst (goes back to 0 for each new user)
    burstStart : float
        start time of the burst (in seconds)
    burstDur : float
        duration of the burst (in seconds)
    pauseDur : float
        duration of the pause between the current burst and the next one (in seconds)
    cycleDur : float
        duration of the cycle (duration of the burst + duration of the pause)
    burstPct : float
        percentage of the cycle that is occupied by the burst
    pausePct : float
        percentage of the cycle that is occupied by the burst
    burstLen : int
        len of the burst in its final form (characters + spaces)
    burst : str
        burst without control and deletion characters
    posStart : int
        starting position of the burst
    posEnd : int
        ending position of the burst
    docLen : int
        length of the text at the end of the corresponding burst
    categ : str
        category of burst (R, RB or P)
    charBurst : str
        burst with control and deletion characters
    ratio : int
        ratio between the duration of the burst and the duration of the pause
    """

    id: str
    control: str
    tool: str
    n_burst: int
    burstStart: float
    burstDur: float
    pauseDur: float
    cycleDur: float
    burstPct: float
    pausePct: float
    totalActions: int
    totalChars: int
    finalChars: int
    totalDeletions: int
    innerDeletions: int
    posStart: int
    posEnd: int
    docLen: int
    categ: str
    charBurst: str
    ratio: float

@dataclass
class Burst:
    """ 
    Each object of this class corresponds to one single burst. Since some bursts need multiple rows to be represented,
    this class is a list of Row objects.

    rows: list[Row]
        List of rows for each burst. If a burst needs only one row to be represented, 'rows' only has one element. 
    """    
    rows: List[Row] = field(default_factory=list)

@dataclass
class Bursts:
    """ 
    This class contains all of our bursts. Those bursts are all represented by a Burst object.

    rows: list[Burst]
        List of Burst objects. There are as many Burst objects as we have bursts in our corpus.
    """    
    bursts: List[Burst] = field(default_factory=list)


def get_idfx_files(corpus_path: str) -> List[str]:

    """
    This function takes the corpus path given in argument by the user and returns
    the list of its files. This list is sorted depending on the '+' or '-' charge and numerically.
    Exemple : [P+S1, P+S2, [...] P-S1, P-S2, P-S3, [...] P-S30]
    
    Parameter(s):
        corpus_path = str : path of the corpus given by the user.
    Returns:
        files_list = List[str] : list of the idfx files from the corpus given by the user.
    """

    files = os.listdir(corpus_path)
    files = [file for file in files if file != ".DS_Store"]
    files_list = sorted(files, key=lambda x: (x[1], int(x[3:x.find('.idfx')])))
    return files_list


def get_file_content(file_path: str) -> bs4.BeautifulSoup:

    """
    This function goes through one idfx file and retrieve its content.
    
    Parameter(s):
        file_path = str : complete path of the idfx file.
    Returns:
        soup = BeautifulSoup Object: complete idfx structure and content of the file.
    """

    with open (file_path, 'r') as tei: 
        data = tei.read()
        soup = BeautifulSoup (data, 'lxml-xml')

    return soup

def create_accents(value, accent):

    """
    This function allows to create accented characters based on the accent and the character given in argument.
    It is used for diacritics that are not directly available on the keyboard such as : â, ê, î, ô, û, ŵ, ŷ, ẑ, ĉ, ĝ, ĥ, ĵ, ŝ...
    For instance, in order to get a 'â', the user needs to press the '^' key  and then the 'a' key.
    In the idfx files, the '^' key is represented by the 'VK_OEM_6' code and is then followed by the 'VK_A' one.
    When the '^' is pressed, we add it to the burst. If it is the last one of that burst, we go onto the next one and separate the '^' from the 'a'.
    However, is most bursts, if a letter is precedeed by a diacritic, these two are sent to this function and return the corresponding accented letter.
    The last element of the burst, the isolated accent, is then removed from it.
    
    Parameter(s):
        value = str : character to accentuate.
        accent = str : accent to add to the character.
    Returns:
        new_value = str : accented character."""

    print(value, accent)
    # Circumflex accents.
    dict_hat = {
        "a" : "â", "c" : "ĉ", "e" : "ê",
        "g" : "ĝ", "h" : "ĥ","i" : "î",
        "j" : "ĵ", "o" : "ô", "s" : "ŝ",
        "u" : "û", "w" : "ŵ", "y" : "ŷ",
        "z" : "ẑ",
    }

    # Trema accents.
    dict_trem = {
        "a" : "ä", "e" : "ë",
        "i" : 'ï', "o" : 'ö', 
        "u" : 'ü', "y" : 'ÿ', 
    }

    # Dictionary of all accents.
    dict_accents = {
        "^" : dict_hat,
        "¨" : dict_trem
    }
    new_value = ""
    # We use the accented character to find the corresponding dictionary.
    for key, val in dict_accents.items():
        if key == accent:
            corresponding_dict = val
    
    # We use the corresponding dictionary to find the accented character.
    for key, val in corresponding_dict.items():
        if key == value:
            new_value = corresponding_dict[key]
    
    return new_value if new_value else value


def get_burst_rows(soup: bs4.BeautifulSoup, file_name: str, thresold: int) -> List[Row]:

    """
    This function allows to retrieve a list of all the bursts in an idfx file.
    The burst segmentation is based on the duration of a pause between two characters.
    If a pause between two characters is longer than the specified thresold, our burst ends and
    another one is created.
    This list has one burst per row. The user can navigate through the text using control characters
    such as "⇦", "⇨", "⇧", "⇩" or "⏎". The first and last positions of each burst (a burst can start
    or end with a control character, a deletion or a normal character) directly follow or precede the positions
    of its neighbouring bursts.

    Parameter(s):
        soup = BeautifulSoup object : complete idfx structure and content of the file.
        file_name = str : name of the idfx file.
    Returns:
        raw_rows = List[Row objects]
            Exemple : Row()

    """
    
    ## Les éléments event correspondent à une touche sur le clavier
    ## Chaque élément event contient deux enfants "parts"
    ## Le premier contient les informations sur la position et la longueur du document
    ## Le deuxième contient la valeur (ex : L), le start time, le end time et le nom de la touche pressée


    # We initialize an empty list named 'running_burst'. We will construct each burst individually,
    # character by character, and then asign it to the charBurst instance of our Row class for now.
    raw_rows = []
    running_burst = []
    previous_event = ""
    id = file_name.strip(".idfx")
    control = "+"
    tool = "TW"
    n_burst = 0

    # We declare control keys, keys that do not impact the position of the cursor.
    CTRL_KEYS = ["VK_LMENU", "VK_TAB", "VK_APPS", "VK_ESCAPE", 
                 "VK_F12", "VK_LCONTROL", "VK_RCONTROL", 
                 "VK_SNAPSHOT", "VK_INSERT"]
                # VK_LMENU, VK_TAB = menu,
                # VK_F12 = shortcut to save, 
                # VK_APPS = windows key on the bottom left, 
                # VK_ESPACE = escape key,
                # VK_LCONTROL, VK_CRONTROL = control keys,
                # VK_SNAPSHOT = screenshot,
                # VK_INSERT = change the writing mode.
    SHIFT_KEYS = ["VK_LSHIFT", "VK_RSHIFT", "VK_CAPITAL"]
 
    DIACRITICS = ["^", "¨"]

    # We iterate through each event tag in the idfx file.
    # These tags have child elements called "part"
    # Each event has two parts elements, 
    # the first one contains the position of the corresponding character and the length of the document.
    # the second one contains the value (ex: "a"), the start time, the end time and the name of the key (ex: VK_A, VK_UP...).
    for event_tag in soup.find_all("event"):
        if event_tag["type"] == "keyboard":
            # We only keep events with a "keyboard" type, others concern mouse or selection actions.
            part_tag_1 = event_tag.findNext("part")
            for child in part_tag_1.children:
                if child.name == "position":
                    position = int(child.text)
                elif child.name == "documentLength":
                    documentLength = int(child.text)
                    # We retrieve the position and the docLength
            part_tag_2 = part_tag_1.findNext("part")
            for child in part_tag_2.children:
                if child.name == "startTime":
                    startTime = int(child.text)
                elif child.name == "endTime":
                    endTime = int(child.text)
                elif child.name == "key":
                    key = child.text
                elif child.name == "value":
                    value = child.text
                elif child.name == "keyboardstate":
                    keyboardstate = child.text

                    # We retrieve the startTime, endTime and value
            
            # We then find the next "event" tag. It allows us to know where a mouvement key such as "DOWN" takes us.
            # As an example, if our event concerns a DOWN key, its position will be where it is pressed on in the text.
            # If we wrote a word from position 125 to 130 and press DOWN at position 130, 130 becomes be the position of the DOWN key.
            # By getting the next "event" element, we are able to retrieve the position of the next character and therefore the position
            # where we landed after pressing the DOWN key. Really important ! For LEFT, RIGHT and RETURN key, the jump will always be 1 position.
            next_event_tag = event_tag.findNext("event")

            # We take the next "event" element only if its type is "keyboard".
            while next_event_tag is not None and next_event_tag["type"] != "keyboard":
                next_event_tag = next_event_tag.findNext("event")

            if next_event_tag is not None and next_event_tag["type"] == "keyboard":
                next_part_tag_1 = next_event_tag.findNext("part")
                # When we find it, we retrieve its position.
                for next_child in next_part_tag_1.children:
                    if next_child.name == "position":
                        next_position = next_child.text
            else:
                next_position = position
                # If we do not find a next "keyboard" "event" element, we keep the current position as the next one.
                # For instance, if the UP key is the last one to be pressed by the user, there is no next event and that 
                # movement can be considered as "null" since it won't affect the rest.
            
            next_part_tag_2 = next_part_tag_1.findNext("part")
            for next_child in next_part_tag_2.children:
                if next_child.name == "key":
                    next_key = next_child.text
                elif next_child.name == "value":
                    next_value = next_child.text

            if value is not None: # Never found a None value but we never know. Might need to add a else condition if you find one.
                # For mouvement and control characters, we add their corresponding symbols to our running burst alongside their initial and final positions.
                if key == "VK_LEFT":
                    running_burst.append(("⇦", position, next_position))
                elif key ==  "VK_RIGHT":
                    running_burst.append(("⇨", position, next_position))
                elif key == "VK_UP":
                    running_burst.append(("⇧", position, next_position))
                elif key == "VK_DOWN":
                    running_burst.append(("⇩", position, next_position))
                elif key == "VK_BACK":
                    running_burst.append(("⌫", position, next_position))
                elif key == "VK_DELETE":
                    running_burst.append(("⌦", position, next_position))
                elif key == "VK_SPACE":
                    running_burst.append(("␣", position, next_position))
                elif key == "VK_RETURN":
                    running_burst.append(("⏎", position, next_position))
                elif key == "VK_END":
                    running_burst.append(("⇲", position, next_position))
                elif key == "VK_OEM_102":
                    if value == "&lt;":
                        running_burst.append(("<", position, next_position))
                    elif value == "&gt;":
                        running_burst.append((">", position, next_position))
                elif key in CTRL_KEYS:
                    running_burst.append(("∅", position, next_position))
                elif key in SHIFT_KEYS:
                    running_burst.append(("⇪", position, next_position))
                elif key == "VK_OEM_6":
                    keyboardstate_value = ""
                    for char in keyboardstate:
                        if char.isspace():
                            continue
                        else:
                            keyboardstate_value += char
                    if keyboardstate_value != "":
                        if keyboardstate_value in SHIFT_KEYS:
                            running_burst.append(("¨", position, next_position))
                    else:
                        running_burst.append(("^", position, next_position))
                else:
                    if len(running_burst) == 0:
                        running_burst.append((value, position, next_position))
                    else:
                        if running_burst[-1][0] in DIACRITICS:
                            position = running_burst[-1][1]
                            new_value = create_accents(value, running_burst[-1][0])
                            running_burst.pop(-1)
                            running_burst.append((new_value, position, next_position))
                        else:
                            running_burst.append((value, position, next_position))

            # After adding the first character (letter, space or any other "keyboard" action),
            # we define the start time of the burst as the start time of that first character.  
            # Same logic for the start position of the burst.    
            if len(running_burst) == 1:
                burstStart = startTime / 1000
                posStart = position
    
            # We find the second part of the next event to see if the pause between our current character
            # and the next one is greater than the specified thresold. 
            for next_child in next_part_tag_2.children:
                if next_child.name == "startTime":
                    next_startTime = int(next_child.text)
                    # We get the start time of the next character
                    if endTime != 0:
                        pause = round(((next_startTime / 1000) - (endTime / 1000)), 2)
                        # We then get the duration of the pause between our current character
                        # and the next one by finding the time interval between their end time
                        # and start time.
                    else:
                        diff = (next_startTime - startTime) / 2
                        endTime = round((startTime + diff), 2)
                        pause = round(((next_startTime / 1000) - (endTime / 1000)), 2)
                        # Some SHIFT keys have "0" as their endTime, don't ask me why.
                        # To provide a value, I decided to find the differences between the start times
                        # of the current character and the next one. Once we have it, we divide it by 2 
                        # and add that value to the current character start time. It's arbitrary but I found
                        # it to be the best solution. We could as well ignore pauses longer than the thresold
                        # if the current character is a SHIFT. 
                    if pause > thresold:
                        # If the found pause is greater than the thresold, we end our burst at the current character.
                        # We can define every value that can be found in the csv file.
                        n_burst += 1
                        burstDur = round(((endTime / 1000) - burstStart),2)
                        pauseDur = pause
                        cycleDur = round((burstDur + pauseDur), 2)
                        burstPct = round((burstDur / cycleDur), 2)
                        pausePct = round((pauseDur / cycleDur), 2)
                        charBurst = running_burst
                        posEnd = position
                        docLen = documentLength
                        ratio = round((burstDur / pauseDur), 2)
                        # We then fill our Row class.
                        burst_row = Row(id=id, control=control, tool=tool, n_burst=n_burst, 
                                          burstStart=burstStart, burstDur=burstDur, 
                                          pauseDur=pauseDur, cycleDur=cycleDur, burstPct=burstPct, 
                                          pausePct=pausePct, totalActions=0, totalChars=0, finalChars=0, 
                                          totalDeletions=0, innerDeletions=0, posStart=posStart, posEnd=posEnd, 
                                          docLen=docLen, categ="", charBurst=charBurst, ratio=ratio)
                        # Each row (that corresponds to a single burst) is added to our global list.
                        raw_rows.append(burst_row)
                        running_burst = [] # Onto the next burst ! 
                    else:
                        continue
                        # If the pause is not greater than the specified thresold, we keep on building
                        # our running burst.
    return raw_rows


def divide_bursts(raw_rows):

    bursts = Bursts()
    for burst in raw_rows:
        list_burst = Burst()
        list_curr = []
        for i in range(len(burst.charBurst)):
            curr_burst = burst.charBurst[i]
            if curr_burst[0] in  ["⇦", "⇨", "⇧", "⇩", "⏎", "⌫", "⌦"]:
                curr = curr_burst
                burst_part =  Row(id=burst.id, control=burst.control, tool=burst.tool, 
                                    n_burst=burst.n_burst, burstStart=burst.burstStart, 
                                    burstDur=burst.burstDur, pauseDur=burst.pauseDur, 
                                    cycleDur=burst.cycleDur, burstPct=burst.burstPct, 
                                    pausePct=burst.pausePct, totalActions=burst.totalActions, 
                                    totalChars=burst.totalChars, finalChars=burst.finalChars, 
                                    totalDeletions=burst.totalDeletions, innerDeletions=burst.innerDeletions,
                                    posStart=curr[1], posEnd=curr[2], docLen=burst.docLen, categ=burst.categ, 
                                    charBurst=curr[0], ratio = burst.ratio)
                list_burst.rows.append(burst_part)
            else:
                list_curr.append(curr_burst)
                if i == (len(burst.charBurst) - 1):
                    curr = "".join([x[0] for x in list_curr])
                    posStart = list_curr[0][1]
                    posEnd = list_curr[-1][2]
                else: 
                    next_part = burst.charBurst[i+1]
                    if next_part[0] in ["⇦", "⇨", "⇧", "⇩", "⏎", "⌫", "⌦"]:
                        curr = "".join([x[0] for x in list_curr])
                        posStart = list_curr[0][1]
                        posEnd = list_curr[-1][2]
                    else:
                        continue

                burst_part = Row(id=burst.id, control=burst.control, tool=burst.tool, 
                                n_burst=burst.n_burst, burstStart=burst.burstStart, 
                                burstDur=burst.burstDur, pauseDur=burst.pauseDur, 
                                cycleDur=burst.cycleDur, burstPct=burst.burstPct, pausePct=burst.pausePct,
                                totalActions=burst.totalActions, totalChars=burst.totalChars,
                                finalChars=burst.finalChars, totalDeletions=burst.totalDeletions,
                                innerDeletions=burst.innerDeletions, posStart=posStart, posEnd=posEnd, 
                                docLen=burst.docLen, categ=burst.categ, charBurst=curr.replace("∅", "").replace("⇪", ""), 
                                ratio = burst.ratio)
                list_burst.rows.append(burst_part)
                list_curr.clear()

        bursts.bursts.append(list_burst)

    return bursts

def get_len(bursts):
   
    NON_LETTERS_OR_DEL = ["⇦", "⇨", "⇧", "⇩", "⏎", "⇲", "⇪", "∅"]
    DEL = ["⌫", "⌦"]
    # We initialize an empty list named 'list_intervals'.
    list_intervals = []
    for index in range(len(bursts.bursts)):
        total_len = [0,0,0,0,0]
        #print(f"NOUVEAU BURST")
        burst = bursts.bursts[index]
        #print(burst.rows)
        intervals_burst = []
        burst_total_chars = 0
        burst_final_chars = 0
        burst_deletions = 0
        burst_inner_deletions = 0
        if len(burst.rows) == 1:
            #print("On a un seul burst. BONJOUR")
            if burst.rows[0].charBurst in NON_LETTERS_OR_DEL:
                #print("On a juste des control characters. donc on saute au prochain burst.")
                continue
            if burst.rows[0].charBurst in DEL:
                #print("On a un seul caractère de suppression. On saute au burst prochain.")
                burst.rows[0].totalDeletions = 1
                burst.rows[0].totalActions = 1
                continue
            else:  
                burst.rows[0].finalChars = len(burst.rows[0].charBurst)
                burst.rows[0].totalChars = len(burst.rows[0].charBurst)
                burst.rows[0].totalActions = len(burst.rows[0].charBurst)
                #print("On a un seul row qui est une chaine de characteres. On passe au burst suivant")
                #print(f"Mais on a {len(burst.rows[0].charBurst)} caractères ajoutés.")
                continue
        else:
            first_row_charBurst = burst.rows[0].charBurst
            count_start, burst_deletions = get_first_character(burst, first_row_charBurst)
            #print(f"Beginning : {count_start}")
        for i in range(count_start, len(burst.rows)):
            #print(i)
            interval_row = ()
            row = burst.rows[i]
            #print(f"ID DU BURST : {row.n_burst}")
            row_charBurst = row.charBurst
            #print(f"CHARBURST DU ROW {i} : {row_charBurst}")
            # For rows that are not control characters, we get the positions where they start and end.
            if row_charBurst != "⇦" and row_charBurst != "⇨" and row_charBurst != "⇧" and row_charBurst != "⇩" and row_charBurst !=  "⏎" and row_charBurst != "∅" and row_charBurst != "⇲" and row_charBurst != "⇪":
                interval_row = (int(row.posStart), int(row.posEnd))
                intervals_burst.append(interval_row)
            #print(f"INTERVAL DU ROW {i} : {interval_row}")
            if row_charBurst in DEL:
                burst_deletions += 1
                #print(f"Le caractère est une suppression. On vérifie ses positions.")
                #print(intervals_burst)
                for interval in intervals_burst:
                    #print(f" Un des intervalle est {interval[0]} - {interval[1]}")
                    #print(f"On le compare à la postion de début du row {row.posEnd}")
                    if interval[0] <= int(row.posEnd) <= interval[1]:
                        burst_inner_deletions += 1
                        burst_final_chars -= 1
                        break   


            elif row_charBurst not in DEL and all(char not in NON_LETTERS_OR_DEL for char in row_charBurst):
                burst_final_chars += len(row_charBurst)
                burst_total_chars += len(row_charBurst)


            #elif row_charBurst in NON_LETTERS_OR_DEL:
                #print(f"There is a control character here. Let's go to the next row {row_charBurst} ")
                #print(f"burst_deletions {burst_deletions}")

            #if row_charBurst not in NON_LETTERS_OR_DEL:
                #print(f"TOTAL deletions : {burst_deletions} et TOTAL ajouté : {burst_final_chars}")

        total_len[0] += (burst_deletions + burst_total_chars)
        total_len[1] += burst_total_chars
        total_len[2] += burst_final_chars
        total_len[3] += burst_deletions
        total_len[4] += burst_inner_deletions
        print(total_len, row.n_burst)
        #print(f"total len : {total_len}")

        for row in burst.rows:
            row.totalActions = total_len[0]
            row.totalChars = total_len[1]
            row.finalChars = total_len[2]
            row.totalDeletions = total_len[3]
            row.innerDeletions = total_len[4]

        list_intervals.append(intervals_burst)


def get_first_character(burst, first_row_charBurst):

    DEL = ["⌫", "⌦"]
    NON_LETTERS_OR_DEL = ["⇦", "⇨", "⇧", "⇩", "⏎", "⇲", "⇪", "∅"]
    if first_row_charBurst in DEL:
        #print(burst.rows[0].n_burst)
        #print("The first character is a deletion.")
        start = 0
        count_start, burst_deletions = first_deletions(start, burst, first_row_charBurst)
        #print(f"count_start = {count_start} et burst_deletions = {burst_deletions}")
        return count_start, burst_deletions
    elif first_row_charBurst in NON_LETTERS_OR_DEL:
        #print("The first character is a control character.")
        count_start, burst_deletions = first_controls(burst, first_row_charBurst)
        #print("We need to find the first character after the control one.")
        print(burst.rows[count_start].charBurst)
        print(burst.rows[count_start].n_burst)
        print(burst_deletions)
        return count_start, burst_deletions
    else:
        count_start = 0
        burst_deletions = 0
        return count_start, burst_deletions

def first_deletions(start, burst, first_row_charBurst):
    DEL = ["⌫", "⌦"]
    burst_deletions = 0
    i = start
    #print(f"on commence de là ! : {start}")
    for i in range(start, len(burst.rows)):
        if burst.rows[i].charBurst in DEL:
            burst_deletions += 1
        else:
            break

    return burst_deletions, burst_deletions
        
def first_controls(burst, first_row_charBurst):
    DEL = ["⌫", "⌦"]
    NON_LETTERS_OR_DEL = ["⇦", "⇨", "⇧", "⇩", "⏎", "⇲", "⇪", "∅"]
    burst_controls = 0
    burst_deletions = 0
    for i in range(len(burst.rows) - 1):
        if burst.rows[i].charBurst in NON_LETTERS_OR_DEL:
            burst_controls += 1
        else:
            break
    
    if burst.rows[i].charBurst in DEL:
        start = burst_controls
        i, burst_deletions = first_deletions(start, burst, first_row_charBurst)
        return i, burst_deletions
    else: 
        start = burst_controls
        return start, burst_deletions

                        
def get_categories(bursts):

    """
    This function allows to categorize each burst based on the position of its characters.
    A burst can be categorized as three different types :
    - Production (P) : the burst is production added to the text directly after its last character.
    It can contains control characters, deletions or normal characters.
    - Edge Revision (ER) : the burst is a revision of the preceeding burst. It can contain control characters, deletions or normal characters.
    - Revision (R) : the burst is a revision of a higher burst. It can contain control characters, deletions or normal characters.

    Revisions can be adding a caracter, a string of caracters, a space, deleting a character or a string of characters.
    A burst can have multiple types since the user can use control characters to navigate through the text and make changes.
    The beginning of a burst can be a production for instance and then the user moves towards the beginning of the text to make a revision.

    We take the current class and add a new corresponding value to the 'categ' attribute.

    Parameter(s):
        bursts = Bursts object : object containing all the bursts of the text.
    """

    # We initialize an empty list named 'list_intervals'.
    list_intervals = []
    for index in range(len(bursts.bursts)):
        burst = bursts.bursts[index] 
        intervals_burst = []  

        # We focus on each row of a single burst and categorize it based on the position of its characters.
        for i in range(len(burst.rows)):
            interval_row = ()
            row = burst.rows[i]
            # For rows that are not control characters, we get the positions where they start and end.
            if row.charBurst != "⇦" and row.charBurst != "⇨" and row.charBurst != "⇧" and row.charBurst != "⇩" and row.charBurst !=  "⏎" and row.charBurst != "∅":
                interval_row = (int(row.posStart), int(row.posEnd))
                intervals_burst.append(interval_row)

            # The first row of the first burst is necessarlily a production.         
            if index == 0:
                row.categ = "P"
            # For the others, if a deletion or a insertion was made in the intervals of the preceeding burst, it is an edge revision.
            else:
                for interval in list_intervals[-1]:
                    if row.posStart >= interval[0] and row.posStart < interval[1]:
                        row.categ = "RB"
                        break
                # If it was made in the intervals of a higher burst, it is a revision.
                for burst_intervals in list_intervals[:-1]:
                    for interval in burst_intervals:
                        if row.posStart >= interval[0] and row.posStart < interval[1]:
                            row.categ = "R"
                            break
                # If it was not made in any of the intervals, it is a production.
                if row.categ == "":
                    row.categ = "P"
        
        list_intervals.append(intervals_burst)      
               
        

def create_csv(table_path, list_all_bursts):

    """This function creates a csv file based on the bursts of a corpus.
    
    Parameter(s):
        table_path = str : path of the csv file.
        list_all_bursts = List[Bursts] : list of all the bursts of the corpus."""

    with open(f"{table_path}.csv", "w") as file:
        structure = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["ID", "control", "tool", "n_burst", "burstStart", "burstDur", "pauseDur", "cycleDur", "burstPct", "pausePct", "totalActions", "totalChars", "finalChars", "totalDeletions", "innerDeletions", "posEnd", "docLen", "categ", "charBurst", "ratio"])
        print("ID", "control", "tool", "n_burst", "burstStart", "burstDur", "pauseDur", "cycleDur", "burstPct", "pausePct", "totalActions", "totalChars", "finalChars", "totalDeletions", "innerDeletions", "posStart", "posEnd", "docLen", "categ", "charBurst", "ratio")
        for bursts in list_all_bursts:
            for Burst in bursts.bursts: 
                for row in Burst.rows:
                    if row.charBurst != "⇦" and row.charBurst != "⇨" and row.charBurst != "⇧" and row.charBurst != "⇩" and row.charBurst !=  "⏎" and row.charBurst != "∅":
                        structure.writerow([row.id, row.control, row.tool, row.n_burst, row.burstStart, row.burstDur, row.pauseDur, row.cycleDur, row.burstPct, row.pausePct, row.totalActions, row.totalChars, row.finalChars, row.totalDeletions, row.innerDeletions, row.posStart, row.posEnd, row.docLen, row.categ, row.charBurst, row.ratio])
                        #print(f"{row.id}\t{row.control}\t{row.tool}\t{row.n_burst}\t{row.burstStart}\t{row.burstDur}\t{row.pauseDur}\t{row.cycleDur}\t{row.burstPct}\t{row.pausePct}\t{row.burstLen1}\t{row.burstLen2}\t{row.posStart}\t{row.posEnd}\t{row.docLen}\t{row.charBurst}\t{row.ratio}")
                    
def main():
    

    parser = argparse.ArgumentParser(
    description="""This script uses the idfx files from one specific sub-corpus to create a csv file. 
                This csv file allows us to get the pausal segmentations of our texts and therefore our 
                bursts alongside multiple informations regarding them, pauses, and others."""
    )
    parser.add_argument("-c", "--corpus", required=True, type=str, choices=["planification", "formulation","revision", "test"],
                        help="""You can choose to create a csv file based on three different corpora:\n
                        - Planification : texts are divided into '+' and '-'. '+' texts were written by users\n
                        with knowledge regarding their thematics. '-' texts were written by users with little to\n
                        no prior knowledge regarding their thematics.""")
    parser.add_argument("-t", "--thresold", required=True, type=float, default=1.5, choices=["1", "1.5", "2", "2.5", "3"], 
                        help="""You can choose the thresold used to divide our texts into bursts.\n
                        If you choose 1.5 for instance, our texts will be divided into bursts based on a pause\n
                        longer than 1.5s in-between two charaters.""" )
    
    args = parser.parse_args()
    
    if args.corpus == "planification":
        corpus_path = ("../data/idfx/planification")
    elif args.corpus == "formulation":
        corpus_path = ("../data/idfx/formulation")
    elif args.corpus == "revision":
        corpus_path = ("../data/idfx/revision")
    elif args.corpus == "test":
        corpus_path = ("../data/idfx/test")

    if args.thresold == "1":
        thresold = 1
    elif args.thresold == "1.5":
        thresold = 1.5
    elif args.thresold == "2":
        thresold = 2            
    elif args.thresold == "2.5":
        thresold = 2.5
    elif args.thresold == "3":
        thresold = 3

    files_list = get_idfx_files(corpus_path)
    list_all_bursts = []
    for file in files_list:
        print(file)
        soup = get_file_content(f"{corpus_path}/{file}")
        raw_rows = get_burst_rows(soup, file, thresold) 
        bursts = divide_bursts(raw_rows)
        get_categories(bursts)
        list_all_bursts.append(bursts)

    create_csv(f"../data/tables/{args.corpus}", list_all_bursts)

if __name__ == "__main__":
    main()
