from main_data import *
import argparse

def longueurs(reconstructed_texts):
    """This function returns informations about the length of each text."""

    liste_longueur_par_texte = []
    liste_longueur_par_texte_expert = []
    liste_longueur_par_texte_non_expert = []

    for texte in liste_textes:
        with open(f"../textes_finaux/{texte}", "r") as file:
            contenu = file.read()
            compteur = 0
            for char in contenu:
                if char.isalnum() or char.isspace():
                    compteur += 1
        
        liste_longueur_par_texte.append(compteur)
        if "+" in texte:
            liste_longueur_par_texte_expert.append(compteur)
        else:
            liste_longueur_par_texte_non_expert.append(compteur)
    
    longueur_totale_textes = sum(liste_longueur_par_texte)
    longueur_totale_textes_expert = sum(liste_longueur_par_texte_expert)
    longueur_totale_textes_non_expert = sum(liste_longueur_par_texte_non_expert)
    print(longueur_totale_textes, longueur_totale_textes_expert, longueur_totale_textes_non_expert)
    return liste_longueur_par_texte, liste_longueur_par_texte_expert, liste_longueur_par_texte_non_expert, longueur_totale_textes, longueur_totale_textes_expert, longueur_totale_textes_non_expert


def expertise(liste_textes):

    nbr_textes = 0
    nbr_textes_experts = 0
    nbr_textes_non_experts = 0

    for fichier in liste_textes:
        if "+" in fichier:
            nbr_textes_experts += 1
        else:
            nbr_textes_non_experts += 1
        nbr_textes += 1

    return nbr_textes, nbr_textes_experts, nbr_textes_non_experts


def main():


    parser = argparse.ArgumentParser(
    description="""This script uses the csv file created thanks to retrieval.py.
                For each user in the csv file, each row is processed to re-create
                in real time what was written or deleted by the user.
                For each text/user in the csv file, a txt file is created in the 
                saved_texts folder. The saved text is the final version of the text as
                it was saved by the user during the experiment"""
    )
    parser.add_argument("-e", "--expertise", required=True, type=str, choices=["+", "-","both"],
                        help="""Choose among the levels of expertise to get informations about it.""")
  
    reconstructed_texts = get_reconstructed_texts("../../data/reconstructed_texts_behaviours")

if __name__ == "__main__":
    main()