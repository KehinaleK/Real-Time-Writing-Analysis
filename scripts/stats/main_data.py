
from collections import defaultdict, Counter
from typing import List
import sys
import os
import json 

""" Ce script permet d'obtenir des comptes utiles à différents calculs statistiques désirés. Il s'appelle dans un autre script à partir de la fonction désirée pour obtenir uniquement les chiffres voulus.
    Créez par exemple un scrip "statistiques.py" et importez y main_comptes.py. Vous pouvez ensuite utiliser la fonction "obtenir_textes" (ou pas) suivie de n'importe qu'elle autre fonction pour obtenir les chiffres
    qui vous intéresse. Attention, quelques fonctions doivent être appelées après une autre (notamment le cas des fonctions suivant celles des concordanciers. Mais vous pouvez le voir, il s'agit des fonctions
    qui ont comme argument autre chose que "liste_textes")"""


""" Voici une liste de tous les chiffres pouvant être obtenus :
    Notez que les listes sont toujours organisées de la même manière car "liste_textes" est organisée par ordre numérique.

        - longueurs(liste_textes):
            liste_longueur_par_texte = liste de la longueur de chaque texte (un élément = le nombre de caractères du texte correspondant)
                ex : [450, 702, 350, 423...]
            liste_longueur_par_texte_expert = liste de la longueur de chaque texte expert (+) (un élément = le nombre de caractères du texte correspondant)
            liste_longueur_par_texte_non_expert = liste de la longueur de chaque texte non expert (-) (un élément = le nombre de caractères du texte correspondant)
            longueur_totale_textes = nombre total de charactères dans tout le corpus
            longueur_totale_textes_expert = nombre total de charactères dans les textes experts
            longueur_totale_textes_non_expert = nombre total de charactères dans les textes non experts

        - nbrpauses(liste_textes):
            liste_pauses_par_texte = liste des nombres de pauses dans chaque texte (un élément = le nombre de pauses du texte correspondant)
                ex : [72, 83, 43...]
            liste_pauses_par_texte_expert = liste des nombres de pauses dans chaque texte expert (un élément = le nombre de pauses du texte correspondant)
            liste_pauses_par_texte_non_expert = liste des nombres de pauses dans chaque texte non expert (un élément = le nombre de pauses du texte correspondant)
            pauses_total_textes = nombre total de pauses dans tout le corpus
            pauses_total_textes_experts = nombre total de pauses dans les textes experts
            pauses_total_textes_non_experts = nombre total de pauses dans les textes non experts

        - chunks(liste_textes):
            dico_chunks_par_texte = dictionnaire avec en clé un type de chunk et en valeur une liste du nombre de chunks de ce type pour chaque texte (un élément de la liste = le nombre de chunks de ce type pour le texte correspondant)
                ex : 
                    {
                    VN : [22, 13, 45, 34...] 
                    AP : [4, 5, 2, 2...]
                    CONJ : [8, 9, 6, 8...]
                    ...
                    }
            dico_chunks_par_texte_experts = dictionnaire avec en clé un type de chunk et en valeur une liste du nombre de chunks de ce type pour chaque texte expert (un élément de la liste = le nombre de chunks de ce type pour le texte correspondant)
            dico_chunks_par_texte_non_experts = dictionnaire avec en clé un type de chunk et en valeur une liste du nombre de chunks de ce type pour chaque texte non expert (un élément de la liste = le nombre de chunks de ce type pour le texte correspondant)
            dico_total_chunks = dictionnaire avec en clé un type de chunk et en valeur le nombre total de ce type de chunks dans le corpus
            ex : 
                    {
                    VN : 425 
                    AP : 83
                    CONJ : 128
                    ...
                    }
            dico_total_chunks_experts = dictionnaire avec en clé un type de chunk et en valeur le nombre total de ce type de chunks dans les textes experts
            dico_total_chunks_non_experts = dictionnaire avec en clé un type de chunk et en valeur le nombre total de ce type de chunks dans les textes non experts
            chunks_total_textes = nombre total de chunks dans le corpus (indifféremment des types)
            chunks_total_textes_experts = nombre total de chunks dans les textes experts (indifféremment des types)
            chunks_textes_non_experts = nombre total de chunks dans les textes non experts (indifféremment des types)

        - superpositions():
            dico_concordanciers_pauses = ce dictionnaire a pour clé le nom d'un texte et en valeur une liste de tuples. Ces tuples sont composées de trois éléments : 
                une première tuple composée d'un chunk et de son type, une seconde tuple composée de la pause, et une troisième composée du chunk suivant la pause et de son type.
                On a donc Dic[List[Tuple(Tuple(str, str), Tuple(str, str), Tuple(str, str))]]. Ce dico permet de voir quels chunks précèdents ou suivent les pauses.
                ex : 
                {
                'P-S22': [(('[sont basé]', 'VN'), ('|', 'Pause'), ('[de cette médi|~ecine]', 'PP'))
                            , (('[,]', 'AdP'), ('|', 'Pause'), ('[sont]', 'VN'))],
                'P-S23' :[(('[<~s>e basant]', 'PP'), ('|', 'Pause'), ('[les erreurs médicale]', 'NP'))]
                }
            liste_pauses_superposees_par_texte = liste du nombre de pauses superposées (donc du nombre de pauses exactement entre deux chunks) par texte (donc un élément = nombre de pauses superposées du texte correspondant)
            liste_pauses_superposees_par_texte_experts = liste du nombre de pauses superposées (donc du nombre de pauses exactement entre deux chunks) par texte expert (donc un élément = nombre de pauses superposées du texte correspondant)
            liste_pauses_superposees_par_texte_non_experts = liste du nombre de pauses superposées (donc du nombre de pauses exactement entre deux chunks) par texte non expert (donc un élément = nombre de pauses superposées du texte correspondant)
            pauses_total_superposees = nombre total de pauses superposées dans tout le corpus
            pauses_total_superposees_experts = nombre total de pauses superposées dans les textes experts
            pauses_total_superposees_non_experts = nombre total de pauses superposées dans les textes non experts

        - superpositions_chunks_gauche_droite_liste(dico_concordanciers_pauses):
        !!! Il faut appeler la fonction superpositions() avant pour avoir dico_concordanciers_pauses !!!
            liste_superpositions_unknown_gauche = une liste ou chaque élément est le nombre chunks unknown précédent une pause (un élément de la liste = le nombre de chunks unknown à gauche du pause pour le texte correspondant)
            liste_superpositions_unknown_droite = une liste ou chaque élément est le nombre chunks unknown suivant une pause (un élément de la liste = le nombre de chunks unknown à droite du pause pour le texte correspondant)
            liste_superpositions_vn_gauche ===
            liste_superpositions_vn_droite ===
            liste_superpositions_ap_gauche ===
            liste_superpositions_ap_droite ===
            liste_superpositions_adp_gauche ===
            liste_superpositions_adp_droite === 
            liste_superpositions_pp_gauche ===
            liste_superpositions_pp_droite === 
            liste_superpositions_conj_gauche ===
            liste_superpositions_conj_droite ===
            liste_superpositions_np_gauche ===
            liste_superpositions_np_droite ===
            liste_superpositions_pause_gauche === 
            liste_superpositions_pause_droite ===
            liste_superpositions_unknown_gauche_experts = pareil mais seulement pour les textes non experts
            liste_superpositions_unknown_droite_experts ===
            liste_superpositions_vn_gauche_experts ===
            liste_superpositions_vn_droite_experts ===
            liste_superpositions_ap_gauche_experts ===
            liste_superpositions_ap_droite_experts ===
            liste_superpositions_adp_gauche_experts ===
            liste_superpositions_adp_droite_experts ===
            liste_superpositions_pp_gauche_experts ===
            liste_superpositions_pp_droite_experts ===
            liste_superpositions_conj_gauche_experts ===
            liste_superpositions_conj_droite_experts ===
            liste_superpositions_np_gauche_experts ===
            liste_superpositions_np_droite_experts ===
            liste_superpositions_pause_gauche_experts === 
            liste_superpositions_pause_droite_experts ===
            liste_superpositions_unknown_gauche_non_experts = pareil mais seulement pous les textes non experts
            liste_superpositions_unknown_droite_non_experts ===
            liste_superpositions_vn_gauche_non_experts ===
            liste_superpositions_vn_droite_non_experts ===
            liste_superpositions_ap_gauche_non_experts ===
            liste_superpositions_ap_droite_non_experts ===
            liste_superpositions_adp_gauche_non_experts ===
            liste_superpositions_adp_droite_non_experts ===
            liste_superpositions_pp_gauche_non_experts ===
            liste_superpositions_pp_droite_non_experts ===
            liste_superpositions_conj_gauche_non_experts ===
            liste_superpositions_conj_droite_non_experts ===
            liste_superpositions_np_gauche_non_experts ===
            liste_superpositions_np_droite_non_experts ===
            liste_superpositions_pause_gauche_non_experts === 
            liste_superpositions_pause_droite_non_experts ===
        
        - superpositions_chunks_droite_gauche_total(liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts):
        !!! Il faut appeler "superpositions_chunks_droite_gauche_listee" avant pour avoir toutes les listes ! et donc appeler superpositions avant !!!
            superpositions_total_unknown_gauche = nombre total de chunks unknown précédent une pause dans tout le corpus.
            superpositions_total_unknown_droite ===
            superpositions_total_vn_gauche ===
            superpositions_total_vn_droite ===
            superpositions_total_ap_gauche ===
            superpositions_total_ap_droite ===
            superpositions_total_adp_gauche ===
            superpositions_total_adp_droite ===
            superpositions_total_pp_gauche ===
            superpositions_total_pp_droite ===
            superpositions_total_conj_gauche ===
            superpositions_total_conj_droite ===
            superpositions_total_np_gauche ===
            superpositions_total_np_droite ===
            superpositions_total_pause_gauche === 
            superpositions_total_pause_droite ===
            superpositions_total_unknown_gauche_experts = pareil mais pour les textes non experts 
            superpositions_total_unknown_droite_experts ===
            superpositions_total_vn_gauche_experts ===
            superpositions_total_vn_droite_experts ===
            superpositions_total_ap_gauche_experts ===
            superpositions_total_ap_droite_experts ===
            superpositions_total_adp_gauche_experts ===
            superpositions_total_adp_droite_experts ===
            superpositions_total_pp_gauche_experts ===
            superpositions_total_pp_droite_experts ===
            superpositions_total_conj_gauche_experts ===
            superpositions_total_conj_droite_experts ===
            superpositions_total_np_gauche_experts ===
            superpositions_total_np_droite_experts ===
            superpositions_total_pause_gauche_experts === 
            superpositions_total_pause_droite_experts ===
            superpositions_total_unknown_gauche_non_experts = pareil mais pour les textes non experts 
            superpositions_total_unknown_droite_non_experts ===
            superpositions_total_vn_gauche_non_experts ===
            superpositions_total_vn_droite_non_experts ===
            superpositions_total_ap_gauche_non_experts ===
            superpositions_total_ap_droite_non_experts ===
            superpositions_total_adp_gauche_non_experts ===
            superpositions_total_adp_droite_non_experts ===
            superpositions_total_pp_gauche_non_experts ===
            superpositions_total_pp_droite_non_experts ===
            superpositions_total_conj_gauche_non_experts ===
            superpositions_total_conj_droite_non_experts ===
            superpositions_total_np_gauche_non_experts ===
            superpositions_total_np_droite_non_experts ===
            superpositions_total_pause_gauche_non_experts === 
            superpositions_total_pause_droite_non_experts ===

        pauses_non_superposees(liste_textes):
            liste_pauses_non_superposees_par_texte = liste des nombres de pauses non superposées (donc de pauses dans des chunks) par texte (donc un élément = nombre de pauses non superposées dans le texte correspondant)
            liste_pauses_non_superposees_par_texte_experts = liste des nombres de pauses non superposées dans les textes experts (donc de pauses dans des chunks) par texte (donc un élément = nombre de pauses non superposées dans le texte correspondant)
            liste_pauses_non_superposees_par_texte_non_experts = liste des nombres de pauses non superposées dans les textes non experts (donc de pauses dans des chunks) par texte (donc un élément = nombre de pauses non superposées dans le texte correspondant)
            pauses_total_non_superposees = nombre total de pauses non superposées dans tout le corpus
            pauses_total_non_superposees_experts = nombre total de pauses non superposées dans les textes experts
            pauses_total_non_superposees_non_experts = nombre total de pauses non superposées dans les textes non experts
        
        erreurs(liste_textes):
            liste_erreurs_par_texte = liste du nombre d'erreurs (peu importe le type) par texte (donc un élément = nombre d'erreurs du texte correspondant)
            liste_erreurs_par_texte_experts = liste du nombre d'erreurs (peu importe le type) par texte expert (donc un élément = nombre d'erreurs du texte correspondant)
            liste_erreurs_par_texte_non_experts = liste du nombre d'erreurs (peu importe le type) par texte non expert (donc un élément = nombre d'erreurs du texte correspondant)
            erreurs_total_textes = nombre total d'erreurs dans tout le corpus
            erreurs_total_textes_experts = nombre total d'erreurs dans les textes experts
            erreurs_total_textes_non_experts = nombre total d'erreurs dans les textes non experts

        erreurs_comptes_par_types(liste_textes):
            dico_erreurs_compte_texte = dictionnaire ou chaque clé est un type d'erreurs (genre "lettre ajoutée" ) et en valeur une liste des nombres d'erreurs de ce type par texte (donc un élément de la liste est le nombre d'erreurs LA dans le texte correspondant)
                ex:
                    {
                    LA : [4, 5, 2, 2],
                    MI : [1, 1, 0, 1],
                    ...
                    }
            dico_erreurs_compte_texte_experts = pareil mais seulement pour les textes experts 
            dico_erreurs_compte_texte_non_experts = pareil mais seulement pour les textes non experts
            dico_total_erreurs_compte = dictionnaire avec en clé le type d'erreur et en valeur le nombre total de ce type d'erreur dans le corpus. 
            dico_total_erreurs_compte_experts = dictionnaire avec en clé le type d'erreur et en valeur le nombre total de ce type d'erreur dans les textes experts.  
            dico_total_erreurs_compte_non_experts = dictionnaire avec en clé le type d'erreur et en valeur le nombre total de ce type d'erreur dans les textes non experts.

        erreurs_concordanciers(liste_textes):
            dico_concordanciers_erreurs = dictionnaire avec un clé le nom du texte (P-S22) et en valeur un autre dictionnaire.
                Ce dictionnaire a lui en clé le type d'erreurs (genre LA) et en valeur une liste de tuples de trois éléments. Le premier élément est une tuple de deux éléments (chunk et son type), le deuxième est une tuple d'un chunk
                contenant l'erreur correspondant à la clé, et en troisième une tuple avec le chunk et son type suivant l'erreur.
                Donc on a Dict[Dict[List[Tuple(Tuple-str, str, Tuple(str, str), Tuple(str, str))]]]
                On obtient ici un ensemble de concordanciers qui permet de voir quels chunks et types de chunks précèdent et suivent un type d'erreur particulier. 
                ex avec la première clé: {'P-S22': {'LA': [(('[sont basé]', 'VN'), ('[sur les fond<s>]', 'PP'), ('[de cette médi|~ecine]', 'PP')), 
                                                           (('[,]', 'AdP'), ('[certain~s remède<s>]', 'NP'), ('[sont]', 'VN')), 
                                                           (('[<~s>e basant]', 'PP'), ('[{sur les} ancienne<s> croyances,]', 'PP'), ('[les erreurs médicale]', 'NP'))], 
                                                    'LAS': [(('[en~ effet fort efficace]', 'PP'), ('[sur certain<~s> points~~.]', 'PP'), ('|', 'PAUSE')), 
                                                            (('[éno~rmément]', 'AdP'), ('[mi<~t>]', 'VN'), ('[en avant]', 'PP')), 
                                                            (('[{malgré tout}]', 'PP'), ('[pos<~é>]', 'VN'), ('[beaucoup]', 'AdP')), 
                                                            (('[de cette médecine]', 'PP'), ('[<~s>e basant]', 'PP'), ('[{sur les} ancienne<s> croyances,]', 'PP'))], 
                                                    'MI':  [(('|', 'PAUSE'), ('[{elle}]', 'NP'), ('|', 'PAUSE')), 
                                                            (('[la médecine alternative]', 'NP'), ('[{peut}]', 'VN'), ('[{malgré tout}]', 'PP')), 
                                                            (('[médi}]', 'NP'), ('[{cal}]', 'PP'), ('|', 'PAUSE'))], 
                                                    'CI':  [(('|', 'PAUSE'), ('[{au final}]', 'PP'), ('|', 'PAUSE')), 
                                                            (('[{peut}]', 'VN'), ('[{malgré tout}]', 'PP'), ('[pos<~é>]', 'VN')), 
                                                            (('[<~s>e basant]', 'PP'), ('[{sur les} ancienne<s> croyances,]', 'PP'), ('[les erreurs médicale]', 'NP'))]}})

                            
    """


