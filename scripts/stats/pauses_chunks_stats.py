from main_data import *
import argparse
import numpy as np
import matplotlib.pyplot as plt


def nbrpauses(reconstructed_texts_dict):
    """Cette fonction permet de renvoyer les valeurs concernant le nombre de pauses présentes dans notre corpus."""

    liste_pauses_par_texte = []
    liste_pauses_par_texte_expert = []
    liste_pauses_par_texte_non_expert = []
    
    for id, text in reconstructed_texts_dict.items():
        compteur = 0
        for char in text:
            if char == "|":
                compteur += 1

        liste_pauses_par_texte.append(compteur)
        if "-" in id:
            liste_pauses_par_texte_expert.append(compteur)
        else:
            liste_pauses_par_texte_non_expert.append(compteur)
    
    pauses_total_textes = sum(liste_pauses_par_texte)
    pauses_total_textes_experts = sum(liste_pauses_par_texte_expert)
    pauses_total_textes_non_experts = sum(liste_pauses_par_texte_non_expert)

    return liste_pauses_par_texte, liste_pauses_par_texte_expert, liste_pauses_par_texte_non_expert, pauses_total_textes, pauses_total_textes_experts, pauses_total_textes_non_experts

def chunks(chunk_lists_dict):
    """Cette fonction permet de renvoyer les valeurs concernant le nombre de chunks de notre corpus."""

    dico_chunks_par_texte = {
        '__UNKNOWN__': [],
        "VN": [],
        "AP" : [],
        "AdP" : [],  
        "PP": [],  
        "CONJ": [],
        "NP" : [],
    }

    dico_chunks_par_texte_experts = {
         '__UNKNOWN__': [],
        "VN": [],
        "AP" : [],
        "AdP" : [],  
        "PP": [],  
        "CONJ": [],
        "NP" : [],
    }

    dico_chunks_par_texte_non_experts = {
         '__UNKNOWN__': [],
        "VN": [],
        "AP" : [],
        "AdP" : [],  
        "PP": [],  
        "CONJ": [],
        "NP" : [],
    }
    
    chunks_total_textes = 0
    chunks_total_textes_experts = 0
    chunks_total_textes_non_experts = 0

    chunks = 0
    chunks_textes_experts = 0
    chunks_textes_non_experts = 0
   

    for id, list_chunks in chunk_lists_dict.items():

        unk = 0
        vn = 0
        ap = 0
        adp = 0
        pp = 0
        conj = 0
        np = 0

        for chunk, type in list_chunks:

            chunks += 1

            if type == "__UNKNOWN__":
                unk += 1
            elif type == "VN":
                vn += 1 
            elif type == "AP":
                ap += 1
            elif type == "AdP":
                adp += 1
            elif type == "PP":
                pp += 1
            elif type == "CONJ":
                conj += 1
            elif type == "NP":
                np += 1
            
            if "-" in id:
                chunks_textes_experts += 1
    
            elif "+" in id: 
                chunks_textes_non_experts += 1
               
        if "-" in id:
            dico_chunks_par_texte_experts["__UNKNOWN__"].append(unk)
            dico_chunks_par_texte_experts["VN"].append(vn)
            dico_chunks_par_texte_experts["AP"].append(ap)
            dico_chunks_par_texte_experts["AdP"].append(adp)
            dico_chunks_par_texte_experts["PP"].append(pp)
            dico_chunks_par_texte_experts["CONJ"].append(conj)
            dico_chunks_par_texte_experts["NP"].append(np)
        elif "+" in id:
            dico_chunks_par_texte_non_experts["__UNKNOWN__"].append(unk)
            dico_chunks_par_texte_non_experts["VN"].append(vn)
            dico_chunks_par_texte_non_experts["AP"].append(ap)
            dico_chunks_par_texte_non_experts["AdP"].append(adp)
            dico_chunks_par_texte_non_experts["PP"].append(pp)
            dico_chunks_par_texte_non_experts["CONJ"].append(conj)
            dico_chunks_par_texte_non_experts["NP"].append(np)
            
        chunks_total_textes += chunks
        chunks_total_textes_experts += chunks_textes_experts
        chunks_total_textes_non_experts += chunks_textes_non_experts

        dico_chunks_par_texte["__UNKNOWN__"].append(unk)
        dico_chunks_par_texte["VN"].append(vn)
        dico_chunks_par_texte["AP"].append(ap)
        dico_chunks_par_texte["AdP"].append(adp)
        dico_chunks_par_texte["PP"].append(pp)
        dico_chunks_par_texte["CONJ"].append(conj)
        dico_chunks_par_texte["NP"].append(np)

    dico_total_chunks = {key: sum(value) for key, value in dico_chunks_par_texte.items()}
    dico_total_chunks_experts =  {key: sum(value) for key, value in dico_chunks_par_texte_experts.items()}
    dico_total_chunks_non_experts =  {key: sum(value) for key, value in dico_chunks_par_texte_non_experts.items()}
        
    return dico_chunks_par_texte, dico_chunks_par_texte_experts, dico_chunks_par_texte_non_experts, dico_total_chunks, dico_total_chunks_experts, dico_total_chunks_non_experts, chunks_total_textes, chunks_total_textes_experts, chunks_total_textes_non_experts

