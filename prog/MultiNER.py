import os.path
from os import path

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

from flair.data import Sentence
from flair.models import SequenceTagger

import spacy

import glob
import json

def lire_fichier (chemin):
    f = open(chemin , encoding = 'utf−8')
    chaine = f.read ()
    f.close ()
    return chaine


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
# Camembert-ner
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
nlp_camenBert = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
# Flair
# spaCy


path_corpora = "../DATA_ELTeC-fra/AUDOUX/*/*.txt"

dico_entite = {}  ##stocker les sorties pour les différents outils de REN
modele = ["camenBert_ner", "sm", "lg","flair"]

for path in glob.glob(path_corpora):
    print("_____________",path)
    for m in modele:
        print(" modele ", m, "start")
        liste_entite = []
        texte = lire_fichier(path)
        if m == "camenBert_ner":

            text = nlp_camenBert(texte)
            for entite in text:
                # print(entite)
                for key, value in entite.items():
                    if value == "LOC":
                        liste_entite.append(entite["word"])
            dico_entite[m] = liste_entite
        if m == "sm" or m=="lg":
            nlp_spacy = spacy.load("fr_core_news_%s" % m)
            nlp_spacy.max_length = 35088220
            doc = nlp_spacy(texte)
            for ent in doc.ents:
                if ent.label_ == "LOC":
                    liste_entite.append(ent.text)
                    # print(m,"--->",ent.text, ent.start_char, ent.end_char, ent.label_)
            dico_entite[m] = liste_entite
        if m=="flair":
            tagger = SequenceTagger.load("flair/ner-french")
            sentence = Sentence(texte)
            tagger.predict(sentence)
            for entity in sentence.get_spans('ner'):
                if entity.tag == "LOC":
                    # print(type(str(entity[0])))
                    liste_entite.append(entity[0].text)
            # print(liste_entite)
                    # print(entity[0], "and", entity.tag)
            dico_entite[m] = liste_entite

    print(dico_entite)
    stocker("%s__multiNER.json"%path,dico_entite)