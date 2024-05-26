import os.path
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
import glob
import json
import time


def lire_fichier(chemin):
    f = open(chemin, encoding='utf−8')
    chaine = f.read()
    f.close()
    return chaine


def stocker(chemin, contenu):
    w = open(chemin, "w")
    w.write(json.dumps(contenu, indent=2))
    w.close()
    # print(chemin)
    return chemin


path_corpora = "../DATA_ELTeC-fra/DAUDET/*/*.txt"

dico_entite = {}  ##stocker les sorties pour les différents outils de REN
dico={}
modele = ["camenBert_ner", "sm", "lg", "flair"]
seconds_total = time.time()
# Camembert-ner
seconds = time.time()
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
nlp_camenBert = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
print("Seconds since epoch Camembert-ner load =", seconds)
#Flair
seconds = time.time()
tagger = SequenceTagger.load("flair/ner-french")
print("Seconds since epoch flair load =", seconds)

for path in glob.glob(path_corpora):
    path_output = "%s_chunk.json" % path
    liste_texte = []
    # print(path_output)
    if os.path.exists(path_output):
        print("<-----Already exist ---> ", path_output)
        continue
    else:
        i = 0
        j = i+2000
        print(i)
        print(j)

        print("<_____", path)

        texte = lire_fichier(path)
        while i < len(texte):
            chunk = []
            # print(texte[i:j])
            chunk.append(texte[i:j])
            i = i+2000
            j = i + 2000
            # print(i)
            # print(j)
            # print(chunk)
            liste_texte.append(chunk)

    print("*"*10,"Le texte est divisé en", len(liste_texte), "morceaux")
    print("\n\n\n")
    for chunk_txt in liste_texte:
        print("_"*10,"annalyse du", liste_texte.index(chunk_txt), "morceau")
        print("\n\n\n")
        for m in modele:
            liste_entite = []
            dico_cle=m+"_"+str(liste_texte.index(chunk_txt))
            if m == "camenBert_ner":
                # cammembert-ner
                print("_"*10,"modele Camembert-ner start")
                text_camembertner = nlp_camenBert(str(chunk_txt))
                print("_"*10,"calcul ", m, "start")
                for entite in text_camembertner:
                    # print(entite)
                    for key, value in entite.items():
                        if value == "LOC":
                            liste_entite.append(entite["word"])
                            # print(liste_entite)
                dico_entite[dico_cle] = liste_entite
            if m == "sm" or m == "lg":
                print("_"*10,"modele ", m, "start")
                nlp_spacy = spacy.load("fr_core_news_%s" % m)
                nlp_spacy.max_length = 35088220
                doc = nlp_spacy(str(chunk_txt))
                print("_"*10,"calcul ", m, "start")
                for ent in doc.ents:
                    if ent.label_ == "LOC":
                        liste_entite.append(ent.text)
                        # print(liste_entite)
                        # print(m,"--->",ent.text, ent.start_char, ent.end_char, ent.label_)
                dico_entite[dico_cle] = liste_entite
                # print(dico_entite)
            if m == "flair":
                # flair
                print("_"*10,"modele Flair start")
                sentence = Sentence(str(chunk_txt))
                tagger.predict(sentence)
                print("_"*10,"calcul ", m, "start")
                for entity in sentence.get_spans('ner'):
                    if entity.tag == "LOC":
                        # print(type(str(entity[0])))
                        liste_entite.append(entity[0].text)
                # print(liste_entite)
                        # print(entity[0], "and", entity.tag)
                dico_entite[dico_cle] = liste_entite
        # print(dico_entite)
        print("\n\n\n")
        stocker(path_output, dico_entite)
# print("Seconds since epoch total =", seconds_total)