## Fonction obligatoire à appeler avant n'importe qu'elle autre fonction

def get_chunk_lists(file):
    
    with open(file) as json_file:
        chunk_lists_dict = json.load(json_file)

    return chunk_lists_dict


def get_reconstructed_texts(folder):

    reconstructed_texts_dict = {}

    files = os.listdir(folder)
    for file in files:
        with open(f"{folder}/{file}") as f:
            reconstructed_text = f.read()
            reconstructed_texts_dict[file] = reconstructed_text

    return reconstructed_texts_dict




# def chunks(liste_textes):
#     """Cette fonction permet de renvoyer les valeurs concernant le nombre de chunks de notre corpus."""

#     dico_chunks_par_texte = {
#         '__UNKNOWN__': [],
#         "VN": [],
#         "AP" : [],
#         "AdP" : [],  
#         "PP": [],  
#         "CONJ": [],
#         "NP" : [],
#         "PAUSE" : []
#     }

#     dico_chunks_par_texte_experts = {
#          '__UNKNOWN__': [],
#         "VN": [],
#         "AP" : [],
#         "AdP" : [],  
#         "PP": [],  
#         "CONJ": [],
#         "NP" : [],
#         "PAUSE" : []
#     }

#     dico_chunks_par_texte_non_experts = {
#          '__UNKNOWN__': [],
#         "VN": [],
#         "AP" : [],
#         "AdP" : [],  
#         "PP": [],  
#         "CONJ": [],
#         "NP" : [],
#         "PAUSE" : []
#     }
    
#     chunks_total_textes = 0
#     chunks_total_textes_experts = 0
#     chunks_total_textes_non_experts = 0

#     chunks = 0
#     chunks_textes_experts = 0
#     chunks_textes_non_experts = 0
   

#     for fichier in liste_textes:
#         fichier_chunks_pipes, num_text = obtenir_fichier_chunks_pipes(fichier)
#         liste_chunks = obtenir_texte_chunks(fichier_chunks_pipes)
#         liste_clean = gestion_recursives(liste_chunks)
#         # C'est à l'aide de cette liste finale que nous pouvons établir nos comptes
#         liste_finale = normalisation_espaces(liste_clean)

