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
    burstLen: int
    burst: str
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


def get_burst_rows(soup: bs4.BeautifulSoup, file_name: str) -> List[Row]:

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


    raw_rows = []
    running_burst = []
    id = file_name.strip(".idfx")
    control = "+"
    tool = "TW"
    n_burst = 0
    CTRL_KEYS = ["VK_APPS", "VK_ESCAPE", "VK_F12", "VK_LCONTROL", "VK_RCONTROL", "VK_OEM_6", "VK_SNAPSHOT", "VK_INSERT"]
    # VK_12 = shortcut to save, VK_APPS = windows key on the bottom left, VK_ESPACE = escape key.
    SHIFT_KEYS = ["VK_LSHIFT", "VK_RSHIFT", "VK_CAPITAL"]


    for event_tag in soup.find_all("event"):
        if event_tag["type"] == "keyboard":
            part_tag_1 = event_tag.findNext("part")
            for child in part_tag_1.children:
                if child.name == "position":
                    position = int(child.text)
                elif child.name == "documentLength":
                    documentLength = int(child.text)
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
            
            next_part_tag_1 = part_tag_2.findNext("part")
            for next_child in next_part_tag_1.children:
                if next_child.name == "position":
                    next_position = next_child.text
                elif next_child.name == "start":
                    next_position = next_child.text
            
            print(file_name)
            print("current 1", part_tag_1)
            print("current 2", part_tag_2)

            if value is not None: #Prend en compte les espaces, ils ne sont pas None
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
                elif key in CTRL_KEYS:
                    running_burst.append(("∅", position, next_position))
                elif key in SHIFT_KEYS:
                    running_burst.append(("⇪", position, position))
                else:
                    running_burst.append((value, position, next_position))

            # En début de burst, donc après que le premier caractère soit ajouté, on définie son startTime comme le début du burst        
            if len(running_burst) == 1:
                burstStart = startTime / 1000
                posStart = position
    
            next_part_tag_2 = next_part_tag_1.findNext("part")
            for next_child in next_part_tag_2.children:
                if next_child.name == "startTime":
                    next_startTime = int(next_child.text)
                    if endTime != 0:
                        pause = round(((next_startTime / 1000) - (endTime / 1000)), 2)
                    else:
                        diff = (next_startTime - startTime) / 2
                        endTime = round((startTime + diff), 2)
                        pause = round(((next_startTime / 1000) - (endTime / 1000)), 2)
                    if pause > 1.5 :
                        n_burst += 1
                        burstDur = round(((endTime / 1000) - burstStart),2)
                        pauseDur = pause
                        cycleDur = round((burstDur + pauseDur), 2)
                        burstPct = round((burstDur / cycleDur), 2)
                        pausePct = round((pauseDur / cycleDur), 2)
                        charBurst = running_burst
                        # print(f"position : {position}")
                        print(f"charBurst : {charBurst}")
                        burst = get_burst(charBurst)
                        burstLen = len(burst)
                        posEnd = position
                        docLen = documentLength
                        ratio = round((burstDur / pauseDur), 2)
                        burst_row = Row(id=id, control=control, tool=tool, n_burst=n_burst, 
                                          burstStart=burstStart, burstDur=burstDur, 
                                          pauseDur=pauseDur, cycleDur=cycleDur, 
                                          burstPct=burstPct, pausePct=pausePct, 
                                          burstLen=burstLen, burst=burst, 
                                          posStart=posStart, posEnd=posEnd, docLen=docLen, categ="",
                                          charBurst=charBurst, ratio=ratio)
                        raw_rows.append(burst_row)
                        running_burst = []
                    else:
                        continue

    return raw_rows


