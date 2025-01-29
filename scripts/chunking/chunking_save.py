import os 
import subprocess
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json

def extract_text(file):

    with open(file, "r") as f:
        text = f.read()

    return text


def place_placeholders(text, file):
 
    placeholders = {
    "~": "\u200B",  # Zero-width space
    "{": "\u200C",  # Zero-width non-joiner
    "}": "\u200D",  # Zero-width joiner
    "<": "\u2060",  # Word joiner
    ">": "\u2061",   # Function application
    "|": "\uFEFF"
    }

    for symbol, placeholder in placeholders.items():
        text = text.replace(symbol, placeholder)
    
    with open(f"texts_with_placeholders/{file}", "w") as f:
        f.write(text)

def sem_chunking(file):

    home_dir = os.path.expanduser("~")
    command = f"python -m sem tagger {home_dir}/sem_data/resources/master/fr/chunking.xml {file} -o sem_output"

    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:

        print(f"Error: {e}")
        print(f"Command Output: {e.output}")

def get_corresponding_xml_file(file):
    
    chemin_dossier_textes_chunks = os.listdir("sem_output")
    liste_fichiers_chunks = []

    for fichier_chunk_pipes in chemin_dossier_textes_chunks:
        liste_fichiers_chunks.append(fichier_chunk_pipes)
    
    num_text = os.path.splitext(file)[0]
    regex = re.compile(re.escape(num_text) + r'\.analec\.tei\.xml')

    for fichier_chunk_pipes in liste_fichiers_chunks:
        if regex.match(fichier_chunk_pipes):
            return fichier_chunk_pipes, num_text


def clean_xml(file):
 
    tree = ET.parse(file)
    root = tree.getroot()

    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    parsed_str = minidom.parseString(xml_str)
    pretty_str = parsed_str.toprettyxml(indent="  ")

    with open(file, 'w', encoding='utf-8') as f:
        f.write(pretty_str)


def extract_xml_infos(fichier_chunk_pipes):

    with open (f"sem_output/{fichier_chunk_pipes}", 'r') as tei: 
        donnees = tei.read()
        soup = BeautifulSoup (donnees, 'lxml-xml')
      
    liste_chunks = []
    id_to_end_tag_map = {}  

    for end_tag in soup.find_all("ns0:anchor", subtype="UnitEnd"):
        id_to_end_tag_map[end_tag["xml:id"].split("-end")[0]] = end_tag

    for element in soup.find_all("ns0:anchor"):
        if element["subtype"] == "UnitStart":
            id = element["xml:id"].split("-start")[0]
            
            end_tag = id_to_end_tag_map.get(id)

            if end_tag:
                parties = []
                chunk_actuel_reste = end_tag.next_sibling
             
                propre = chunk_actuel_reste.replace("\n", " ").strip()
               
                if propre:
                    parties.append(propre)
                
               
                chunk_actuel = element.next_sibling.strip()
                chunk_reste_texte = "".join(parties)
                if chunk_reste_texte:
                    chunk_texte = chunk_actuel + " " + chunk_reste_texte
                    chunk_texte_balise = f"{chunk_texte}"
                else:
                    chunk_texte = chunk_actuel
                    chunk_texte_balise = f"{chunk_texte}"

                chunk_type = id.split("u-")[1].split("-")[0]
                liste_chunks.append((chunk_texte_balise, chunk_type))
   
    return liste_chunks