def superpositions(chunk_lists_dict):

    ### Ici, on vient créer comme un concordancier ! On peut le visualiser en printant ou en le mettant dans un fichier txt.
    ### Pour chaque fichier, on crée une liste de tuple. Cette tuple contient le chunk précédent la pause,
    ## le chunk de la pause et le chunk suivant la pause. 
    # On a un dico_concordanciers qui a comme clés les titres de textes et en valeur le concordancier du fichier concerné.
    # On utilise ce dico pour pouvoir faire un compte des types de chunks le plus souvent avant et après des erreurs

    liste_pauses_superposees_par_texte = []
    liste_pauses_superposees_par_texte_experts = []
    liste_pauses_superposees_par_texte_non_experts = []

    dico_concordanciers_pauses = defaultdict(list)
    for id, list_chunks in chunk_lists_dict.items():
        pause_superposee = 0
        concordancier = []
        for i in range(len(list_chunks)-1):
            if list_chunks[i][1] == "PAUSE":
                pause_superposee += 1
                # et pour le dernier ? pas important parce que si | à la fin bah bon.
                concordancier.append((list_chunks[i-1], list_chunks[i], list_chunks[i+1]))

        if "-" in id:
            liste_pauses_superposees_par_texte_experts.append(pause_superposee)
        else:
            liste_pauses_superposees_par_texte_non_experts.append(pause_superposee)
        
        liste_pauses_superposees_par_texte.append(pause_superposee)
        dico_concordanciers_pauses[id.strip(".txt")] = concordancier

    pauses_total_superposees = sum(liste_pauses_superposees_par_texte)
    pauses_total_superposees_experts = sum(liste_pauses_superposees_par_texte_experts)
    pauses_total_superposees_non_experts = sum(liste_pauses_superposees_par_texte_non_experts)

    return dico_concordanciers_pauses, liste_pauses_superposees_par_texte, liste_pauses_superposees_par_texte_experts, liste_pauses_superposees_par_texte_non_experts, pauses_total_superposees, pauses_total_superposees_experts, pauses_total_superposees_non_experts


