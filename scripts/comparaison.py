import difflib
import os

def get_files(reconstructed_path, saved_path):

    reconstructed_files = os.listdir(reconstructed_path)
    reconstructed_files = [file for file in reconstructed_files if file != ".DS_Store" and file.endswith(".txt")]
    reconstructed_files_list = sorted(reconstructed_files, key=lambda x: (x[0], x[1], int(x[3:-4])))

    saved_files = os.listdir(saved_path)
    saved_files = [file for file in saved_files if file != ".DS_Store" and file.endswith(".txt")]
    saved_files_list = sorted(saved_files, key=lambda x: (x[0], x[1], int(x[3:-4])))

    return reconstructed_files_list, saved_files_list

reconstructed_files_list, saved_files_list = get_files("../data/reconstructed_texts", "../data/saved_texts_txt")

def compare_files(reconstructed_files_list, saved_files_list):

    true = 0
    false = 0
    for reconstructed_file, saved_file in zip(reconstructed_files_list, saved_files_list):
        with open(f"../data/reconstructed_texts/{reconstructed_file}", "r") as rf, open(f"../data/saved_texts_txt/{saved_file}", "r") as sf:
            reconstructed_lines = rf.read().split()
            saved_lines = sf.read().split()

        words_in_reconstructed = [word for word in reconstructed_lines]
        words_in_saved = [words for words in saved_lines]

        if words_in_reconstructed == words_in_saved:
            true += 1
        else:
            false += 1
            print(reconstructed_file)
            # for a, b in zip(words_in_reconstructed, words_in_saved):
            #     if a != b:
            #         print(f"Reconstructed: {a}, Saved: {b} - difference")
            #     else:
            #         print(f"Reconstructed: {a}, Saved: {b}")

    print(f"True: {true}, False: {false}")

compare_files(reconstructed_files_list, saved_files_list)