def gestion_pipes_accolades(liste_chunks):
    
    ("Nous voilà dans gestion_pipes_accolades")
    liste_clean = []
    sauter = False
    for i in range(len(liste_chunks)):
        # Permet de prendre en compte le saut ou non d'une itération
        if sauter == True:
            sauter = False
            continue
        ## GESTION DES PIPES 
        if liste_chunks[i][0] == "|":
            liste_clean.append((liste_chunks[i][0], liste_chunks[i][1]))
            continue
        
        #print(liste_chunks[i]) 
        #print(i)

        if liste_chunks[i][0] == "{|":

            chunk_clean = liste_chunks[i][0][1]
            next_chunk = "{" + liste_chunks[i+1][0]
            liste_clean.pop(-1)
            liste_clean.append((chunk_clean, "PAUSE"))
            liste_clean.append((next_chunk, liste_chunks[i+1][1]))
            sauter = True

            continue

        if liste_chunks[i][0][0] == "|" and liste_chunks[i][0][-1] != "|":
            chunk_clean = liste_chunks[i][0][1:].strip()
            liste_clean.append(("|", "PAUSE"))
            liste_clean.append((chunk_clean, liste_chunks[i][1]))
            continue

        if liste_chunks[i][0][0] != "|" and liste_chunks[i][0][-1] == "|":
            chunk_clean = liste_chunks[i][0][:-1].strip()
            liste_clean.append((chunk_clean, liste_chunks[i][1]))
            liste_clean.append(("|", "PAUSE"))
            continue

        if liste_chunks[i][0][0] == "|" and liste_chunks[i][0][-1] == "|":
            chunk_clean = liste_chunks[i][0][1:-1].strip()
            liste_clean.append(("|", "PAUSE"))
            liste_clean.append((f"{chunk_clean}", liste_chunks[i][1]))
            liste_clean.append(("|", "PAUSE"))
            continue


        ## Gestion des accolades
        if liste_chunks[i][0] == "{":
            chunk_next = "{" + liste_chunks[i+1][0].strip()
            liste_clean.append((chunk_next, liste_chunks[i+1][1]))
            sauter = True
            continue
        if liste_chunks[i][0] == "}":
            if "{" or "}" in liste_clean(-1):
                # Obligé de mettre des conditions supplémentaires car :
                # ('[actu}| {]', 'PP'), ('[elle]', 'NP'), ('[}]', 'VN'),
                # Dans ce cas, si je modifie elle en y rajoutant "{" alors j'ai :
                # ('[actu}|]', 'PP'), ('[{elle]', 'NP'), ('[}]', 'VN'),
                # Seulement, lorsqu'on va prendre le "}" seul, alors on va chercher
                # l'élément i-1, donc "elle" et lui coller }, mais sans la condition if nous aurions :
                # ('[actu}|]', 'PP'), ('[elle}]', 'NP'),
                # On perd l'accolade précédemment attribuée car on prend un élément de 
                # liste_chunks et non pas de liste_clean
                chunk_prev = liste_clean[-1][0].strip() + "}"
                liste_clean.pop(-1)
                liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                continue
            else:
                chunk_prev = liste_chunks[i-1][0][:-1].strip() + "}" 
                liste_clean.pop(-1)
                liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                continue
        if liste_chunks[i][0][0] == "}" and liste_chunks[i][0][-1] != "{":
            if "{" or "}" in liste_clean(-1):
                chunk_prev = liste_clean[-1][0][:-1].strip() + "}"
                chunk_clean = liste_chunks[i][0][1:].strip()
                liste_clean.pop(-1)
                liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                liste_clean.append((chunk_clean, liste_chunks[i][1]))
                continue
            else:
                chunk_prev = liste_chunks[i-1][0][:-1].strip() + "}" 
                chunk_clean = liste_chunks[i][0][1:].strip()
                liste_clean.pop(-1)
                liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                liste_clean.append((chunk_clean, liste_chunks[i][1]))
                continue

        if liste_chunks[i][0][0] != "}" and liste_chunks[i][0][-1] == "{":
            chunk_next = "{" + liste_chunks[i+1][0]
            # De base tu avais liste_chunks[i+1][0][1:-1] + "{" + liste_chunks[i+1][0][1:]
            # Mais ça ne marche pas quand tu as { en frontière et une pause après. Faire attention à ça parce que du coup pour l'instant
            # Tu as des éléments qui sont pit-être chelous. Attention !
            chunk_clean = liste_chunks[i][0][:-1].strip()
            liste_clean.append((chunk_clean, liste_chunks[i][1])) 
            liste_clean.append((chunk_next, liste_chunks[i+1][1]))
            sauter = True
            continue

        if liste_chunks[i][0][0] == "}" and liste_chunks[i][0][-1] == "{":
            chunk_clean = liste_chunks[i][0][1:-1].strip()
            if chunk_clean.isspace() or chunk_clean == "":
                if "{" or "}" in liste_clean(-1):
                    chunk_prev = liste_clean[-1][0].strip() + "}"
                    chunk_next = "{" + liste_chunks[i+1][0].strip()
                    liste_clean.pop(-1)
                    liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                    liste_clean.append((chunk_next, liste_chunks[i+1][1]))
                    sauter = True # Pour skipper la prochaine itération et pas ajouter deux fois le même chunk ! 
                    continue
                else:
                    chunk_prev = liste_chunks[i-1][0].strip() + "}" 
                    chunk_next =  "{" + liste_chunks[i+1][0].strip()
                    liste_clean.pop(-1)
                    liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                    liste_clean.append((chunk_next, liste_chunks[i+1][1]))
                    sauter = True # Pour skipper la prochaine itération et pas ajouter deux fois le même chunk ! 
                    continue
            else:
                if "{" or "}" in liste_clean(-1):
                    chunk_prev = liste_clean[-1][0].strip() + "}"
                    chunk_next = "{" + liste_chunks[i+1][0].strip()
                    liste_clean.pop(-1)
                    liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                    liste_clean.append((f"{chunk_clean}", liste_chunks[i][1]))
                    liste_clean.append((chunk_next, liste_chunks[i+1][1]))
                    sauter = True
                    continue
                else:
                    chunk_prev = liste_chunks[i-1][0].strip() + "}" 
                    chunk_next = "{" + liste_chunks[i+1][0].strip()
                    liste_clean.pop(-1)
                    liste_clean.append((chunk_prev, liste_chunks[i-1][1]))
                    liste_clean.append((f"{chunk_clean}", liste_chunks[i][1]))
                    liste_clean.append((chunk_next, liste_chunks[i+1][1]))
                    sauter = True
                    continue
        if liste_chunks[i][0][0] == "{" and liste_chunks[i][0][1] == "|":
            new_chunk = "|" + "{" + liste_chunks[i][0][2:]
            liste_clean.append((new_chunk, liste_chunks[i][1]))
            continue

        if liste_chunks[i][0][-1] == "{" and liste_chunks[i][0][-2] == "|":
            new_chunk = liste_chunks[i][0][:-2] + "}" + "|"
            liste_clean.append((new_chunk, liste_chunks[i][1]))
       
        else:
            liste_clean.append((liste_chunks[i][0], liste_chunks[i][1]))
            i += 1

    changements = 0
    for chunk, type in liste_chunks:
        if chunk != "|" and chunk != "{" and chunk != "}":
            if chunk[0] == "|":
                #print(chunk)
                changements += 1
            if chunk[0] == "}":
                #print(chunk)
                changements += 1
            if chunk[-1] == "|":
                #print(chunk)
                changements += 1
            if chunk[-1] == "{":
                changements += 1
    #print(changements)
    # print(liste_chunks)
    # print("Nous avons fait ce changement")
    # print(liste_clean)
    # print(f"Il ya {changements} changements à faire. Allons dans gestion_recursive.")
    #print(liste_clean)
    return liste_clean, changements

        
