import re

def contains(sentence, dicti):
    """
    Esta función limpia los títulos de los labs que están mal escritos para homogeneizarlos.
    """
    for i in dicti.keys():
        if re.search(i,sentence):
            return dicti[i]
    return sentence