def superpositions_chunks_gauche_droite_liste(dico_concordanciers_pauses):

    liste_superpositions_unknown_gauche = []
    liste_superpositions_unknown_droite = []
    liste_superpositions_vn_gauche = []
    liste_superpositions_vn_droite = []
    liste_superpositions_ap_gauche = []
    liste_superpositions_ap_droite = []
    liste_superpositions_adp_gauche = []
    liste_superpositions_adp_droite = []
    liste_superpositions_pp_gauche = []
    liste_superpositions_pp_droite = []
    liste_superpositions_conj_gauche = []
    liste_superpositions_conj_droite = []
    liste_superpositions_np_gauche = []
    liste_superpositions_np_droite = []
    liste_superpositions_pause_gauche = []
    liste_superpositions_pause_droite = []

    liste_superpositions_unknown_gauche_experts = []
    liste_superpositions_unknown_droite_experts = []
    liste_superpositions_vn_gauche_experts = []
    liste_superpositions_vn_droite_experts = []
    liste_superpositions_ap_gauche_experts = []
    liste_superpositions_ap_droite_experts = []
    liste_superpositions_adp_gauche_experts = []
    liste_superpositions_adp_droite_experts = []
    liste_superpositions_pp_gauche_experts = []
    liste_superpositions_pp_droite_experts = []
    liste_superpositions_conj_gauche_experts = []
    liste_superpositions_conj_droite_experts = []
    liste_superpositions_np_gauche_experts = []
    liste_superpositions_np_droite_experts = []
    liste_superpositions_pause_gauche_experts = []
    liste_superpositions_pause_droite_experts = []

    liste_superpositions_unknown_gauche_non_experts = []
    liste_superpositions_unknown_droite_non_experts = []
    liste_superpositions_vn_gauche_non_experts = []
    liste_superpositions_vn_droite_non_experts = []
    liste_superpositions_ap_gauche_non_experts = []
    liste_superpositions_ap_droite_non_experts = []
    liste_superpositions_adp_gauche_non_experts = []
    liste_superpositions_adp_droite_non_experts = []
    liste_superpositions_pp_gauche_non_experts = []
    liste_superpositions_pp_droite_non_experts = []
    liste_superpositions_conj_gauche_non_experts = []
    liste_superpositions_conj_droite_non_experts = []
    liste_superpositions_np_gauche_non_experts = []
    liste_superpositions_np_droite_non_experts = []
    liste_superpositions_pause_gauche_non_experts = []
    liste_superpositions_pause_droite_non_experts = []

    pls_gauche = 0
    pls_droite = 0

    for key, value in dico_concordanciers_pauses.items():

        superpositions_unknown_gauche = 0
        superpositions_unknown_droite = 0
        superpositions_vn_gauche = 0
        superpositions_vn_droite = 0
        superpositions_ap_gauche = 0
        superpositions_ap_droite = 0
        superpositions_adp_gauche = 0 
        superpositions_adp_droite = 0
        superpositions_pp_gauche = 0
        superpositions_pp_droite = 0
        superpositions_conj_gauche = 0
        superpositions_conj_droite = 0
        superpositions_np_gauche = 0
        superpositions_np_droite = 0
        superpositions_pause_gauche = 0
        superpositions_pause_droite = 0

        superpositions_unknown_gauche_experts = 0
        superpositions_unknown_droite_experts = 0
        superpositions_vn_gauche_experts = 0
        superpositions_vn_droite_experts = 0
        superpositions_ap_gauche_experts = 0
        superpositions_ap_droite_experts = 0
        superpositions_adp_gauche_experts = 0 
        superpositions_adp_droite_experts = 0
        superpositions_pp_gauche_experts = 0
        superpositions_pp_droite_experts = 0
        superpositions_conj_gauche_experts = 0
        superpositions_conj_droite_experts = 0
        superpositions_np_gauche_experts = 0
        superpositions_np_droite_experts = 0
        superpositions_pause_gauche_experts = 0
        superpositions_pause_droite_experts = 0

        superpositions_unknown_gauche_non_experts = 0
        superpositions_unknown_droite_non_experts = 0
        superpositions_vn_gauche_non_experts = 0
        superpositions_vn_droite_non_experts = 0
        superpositions_ap_gauche_non_experts = 0
        superpositions_ap_droite_non_experts = 0
        superpositions_adp_gauche_non_experts = 0 
        superpositions_adp_droite_non_experts = 0
        superpositions_pp_gauche_non_experts = 0
        superpositions_pp_droite_non_experts = 0
        superpositions_conj_gauche_non_experts = 0
        superpositions_conj_droite_non_experts = 0
        superpositions_np_gauche_non_experts = 0
        superpositions_np_droite_non_experts = 0
        superpositions_pause_gauche_non_experts = 0
        superpositions_pause_droite_non_experts = 0

        for contexte in value:
            if contexte[0][1] == "__UNKNOWN__":
                if "-" in key:
                    superpositions_unknown_gauche_experts += 1
                else:
                    superpositions_unknown_gauche_non_experts += 1
                superpositions_unknown_gauche += 1
            elif contexte[0][1] == "VN":
                if "-" in key:
                    superpositions_vn_gauche_experts += 1
                else:
                    superpositions_vn_gauche_non_experts += 1
                superpositions_vn_gauche += 1
            elif contexte[0][1] == "AP":
                if "-" in key:
                    superpositions_ap_gauche_experts += 1
                else:
                    superpositions_ap_gauche_non_experts += 1
                superpositions_ap_gauche += 1 
            elif contexte[0][1] == "AdP":
                if "-" in key:
                    superpositions_adp_gauche_experts += 1
                else:
                    superpositions_adp_gauche_non_experts += 1
                superpositions_adp_gauche += 1
            elif contexte[0][1] == "PP":
                if "-" in key:
                    superpositions_pp_gauche_experts += 1
                else:
                    superpositions_pp_gauche_non_experts += 1
                superpositions_pp_gauche += 1
            elif contexte[0][1] == "CONJ":
                if "-" in key:
                    superpositions_conj_gauche_experts += 1
                else:
                    superpositions_conj_gauche_non_experts += 1
                superpositions_conj_gauche += 1
            elif contexte[0][1] == "NP":
                print("gauche", contexte)
                if "-" in key:
                    superpositions_np_gauche_experts += 1
                else:
                    superpositions_np_gauche_non_experts += 1 
                superpositions_np_gauche += 1
                pls_gauche += 1
            elif contexte[0][1] == "PAUSE":
                if "-" in key:
                    superpositions_pause_gauche_experts += 1
                else:
                    superpositions_pause_gauche_non_experts += 1
                superpositions_pause_gauche += 1
            if contexte[2][1] == "__UNKNOWN__":
                if "-" in key:
                    superpositions_unknown_droite_experts += 1
                else:
                    superpositions_unknown_droite_non_experts += 1
                superpositions_unknown_droite += 1
            elif contexte[2][1] == "VN":
                if "-" in key:
                    superpositions_vn_droite_experts += 1
                else:
                    superpositions_vn_droite_non_experts += 1
                superpositions_vn_droite += 1
            elif contexte[2][1] == "AP":
                if "-" in key:
                    superpositions_ap_droite_experts += 1 
                else:
                    superpositions_ap_droite_non_experts += 1 
                print(key)
                print(contexte)
                superpositions_ap_droite += 1 
            elif contexte[2][1] == "AdP":
                if "-" in key:
                    superpositions_adp_droite_experts += 1
                else:
                    superpositions_adp_droite_non_experts += 1
                superpositions_adp_droite += 1
            elif contexte[2][1] == "PP":
                if "-" in key:
                    superpositions_pp_droite_experts += 1
                else:
                    superpositions_pp_droite_non_experts += 1
                superpositions_pp_droite += 1
            elif contexte[2][1] == "CONJ":
                if "-" in key:
                    superpositions_conj_droite_experts += 1
                else:
                    superpositions_conj_droite_non_experts += 1
                superpositions_conj_droite += 1
            elif contexte[2][1] == "NP":
                print("droite", contexte)
                if "-" in key:
                    superpositions_np_droite_experts += 1
                else:
                    superpositions_np_droite_non_experts += 1
                superpositions_np_droite += 1
                pls_droite += 1
            elif contexte[2][1] == "PAUSE":
                if "-" in key:
                    superpositions_pause_droite_experts += 1
                else:
                    superpositions_pause_droite_non_experts += 1
                superpositions_pause_droite += 1

        liste_superpositions_unknown_gauche.append(superpositions_unknown_gauche)
        liste_superpositions_unknown_droite.append(superpositions_unknown_droite)
        liste_superpositions_vn_gauche.append(superpositions_vn_gauche)
        liste_superpositions_vn_droite.append(superpositions_vn_droite)
        liste_superpositions_ap_gauche.append(superpositions_ap_gauche)
        liste_superpositions_ap_droite.append(superpositions_ap_droite)
        liste_superpositions_adp_gauche.append(superpositions_adp_gauche)
        liste_superpositions_adp_droite.append(superpositions_adp_droite)
        liste_superpositions_pp_gauche.append(superpositions_pp_gauche)
        liste_superpositions_pp_droite.append(superpositions_pp_droite)
        liste_superpositions_conj_gauche.append(superpositions_conj_gauche)
        liste_superpositions_conj_droite.append(superpositions_conj_droite)
        liste_superpositions_np_gauche.append(superpositions_np_gauche)
        liste_superpositions_np_droite.append(superpositions_np_droite)
        liste_superpositions_pause_gauche.append(superpositions_pause_gauche)
        liste_superpositions_pause_droite.append(superpositions_pause_droite)

        liste_superpositions_unknown_gauche_experts.append(superpositions_unknown_gauche_experts)
        liste_superpositions_unknown_droite_experts.append(superpositions_unknown_gauche_non_experts)
        liste_superpositions_vn_gauche_experts.append(superpositions_vn_gauche_experts)
        liste_superpositions_vn_droite_experts.append(superpositions_vn_droite_experts)
        liste_superpositions_ap_gauche_experts.append(superpositions_ap_gauche_experts)
        liste_superpositions_ap_droite_experts.append(superpositions_ap_droite_experts)
        liste_superpositions_adp_gauche_experts.append(superpositions_adp_gauche_experts)
        liste_superpositions_adp_droite_experts.append(superpositions_adp_droite_experts)
        liste_superpositions_pp_gauche_experts.append(superpositions_pp_gauche_experts)
        liste_superpositions_pp_droite_experts.append(superpositions_pp_droite_experts)
        liste_superpositions_conj_gauche_experts.append(superpositions_conj_gauche_experts)
        liste_superpositions_conj_droite_experts.append(superpositions_conj_droite_experts)
        liste_superpositions_np_gauche_experts.append(superpositions_np_gauche_experts)
        liste_superpositions_np_droite_experts.append(superpositions_np_droite_experts)
        liste_superpositions_pause_gauche_experts.append(superpositions_pause_gauche_experts)
        liste_superpositions_pause_droite_experts.append(superpositions_pause_droite_experts)

        liste_superpositions_unknown_gauche_non_experts.append(superpositions_unknown_gauche_non_experts)
        liste_superpositions_unknown_droite_non_experts.append(superpositions_unknown_droite_non_experts)
        liste_superpositions_vn_gauche_non_experts.append(superpositions_vn_gauche_non_experts)
        liste_superpositions_vn_droite_non_experts.append(superpositions_vn_droite_non_experts)
        liste_superpositions_ap_gauche_non_experts.append(superpositions_ap_gauche_non_experts)
        liste_superpositions_ap_droite_non_experts.append(superpositions_ap_droite_non_experts)
        liste_superpositions_adp_gauche_non_experts.append(superpositions_adp_gauche_non_experts)
        liste_superpositions_adp_droite_non_experts.append(superpositions_adp_droite_non_experts)
        liste_superpositions_pp_gauche_non_experts.append(superpositions_pp_gauche_non_experts)
        liste_superpositions_pp_droite_non_experts.append(superpositions_pp_droite_non_experts)
        liste_superpositions_conj_gauche_non_experts.append(superpositions_conj_gauche_non_experts)
        liste_superpositions_conj_droite_non_experts.append(superpositions_conj_droite_non_experts)
        liste_superpositions_np_gauche_non_experts.append(superpositions_np_gauche_non_experts)
        liste_superpositions_np_droite_non_experts.append(superpositions_np_droite_non_experts)
        liste_superpositions_pause_gauche_non_experts.append(superpositions_pause_gauche_non_experts)
        liste_superpositions_pause_droite_non_experts.append(superpositions_pause_droite_non_experts)

        print(pls_gauche, pls_droite)
        
    return liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts

#liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts = superpositions_chunks_gauche_droite_liste(dico_concordanciers_pauses)

def superpositions_chunks_droite_gauche_total(liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts):

    superpositions_total_unknown_gauche = sum(liste_superpositions_unknown_gauche)
    superpositions_total_unknown_droite = sum(liste_superpositions_unknown_droite)
    superpositions_total_vn_gauche = sum(liste_superpositions_vn_gauche)
    superpositions_total_vn_droite = sum(liste_superpositions_vn_droite)
    superpositions_total_ap_gauche = sum(liste_superpositions_ap_gauche)
    superpositions_total_ap_droite = sum(liste_superpositions_ap_droite)
    superpositions_total_adp_gauche = sum(liste_superpositions_adp_gauche)
    superpositions_total_adp_droite = sum(liste_superpositions_adp_droite)
    superpositions_total_pp_gauche = sum(liste_superpositions_pp_gauche)
    superpositions_total_pp_droite = sum(liste_superpositions_pp_droite)
    superpositions_total_conj_gauche = sum(liste_superpositions_conj_gauche)
    superpositions_total_conj_droite = sum(liste_superpositions_conj_droite)
    superpositions_total_np_gauche = sum(liste_superpositions_np_gauche)
    superpositions_total_np_droite = sum(liste_superpositions_np_droite)
    superpositions_total_pause_gauche = sum(liste_superpositions_pause_gauche)
    superpositions_total_pause_droite = sum(liste_superpositions_pause_droite)

    superpositions_total_unknown_gauche_experts = sum(liste_superpositions_unknown_gauche_experts)
    superpositions_total_unknown_droite_experts = sum(liste_superpositions_unknown_droite_experts)
    superpositions_total_vn_gauche_experts = sum(liste_superpositions_vn_gauche_experts)
    superpositions_total_vn_droite_experts = sum(liste_superpositions_vn_droite_experts)
    superpositions_total_ap_gauche_experts = sum(liste_superpositions_ap_gauche_experts)
    superpositions_total_ap_droite_experts = sum(liste_superpositions_ap_droite_experts)
    superpositions_total_adp_gauche_experts = sum(liste_superpositions_adp_gauche_experts)
    superpositions_total_adp_droite_experts = sum(liste_superpositions_adp_droite_experts)
    superpositions_total_pp_gauche_experts = sum(liste_superpositions_pp_gauche_experts)
    superpositions_total_pp_droite_experts = sum(liste_superpositions_pp_droite_experts)
    superpositions_total_conj_gauche_experts = sum(liste_superpositions_conj_gauche_experts)
    superpositions_total_conj_droite_experts = sum(liste_superpositions_conj_droite_experts)
    superpositions_total_np_gauche_experts = sum(liste_superpositions_np_gauche_experts)
    superpositions_total_np_droite_experts = sum(liste_superpositions_np_droite_experts)
    superpositions_total_pause_gauche_experts = sum(liste_superpositions_pause_gauche_experts)
    superpositions_total_pause_droite_experts = sum(liste_superpositions_pause_droite_experts)

    superpositions_total_unknown_gauche_non_experts = sum(liste_superpositions_unknown_gauche_non_experts)
    superpositions_total_unknown_droite_non_experts = sum(liste_superpositions_unknown_droite_non_experts)
    superpositions_total_vn_gauche_non_experts = sum(liste_superpositions_vn_gauche_non_experts)
    superpositions_total_vn_droite_non_experts = sum(liste_superpositions_vn_droite_non_experts)
    superpositions_total_ap_gauche_non_experts = sum(liste_superpositions_ap_gauche_non_experts)
    superpositions_total_ap_droite_non_experts = sum(liste_superpositions_ap_droite_non_experts)
    superpositions_total_adp_gauche_non_experts = sum(liste_superpositions_adp_gauche_non_experts)
    superpositions_total_adp_droite_non_experts = sum(liste_superpositions_adp_droite_non_experts)
    superpositions_total_pp_gauche_non_experts = sum(liste_superpositions_pp_gauche_non_experts)
    superpositions_total_pp_droite_non_experts = sum(liste_superpositions_pp_droite_non_experts)
    superpositions_total_conj_gauche_non_experts = sum(liste_superpositions_conj_gauche_non_experts)
    superpositions_total_conj_droite_non_experts = sum(liste_superpositions_conj_droite_non_experts)
    superpositions_total_np_gauche_non_experts = sum(liste_superpositions_np_gauche_non_experts)
    superpositions_total_np_droite_non_experts = sum(liste_superpositions_np_droite_non_experts)
    superpositions_total_pause_gauche_non_experts = sum(liste_superpositions_pause_gauche_non_experts)
    superpositions_total_pause_droite_non_experts = sum(liste_superpositions_pause_droite_non_experts)

    #print(superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, "hello", superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, "hallo", superpositions_total_np_gauche, "hello", superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts)

    return superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, superpositions_total_np_gauche, superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts
    
#superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, superpositions_total_np_gauche, superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts = superpositions_chunks_droite_gauche_total(liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts)

# def pauses_non_superposees(liste_textes):

#     liste_pauses_non_superposees_par_texte = []
#     liste_pauses_non_superposees_par_texte_experts = []
#     liste_pauses_non_superposees_par_texte_non_experts = []

#     for fichier in liste_textes:
#         pause_non_superposee = 0
#         fichier_chunks_pipes, num_text = obtenir_fichier_chunks_pipes(fichier)
#         liste_chunks = obtenir_texte_chunks(fichier_chunks_pipes)
#         liste_clean = gestion_recursives(liste_chunks)
#         liste_finale = normalisation_espaces(liste_clean)
#         for chunk, type in liste_finale:
#             if "|" in chunk and chunk != "|":
#                 pause_non_superposee += 1

#         if "+" in fichier:
#             liste_pauses_non_superposees_par_texte_experts.append(pause_non_superposee)
#         else:
#             liste_pauses_non_superposees_par_texte_non_experts.append(pause_non_superposee)
#         liste_pauses_non_superposees_par_texte.append(pause_non_superposee)
    
#     pauses_total_non_superposees = sum(liste_pauses_non_superposees_par_texte)
#     pauses_total_non_superposees_experts = sum(liste_pauses_non_superposees_par_texte_experts)
#     pauses_total_non_superposees_non_experts = sum(liste_pauses_non_superposees_par_texte_non_experts)

#     return liste_pauses_non_superposees_par_texte, liste_pauses_non_superposees_par_texte_experts, liste_pauses_non_superposees_par_texte_non_experts, pauses_total_non_superposees, pauses_total_non_superposees_experts, pauses_total_non_superposees_non_experts