def gestion_recursives(liste_chunks):
    # Pour avoir les pipes en dehors des chunks quand ils sont en frontières
    # EVENTUELLEMENT GÉRER CAS OU L'ACCOLADE OU QUOI EST MIS AVANT LE CHUNK MAIS NORMALEMENT JAMAIS

    changements = True
   
    #print("C'est reparti pour obtenir_liste_clean")
    while changements:
       liste_chunks, changements = gestion_pipes_accolades(liste_chunks)
       if changements == 0:
           changements = False
    
    return liste_chunks


def obtenir_texte_final(liste_finale):

    texte_final = ""
    for chunk, type in liste_finale:
        texte_final += f"[{chunk}]"
    return texte_final


def replace_placeholders(liste_chunks):

    placeholders = {
    "~": "\u200b",  # Zero-width space
    "{": "\u200c",  # Zero-width non-joiner
    "}": "\u200d",  # Zero-width joiner
    "<": "\u2060",  # Word joiner
    ">": "\u2061",   # Function application
    "|": "\ufeff"
    }

    for i, chunk_tuple in enumerate(liste_chunks):
        chunk = chunk_tuple[0]  
        chunk_type = chunk_tuple[1]  
        for symbol, placeholder in placeholders.items():
            chunk = chunk.replace(placeholder, symbol) 

        liste_chunks[i] = (chunk, chunk_type)

    return liste_chunks

def save_list_chunks(dict_lists):

    
    json_string = json.dumps(dict_lists, indent=4)

    with open('../../data/list_chunks/chunks.json', 'w') as json_file:
        json.dump(dict_lists, json_file, indent=4)

def main():

    folder = os.listdir("../../data/reconstructed_texts_behaviours")
    files = sorted(folder, key=lambda x: (x[1], int(x[3:x.find('.')]), x[0]))
    dict_lists = {}
    for file in files:
        text = extract_text(f"../../data/reconstructed_texts_behaviours/{file}")
        place_placeholders(text, file)
        print(f"Punctuations have been replaced by invisible characters in file {file}...")
        sem_chunking(f"texts_with_placeholders/{file}")
        print(f"File {file} has been chunked by SEM..")
        fichier, num = get_corresponding_xml_file(file)
        clean_xml(f"sem_output/{fichier}")
        chunks_list = extract_xml_infos(fichier)
        liste_chunks = replace_placeholders(chunks_list)
        print(liste_chunks)
        liste_clean = gestion_recursives(liste_chunks)
        dict_lists[file] = liste_clean
        text_final = obtenir_texte_final(liste_clean)
        print(text_final)
    
    save_list_chunks(dict_lists)
    return dict_lists


if __name__ == "__main__":
    main()