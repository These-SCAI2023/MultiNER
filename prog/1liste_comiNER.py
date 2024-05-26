import glob
import json


def lire_json(chemin):
    with open(chemin) as mon_fichier:
        data = json.load(mon_fichier)
    return data


def titre_auteur(chemin):
    nomfich = chemin.split("/")[-1]
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


path_corpora = "../DATA_ELTeC-fra/DAUDET/*/*chunk.json"

dico_entite = {}
dico_out = {}
modeles = ["camenBert_ner", "sm", "lg", "flair"]

for path in glob.glob(path_corpora):
    print("_____________", path)
    dico_entite = lire_json(path)
    path_output = path.split(".txt")[0]
    path_output = "%s_multiNER.json" % path_output
    print(path_output)
    # print(dico_entite)
    dico_out = {}
    for k, value in dico_entite.items():

        # print("______________________________________________________")
        # # print("résultats pour le modèle", k, "--->", value)
        # print("______________________________________________________")
        if "sm" in k:
            if "sm" not in dico_out:
                dico_out["sm"] = {}
            tmp_list = list(dico_out["sm"])
            for v in value:
                tmp_list.append(v)
            dico_out["sm"] = tmp_list
            # print(dico_out)
        if "lg" in k:
            if "lg" not in dico_out:
                dico_out["lg"] = {}
            tmp_list = list(dico_out["lg"])
            for v in value:
                tmp_list.append(v)
            dico_out["lg"] = tmp_list

        if "camenBert" in k:
            # print(k)
            if "camenBert" not in dico_out:
                dico_out["camenBert"] = {}
            tmp_list = list(dico_out["camenBert"])
            for v in value:
                tmp_list.append(v)
            dico_out["camenBert"] = tmp_list

        if "flair" in k:
            # print(k)
            if "flair" not in dico_out:
                dico_out["flair"] = {}
            tmp_list = list(dico_out["flair"])
            for v in value:
                tmp_list.append(v)
            dico_out["flair"] = tmp_list

    stocker(path_output, dico_out)