def pauses_non_superposees_type_chunk(chunk_lists_dict):


    dico_pauses_non_sup_par_texte = {
             '__UNKNOWN__': [],
                "VN": [],
                "AP" : [],
                "AdP" : [],  
                "PP": [],  
                "CONJ": [],
                "NP" : [],
                "PAUSE" : []
            }
    
    dico_pauses_non_sup_par_texte_experts = {
             '__UNKNOWN__': [],
                "VN": [],
                "AP" : [],
                "AdP" : [],  
                "PP": [],  
                "CONJ": [],
                "NP" : [],
                "PAUSE" : []
            }
    
    dico_pauses_non_sup_par_texte_non_experts = {
             '__UNKNOWN__': [],
                "VN": [],
                "AP" : [],
                "AdP" : [],  
                "PP": [],  
                "CONJ": [],
                "NP" : [],
                "PAUSE" : []
            }

    for id, liste_chunks in chunk_lists_dict.items():
        unknown = 0
        vn = 0
        ap = 0
        adp = 0
        pp = 0
        conj = 0
        np = 0

        for chunk, type in liste_chunks:
            if "|" in chunk and chunk != "|":
                if type == "__UNKNOWN__":
                    unknown += 1
                elif type == "VN":
                    #print(chunk, type)
                    vn += 1
                elif type == "AP":
                    #print(chunk, type)
                    ap += 1
                elif type == "AdP":
                    #print(chunk, type)
                    adp += 1
                elif type == "PP":
                    #print(chunk, type)
                    pp += 1
                elif type == "CONJ":
                    #print(chunk, type)
                    conj += 1
                elif type == "NP":
                    #print(id)
                    #print(chunk, type)
                    np += 1 
        
        if "-" in id:
            dico_pauses_non_sup_par_texte_experts["__UNKNOWN__"].append(unknown)
            dico_pauses_non_sup_par_texte_experts["VN"].append(vn)
            dico_pauses_non_sup_par_texte_experts["AP"].append(ap)
            dico_pauses_non_sup_par_texte_experts["AdP"].append(adp)
            dico_pauses_non_sup_par_texte_experts["PP"].append(pp)
            dico_pauses_non_sup_par_texte_experts["CONJ"].append(conj)
            dico_pauses_non_sup_par_texte_experts["NP"].append(np)
        else: 
            dico_pauses_non_sup_par_texte_non_experts["__UNKNOWN__"].append(unknown)
            dico_pauses_non_sup_par_texte_non_experts["VN"].append(vn)
            dico_pauses_non_sup_par_texte_non_experts["AP"].append(ap)
            dico_pauses_non_sup_par_texte_non_experts["AdP"].append(adp)
            dico_pauses_non_sup_par_texte_non_experts["PP"].append(pp)
            dico_pauses_non_sup_par_texte_non_experts["CONJ"].append(conj)
            dico_pauses_non_sup_par_texte_non_experts["NP"].append(np)

        dico_pauses_non_sup_par_texte["__UNKNOWN__"].append(unknown)
        dico_pauses_non_sup_par_texte["VN"].append(vn)
        dico_pauses_non_sup_par_texte["AP"].append(ap)
        dico_pauses_non_sup_par_texte["AdP"].append(adp)
        dico_pauses_non_sup_par_texte["PP"].append(pp)
        dico_pauses_non_sup_par_texte["CONJ"].append(conj)
        dico_pauses_non_sup_par_texte["NP"].append(np)
                
    dico_total_pauses_non_super = {key: sum(value) for key, value in dico_pauses_non_sup_par_texte.items()}
    dico_total_pauses_non_super_experts =  {key: sum(value) for key, value in dico_pauses_non_sup_par_texte_experts.items()}
    dico_total_pauses_non_super_non_experts =  {key: sum(value) for key, value in dico_pauses_non_sup_par_texte_non_experts.items()}

    return dico_pauses_non_sup_par_texte, dico_pauses_non_sup_par_texte_experts, dico_pauses_non_sup_par_texte_non_experts, dico_total_pauses_non_super, dico_total_pauses_non_super_experts, dico_total_pauses_non_super_non_experts


