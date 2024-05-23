

from flair.data import Sentence
from flair.models import SequenceTagger

def lire_fichier (chemin):
    f = open(chemin , encoding = 'utf−8')
    chaine = f.read ()
    f.close ()
    return chaine
liste_entite=[]
# load tagger
tagger = SequenceTagger.load("flair/ner-french")

# make example sentence
sentence = Sentence("George Washington est allé à Washington")

# predict NER tags
tagger.predict(sentence)

# print sentence
# print(sentence)

# print predicted NER spans
print('The following NER tags are found:')
# iterate over entities and print
for entity in sentence.get_spans('ner'):
    if entity.tag =="LOC":
        liste_entite.append(entity[0].text)
        print(entity[0], "and",entity.tag)
print("liste_entite : ",liste_entite)