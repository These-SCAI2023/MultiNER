from supervenn import supervenn
from matplotlib import pyplot as plt
import glob
import json
import pandas as pd
from upsetplot import from_memberships
from matplotlib import pyplot as plt
from upsetplot import from_contents, UpSet, plot
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



path_corpora = "../DATA_ELTeC-fra/DAUDET_test/DAUDET_kraken/*multiNER.json"



for path in glob.glob(path_corpora):
    print("_____________",path)
    path_output = path.split(".json")[0]
    print(path_output)
    dico_entite=lire_json(path)
    # print(dico_entite)
    dico_entite = {k: set(v) for k,v in dico_entite.items()}
    test = from_contents(dico_entite)
    upset = UpSet(
        test,
        orientation='vertical',
        # sort_by='degree',
        # subset_size='count',
        # show_counts=True,
        # totals_plot_elements=5,
        show_percentages=True
    )
    upset.style_subsets(
        present=["sm", "ls"],
        absent=[
            "flair",
            "bert"
        ],
        edgecolor="yellow",
        facecolor="blue",
    )
    fig = plt.figure()
    fig.legend(loc=7)

    upset.plot(fig=fig)
    fig.figsize = (20, 20)
    plt.suptitle("Représentation de \n l'intersection des lexiques", fontsize=20)
    plt.savefig("%s_image.png"%path_output)
    plt.show()

# # ##SuperVenn
    # for key, value in dico_entite.items():
    #     if key=="sm":
    #         sm=set(value)
    #         print(len(sm))
    #     if key=="lg":
    #         lg = set(value)
    #     if key=="camenBert":
    #         camenBert = set(value)
    #     if key=="flair":
    #         flair = set(value)

    # sets = [sm, lg, camenBert, flair]
    # labels = ["sm", "lg", "camenBert", "flair"]
    # plt.figure(figsize=(10, 6))
    # supervenn(sets, labels, widths_minmax_ratio=0.1, sets_ordering='minimize gaps', rotate_col_annotations=True, col_annotations_area_height=1.2 )
    #
    # plt.savefig("%s_image.png"%path_output,dpi=300, bbox_inches="tight")


