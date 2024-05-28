# import time
import json
from pathlib import Path

# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline
from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
from tqdm.auto import tqdm


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
modele = [# "camenBert_ner",
    # "sm",
    # "lg",
    "flair"]

# Camembert-ner
# tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
# model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
# nlp_camenBert = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
# print("Seconds since epoch Camembert-ner load =", seconds)

# Flair
tagger = SequenceTagger.load("flair/ner-french")
# print("Seconds since epoch flair load =", seconds)

spacys = {}
for m in modele:
    if m == "sm":
        spacys[m] = spacy.load("fr_core_news_sm")
        spacys[m].max_length = 35088220
    if m == "lg":
        spacys[m] = spacy.load("fr_core_news_lg")
        spacys[m].max_length = 35088220

pbar = tqdm(list(path_corpora.glob("*/*/*.txt")))
for path in pbar:
    dico_entite = {}

    path_output = f"{path.name}_flair_only.json"
    texte = lire_fichier(path)

    pbar.set_description(f"Traitement de {path.name}")

    for m in modele:
        liste_entite = []

        if m == "camenBert_ner":
            pbar.set_postfix_str("Camembert-ner 1")
            text_camembertner = nlp_camenBert(texte)
            pbar.set_postfix_str("Camembert-ner 2")
            dico_entite[m] = [entite["word"] for entite in text_camembertner if entite["entity"] == "LOC"]

        if m in ("sm", "lg"):
            pbar.set_postfix_str(f"Spacy {m} 1")
            doc = spacys[m](texte)
            pbar.set_postfix_str(f"Spacy {m} 2")
            dico_entite[m] = [ent.text for ent in doc.ents if ent.label_ == "LOC"]

        if m == "flair":
            try:
                pbar.set_postfix_str(f"Flair 1")
                sentence = Sentence(texte)
                tagger.predict(sentence)
                pbar.set_postfix_str(f"Flair 2")
                dico_entite[m] = [entity[0].text for entity in sentence.get_spans('ner') if entity.tag == "LOC"]
            except Exception as e:
                print(e)
                texte1, texte2 = texte[:len(texte) // 2], texte[len(texte) // 2:]
                sentence1 = Sentence(texte1)
                tagger.predict(sentence1)
                dico_entite[m] = [entity[0].text for entity in sentence1.get_spans('ner') if entity.tag == "LOC"]
                del sentence1
                sentence2 = Sentence(texte2)
                tagger.predict(sentence2)
                pbar.set_postfix_str(f"Flair 1")
                dico_entite[m].extend([entity[0].text for entity in sentence2.get_spans('ner') if entity.tag == "LOC"])

    stocker(path_output, dico_entite)  # print("Seconds since epoch total =", seconds_total)
