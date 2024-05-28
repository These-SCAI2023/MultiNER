import json
from pathlib import Path

from tqdm.auto import tqdm

path_corpora = Path("../DATA2")

pbar = tqdm(sorted(path_corpora.glob("*/*/*.txt"), reverse=True))

suffix_to_fuze = {
    "_others.json",
    "_flair_only.json",
}

for path in pbar:
    pbar.set_description(str(path))
    for suffix in suffix_to_fuze:
        if not (path.parent / (path.name + suffix)).exists():
            print(f"{path.name + suffix} not found")
            continue

    dico = {}
    for suffix in suffix_to_fuze:
        with open(path.parent / (path.name + suffix), "r") as f:
            dico.update(json.load(f))

    with open(path.parent / (path.name + "_fuze.json"), "w") as f:
        json.dump(dico, f, indent=2)

    dico_sets = {k: list(set(v)) for k, v in dico.items()}

    with open(path.parent / (path.name + "_fuze_sets.json"), "w") as f:
        json.dump(dico_sets, f, indent=2)