def main():

    reconstructed_texts_dict = get_reconstructed_texts("../../data/reconstructed_texts_behaviours")
    chunk_lists_dict = get_chunk_lists("../../data/list_chunks/chunks.json")
    liste_pauses_par_texte, liste_pauses_par_texte_expert, liste_pauses_par_texte_non_expert, pauses_total_textes, pauses_total_textes_experts, pauses_total_textes_non_experts = nbrpauses(reconstructed_texts_dict)
    dico_chunks_par_texte, dico_chunks_par_texte_experts, dico_chunks_par_texte_non_experts, dico_total_chunks, dico_total_chunks_experts, dico_total_chunks_non_experts, chunks_total_textes, chunks_total_textes_experts, chunks_total_textes_non_experts = chunks(chunk_lists_dict)
    dico_concordanciers_pauses, liste_pauses_superposees_par_texte, liste_pauses_superposees_par_texte_experts, liste_pauses_superposees_par_texte_non_experts, pauses_total_superposees, pauses_total_superposees_experts, pauses_total_superposees_non_experts = superpositions(chunk_lists_dict)
    liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts = superpositions_chunks_gauche_droite_liste(dico_concordanciers_pauses)
    superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, superpositions_total_np_gauche, superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts = superpositions_chunks_droite_gauche_total(liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts)
    dico_pauses_non_sup_par_texte, dico_pauses_non_sup_par_texte_experts, dico_pauses_non_sup_par_texte_non_experts, dico_total_pauses_non_super, dico_total_pauses_non_super_experts, dico_total_pauses_non_super_non_experts = pauses_non_superposees_type_chunk(chunk_lists_dict)

    print("What number do you want to have ?\nPress the corresponding number.")
    print("1 - Number of pauses in the corpus.")
    print("2 - Number of chunks in the corpus.")
    print("3 - Number of superpositions between chunks and pauses.")
    print("4 - Most commun chunk types involved in chunk/pause superpositions. ")
    print("5 - Number of pauses within chunks.")
    print("6 - Most common chunk types containing pauses.")

    choice = input("")
    if choice == "1":

        number_non_expert = pauses_total_textes_non_experts
        mean_non_expert = number_non_expert / len(liste_pauses_par_texte_non_expert)
        non_expert_median = np.median(liste_pauses_par_texte_non_expert)
        number_expert = pauses_total_textes_experts
        mean_expert = number_expert / len(liste_pauses_par_texte_expert)
        expert_median = np.median(liste_pauses_par_texte_expert)
        number = pauses_total_textes
        mean = number / len(liste_pauses_par_texte)
        median = np.median(liste_pauses_par_texte)

        print(f"Number of pauses in the entire corpus : {number}.")
        print(f"Mean of pauses per text : {mean}.")
        print(f"Median of all pauses : {median}.")
        print(f"Number of pauses in the expert texts : {number_expert}.")
        print(f"Mean of pauses per expert text : {mean_expert}.")
        print(f"Median of pauses in expert texts : {expert_median}.")
        print(f"Number of pauses in the non-expert texts : {number_non_expert}.")
        print(f"Mean of pauses per non-expert text : {mean_non_expert}.")
        print(f"Median of pauses in non-expert texts : {non_expert_median}.")

        if mean_non_expert > mean_expert:
            print("There are more pauses in the non-expert texts.")
        else:
            print("There are more pauses in the expert texts.")
    
    if choice == "2":
        print(dico_total_chunks)
        total_chunks_expert = sum(dico_total_chunks_experts.values())
        total_chunks_non_expert = sum(dico_total_chunks_non_experts.values())
        total_chunks = sum(dico_total_chunks.values())

        normalized_expert_values = [val / total_chunks_expert for val in dico_total_chunks_experts.values()]
        print(normalized_expert_values)
        normalized_non_expert_values = [val / total_chunks_non_expert for val in dico_total_chunks_non_experts.values()]
        print(normalized_non_expert_values)
        normalized_total_values = [val / total_chunks for val in dico_total_chunks.values()]
        print(normalized_total_values)

        labels = list(dico_total_chunks.keys())  
        x = np.arange(len(labels))  
        width = 0.25 

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.barh(x - width, normalized_total_values, height=width, label='Total (Normalized)', color='skyblue')
        ax.barh(x, normalized_expert_values, height=width, label='Experts (Normalized)', color='lightgreen')
        ax.barh(x + width, normalized_non_expert_values, height=width, label='Non-experts (Normalized)', color='pink')

        ax.set_ylabel('Type of chunk')
        ax.set_xlabel('Proportion of chunks')
        ax.set_title('Normalized Chunk Repartition in All, Expert, and Non-Expert Texts')
        ax.set_yticks(x)
        ax.set_yticklabels(labels)
        ax.legend()

        plt.tight_layout()
        plt.show()


    if choice == "3":
        number_non_expert = pauses_total_superposees_non_experts
        percentage_non_expert = (pauses_total_superposees_non_experts / pauses_total_textes_non_experts) * 100 
        mean_non_expert = number_non_expert / len(liste_pauses_superposees_par_texte_non_experts)
        non_expert_median = np.median(liste_pauses_superposees_par_texte_non_experts)


        number_expert = pauses_total_superposees_experts
        percentage_expert = (pauses_total_superposees_experts / pauses_total_textes_experts) * 100 
        mean_expert = number_expert / len(liste_pauses_superposees_par_texte_experts)
        expert_median = np.median(liste_pauses_superposees_par_texte_experts)

        number = pauses_total_superposees
        percentage = (pauses_total_superposees / pauses_total_textes) * 100 
        mean = number / len(liste_pauses_superposees_par_texte)
        median = np.median(liste_pauses_superposees_par_texte)


        print(f"Number of overlapping pauses in the entire corpus : {number}.")
        print(f"Mean of overlapping pauses per text : {mean}.")
        print(f"Median of all overlapping pauses : {median}.")
        print(f"Percentage of overlapping pauses based on all pauses : {percentage}%.\n")

        print(f"Number of overlapping pauses in the expert texts : {number_expert}.")
        print(f"Mean of overlapping pauses per expert text : {mean_expert}.")
        print(f"Median of overlapping pauses in expert texts : {expert_median}.")
        print(f"Percentage of overlapping pauses based on all pauses in expert texts : {percentage_expert}%.\n")

        print(f"Number of overlapping pauses in the non-expert texts : {number_non_expert}.")
        print(f"Mean of overlapping pauses per non-expert text : {mean_non_expert}.")
        print(f"Median of overlapping pauses in non-expert texts : {non_expert_median}.")
        print(f"Percentage of overlapping pauses based on all pauses in non-expert texts : {percentage_non_expert}%.")

        if percentage_non_expert > percentage_expert:
            print("There are more overlapping pauses in the non-expert texts.")
        else:
            print("There are more overlapping pauses in the expert texts.")
    
    if choice == "4":
      
        chunk_labels = ["__UNKNOWN__", "VN", "AP", "AdP", "PP", "CONJ", "NP"]
        dico_total_gauche = {
            '__UNKNOWN__' : superpositions_total_unknown_gauche, 
            'VN' : superpositions_total_vn_gauche,
            'AP' : superpositions_total_ap_gauche,
            'AdP' : superpositions_total_adp_gauche,
            'PP' : superpositions_total_pp_gauche,
            'CONJ' : superpositions_total_conj_gauche, 
            'NP' : superpositions_total_np_gauche
        }
        print(dico_total_gauche)
        dico_total_droite = {
            '__UNKNOWN__' : superpositions_total_unknown_droite,          
            'VN' : superpositions_total_vn_droite,
            'AP' :  superpositions_total_ap_droite,
            'AdP' : superpositions_total_adp_droite, 
            'PP' :  superpositions_total_pp_droite,
            'CONJ' :  superpositions_total_conj_droite, 
            'NP' :   superpositions_total_np_droite 

        }
        print(dico_total_droite)
        dico_total_gauche_experts = {
            '__UNKNOWN__' : superpositions_total_unknown_gauche_experts, 
            'VN' : superpositions_total_vn_gauche_experts,
            'AP' : superpositions_total_ap_gauche_experts,
            'AdP' : superpositions_total_adp_gauche_experts,
            'PP' : superpositions_total_pp_gauche_experts,
            'CONJ' : superpositions_total_conj_gauche_experts, 
            'NP' : superpositions_total_np_gauche_experts
        }

        dico_total_droite_experts = {
            '__UNKNOWN__' : superpositions_total_unknown_droite_experts, 
            'VN' : superpositions_total_vn_droite_experts,
            'AP' : superpositions_total_ap_droite_experts,
            'AdP' : superpositions_total_adp_droite_experts,
            'PP' : superpositions_total_pp_droite_experts,
            'CONJ' : superpositions_total_conj_droite_experts,
            'NP' : superpositions_total_np_droite_experts
        }

        dico_total_gauche_non_experts = {
            '__UNKNOWN__' : superpositions_total_unknown_gauche_non_experts, 
            'VN' : superpositions_total_vn_gauche_non_experts,
            'AP' : superpositions_total_ap_gauche_non_experts,
            'AdP' : superpositions_total_adp_gauche_non_experts,
            'PP' : superpositions_total_pp_gauche_non_experts,
            'CONJ' : superpositions_total_conj_gauche_non_experts, 
            'NP' : superpositions_total_np_gauche_non_experts
        }

        dico_total_droite_non_experts = {
            '__UNKNOWN__' : superpositions_total_unknown_droite_non_experts, 
            'VN' : superpositions_total_vn_droite_non_experts,
            'AP' : superpositions_total_ap_droite_non_experts,
            'AdP' : superpositions_total_adp_droite_non_experts,
            'PP' : superpositions_total_pp_droite_non_experts,
            'CONJ' : superpositions_total_conj_droite_non_experts,
            'NP' : superpositions_total_np_droite_non_experts
        }

        chunks_left_total = [
        (dico_total_gauche[label] / dico_total_chunks[label] * 100 if dico_total_chunks[label] != 0 else 0)
        for label in chunk_labels
        ]

        print(chunks_left_total)
     

        chunks_left_experts = [
            (dico_total_gauche_experts[label] / dico_total_chunks[label] * 100 if dico_total_chunks[label] != 0 else 0)
            for label in chunk_labels
        ]

        chunks_left_non_experts = [
            (dico_total_gauche_non_experts[label] / dico_total_chunks[label] * 100 if dico_total_chunks[label] != 0 else 0)
            for label in chunk_labels
        ]


        chunks_right_total = [
            (dico_total_droite[label] / dico_total_chunks[label] * 100 if dico_total_chunks[label] != 0 else 0)
            for label in chunk_labels
        ]

        print(chunks_right_total)

        chunks_right_experts = [
            (dico_total_droite_experts[label] / dico_total_chunks[label] * 100 if dico_total_chunks[label] != 0 else 0)
            for label in chunk_labels
        ]

        chunks_right_non_experts = [
            (dico_total_droite_non_experts[label] / dico_total_chunks[label] * 100 if dico_total_chunks[label] != 0 else 0)
            for label in chunk_labels
        ]


        fig, ax = plt.subplots(1, 2, figsize=(15, 8))

        x = np.arange(len(chunk_labels))  
        width = 0.2  
        ax[0].barh(x - width, chunks_left_total, height=width, label='Total', color='skyblue')
        ax[0].barh(x, chunks_left_experts, height=width, label='Experts', color='lightgreen')
        ax[0].barh(x + width, chunks_left_non_experts, height=width, label='Non-Experts', color='pink')
        ax[0].set_xlabel('Percentage of chunks')
        ax[0].set_title('Chunks placed before a pause (left)')
        ax[0].set_yticks(x)
        ax[0].set_yticklabels(chunk_labels)
        ax[0].legend()

        ax[1].barh(x - width, chunks_right_total, height=width, label='Total', color='skyblue')
        ax[1].barh(x, chunks_right_experts, height=width, label='Experts', color='lightgreen')
        ax[1].barh(x + width, chunks_right_non_experts, height=width, label='Non-Experts', color='pink')
        ax[1].set_xlabel('Percentage of chunks')
        ax[1].set_title('Chunks placed after a pause (right)')
        ax[1].set_yticks(x)
        ax[1].set_yticklabels(chunk_labels)
        ax[1].legend()

        plt.tight_layout()
        plt.show()


    if choice == "5":

        print(dico_total_pauses_non_super, dico_pauses_non_sup_par_texte_non_experts)
        number_non_expert = dico_total_pauses_non_super_non_experts
        percentage_non_expert = (dico_total_pauses_non_super_non_experts/ pauses_total_textes_non_experts) * 100 
        mean_non_expert = number_non_expert / len(dico_pauses_non_sup_par_texte_non_experts)
        non_expert_median = np.median(dico_pauses_non_sup_par_texte_non_experts)


        number_expert = dico_total_pauses_non_super_experts
        percentage_expert = (dico_total_pauses_non_super_experts / pauses_total_textes_experts) * 100 
        mean_expert = number_expert / len(dico_pauses_non_sup_par_texte_experts)
        expert_median = np.median(dico_pauses_non_sup_par_texte_experts)

        numer = 0
        percentage = (pauses_total_superposees / pauses_total_textes) * 100 
        mean = number / len(liste_pauses_superposees_par_texte)
        median = np.median(liste_pauses_superposees_par_texte)

        print(f"Number of pauses located within a chunk in the entire corpus : {number}.")
        print(f"Mean of pauses located within a chunk per text : {mean}.")
        print(f"Median of all pauses located within a chunk : {median}.")
        print(f"Number of pauses located within a chunk in the expert texts : {number_expert}.")
        print(f"Mean of pauses located within a chunk per expert text : {mean_expert}.")
        print(f"Median of pauses located within a chunk in expert texts : {expert_median}.")
        print(f"Number of pauses located within a chunk in the non-expert texts : {number_non_expert}.")
        print(f"Mean of pauses located within a chunk per non-expert text : {mean_non_expert}.")
        print(f"Median of pauses located within a chunk in non-expert texts : {non_expert_median}.")






    
if __name__ == "__main__":
    main()