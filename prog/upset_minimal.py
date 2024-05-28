import json
from pathlib import Path

from tqdm.auto import tqdm
from matplotlib import pyplot as plt
from upsetplot import from_contents, UpSet, plot

path_corpora = Path("../DATA2")

pbar = tqdm(sorted(path_corpora.glob("*/*/*_fuze_sets.json"), reverse=True))

for path in pbar:
    pbar.set_description(str(path))
    dico_entite = json.loads(path.read_text())
    dico_entite = {k: set(v) for k, v in dico_entite.items() if k != 'sm'}
    test = from_contents(dico_entite)
    upset = UpSet(
        test,
        orientation='horizontal',
        show_percentages=True
    )

    fig = plt.figure()
    fig.legend(loc=7)
    upset.plot(fig=fig)
    fig.figsize = (20, 20)
    plt.suptitle(path.stem.replace("_fuze_sets", ""), fontsize=20)
    plt.savefig(path.parent / (path.stem + "_wo_sm.png"))
    plt.close()