#         unk = 0
#         vn = 0
#         ap = 0
#         adp = 0
#         pp = 0
#         conj = 0
#         np = 0
#         pause = 0 #On crée une variable pause parce que nous avons techniquement
#         # des chunks de type "pause". Ces derniers correspondent en réalité aux pauses
#         # en frontières de burst.

#         for chunk, type in liste_clean:

#             chunks += 1

#             if type == "__UNKNOWN__":
#                 unk += 1
#             elif type == "VN":
#                 vn += 1 
#             elif type == "AP":
#                 ap += 1
#             elif type == "AdP":
#                 adp += 1
#             elif type == "PP":
#                 pp += 1
#             elif type == "CONJ":
#                 conj += 1
#             elif type == "NP":
#                 np += 1
            
#             if "+" in fichier:
#                 chunks_textes_experts += 1
    
#             elif "-" in fichier: 
#                 chunks_textes_non_experts += 1
               
#         if "+" in fichier:
#             dico_chunks_par_texte_experts["__UNKNOWN__"].append(unk)
#             dico_chunks_par_texte_experts["VN"].append(vn)
#             dico_chunks_par_texte_experts["AP"].append(ap)
#             dico_chunks_par_texte_experts["AdP"].append(adp)
#             dico_chunks_par_texte_experts["PP"].append(pp)
#             dico_chunks_par_texte_experts["CONJ"].append(conj)
#             dico_chunks_par_texte_experts["NP"].append(np)
#             dico_chunks_par_texte_experts["PAUSE"].append(pause)
#         elif "-" in fichier:
#             dico_chunks_par_texte_non_experts["__UNKNOWN__"].append(unk)
#             dico_chunks_par_texte_non_experts["VN"].append(vn)
#             dico_chunks_par_texte_non_experts["AP"].append(ap)
#             dico_chunks_par_texte_non_experts["AdP"].append(adp)
#             dico_chunks_par_texte_non_experts["PP"].append(pp)
#             dico_chunks_par_texte_non_experts["CONJ"].append(conj)
#             dico_chunks_par_texte_non_experts["NP"].append(np)
#             dico_chunks_par_texte_non_experts["PAUSE"].append(pause)
            
#         chunks_total_textes += chunks
#         chunks_total_textes_experts += chunks_textes_experts
#         chunks_total_textes_non_experts += chunks_textes_non_experts

#         dico_chunks_par_texte["__UNKNOWN__"].append(unk)
#         dico_chunks_par_texte["VN"].append(vn)
#         dico_chunks_par_texte["AP"].append(ap)
#         dico_chunks_par_texte["AdP"].append(adp)
#         dico_chunks_par_texte["PP"].append(pp)
#         dico_chunks_par_texte["CONJ"].append(conj)
#         dico_chunks_par_texte["NP"].append(np)
#         dico_chunks_par_texte["PAUSE"].append(pause)

#     dico_total_chunks = {key: sum(value) for key, value in dico_chunks_par_texte.items()}
#     dico_total_chunks_experts =  {key: sum(value) for key, value in dico_chunks_par_texte_experts.items()}
#     dico_total_chunks_non_experts =  {key: sum(value) for key, value in dico_chunks_par_texte_non_experts.items()}
        
#     return dico_chunks_par_texte, dico_chunks_par_texte_experts, dico_chunks_par_texte_non_experts, dico_total_chunks, dico_total_chunks_experts, dico_total_chunks_non_experts, chunks_total_textes, chunks_total_textes_experts, chunks_total_textes_non_experts

# def superpositions():

#     ### Ici, on vient créer comme un concordancier ! On peut le visualiser en printant ou en le mettant dans un fichier txt.
#     ### Pour chaque fichier, on crée une liste de tuple. Cette tuple contient le chunk précédent la pause,
#     ## le chunk de la pause et le chunk suivant la pause. 
#     # On a un dico_concordanciers qui a comme clés les titres de textes et en valeur le concordancier du fichier concerné.
#     # On utilise ce dico pour pouvoir faire un compte des types de chunks le plus souvent avant et après des erreurs

#     liste_pauses_superposees_par_texte = []
#     liste_pauses_superposees_par_texte_experts = []
#     liste_pauses_superposees_par_texte_non_experts = []

#     dico_concordanciers_pauses = defaultdict(list)
#     for fichier in liste_textes:
#         pause_superposee = 0
#         concordancier = []
#         fichier_chunks_pipes, num_text = obtenir_fichier_chunks_pipes(fichier)
#         liste_chunks = obtenir_texte_chunks(fichier_chunks_pipes)
#         liste_clean = gestion_recursives(liste_chunks)
#         liste_finale = normalisation_espaces(liste_clean)
#         for i in range(len(liste_finale)-1):
#             if liste_finale[i][1] == "PAUSE":
#                 pause_superposee += 1
#                 # et pour le dernier ? pas important parce que si | à la fin bah bon.
#                 concordancier.append((liste_finale[i-1], liste_finale[i], liste_finale[i+1]))
#         if "+" in fichier:
#             liste_pauses_superposees_par_texte_experts.append(pause_superposee)
#         else:
#             liste_pauses_superposees_par_texte_non_experts.append(pause_superposee)
        
#         liste_pauses_superposees_par_texte.append(pause_superposee)
#         dico_concordanciers_pauses[fichier.strip(".txt")] = concordancier
#     print(liste_textes)
#     print(liste_pauses_par_texte)
#     pauses_total_superposees = sum(liste_pauses_superposees_par_texte)
#     print("Nombre de pauses superposées :",pauses_total_superposees)
#     pauses_total_superposees_experts = sum(liste_pauses_superposees_par_texte_experts)
#     pauses_total_superposees_non_experts = sum(liste_pauses_superposees_par_texte_non_experts)

#     return dico_concordanciers_pauses, liste_pauses_superposees_par_texte, liste_pauses_superposees_par_texte_experts, liste_pauses_superposees_par_texte_non_experts, pauses_total_superposees, pauses_total_superposees_experts, pauses_total_superposees_non_experts

# dico_concordanciers_pauses, liste_pauses_superposees_par_texte, liste_pauses_superposees_par_texte_experts, liste_pauses_superposees_par_texte_non_experts, pauses_total_superposees, pauses_total_superposees_experts, pauses_total_superposees_non_experts = superpositions()

# def superpositions_chunks_gauche_droite_liste(dico_concordanciers_pauses):

#     liste_superpositions_unknown_gauche = []
#     liste_superpositions_unknown_droite = []
#     liste_superpositions_vn_gauche = []
#     liste_superpositions_vn_droite = []
#     liste_superpositions_ap_gauche = []
#     liste_superpositions_ap_droite = []
#     liste_superpositions_adp_gauche = []
#     liste_superpositions_adp_droite = []
#     liste_superpositions_pp_gauche = []
#     liste_superpositions_pp_droite = []
#     liste_superpositions_conj_gauche = []
#     liste_superpositions_conj_droite = []
#     liste_superpositions_np_gauche = []
#     liste_superpositions_np_droite = []
#     liste_superpositions_pause_gauche = []
#     liste_superpositions_pause_droite = []

#     liste_superpositions_unknown_gauche_experts = []
#     liste_superpositions_unknown_droite_experts = []
#     liste_superpositions_vn_gauche_experts = []
#     liste_superpositions_vn_droite_experts = []
#     liste_superpositions_ap_gauche_experts = []
#     liste_superpositions_ap_droite_experts = []
#     liste_superpositions_adp_gauche_experts = []
#     liste_superpositions_adp_droite_experts = []
#     liste_superpositions_pp_gauche_experts = []
#     liste_superpositions_pp_droite_experts = []
#     liste_superpositions_conj_gauche_experts = []
#     liste_superpositions_conj_droite_experts = []
#     liste_superpositions_np_gauche_experts = []
#     liste_superpositions_np_droite_experts = []
#     liste_superpositions_pause_gauche_experts = []
#     liste_superpositions_pause_droite_experts = []

#     liste_superpositions_unknown_gauche_non_experts = []
#     liste_superpositions_unknown_droite_non_experts = []
#     liste_superpositions_vn_gauche_non_experts = []
#     liste_superpositions_vn_droite_non_experts = []
#     liste_superpositions_ap_gauche_non_experts = []
#     liste_superpositions_ap_droite_non_experts = []
#     liste_superpositions_adp_gauche_non_experts = []
#     liste_superpositions_adp_droite_non_experts = []
#     liste_superpositions_pp_gauche_non_experts = []
#     liste_superpositions_pp_droite_non_experts = []
#     liste_superpositions_conj_gauche_non_experts = []
#     liste_superpositions_conj_droite_non_experts = []
#     liste_superpositions_np_gauche_non_experts = []
#     liste_superpositions_np_droite_non_experts = []
#     liste_superpositions_pause_gauche_non_experts = []
#     liste_superpositions_pause_droite_non_experts = []

#     for key, value in dico_concordanciers_pauses.items():
#         superpositions_unknown_gauche = 0
#         superpositions_unknown_droite = 0
#         superpositions_vn_gauche = 0
#         superpositions_vn_droite = 0
#         superpositions_ap_gauche = 0
#         superpositions_ap_droite = 0
#         superpositions_adp_gauche = 0 
#         superpositions_adp_droite = 0
#         superpositions_pp_gauche = 0
#         superpositions_pp_droite = 0
#         superpositions_conj_gauche = 0
#         superpositions_conj_droite = 0
#         superpositions_np_gauche = 0
#         superpositions_np_droite = 0
#         superpositions_pause_gauche = 0
#         superpositions_pause_droite = 0

