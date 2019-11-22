import re
import nltk
from nltk.stem.snowball import EnglishStemmer
from project.model import Documents
from project import db

class Appearance:
    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency
    

class InvertedIndex:
    def __init__(self):
        self.index = dict()

    def index_document(self, document, isPdf=False):
        stopwords = nltk.corpus.stopwords.words('english')
        simplifiedTokens = []
        tokens = [token.lower() for token in nltk.word_tokenize(document)]
        for token in tokens:
            if token in stopwords:
                continue
            simplifiedTokens.append(token)
        newDoc = Documents(text=document, isPdf=isPdf)
        db.session.add(newDoc)
        db.session.commit()
        appearances_dict = dict()
        for term in simplifiedTokens:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(newDoc.id, term_frequency + 1)
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        return document
    
    def lookup_query(self, query):
        query = query.lower()
        if query in self.index:
            return (True, {query: self.index[query]})
        else:
            return (False, None)
