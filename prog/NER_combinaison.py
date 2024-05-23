import glob
import json

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



path_corpora = "../DATA_ELTeC-fra/*/*/*.json"

dico_entite = {}  ##stocker les sorties de camembert-ner
modele = ["camenBert_ner", "sm", "lg","flair"]

for path in glob.glob(path_corpora):
    print("_____________",path)
    dico_entite=lire_json(path)
    # print(dico_entite)



# for k, value in dico_entite.items():
#     print("______________________________________________________")
#     print("résultats pour le modèle", k, "--->", value)
#     print("______________________________________________________")
    dico_intersection={}
    liste_key = []
    liste_key = list(dico_entite.keys())
    print(type(liste_key))

    i = 0
    j = 0
    for i in range(len(liste_key) - 1):
        j = 0

        while j < (len(liste_key) - 1):
            j += 1
            if liste_key[i] != liste_key[j]:
                dico_intersection[liste_key[i]+" -- "+liste_key[j]]= set(dico_entite[liste_key[i]]).intersection(set(dico_entite[liste_key[j]]))
    # print(dico_intersection)
    #             print("______________________________________________________")
    #             print("Intersection pour les ensembles ", liste_key[i], " -- ", liste_key[j], "--> ",
    #                   set(dico_entite[liste_key[i]]).intersection(set(dico_entite[liste_key[j]])))
    #             print("______________________________________________________")
    #
    # print("________________________Intersection entre les 3 modèles de langue__________________________________")
    k = 0
    for k in range(0,len(liste_key),1):
        intersection_3tools=set(dico_entite[liste_key[k]])&set(dico_entite[liste_key[(k + 1)%4]])&set(dico_entite[liste_key[(k + 2)%4]])
        dico_intersection[liste_key[k]+" -- "+liste_key[(k + 1)%4]+" -- "+liste_key[(k + 2)%4]]=intersection_3tools
        # print(liste_key[k],liste_key[(k + 1)%4],liste_key[(k + 2)%4], intersection_3tools)
    # print(dico_intersection)
    # print(f"________________________Intersection entre les {len(liste_key)} modèles de langue__________________________________")
    c=0
    intersection_multitools = dico_entite[liste_key[0]]
    for c in range(1,len(liste_key)-1,1):
        intersection_multitools=set(intersection_multitools)&set(dico_entite[liste_key[c]])
        dico_intersection["--".join(liste_key)] =intersection_multitools
    # print(intersection_multitools)
    print(dico_intersection)
    # stocker("%s_.json"%path,dico_entite)
    # print(liste_key[i], "--", liste_key[i + 1], "--", liste_key[i + 2], "--", liste_key[i + 3], " --> ",
    #       dico_entite[liste_key[i]]&dico_entite[liste_key[i + 1]]& dico_entite[liste_key[i + 2]]&dico_entite[liste_key[i + 3]])

 # ________________________________Début des tests pour la création du programme

    # print(liste_key[i], "--", liste_key[i + 1], "--", liste_key[i + 2], "--", liste_key[i + 3], " --> ",
    #       dico_entite[liste_key[i]].intersection(dico_entite[liste_key[i + 1]].intersection(dico_entite[liste_key[i + 2]])))

    # print(liste_key[i], "--", liste_key[i + 1], "--", liste_key[i + 2], "--"," --> ",dico_entite[liste_key[i]]&dico_entite[liste_key[i + 1]]& dico_entite[liste_key[i + 2]])