#         superpositions_unknown_gauche_experts = 0
#         superpositions_unknown_droite_experts = 0
#         superpositions_vn_gauche_experts = 0
#         superpositions_vn_droite_experts = 0
#         superpositions_ap_gauche_experts = 0
#         superpositions_ap_droite_experts = 0
#         superpositions_adp_gauche_experts = 0 
#         superpositions_adp_droite_experts = 0
#         superpositions_pp_gauche_experts = 0
#         superpositions_pp_droite_experts = 0
#         superpositions_conj_gauche_experts = 0
#         superpositions_conj_droite_experts = 0
#         superpositions_np_gauche_experts = 0
#         superpositions_np_droite_experts = 0
#         superpositions_pause_gauche_experts = 0
#         superpositions_pause_droite_experts = 0

#         superpositions_unknown_gauche_non_experts = 0
#         superpositions_unknown_droite_non_experts = 0
#         superpositions_vn_gauche_non_experts = 0
#         superpositions_vn_droite_non_experts = 0
#         superpositions_ap_gauche_non_experts = 0
#         superpositions_ap_droite_non_experts = 0
#         superpositions_adp_gauche_non_experts = 0 
#         superpositions_adp_droite_non_experts = 0
#         superpositions_pp_gauche_non_experts = 0
#         superpositions_pp_droite_non_experts = 0
#         superpositions_conj_gauche_non_experts = 0
#         superpositions_conj_droite_non_experts = 0
#         superpositions_np_gauche_non_experts = 0
#         superpositions_np_droite_non_experts = 0
#         superpositions_pause_gauche_non_experts = 0
#         superpositions_pause_droite_non_experts = 0

#         for contexte in value:
#             if contexte[0][1] == "__UNKNOWN__":
#                 if "+" in key:
#                     superpositions_unknown_gauche_experts += 1
#                 else:
#                     superpositions_unknown_gauche_non_experts += 1
#                 superpositions_unknown_gauche += 1
#             elif contexte[0][1] == "VN":
#                 if "+" in key:
#                     superpositions_vn_gauche_experts += 1
#                 else:
#                     superpositions_vn_gauche_non_experts += 1
#                 superpositions_vn_gauche += 1
#             elif contexte[0][1] == "AP":
#                 if "+" in key:
#                     superpositions_ap_gauche_experts += 1
#                 else:
#                     superpositions_ap_gauche_non_experts += 1
#                 superpositions_ap_gauche += 1 
#             elif contexte[0][1] == "AdP":
#                 if "+" in key:
#                     superpositions_adp_gauche_experts += 1
#                 else:
#                     superpositions_adp_gauche_non_experts += 1
#                 superpositions_adp_gauche += 1
#             elif contexte[0][1] == "PP":
#                 if "+" in key:
#                     superpositions_pp_gauche_experts += 1
#                 else:
#                     superpositions_pp_gauche_non_experts += 1
#                 superpositions_pp_gauche += 1
#             elif contexte[0][1] == "CONJ":
#                 if "+" in key:
#                     superpositions_conj_gauche_experts += 1
#                 else:
#                     superpositions_conj_gauche_non_experts += 1
#                 superpositions_conj_gauche += 1
#             elif contexte[0][1] == "NP":
#                 if "+" in key:
#                     superpositions_np_gauche_experts += 1
#                 else:
#                     superpositions_np_gauche_non_experts += 1 
#                 superpositions_np_gauche += 1
#             elif contexte[0][1] == "PAUSE":
#                 if "+" in key:
#                     superpositions_pause_gauche_experts += 1
#                 else:
#                     superpositions_pause_gauche_non_experts += 1
#                 superpositions_pause_gauche += 1
#             if contexte[2][1] == "__UNKNOWN__":
#                 if "+" in key:
#                     superpositions_unknown_droite_experts += 1
#                 else:
#                     superpositions_unknown_droite_non_experts += 1
#                 superpositions_unknown_droite += 1
#             elif contexte[2][1] == "VN":
#                 if "+" in key:
#                     superpositions_vn_droite_experts += 1
#                 else:
#                     superpositions_vn_droite_non_experts += 1
#                 superpositions_vn_droite += 1
#             elif contexte[2][1] == "AP":
#                 if "+" in key:
#                     superpositions_ap_droite_experts += 1 
#                 else:
#                     superpositions_ap_droite_non_experts += 1 
#                 superpositions_ap_droite += 1 
#             elif contexte[2][1] == "AdP":
#                 if "+" in key:
#                     superpositions_adp_droite_experts += 1
#                 else:
#                     superpositions_adp_droite_non_experts += 1
#                 superpositions_adp_droite += 1
#             elif contexte[2][1] == "PP":
#                 if "+" in key:
#                     superpositions_pp_droite_experts += 1
#                 else:
#                     superpositions_pp_droite_non_experts += 1
#             elif contexte[2][1] == "CONJ":
#                 if "+" in key:
#                     superpositions_conj_droite_experts += 1
#                 else:
#                     superpositions_conj_droite_non_experts += 1
#                 superpositions_conj_droite += 1
#             elif contexte[2][1] == "NP":
#                 if "+" in key:
#                     superpositions_np_droite_experts += 1
#                 else:
#                     superpositions_np_droite_non_experts += 1
#                 superpositions_np_droite += 1
#             elif contexte[2][1] == "PAUSE":
#                 if "+" in key:
#                     superpositions_pause_droite_experts += 1
#                 else:
#                     superpositions_pause_droite_non_experts += 1
#                 superpositions_pause_droite += 1

#         liste_superpositions_unknown_gauche.append(superpositions_unknown_gauche)
#         liste_superpositions_unknown_droite.append(superpositions_unknown_droite)
#         liste_superpositions_vn_gauche.append(superpositions_vn_gauche)
#         liste_superpositions_vn_droite.append(superpositions_vn_droite)
#         liste_superpositions_ap_gauche.append(superpositions_ap_gauche)
#         liste_superpositions_ap_droite.append(superpositions_ap_droite)
#         liste_superpositions_adp_gauche.append(superpositions_adp_gauche)
#         liste_superpositions_adp_droite.append(superpositions_adp_droite)
#         liste_superpositions_pp_gauche.append(superpositions_pp_gauche)
#         liste_superpositions_pp_droite.append(superpositions_pp_droite)
#         liste_superpositions_conj_gauche.append(superpositions_conj_gauche)
#         liste_superpositions_conj_droite.append(superpositions_conj_droite)
#         liste_superpositions_np_gauche.append(superpositions_np_gauche)
#         liste_superpositions_np_droite.append(superpositions_np_droite)
#         liste_superpositions_pause_gauche.append(superpositions_pause_gauche)
#         liste_superpositions_pause_droite.append(superpositions_pause_droite)

#         liste_superpositions_unknown_gauche_experts.append(superpositions_unknown_gauche_experts)
#         liste_superpositions_unknown_droite_experts.append(superpositions_unknown_gauche_non_experts)
#         liste_superpositions_vn_gauche_experts.append(superpositions_vn_gauche_experts)
#         liste_superpositions_vn_droite_experts.append(superpositions_vn_droite_experts)
#         liste_superpositions_ap_gauche_experts.append(superpositions_ap_gauche_experts)
#         liste_superpositions_ap_droite_experts.append(superpositions_ap_droite_experts)
#         liste_superpositions_adp_gauche_experts.append(superpositions_adp_gauche_experts)
#         liste_superpositions_adp_droite_experts.append(superpositions_adp_droite_experts)
#         liste_superpositions_pp_gauche_experts.append(superpositions_pp_gauche_experts)
#         liste_superpositions_pp_droite_experts.append(superpositions_pp_droite_experts)
#         liste_superpositions_conj_gauche_experts.append(superpositions_conj_gauche_experts)
#         liste_superpositions_conj_droite_experts.append(superpositions_conj_droite_experts)
#         liste_superpositions_np_gauche_experts.append(superpositions_np_gauche_experts)
#         liste_superpositions_np_droite_experts.append(superpositions_np_droite_experts)
#         liste_superpositions_pause_gauche_experts.append(superpositions_pause_gauche_experts)
#         liste_superpositions_pause_droite_experts.append(superpositions_pause_droite_experts)

#         liste_superpositions_unknown_gauche_non_experts.append(superpositions_unknown_gauche_non_experts)
#         liste_superpositions_unknown_droite_non_experts.append(superpositions_unknown_droite_non_experts)
#         liste_superpositions_vn_gauche_non_experts.append(superpositions_vn_gauche_non_experts)
#         liste_superpositions_vn_droite_non_experts.append(superpositions_vn_droite_non_experts)
#         liste_superpositions_ap_gauche_non_experts.append(superpositions_ap_gauche_non_experts)
#         liste_superpositions_ap_droite_non_experts.append(superpositions_ap_droite_non_experts)
#         liste_superpositions_adp_gauche_non_experts.append(superpositions_adp_gauche_non_experts)
#         liste_superpositions_adp_droite_non_experts.append(superpositions_adp_droite_non_experts)
#         liste_superpositions_pp_gauche_non_experts.append(superpositions_pp_gauche_non_experts)
#         liste_superpositions_pp_droite_non_experts.append(superpositions_vn_droite_non_experts)
#         liste_superpositions_conj_gauche_non_experts.append(superpositions_conj_gauche_non_experts)
#         liste_superpositions_conj_droite_non_experts.append(superpositions_conj_droite_non_experts)
#         liste_superpositions_np_gauche_non_experts.append(superpositions_np_gauche_non_experts)
#         liste_superpositions_np_droite_non_experts.append(superpositions_np_droite_non_experts)
#         liste_superpositions_pause_gauche_non_experts.append(superpositions_pause_gauche_non_experts)
#         liste_superpositions_pause_droite_non_experts.append(superpositions_pause_droite_non_experts)

    
#     return liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts

# liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts = superpositions_chunks_gauche_droite_liste(dico_concordanciers_pauses)

# def superpositions_chunks_droite_gauche_total(liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts):

#     superpositions_total_unknown_gauche = sum(liste_superpositions_unknown_gauche)
#     superpositions_total_unknown_droite = sum(liste_superpositions_unknown_droite)
#     superpositions_total_vn_gauche = sum(liste_superpositions_vn_gauche)
#     superpositions_total_vn_droite = sum(liste_superpositions_vn_droite)
#     superpositions_total_ap_gauche = sum(liste_superpositions_ap_gauche)
#     superpositions_total_ap_droite = sum(liste_superpositions_ap_droite)
#     superpositions_total_adp_gauche = sum(liste_superpositions_adp_gauche)
#     superpositions_total_adp_droite = sum(liste_superpositions_adp_droite)
#     superpositions_total_pp_gauche = sum(liste_superpositions_pp_gauche)
#     superpositions_total_pp_droite = sum(liste_superpositions_pp_droite)
#     superpositions_total_conj_gauche = sum(liste_superpositions_conj_gauche)
#     superpositions_total_conj_droite = sum(liste_superpositions_conj_droite)
#     superpositions_total_np_gauche = sum(liste_superpositions_np_gauche)
#     superpositions_total_np_droite = sum(liste_superpositions_np_droite)
#     superpositions_total_pause_gauche = sum(liste_superpositions_pause_gauche)
#     superpositions_total_pause_droite = sum(liste_superpositions_pause_droite)

#     superpositions_total_unknown_gauche_experts = sum(liste_superpositions_unknown_gauche_experts)
#     superpositions_total_unknown_droite_experts = sum(liste_superpositions_unknown_droite_experts)
#     superpositions_total_vn_gauche_experts = sum(liste_superpositions_vn_gauche_experts)
#     superpositions_total_vn_droite_experts = sum(liste_superpositions_vn_droite_experts)
#     superpositions_total_ap_gauche_experts = sum(liste_superpositions_ap_gauche_experts)
#     superpositions_total_ap_droite_experts = sum(liste_superpositions_ap_droite_experts)
#     superpositions_total_adp_gauche_experts = sum(liste_superpositions_adp_gauche_experts)
#     superpositions_total_adp_droite_experts = sum(liste_superpositions_adp_droite_experts)
#     superpositions_total_pp_gauche_experts = sum(liste_superpositions_pp_gauche_experts)
#     superpositions_total_pp_droite_experts = sum(liste_superpositions_pp_droite_experts)
#     superpositions_total_conj_gauche_experts = sum(liste_superpositions_conj_gauche_experts)
#     superpositions_total_conj_droite_experts = sum(liste_superpositions_conj_droite_experts)
#     superpositions_total_np_gauche_experts = sum(liste_superpositions_np_gauche_experts)
#     superpositions_total_np_droite_experts = sum(liste_superpositions_np_droite_experts)
#     superpositions_total_pause_gauche_experts = sum(liste_superpositions_pause_gauche_experts)
#     superpositions_total_pause_droite_experts = sum(liste_superpositions_pause_droite_experts)

#     superpositions_total_unknown_gauche_non_experts = sum(liste_superpositions_unknown_gauche_non_experts)
#     superpositions_total_unknown_droite_non_experts = sum(liste_superpositions_unknown_droite_non_experts)
#     superpositions_total_vn_gauche_non_experts = sum(liste_superpositions_vn_gauche_non_experts)
#     superpositions_total_vn_droite_non_experts = sum(liste_superpositions_vn_droite_non_experts)
#     superpositions_total_ap_gauche_non_experts = sum(liste_superpositions_ap_gauche_non_experts)
#     superpositions_total_ap_droite_non_experts = sum(liste_superpositions_ap_droite_non_experts)
#     superpositions_total_adp_gauche_non_experts = sum(liste_superpositions_adp_gauche_non_experts)
#     superpositions_total_adp_droite_non_experts = sum(liste_superpositions_adp_droite_non_experts)
#     superpositions_total_pp_gauche_non_experts = sum(liste_superpositions_pp_gauche_non_experts)
#     superpositions_total_pp_droite_non_experts = sum(liste_superpositions_pp_droite_non_experts)
#     superpositions_total_conj_gauche_non_experts = sum(liste_superpositions_conj_gauche_non_experts)
#     superpositions_total_conj_droite_non_experts = sum(liste_superpositions_conj_droite_non_experts)
#     superpositions_total_np_gauche_non_experts = sum(liste_superpositions_np_gauche_non_experts)
#     superpositions_total_np_droite_non_experts = sum(liste_superpositions_np_droite_non_experts)
#     superpositions_total_pause_gauche_non_experts = sum(liste_superpositions_pause_gauche_non_experts)
#     superpositions_total_pause_droite_non_experts = sum(liste_superpositions_pause_droite_non_experts)

#     print(superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, "hello", superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, "hallo", superpositions_total_np_gauche, "hello", superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts)

#     return superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, superpositions_total_np_gauche, superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts
    
# superpositions_total_unknown_gauche, superpositions_total_unknown_droite, superpositions_total_vn_gauche, superpositions_total_vn_droite, superpositions_total_ap_gauche, superpositions_total_ap_droite, superpositions_total_adp_gauche, superpositions_total_adp_droite, superpositions_total_pp_gauche, superpositions_total_pp_droite, superpositions_total_conj_gauche, superpositions_total_conj_droite, superpositions_total_np_gauche, superpositions_total_np_droite, superpositions_total_pause_gauche, superpositions_total_pause_droite, superpositions_total_unknown_gauche_experts, superpositions_total_unknown_droite_experts, superpositions_total_vn_gauche_experts, superpositions_total_vn_droite_experts, superpositions_total_ap_gauche_experts, superpositions_total_ap_droite_experts, superpositions_total_adp_gauche_experts, superpositions_total_adp_droite_experts, superpositions_total_pp_gauche_experts, superpositions_total_pp_droite_experts, superpositions_total_conj_gauche_experts, superpositions_total_conj_droite_experts, superpositions_total_np_gauche_experts, superpositions_total_np_droite_experts, superpositions_total_pause_gauche_experts, superpositions_total_pause_droite_experts, superpositions_total_unknown_gauche_non_experts, superpositions_total_unknown_droite_non_experts, superpositions_total_vn_gauche_non_experts, superpositions_total_vn_droite_non_experts, superpositions_total_ap_gauche_non_experts, superpositions_total_ap_droite_non_experts, superpositions_total_adp_gauche_non_experts, superpositions_total_adp_droite_non_experts, superpositions_total_pp_gauche_non_experts, superpositions_total_pp_droite_non_experts, superpositions_total_conj_gauche_non_experts, superpositions_total_conj_droite_non_experts, superpositions_total_np_gauche_non_experts, superpositions_total_np_droite_non_experts, superpositions_total_pause_gauche_non_experts, superpositions_total_pause_droite_non_experts = superpositions_chunks_droite_gauche_total(liste_superpositions_unknown_gauche, liste_superpositions_unknown_droite, liste_superpositions_vn_gauche, liste_superpositions_vn_droite, liste_superpositions_ap_gauche, liste_superpositions_ap_droite, liste_superpositions_adp_gauche, liste_superpositions_adp_droite, liste_superpositions_pp_gauche, liste_superpositions_pp_droite, liste_superpositions_conj_gauche, liste_superpositions_conj_droite, liste_superpositions_np_gauche, liste_superpositions_np_droite, liste_superpositions_pause_gauche, liste_superpositions_pause_droite, liste_superpositions_unknown_gauche_experts, liste_superpositions_unknown_droite_experts, liste_superpositions_vn_gauche_experts, liste_superpositions_vn_droite_experts, liste_superpositions_ap_gauche_experts, liste_superpositions_ap_droite_experts, liste_superpositions_adp_gauche_experts, liste_superpositions_adp_droite_experts, liste_superpositions_pp_gauche_experts, liste_superpositions_pp_droite_experts, liste_superpositions_conj_gauche_experts, liste_superpositions_conj_droite_experts, liste_superpositions_np_gauche_experts, liste_superpositions_np_droite_experts, liste_superpositions_pause_gauche_experts, liste_superpositions_pause_droite_experts, liste_superpositions_unknown_gauche_non_experts, liste_superpositions_unknown_droite_non_experts, liste_superpositions_vn_gauche_non_experts, liste_superpositions_vn_droite_non_experts, liste_superpositions_ap_gauche_non_experts, liste_superpositions_ap_droite_non_experts, liste_superpositions_adp_gauche_non_experts, liste_superpositions_adp_droite_non_experts, liste_superpositions_pp_gauche_non_experts, liste_superpositions_pp_droite_non_experts, liste_superpositions_conj_gauche_non_experts, liste_superpositions_conj_droite_non_experts, liste_superpositions_np_gauche_non_experts, liste_superpositions_np_droite_non_experts, liste_superpositions_pause_gauche_non_experts, liste_superpositions_pause_droite_non_experts)

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

# def pauses_non_superposees_type_chunk(liste_textes):


#     dico_pauses_non_sup_par_texte = {
#              '__UNKNOWN__': [],
#                 "VN": [],
#                 "AP" : [],
#                 "AdP" : [],  
#                 "PP": [],  
#                 "CONJ": [],
#                 "NP" : [],
#                 "PAUSE" : []
#             }
    
