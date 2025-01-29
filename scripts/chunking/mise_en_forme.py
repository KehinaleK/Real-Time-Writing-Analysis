import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def joli_print_xml(fichier):
 
    tree = ET.parse(fichier)
    root = tree.getroot()

    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    parsed_str = minidom.parseString(xml_str)
    pretty_str = parsed_str.toprettyxml(indent="  ")

    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(pretty_str)

def obtenir_fichiers(dossier):

    for fichier in os.listdir(dossier):
        fichier_chemin = os.path.join(dossier, fichier)
        joli_print_xml(fichier_chemin)
      
          

if __name__ == "__main__":
    dossier = "sem_output"  
    obtenir_fichiers(dossier)