def divide_bursts(raw_rows):

    bursts = Bursts()
    for burst in raw_rows:
        list_burst = Burst()
        list_curr = []
        print(burst)
        for i in range(len(burst.charBurst)):
            curr_burst = burst.charBurst[i]
            if curr_burst[0] in  ["⇦", "⇨", "⇧", "⇩", "⏎", "⌫"]:
                curr = curr_burst
                curr_bust_col = get_burst(curr[0])
                #print(burst.n_burst, curr[0], curr[1], curr[2], curr_bust_col)
                burst_part =  Row(id=burst.id, control=burst.control, tool=burst.tool, 
                                    n_burst=burst.n_burst, burstStart=burst.burstStart, 
                                    burstDur=burst.burstDur, pauseDur=burst.pauseDur, 
                                    cycleDur=burst.cycleDur, burstPct=burst.burstPct, pausePct=burst.pausePct, 
                                    burstLen=burst.burstLen, burst=curr_bust_col, posStart=curr[1], posEnd=curr[2], 
                                    docLen=burst.docLen, categ=burst.categ, charBurst=curr[0], ratio = burst.ratio)
                list_burst.rows.append(burst_part)
            else:
                list_curr.append(curr_burst)
                if i == (len(burst.charBurst) - 1):
                    curr = "".join([x[0] for x in list_curr])
                    curr_bust_col = get_burst(curr)
                    posStart = list_curr[0][1]
                    posEnd = list_curr[-1][2]
                    #print(burst.n_burst, curr, posStart, posEnd, curr_bust_col)
                else: 
                    next_part = burst.charBurst[i+1]
                    if next_part[0] in ["⇦", "⇨", "⇧", "⇩", "⏎", "⌫"]:
                        curr = "".join([x[0] for x in list_curr])
                        print(list_curr)
                        curr_bust_col = get_burst(curr)
                        posStart = list_curr[0][1]
                        posEnd = list_curr[-1][2]
                        #print("euh", burst.n_burst, curr, posStart, posEnd, curr_bust_col)
                    else:
                        continue

                burst_part = Row(id=burst.id, control=burst.control, tool=burst.tool, 
                                n_burst=burst.n_burst, burstStart=burst.burstStart, 
                                burstDur=burst.burstDur, pauseDur=burst.pauseDur, 
                                cycleDur=burst.cycleDur, burstPct=burst.burstPct, pausePct=burst.pausePct,
                                burstLen=burst.burstLen, burst=curr_bust_col, posStart=posStart, posEnd=posEnd, 
                                docLen=burst.docLen, categ=burst.categ, charBurst=curr, ratio = burst.ratio)
                list_burst.rows.append(burst_part)
                list_curr.clear()

        bursts.bursts.append(list_burst)
    


    return bursts

def get_categories(bursts):

    list_intervals = []
    for index in range(len(bursts.bursts)):
        burst = bursts.bursts[index] 
        # if index == 0:
        #     print(burst)
        intervals_burst = []  
        for i in range(len(burst.rows)):
            interval_row = ()
            row = burst.rows[i]
            # if i == 0:
            #     print(row)
            if row.charBurst != "⇦" and row.charBurst != "⇨" and row.charBurst != "⇧" and row.charBurst != "⇩" and row.charBurst !=  "⏎" and row.charBurst != "∅":
                interval_row = (int(row.posStart), int(row.posEnd))
                intervals_burst.append(interval_row)
 
            if index == 0:
                row.categ = "P"
            else:
                for interval in list_intervals[-1]:
                    if row.posStart >= interval[0] and row.posStart < interval[1]:
                        row.categ = "RB"
                        break
        
                for burst_intervals in list_intervals[:-1]:
                    for interval in burst_intervals:
                        if row.posStart >= interval[0] and row.posStart < interval[1]:
                            row.categ = "R"
                            break
                
                if row.categ == "":
                    row.categ = "P"
        
        list_intervals.append(intervals_burst)      

# def get_categories(bursts, list_intervals):

#     # Bursts and list_intervals => same length
#     for index in range(len(bursts.bursts)):
#         burst = bursts.bursts[index] 
#         for i in range(len(burst.rows)):
#             row = burst.rows[i]
#             print(row)
               