#     dico_pauses_non_sup_par_texte_experts = {
#              '__UNKNOWN__': [],
#                 "VN": [],
#                 "AP" : [],
#                 "AdP" : [],  
#                 "PP": [],  
#                 "CONJ": [],
#                 "NP" : [],
#                 "PAUSE" : []
#             }
    
#     dico_pauses_non_sup_par_texte_non_experts = {
#              '__UNKNOWN__': [],
#                 "VN": [],
#                 "AP" : [],
#                 "AdP" : [],  
#                 "PP": [],  
#                 "CONJ": [],
#                 "NP" : [],
#                 "PAUSE" : []
#             }

#     for fichier in liste_textes:
#         unknown = 0
#         vn = 0
#         ap = 0
#         adp = 0
#         pp = 0
#         conj = 0
#         np = 0

#         fichier_chunks_pipes, num_text = obtenir_fichier_chunks_pipes(fichier)
#         liste_chunks = obtenir_texte_chunks(fichier_chunks_pipes)
#         liste_clean = gestion_recursives(liste_chunks)
#         liste_finale = normalisation_espaces(liste_clean)

    

#         for chunk, type in liste_finale:
#             if "|" in chunk and chunk != "|":
#                 if type == "__UNKNOWN__":
#                     unknown += 1
#                 elif type == "VN":
#                     vn += 1
#                 elif type == "AP":
#                     ap += 1
#                 elif type == "AdP":
#                     adp += 1
#                 elif type == "PP":
#                     pp += 1
#                 elif type == "CONJ":
#                     conj += 1
#                 elif type == "NP":
#                     pp += 1 
        
#         if "+" in fichier:
#             dico_pauses_non_sup_par_texte_experts["__UNKNOWN__"].append(unknown)
#             dico_pauses_non_sup_par_texte_experts["VN"].append(vn)
#             dico_pauses_non_sup_par_texte_experts["AP"].append(ap)
#             dico_pauses_non_sup_par_texte_experts["AdP"].append(adp)
#             dico_pauses_non_sup_par_texte_experts["PP"].append(pp)
#             dico_pauses_non_sup_par_texte_experts["CONJ"].append(conj)
#             dico_pauses_non_sup_par_texte_experts["NP"].append(np)
#         else: 
#             dico_pauses_non_sup_par_texte_non_experts["__UNKNOWN__"].append(unknown)
#             dico_pauses_non_sup_par_texte_non_experts["VN"].append(vn)
#             dico_pauses_non_sup_par_texte_non_experts["AP"].append(ap)
#             dico_pauses_non_sup_par_texte_non_experts["AdP"].append(adp)
#             dico_pauses_non_sup_par_texte_non_experts["PP"].append(pp)
#             dico_pauses_non_sup_par_texte_non_experts["CONJ"].append(conj)
#             dico_pauses_non_sup_par_texte_non_experts["NP"].append(np)

#         dico_pauses_non_sup_par_texte["__UNKNOWN__"].append(unknown)
#         dico_pauses_non_sup_par_texte["VN"].append(vn)
#         dico_pauses_non_sup_par_texte["AP"].append(ap)
#         dico_pauses_non_sup_par_texte["AdP"].append(adp)
#         dico_pauses_non_sup_par_texte["PP"].append(pp)
#         dico_pauses_non_sup_par_texte["CONJ"].append(conj)
#         dico_pauses_non_sup_par_texte["NP"].append(np)
                
#     dico_total_pauses_non_super = {key: sum(value) for key, value in dico_pauses_non_sup_par_texte.items()}
#     dico_total_pauses_non_super_experts =  {key: sum(value) for key, value in dico_pauses_non_sup_par_texte_experts.items()}
#     dico_total_pauses_non_super_non_experts =  {key: sum(value) for key, value in dico_pauses_non_sup_par_texte_non_experts.items()}

#     return dico_pauses_non_sup_par_texte, dico_pauses_non_sup_par_texte_experts, dico_pauses_non_sup_par_texte_non_experts, dico_total_pauses_non_super, dico_total_pauses_non_super_experts, dico_total_pauses_non_super_non_experts


# def erreurs(liste_textes):

#     liste_erreurs_par_texte = []
#     liste_erreurs_par_texte_experts = []
#     liste_erreurs_par_texte_non_experts = []


#     lettre_ajoutee =  r"<([a-zA-ZÀ-Ÿ])>"
#     lettre_ajoutee_et_supp = r"<~([a-zA-ZÀ-Ÿ])>"
#     mot_insere = r"{([\wÀ-Ÿ~.,;!?<>-]+]+)}"
#     chaine_inseree = r"\{([\wÀ-Ÿ]+\s+[\wÀ-Ÿ]+)+\}"

#     for texte in liste_textes:
#         with open(f"../textes_finaux/{texte}", "r") as file:
#             contenu = file.read()
#             erreur = 0
#             #print(contenu)
#             la = re.findall(lettre_ajoutee, contenu)
#             las = re.findall(lettre_ajoutee_et_supp, contenu)
#             mi = re.findall(mot_insere, contenu)
#             ci = re.findall(chaine_inseree, contenu)

#             if len(la) > 0:
#                 erreur += len(la)
#             if len(las) > 0:
#                 erreur += len(las)
#             if len(mi) > 0:
#                 erreur += len(mi)
#             if len(ci) > 0:
#                 erreur += len(ci)

#         if "+" in texte:
#             liste_erreurs_par_texte_experts.append(erreur)
#         else:
#             liste_erreurs_par_texte_non_experts.append(erreur)
#         liste_erreurs_par_texte.append(erreur)
        
#     erreurs_total_textes = sum(liste_erreurs_par_texte)
#     erreurs_total_textes_experts = sum(liste_erreurs_par_texte_experts)
#     erreurs_total_textes_non_experts = sum(liste_erreurs_par_texte_non_experts)

#     return liste_erreurs_par_texte, liste_erreurs_par_texte_experts, liste_erreurs_par_texte_non_experts, erreurs_total_textes, erreurs_total_textes_experts, erreurs_total_textes_non_experts
        

# def erreurs_comptes_par_types(liste_textes):

#     lettre_ajoutee =  r"<([a-zA-ZÀ-Ÿ])>"
#     lettre_ajoutee_et_supp = r"<~([a-zA-ZÀ-Ÿ])>"
#     mot_insere = r"{[\wÀ-Ÿ~.,;!?<>-]+}"
#     chaine_inseree = r"\{(?:[^{}]*|\{[^{}]*\})*\}"


#     for texte in liste_textes:

#         dico_erreurs_compte_texte = {
#             "LA" : [],
#             "LAS" : [],
#             "MI" : [],
#             "CI" : []
#         }

#         dico_erreurs_compte_texte_experts = {
#             "LA" : [],
#             "LAS" : [],
#             "MI" : [],
#             "CI" : []
#         }  

#         dico_erreurs_compte_texte_non_experts = {
#             "LA" : [],
#             "LAS" : [],
#             "MI" : [],
#             "CI" : []
#         }  

#         with open(f"../textes_finaux/{texte}", "r") as file:
#             contenu = file.read()
#             erreur = 0
#             #print(contenu)
#             la = re.findall(lettre_ajoutee, contenu)
#             las = re.findall(lettre_ajoutee_et_supp, contenu)
#             mi = re.findall(mot_insere, contenu)
#             ci_brute = re.findall(chaine_inseree, contenu)
            
#             # Ici j'enlève les mots uniques  OK
#             for chaine in ci_brute:
#                 retirer = re.findall(mot_insere, chaine)
#                 if len(retirer) == 1:
#                     ci_brute.remove(retirer[0])
            
#             # Ici, on vient extraire les chaines dans les chaines:
#             ci = []
#             for chaine in ci_brute:
#                 chaine_sans_frontieres = chaine[1:-1]
#                 print(chaine_sans_frontieres)
#                 if "{" and "}" in chaine_sans_frontieres:
#                     nombre_ch = chaine_sans_frontieres.count("{")
#                     if nombre_ch == 0:
#                         ci.append(chaine)
#                     elif nombre_ch == 1:
#                         chaine_imbri = re.findall(chaine_inseree, chaine_sans_frontieres)
#                         ci.append(chaine)
#                         ci.append(chaine_imbri[0])
#                 else:
#                     ci.append(chaine)
#             print(ci)


#         if "+" in texte:
#             dico_erreurs_compte_texte_experts["LA"].append(len(la))
#             dico_erreurs_compte_texte_experts["LAS"].append(len(las))
#             dico_erreurs_compte_texte_experts["MI"].append(len(mi))
#             dico_erreurs_compte_texte_experts["CI"].append(len(ci))
#         else:
#             dico_erreurs_compte_texte_non_experts["LA"].append(len(la))
#             dico_erreurs_compte_texte_non_experts["LAS"].append(len(las))
#             dico_erreurs_compte_texte_non_experts["MI"].append(len(mi))
#             dico_erreurs_compte_texte_non_experts["CI"].append(len(ci))

     
#         dico_erreurs_compte_texte["LA"].append(len(la))
#         dico_erreurs_compte_texte["LAS"].append(len(las))
#         dico_erreurs_compte_texte["MI"].append(len(mi))
#         dico_erreurs_compte_texte["CI"].append(len(ci))
        
#     dico_total_erreurs_compte = {key: sum(value) for key, value in dico_erreurs_compte_texte.items()}
#     dico_total_erreurs_compte_experts =  {key: sum(value) for key, value in dico_erreurs_compte_texte_experts.items()}
#     dico_total_erreurs_compte_non_experts =  {key: sum(value) for key, value in dico_erreurs_compte_texte_non_experts.items()}

#     return dico_erreurs_compte_texte, dico_erreurs_compte_texte_experts, dico_erreurs_compte_texte_non_experts, dico_total_erreurs_compte, dico_total_erreurs_compte_experts, dico_total_erreurs_compte_non_experts

