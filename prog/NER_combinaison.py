import glob
import json
import pandas as pd

def lire_json (chemin):
    with open(chemin) as mon_fichier:
        data = json.load(mon_fichier)
    return data


def titre_auteur(chemin):
    nomfich= chemin.split("/")[-1]
    # nomfich= nomfich.split(".")[0]
    # nomfich= nomfich.split("_")
    # # nomfich= nomfich.upper()
    # nomfich= ("_").join([nomfich[0]])
    return nomfich


def stocker(chemin, contenu):
    w = open(chemin, "w")
    w.write(json.dumps(contenu, indent=2))
    w.close()
    # print(chemin)

    return chemin



path_corpora = "../DATA_ELTeC-fra/DAUDET_test/*/*multiNER.json"

dico_entite = {}
modeles = ["camenBert_ner", "sm", "lg","flair"]

for path in glob.glob(path_corpora):
    print("_____________",path)
    dico_entite=lire_json(path)
    path_output=path.split(".json")[0]
    # path_output = "%s_4tools-intersection.json" % path_output
    print(path_output)
    # print(dico_entite)

    # for k, value in dico_entite.items():

        # print("______________________________________________________")
        # # print("résultats pour le modèle", k, "--->", value)
        # print("______________________________________________________")

    dico_intersection={}
    liste_key = []
    liste_key = list(dico_entite.keys())
    print(liste_key)

    i = 0
    j = 0
    for i in range(len(liste_key) - 1):
        j = 0

        while j < (len(liste_key) - 1):
            j += 1
            if liste_key[i] != liste_key[j]:
                tootools= set(dico_entite[liste_key[i]]).intersection(set(dico_entite[liste_key[j]]))
                dico_intersection[liste_key[i] + " -- " + liste_key[j]] = list(tootools)
                # print("longeur de l'intersection pour 2 outils ",liste_key[i] + " -- " + liste_key[j], len(tootools))


    # stocker("%s_2tools-intersection2.json" % path_output, dico_intersection)

    # # print("________________________Intersection entre les 3 modèles de langue__________________________________")
    # k = 0
    # dico_intersection = {}
    # for k in range(0,len(liste_key),1):
    #     intersection_3tools=set(dico_entite[liste_key[k]])&set(dico_entite[liste_key[(k + 1)%4]])&set(dico_entite[liste_key[(k + 2)%4]])
    #     dico_intersection[liste_key[k]+" -- "+liste_key[(k + 1)%4]+" -- "+liste_key[(k + 2)%4]]=list(intersection_3tools)
    #     # print("longeur de l'intersection pour 3 outils ", liste_key[k]+" -- "+liste_key[(k + 1)%4]+" -- "+liste_key[(k + 2)%4], len(intersection_3tools))
    # # stocker("%s_3tools-intersection2.json" % path_output, dico_intersection)
    # # print(dico_intersection)

 # #    # print(f"________________________Intersection entre les {len(liste_key)} modèles de langue__________________________________")
 #    c=0
 #    intersection_multitools = list(dico_entite[liste_key[0]])
 #    for c in range(1,len(liste_key)-1,1):
 #        dico_intersection = {}
 #        intersection_multitools=set(intersection_multitools)&set(dico_entite[liste_key[c]])
 #        dico_intersection["--".join(liste_key)] =list(intersection_multitools)
 #    # print("longeur de l'intersection pour 4 outils ", "--".join(liste_key), len(intersection_multitools))
 # #    # print(intersection_multitools)
 # #    # print(dico_intersection)
 # #    stocker("%s_4tools-intersection2.json" % path_output, dico_intersection)