def get_burst(charBurst):
### Cette fonction permet de créer la ligne "Burst du fichier csv"y
    ### Pour les cas ou un burst est une suite de caractères identiques
    # Le burst renvoyé est vide sauf si on a un espace ou un carac
    charBurst = "".join([x[0] for x in charBurst])
    set_char = set(charBurst)
    if len(set_char) == 1:
        for char in set_char:
            if char in ["⇦", "⇨", "⇧", "⇩", "⌫", "⏎", "∅", "⇪"]:
                burst = ""
                return burst
            elif char == "␣":
                burst = " "
                return burst
    if charBurst[0] == "⌫":
        while charBurst[0] == "⌫":
            new_burst = charBurst[1:]
            charBurst = new_burst

    while True:

        if not charBurst or charBurst[-1] != "⌫":
            break

        count = 0
        i = -1
        while i >= -len(charBurst) and charBurst[i] == "⌫":
            count += 1
            i -= 1
        
        deletions = count * 2
        charBurst = charBurst[:-deletions]
    
    
    
    ### DONC ICI !!! LANCE DIRECT ET TU VERRAS QUE LES ESPACES DE FIN SONT EFFACÉS MAIS 
    ### QUE APRÈS IL Y A D'AUTRES ESPACES QUI DEVIENNENT LES ESPACES DE FIN !!
    ### PLUS REGARDE LES DELETE CHARACTERS GURL ! POUR CETTE FONCTION C'EST IMPORTANT


    burst = ""
    if len(charBurst) > 1:
        for i in range(len(charBurst)):
            if charBurst[i] == "⌫":
                if i<len(charBurst):
                    if charBurst[i+1] != "⌫" and charBurst[i-1] != "⌫":
                        burst = burst[:-1]
                        i += 1
                    elif charBurst[i+1] == "⌫" and charBurst[i-1] != "⌫":
                        count = 0
                        j = i
                        while j < len(charBurst) and charBurst[j] == "⌫":
                            count += 1
                            j += 1
                        burst = burst[:-count]
                        i = j
            elif charBurst[i] in ["⇦", "⇨", "⇧", "⇩", "⏎", "∅", "⇪"]:
                burst += "" 
            elif charBurst[i] == "␣":
                burst += " "
            else:
                burst += charBurst[i]

    else:
        if charBurst != "":
            if charBurst[0] in ["⇦", "⇨", "⇧", "⇩", "⌫", "⏎", "∅", "⇪"]:
                burst = ""
            elif charBurst[0] == "␣":
                burst = " "
            else:
                burst = charBurst[0]
        else:
            burst = ""
    
    return burst
        

def create_csv(table_path, list_all_bursts):

    with open(f"{table_path}.csv", "w") as file:
        structure = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["ID", "control", "tool", "n_burst", "burstStart", "burstDur", "pauseDur", "cycleDur", "burstPct", "pausePct", "burstLen", "burst", "posStart", "posEnd", "docLen", "categ", "charBurst", "ratio"])
        for bursts in list_all_bursts:
            for Burst in bursts.bursts: 
                for row in Burst.rows:
                    if row.charBurst != "⇦" and row.charBurst != "⇨" and row.charBurst != "⇧" and row.charBurst != "⇩" and row.charBurst !=  "⏎" and row.charBurst != "∅":
                        structure.writerow([row.id, row.control, row.tool, row.n_burst, row.burstStart, row.burstDur, row.pauseDur, row.cycleDur, row.burstPct, row.pausePct, row.burstLen, row.burst, row.posStart, row.posEnd, row.docLen, row.categ, row.charBurst, row.ratio])
                        print(f"{row.id}\t{row.control}\t{row.tool}\t{row.n_burst}\t{row.burstStart}\t{row.burstDur}\t{row.pauseDur}\t{row.cycleDur}\t{row.burstPct}\t{row.pausePct}\t{row.burstLen}\t{row.burst}{row.posStart}\t{row.posEnd}\t{row.docLen}\t{row.charBurst}\t{row.ratio}")

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
    # parser.add_argument("-t", "--thresold", required=True, type=float, 
    #                     help="""You can choose the thresold used to divide our texts into bursts.\n
    #                     If you choose 1.5 for instance, our texts will be divided into bursts based on a pause\n
    #                     longer than 1.5s in-between two charaters.""" )
    
    args = parser.parse_args()
    
    if args.corpus == "planification":
        corpus_path = ("../data/idfx/planification")
    elif args.corpus == "formulation":
        corpus_path = ("../data/idfx/formulation")
    elif args.corpus == "revision":
        corpus_path = ("../data/idfx/revision")
    elif args.corpus == "test":
        corpus_path = ("../data/idfx/test")

    files_list = get_idfx_files(corpus_path)
    list_all_bursts = []
    for file in files_list:
        soup = get_file_content(f"{corpus_path}/{file}")
        raw_rows = get_burst_rows(soup, file) 
        bursts = divide_bursts(raw_rows)
        get_categories(bursts)
        list_all_bursts.append(bursts)

    create_csv(f"../data/tables/{args.corpus}", list_all_bursts)




    # soup, file_name = open_idfx_file("../data/idfx/S24.idfx")
    # raw_rows = get_burst_rows(soup, file_name)
    # bursts = divide_bursts(raw_rows)
    # list_intervals = get_intervals(bursts)
    # create_csv(bursts)

if __name__ == "__main__":
    main()