# dico_erreurs_compte_texte, dico_erreurs_compte_texte_experts, dico_erreurs_compte_texte_non_experts, dico_total_erreurs_compte, dico_total_erreurs_compte_experts, dico_total_erreurs_compte_non_experts = erreurs_comptes_par_types(liste_textes)

# def erreurs_concordanciers(liste_textes):

#     lettre_ajoutee =  r"<([a-zA-ZÀ-Ÿ])>"
#     lettre_ajoutee_et_supp = r"<~([a-zA-ZÀ-Ÿ])>"
#     mot_insere = r"{([\wÀ-Ÿ]+)}"
#     chaine_inseree = r"\{([\wÀ-Ÿ]+\s+[\wÀ-Ÿ]+)+\}"

#     dico_concordanciers_erreurs = defaultdict(dict)

#     for fichier in liste_textes:
        
#         concordancier = {
#             "LA" : [],
#             "LAS" : [],
#             "MI" : [],
#             "CI" : [],
#         }

#         fichier_chunks_pipes, num_text = obtenir_fichier_chunks_pipes(fichier)
#         liste_chunks = obtenir_texte_chunks(fichier_chunks_pipes)
#         liste_clean = gestion_recursives(liste_chunks)
#         liste_finale = normalisation_espaces(liste_clean)
#         for i in range(len(liste_finale)-1):
#             chunk = liste_finale[i][0]
#             la = re.findall(lettre_ajoutee, chunk)
#             las = re.findall(lettre_ajoutee_et_supp, chunk)
#             mi = re.findall(mot_insere, chunk)
#             ci = re.findall(chaine_inseree, chunk)

#             if len(la) > 0:
#                 concordancier["LA"].append((liste_finale[i-1], liste_finale[i], liste_finale[i+1]))
#             if len(las) > 0:
#                 concordancier["LAS"].append((liste_finale[i-1], liste_finale[i], liste_finale[i+1]))
#             if len(mi) > 0:
#                 concordancier["MI"].append((liste_finale[i-1], liste_finale[i], liste_finale[i+1]))
#             if len(ci) > 0:
#                 concordancier["CI"].append((liste_finale[i-1], liste_finale[i], liste_finale[i+1]))

#         dico_concordanciers_erreurs[fichier.strip(".txt")] = concordancier

#     return dico_concordanciers_erreurs
# dico_concordanciers_erreurs = erreurs_concordanciers(liste_textes)

# def chunks_des_erreurs(dico_concordanciers_erreurs):

#     liste_la_dans_chunk = []
#     liste_las_dans_chunk = []
#     liste_mi_dans_chunk = []
#     liste_ci_dans_chunk = []

#     liste_la_dans_chunk_experts = []
#     liste_las_dans_chunk_experts = []
#     liste_mi_dans_chunk_experts = []
#     liste_ci_dans_chunk_experts = []

#     liste_la_dans_chunk_non_experts = []
#     liste_las_dans_chunk_non_experts = []
#     liste_mi_dans_chunk_non_experts = []
#     liste_ci_dans_chunk_non_experts = []

#     for texte, concordancier in dico_concordanciers_erreurs.items():
#         if "+" in texte:
#             contextes_la_experts = concordancier.get("LA")
#             for contexte in contextes_la_experts:
#                 #print(contexte)
#                 liste_la_dans_chunk_experts.append(contexte[1][1])
#             contextes_las_experts = concordancier.get("LAS")
#             for contexte in contextes_las_experts:
#                 #print(contexte)
#                 liste_las_dans_chunk_experts.append(contexte[1][1])
#             contextes_mi_experts = concordancier.get("MI")
#             for contexte in contextes_mi_experts:
#                 #print(contexte)
#                 liste_mi_dans_chunk_experts.append(contexte[1][1])
#             contextes_ci_experts = concordancier.get("CI")
#             for contexte in contextes_ci_experts:
#                 #print(contexte)
#                 liste_ci_dans_chunk_experts.append(contexte[1][1])
#         else:
#             contextes_la_non_experts = concordancier.get("LA")
#             for contexte in contextes_la_non_experts:
#                 #print(contexte)
#                 liste_la_dans_chunk_non_experts.append(contexte[1][1])
#             contextes_las_non_experts = concordancier.get("LAS")
#             for contexte in contextes_las_non_experts:
#                 #print(contexte)
#                 liste_las_dans_chunk_non_experts.append(contexte[1][1])
#             contextes_mi_non_experts = concordancier.get("MI")
#             for contexte in contextes_mi_non_experts:
#                 #print(contexte)
#                 liste_mi_dans_chunk_non_experts.append(contexte[1][1])
#             contextes_ci_non_experts = concordancier.get("CI")
#             for contexte in contextes_ci_non_experts:
#                 #print(contexte)
#                 liste_ci_dans_chunk_non_experts.append(contexte[1][1])

#         contextes_la = concordancier.get("LA")
#         for contexte in contextes_la:
#             #print(contexte)
#             liste_la_dans_chunk.append(contexte[1][1])
#         contextes_las = concordancier.get("LAS")
#         for contexte in contextes_las:
#             #print(contexte)
#             liste_las_dans_chunk.append(contexte[1][1])
#         contextes_mi = concordancier.get("MI")
#         for contexte in contextes_mi:
#             #print(contexte)
#             liste_mi_dans_chunk.append(contexte[1][1])
#         contextes_ci = concordancier.get("CI")
#         for contexte in contextes_ci:
#             #print(contexte)
#             liste_ci_dans_chunk.append(contexte[1][1])

#     dico_total_la_dans_chunks = Counter(liste_la_dans_chunk)
#     dico_total_las_dans_chunks = Counter(liste_las_dans_chunk)
#     dico_total_mi_dans_chunks = Counter(liste_mi_dans_chunk)
#     dico_total_ci_dans_chunks = Counter(liste_ci_dans_chunk)

#     dico_total_la_dans_chunks_experts = Counter(liste_la_dans_chunk_experts)
#     dico_total_las_dans_chunks_experts = Counter(liste_las_dans_chunk_experts)
#     dico_total_mi_dans_chunks_experts = Counter(liste_mi_dans_chunk_experts)
#     dico_total_ci_dans_chunks_experts = Counter(liste_ci_dans_chunk_experts)

#     dico_total_la_dans_chunks_non_experts = Counter(liste_la_dans_chunk_non_experts)
#     dico_total_las_dans_chunks_non_experts = Counter(liste_las_dans_chunk_non_experts)
#     dico_total_mi_dans_chunks_non_experts = Counter(liste_mi_dans_chunk_non_experts)
#     dico_total_ci_dans_chunks_non_experts = Counter(liste_ci_dans_chunk_non_experts)

#     #return dico_total_la_dans_chunks, dico_total_las_dans_chunks, dico_total_mi_dans_chunks, dico_total_ci_dans_chunks, dico_total_la_dans_chunks_experts, dico_total_la_dans_chunks_non_experts, dico_total_las_dans_chunks_experts, dico_total_las_dans_chunks_non_experts, dico_total_mi_dans_chunks_experts, dico_total_mi_dans_chunks_non_experts, dico_total_ci_dans_chunks_experts, dico_total_ci_dans_chunks_non_experts

# chunks_des_erreurs(dico_concordanciers_erreurs)
# def chunks_gauche_droite_des_erreurs(dico_concordanciers_erreurs):

#     liste_la_dans_chunk_gauche = []
#     liste_las_dans_chunk_gauche = []
#     liste_mi_dans_chunk_gauche = []
#     liste_ci_dans_chunk_gauche = []

#     liste_la_dans_chunk_droite = []
#     liste_las_dans_chunk_droite = []
#     liste_mi_dans_chunk_droite = []
#     liste_ci_dans_chunk_droite = []

#     liste_la_dans_chunk_experts_gauche = []
#     liste_las_dans_chunk_experts_gauche = []
#     liste_mi_dans_chunk_experts_gauche = []
#     liste_ci_dans_chunk_experts_gauche = []

#     liste_la_dans_chunk_experts_droite = []
#     liste_las_dans_chunk_experts_droite = []
#     liste_mi_dans_chunk_experts_droite = []
#     liste_ci_dans_chunk_experts_droite = []

#     liste_la_dans_chunk_non_experts_gauche = []
#     liste_las_dans_chunk_non_experts_gauche = []
#     liste_mi_dans_chunk_non_experts_gauche = []
#     liste_ci_dans_chunk_non_experts_gauche = []

#     liste_la_dans_chunk_non_experts_droite = []
#     liste_las_dans_chunk_non_experts_droite = []
#     liste_mi_dans_chunk_non_experts_droite = []
#     liste_ci_dans_chunk_non_experts_droite = []

