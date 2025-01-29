from main_data import *
import argparse
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter


def single_action_insertions(reconstructed_texts_dict):

    liste_sai_par_texte = []
    liste_sai_par_texte_experts = []
    liste_sai_par_texte_non_experts = []


    lettre_ajoutee =  r'<\|?\s*[^"~<>\s]{1,2}\s*\|?>'
    effacement_ajoute = r"<\|?\s*~\s*\|?>"
    # mot_insere = r"\{\s*[^a-zA-ZÀ-ÿ]*([a-zA-ZÀ-ÿ]+)[^a-zA-ZÀ-ÿ]*\s*\}" #compte les trucs genre " d"
    # chaine_inseree = r"\{([\wÀ-Ÿ]+\s+[\wÀ-Ÿ]+)+\}"


    for id, text in reconstructed_texts_dict.items():
    
        erreur = 0
        #print(contenu)
        la = re.findall(lettre_ajoutee, text)
        efa = re.findall(effacement_ajoute, text)
        #mi = re.findall(mot_insere, text)
        # print(id)
        # print(la)
        # #print(mi)
        # print(efa)
        #ci = re.findall(chaine_inseree, text)
        #print(ci)

        if len(la) > 0:
            erreur += len(la)
        if len(efa) > 0:
           erreur += len(efa)
        #if len(ci) > 0:
        #    erreur += len(ci)

        if "-" in id:
            liste_sai_par_texte_experts.append(erreur)
        else:
            liste_sai_par_texte_non_experts.append(erreur)
        liste_sai_par_texte.append(erreur)
        
        sai_total_textes = sum(liste_sai_par_texte)
    sai_total_textes_experts = sum(liste_sai_par_texte_experts)
    sai_total_textes_non_experts = sum(liste_sai_par_texte_non_experts)

    return liste_sai_par_texte, liste_sai_par_texte_experts, liste_sai_par_texte_non_experts, sai_total_textes, sai_total_textes_experts, sai_total_textes_non_experts
        

def sai_comptes_par_types(reconstructed_texts_dict):


    
    lettre_ajoutee =  r'<\|?\s*[^"~<>\s]{1,2}\s*\|?>'
    effacement_ajoute = r"<\|?\s*~\s*\|?>"

    dico_sai_compte_texte = {
        "LA" : [],
        "EFA" : []
    }

    dico_sai_compte_texte_experts = {
        "LA" : [],
        "EFA" : []
    }


    dico_sai_compte_texte_non_experts = {
        "LA" : [],
        "EFA" : []
    }
    for id, text in reconstructed_texts_dict.items():



       
     
        la = re.findall(lettre_ajoutee, text)
        efa = re.findall(effacement_ajoute, text)
        
        if "-" in id:
            dico_sai_compte_texte_experts["LA"].extend(la)
            dico_sai_compte_texte_experts["EFA"].extend(efa)

        else:
            dico_sai_compte_texte_non_experts["LA"].extend(la)
            dico_sai_compte_texte_non_experts["EFA"].extend(efa)
       

        dico_sai_compte_texte["LA"].extend(la)
        dico_sai_compte_texte["EFA"].extend(efa)


    return dico_sai_compte_texte, dico_sai_compte_texte_experts, dico_sai_compte_texte_non_experts




    

 # print(id)
        # print(la)
        # #print(mi)
        # print(efa)


def main():

    reconstructed_texts_dict = get_reconstructed_texts("../../data/reconstructed_texts_behaviours")
    chunk_lists_dict = get_chunk_lists("../../data/list_chunks/chunks.json")
    liste_sai_par_texte, liste_sai_par_texte_experts, liste_sai_par_texte_non_experts, sai_total_textes, sai_total_textes_experts, sai_total_textes_non_experts = single_action_insertions(reconstructed_texts_dict)
    dico_sai_compte_texte, dico_sai_compte_texte_experts, dico_sai_compte_texte_non_experts = sai_comptes_par_types(reconstructed_texts_dict)
    print("What number do you want to have ?\nPress the corresponding number.")
    print("1 - Numbers on single action insertions.")
    print("2 - Most common single action insertions.")
    #print("3 - Number of superpositions between chunks and pauses.")
    #print("4 - Most commun chunk types involved in chunk/pause superpositions. ")


    choice = input("")
    # expertise = args.expertise

    if choice == "1":
        number_non_expert = sai_total_textes_non_experts
        mean_non_expert = number_non_expert / len(liste_sai_par_texte_non_experts)
        non_expert_median = np.median(liste_sai_par_texte_non_experts)
        number_expert = sai_total_textes_experts
        mean_expert = number_expert / len(liste_sai_par_texte_experts)
        expert_median = np.median(liste_sai_par_texte_experts)
        number = sai_total_textes
        mean = number / len(liste_sai_par_texte)
        median = np.median(liste_sai_par_texte)

        print(f"Number of single action insertions in the entire corpus : {number}.")
        print(f"Mean of single action insertions per text : {mean}.")
        print(f"Median of all single action insertions : {median}.")
        print(f"Number of single action insertions in the expert texts : {number_expert}.")
        print(f"Mean of single action insertions per expert text : {mean_expert}.")
        print(f"Median of single action insertions in expert texts : {expert_median}.")
        print(f"Number of single action insertions in the non-expert texts : {number_non_expert}.")
        print(f"Mean of single action insertions per non-expert text : {mean_non_expert}.")
        print(f"Median of single action insertions in non-expert texts : {non_expert_median}.")

    if choice == "2":

        common_texte = {
            "LA": Counter(dico_sai_compte_texte["LA"]).most_common(10),
            "EFA": Counter(dico_sai_compte_texte["EFA"]).most_common(10)
        }
        
        common_expert_texte = {
            "LA": Counter(dico_sai_compte_texte_experts["LA"]).most_common(10),
            "EFA": Counter(dico_sai_compte_texte_experts["EFA"]).most_common(10)
        }

        common_non_expert_texte = {
            "LA": Counter(dico_sai_compte_texte_non_experts["LA"]).most_common(10),
            "EFA": Counter(dico_sai_compte_texte_non_experts["EFA"]).most_common(10)
        }


        print("Top 10 most common single action insertions (all texts):")
        print("Added characters :")
        for la, count in common_texte["LA"]:
            print(f"  {la}: {count} occurrences")

        print("Inserted deletions:")
        for efa, count in common_texte["EFA"]:
            print(f"  {efa}: {count} occurrences")

        print("\nTop 10 most common single action insertions (expert texts):")
        print("Added characters :")
        for la, count in common_expert_texte["LA"]:
            print(f"  {la}: {count} occurrences")

        print("Inserted deletions :")
        for efa, count in common_expert_texte["EFA"]:
            print(f"  {efa}: {count} occurrences")

        print("\nTop 10 most common single action insertions (non-expert texts):")
        print("Added characters :")
        for la, count in common_non_expert_texte["LA"]:
            print(f"  {la}: {count} occurrences")

        print("Inserted deletions :")
        for efa, count in common_non_expert_texte["EFA"]:
            print(f"  {efa}: {count} occurrences")


if __name__ == "__main__":
    main()