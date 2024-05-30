import json
from pathlib import Path

from matplotlib import pyplot as plt
from tqdm.auto import tqdm
from upsetplot import from_contents, UpSet

path_corpora = Path("../DATA2")

pbar = tqdm(sorted(path_corpora.glob("*/*/*_fuze_sets.json"), reverse=True))

for path in pbar:
    pbar.set_description(str(path))
    dico_entite = json.loads(path.read_text())
    dico_entite = {k: set(v) for k, v in dico_entite.items() if k != 'sm'}
    # dico_entite = {k: set(v) for k, v in dico_entite.items()}
    test = from_contents(dico_entite)
    upset = UpSet(test, orientation='horizontal', show_percentages=True)
    upset.style_subsets(
        present=["Flair",],
        absent=["Bert", "SpaCy"],
        facecolor="red"
    )
    upset.style_subsets(
        present=["SpaCy",],
        absent=["Bert", "Flair"],
        facecolor="blue"
    )
    upset.style_subsets(
        present=["Bert",],
        absent=["Flair", "SpaCy"],
        facecolor="green"
    )
    upset.style_subsets(
        present=["Flair", "SpaCy"],
        absent=["Bert",],
        facecolor="purple"
    )

    fig = plt.figure()
    # fig.legend(loc=7)
    upset.plot(fig=fig)
    fig.figsize = (20, 20)
    plt.savefig(path.parent / (path.stem + "_wo_sm.png"))
    # plt.savefig(path.with_suffix(".png"))
    plt.close()