#     for texte, concordancier in dico_concordanciers_erreurs.items():
#         #print(texte)
#         if "+" in texte:
#             contextes_la_experts = concordancier.get("LA")
#             for contexte in contextes_la_experts:
#                 #print(contexte)
#                 liste_la_dans_chunk_experts_gauche.append(contexte[0][1])
#                 liste_la_dans_chunk_experts_droite.append(contexte[2][1])
#             contextes_las_experts = concordancier.get("LAS")
#             for contexte in contextes_las_experts:
#                 #print(contexte)
#                 liste_las_dans_chunk_experts_gauche.append(contexte[0][1])
#                 liste_las_dans_chunk_experts_droite.append(contexte[2][1])
#             contextes_mi_experts = concordancier.get("MI")
#             for contexte in contextes_mi_experts:
#                 #print(contexte)
#                 liste_mi_dans_chunk_experts_gauche.append(contexte[0][1])
#                 liste_mi_dans_chunk_experts_droite.append(contexte[2][1])
#             contextes_ci_experts = concordancier.get("CI")
#             for contexte in contextes_ci_experts:
#                 #print(contexte)
#                 liste_ci_dans_chunk_experts_gauche.append(contexte[0][1])
#                 liste_ci_dans_chunk_experts_droite.append(contexte[2][1])
#         else:
#             contextes_la_non_experts = concordancier.get("LA")
#             for contexte in contextes_la_non_experts:
#                 #print(contexte)
#                 liste_la_dans_chunk_non_experts_gauche.append(contexte[0][1])
#                 liste_la_dans_chunk_non_experts_droite.append(contexte[2][1])
#             contextes_las_non_experts = concordancier.get("LAS")
#             for contexte in contextes_las_non_experts:
#                 #print(contexte)
#                 liste_las_dans_chunk_non_experts_gauche.append(contexte[0][1])
#                 liste_las_dans_chunk_non_experts_droite.append(contexte[2][1])
#             contextes_mi_non_experts = concordancier.get("MI")
#             for contexte in contextes_mi_non_experts:
#                 #print(contexte)
#                 liste_mi_dans_chunk_non_experts_gauche.append(contexte[0][1])
#                 liste_mi_dans_chunk_non_experts_droite.append(contexte[2][1])
#             contextes_ci_non_experts = concordancier.get("CI")
#             for contexte in contextes_ci_non_experts:
#                 #print(contexte)
#                 liste_ci_dans_chunk_non_experts_gauche.append(contexte[0][1])
#                 liste_ci_dans_chunk_non_experts_droite.append(contexte[2][1])

#         contextes_la = concordancier.get("LA")
#         for contexte in contextes_la:
#             #print(contexte)
#             liste_la_dans_chunk_gauche.append(contexte[0][1])
#             liste_la_dans_chunk_droite.append(contexte[2][1])
#         contextes_las = concordancier.get("LAS")
#         for contexte in contextes_las:
#             #print(contexte)
#             liste_las_dans_chunk_gauche.append(contexte[0][1])
#             liste_las_dans_chunk_droite.append(contexte[2][1])
#         contextes_mi = concordancier.get("MI")
#         for contexte in contextes_mi:
#             #print(contexte)
#             liste_mi_dans_chunk_gauche.append(contexte[0][1])
#             liste_mi_dans_chunk_droite.append(contexte[2][1])
#         contextes_ci = concordancier.get("CI")
#         for contexte in contextes_ci:
#             #print(contexte)
#             liste_ci_dans_chunk_gauche.append(contexte[0][1])
#             liste_ci_dans_chunk_droite.append(contexte[2][1])

#     dico_total_la_dans_chunks_gauche = Counter(liste_la_dans_chunk_gauche)
#     dico_total_las_dans_chunks_gauche = Counter(liste_las_dans_chunk_gauche)
#     dico_total_mi_dans_chunks_gauche = Counter(liste_mi_dans_chunk_gauche)
#     dico_total_ci_dans_chunks_gauche = Counter(liste_ci_dans_chunk_gauche)

#     dico_total_la_dans_chunks_droite = Counter(liste_la_dans_chunk_droite)
#     dico_total_las_dans_chunks_droite = Counter(liste_las_dans_chunk_droite)
#     dico_total_mi_dans_chunks_droite= Counter(liste_mi_dans_chunk_droite)
#     dico_total_ci_dans_chunks_droite = Counter(liste_ci_dans_chunk_droite)

#     dico_total_la_dans_chunks_gauche_experts = Counter(liste_la_dans_chunk_experts_gauche)
#     dico_total_las_dans_chunks_gauche_experts = Counter(liste_las_dans_chunk_experts_gauche)
#     dico_total_mi_dans_chunks_gauche_experts = Counter(liste_mi_dans_chunk_experts_gauche)
#     dico_total_ci_dans_chunks_gauche_experts = Counter(liste_ci_dans_chunk_experts_gauche)

#     dico_total_la_dans_chunks_droite_experts = Counter(liste_la_dans_chunk_experts_droite)
#     dico_total_las_dans_chunks_droite_experts = Counter(liste_las_dans_chunk_experts_droite)
#     dico_total_mi_dans_chunks_droite_experts = Counter(liste_mi_dans_chunk_experts_droite)
#     dico_total_ci_dans_chunks_droite_experts = Counter(liste_ci_dans_chunk_experts_droite)

#     dico_total_la_dans_chunks_gauche_non_experts = Counter(liste_la_dans_chunk_non_experts_gauche)
#     dico_total_las_dans_chunks_gauche_non_experts = Counter(liste_las_dans_chunk_non_experts_gauche)
#     dico_total_mi_dans_chunks_gauche_non_experts = Counter(liste_mi_dans_chunk_non_experts_gauche)
#     dico_total_ci_dans_chunks_gauche_non_experts = Counter(liste_ci_dans_chunk_non_experts_gauche)

#     dico_total_la_dans_chunks_droite_non_experts = Counter(liste_la_dans_chunk_non_experts_droite)
#     dico_total_las_dans_chunks_droite_non_experts = Counter(liste_las_dans_chunk_non_experts_droite)
#     dico_total_mi_dans_chunks_droite_non_experts = Counter(liste_mi_dans_chunk_non_experts_droite)
#     dico_total_ci_dans_chunks_droite_non_experts = Counter(liste_ci_dans_chunk_non_experts_droite)

#     # print("dico_total_la_dans_chunks_gauche:", dico_total_la_dans_chunks_gauche)
#     # print("dico_total_las_dans_chunks_gauche:", dico_total_las_dans_chunks_gauche)
#     # print("dico_total_mi_dans_chunks_gauche:", dico_total_mi_dans_chunks_gauche)
#     # print("dico_total_ci_dans_chunks_gauche:", dico_total_ci_dans_chunks_gauche)
#     # print("dico_total_la_dans_chunks_droite:", dico_total_la_dans_chunks_droite)
#     # print("dico_total_las_dans_chunks_droite:", dico_total_las_dans_chunks_droite)
#     # print("dico_total_mi_dans_chunks_droite:", dico_total_mi_dans_chunks_droite)
#     # print("dico_total_ci_dans_chunks_droite:", dico_total_ci_dans_chunks_droite)
#     # print("dico_total_la_dans_chunks_gauche_experts:", dico_total_la_dans_chunks_gauche_experts)
#     # print("dico_total_las_dans_chunks_gauche_experts:", dico_total_las_dans_chunks_gauche_experts)
#     # print("dico_total_mi_dans_chunks_gauche_experts:", dico_total_mi_dans_chunks_gauche_experts)
#     # print("dico_total_ci_dans_chunks_gauche_experts:", dico_total_ci_dans_chunks_gauche_experts)
#     # print("dico_total_la_dans_chunks_droite_experts:", dico_total_la_dans_chunks_droite_experts)
#     # print("dico_total_las_dans_chunks_droite_experts:", dico_total_las_dans_chunks_droite_experts)
#     # print("dico_total_mi_dans_chunks_droite_experts:", dico_total_mi_dans_chunks_droite_experts)
#     # print("dico_total_ci_dans_chunks_droite_experts:", dico_total_ci_dans_chunks_droite_experts)
#     # print("dico_total_la_dans_chunks_gauche_non_experts:", dico_total_la_dans_chunks_gauche_non_experts)
#     # print("dico_total_las_dans_chunks_gauche_non_experts:", dico_total_las_dans_chunks_gauche_non_experts)
#     # print("dico_total_mi_dans_chunks_gauche_non_experts:", dico_total_mi_dans_chunks_gauche_non_experts)
#     # print("dico_total_ci_dans_chunks_gauche_non_experts:", dico_total_ci_dans_chunks_gauche_non_experts)
#     # print("dico_total_la_dans_chunks_droite_non_experts:", dico_total_la_dans_chunks_droite_non_experts)
#     # print("dico_total_las_dans_chunks_droite_non_experts:", dico_total_las_dans_chunks_droite_non_experts)
#     # print("dico_total_mi_dans_chunks_droite_non_experts:", dico_total_mi_dans_chunks_droite_non_experts)
#     # print("dico_total_ci_dans_chunks_droite_non_experts:", dico_total_ci_dans_chunks_droite_non_experts)

#     return  dico_total_la_dans_chunks_gauche, dico_total_las_dans_chunks_gauche, dico_total_mi_dans_chunks_gauche, dico_total_ci_dans_chunks_gauche, dico_total_la_dans_chunks_gauche_experts, dico_total_las_dans_chunks_gauche_experts, dico_total_mi_dans_chunks_gauche_experts, dico_total_ci_dans_chunks_gauche_experts, dico_total_la_dans_chunks_droite_experts, dico_total_las_dans_chunks_droite_experts, dico_total_mi_dans_chunks_droite_experts, dico_total_ci_dans_chunks_droite_experts, dico_total_la_dans_chunks_gauche_non_experts, dico_total_las_dans_chunks_gauche_non_experts, dico_total_mi_dans_chunks_gauche_non_experts, dico_total_ci_dans_chunks_gauche_non_experts, dico_total_la_dans_chunks_droite_non_experts, dico_total_las_dans_chunks_droite_non_experts, dico_total_mi_dans_chunks_droite_non_experts, dico_total_ci_dans_chunks_droite_non_experts

# chunks_gauche_droite_des_erreurs(dico_concordanciers_erreurs)



def main():

    corpus_dict = get_chunk_lists("../../data/list_chunks/chunks.json")
    reconstructed_texts = get_reconstructed_texts("../../data/reconstructed_texts_behaviours")
    

if __name__ == "__main__":
    main()