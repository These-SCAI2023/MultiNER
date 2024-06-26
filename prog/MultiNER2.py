import json
from pathlib import Path

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
from tqdm.auto import tqdm
from torch.cuda import empty_cache, OutOfMemoryError


def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def stocker(chemin, contenu):
    with open(chemin, "w") as f:
        json.dump(contenu, f, indent=2)
        return chemin


def upd_dico(chemin, contenu):
    with open(chemin, "r") as f:
        dico = json.load(f)
        dico.update(contenu)
    with open(chemin, "w") as f:
        json.dump(dico, f, indent=2)
        return chemin


path_corpora = Path("../DATA2")

dico = {}
modele = [
    "camenBert_ner",
    # "sm",
    # "lg",
    # "flair"
]

# Camembert-ner
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
nlp_camenBert = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple", device="cuda")

# Flair
tagger = SequenceTagger.load("flair/ner-french")

nlp = spacy.load("fr_core_news_sm")
nlp.max_length = 35088220

spacys = {}
for m in modele:
    if m == "sm":
        spacys[m] = spacy.load("fr_core_news_sm")
        spacys[m].max_length = 35088220
    if m == "lg":
        spacys[m] = spacy.load("fr_core_news_lg")
        spacys[m].max_length = 35088220

pbar = tqdm(sorted(path_corpora.glob("*/*/*.txt"), reverse=True))
for path in pbar:
    path_output = path.parent / f"{path.name}_bert_only.json"
    # if path_output.exists():
    #     continue

    dico_entite = {}

    texte = lire_fichier(path)

    pbar.set_description(f"Traitement de {path.name}")

    for m in modele:
        liste_entite = []

        if m == "camenBert_ner":
            pbar.set_postfix_str("Camembert-ner 1")
            # text_camembertner = nlp_camenBert(texte)
            # pbar.set_postfix_str("Camembert-ner 2")
            # dico_entite[m] = [entite["word"] for entite in text_camembertner for key, value in entite.items() if value == "LOC"]
            # nb_chunks = len(texte) // 500
            # chunks = [0] + [len(texte) // nb_chunks * j for j in range(1, nb_chunks)] + [len(texte)]
            doc = nlp(texte)
            sents = [sent.text.strip() for sent in doc.sents]

            dico_entite[m] = []
            for s in sents:
                text_camembertner = nlp_camenBert(s)
                dico_entite[m].extend([entite["word"] for entite in text_camembertner for key, value in entite.items() if value == "LOC"])


        if m in ("sm", "lg"):
            pbar.set_postfix_str(f"Spacy {m} 1")
            doc = spacys[m](texte)
            pbar.set_postfix_str(f"Spacy {m} 2")
            dico_entite[m] = [ent.text for ent in doc.ents if ent.label_ == "LOC"]

        if m == "flair":
            i = 0
            pbar.set_postfix_str(f"Flair 1")
            while i < 10:
                try:
                    if i == 0:
                        sentence = Sentence(texte)
                        tagger.predict(sentence)
                        pbar.set_postfix_str(f"Flair 2")
                        dico_entite[m] = [entity[0].text for entity in sentence.get_spans('ner') if entity.tag == "LOC"]
                        break
                    else:
                        empty_cache()
                        print(f"Erreur {i}")
                        chunks = [0] + [len(texte) // i * j for j in range(1, i)] + [len(texte)]
                        dico_entite[m] = []
                        for j in range(i):
                            sentence = Sentence(texte[chunks[j]:chunks[j + 1]])
                            tagger.predict(sentence)
                            dico_entite[m].extend([entity[0].text for entity in sentence.get_spans('ner') if entity.tag == "LOC"])
                        break
                except OutOfMemoryError:
                    if i == 0:
                        i = 2
                    else:
                        i += 1
            else:
                raise OutOfMemoryError

    stocker(path_output, dico_entite)
