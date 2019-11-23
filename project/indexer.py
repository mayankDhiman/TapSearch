
import re
"""
import nltk
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
"""

class Appearance:
    """
    Contains document's unique ID & the frequency with which a particular work occurs in a document.
    """
    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency

class Database:
    """
    In-memory database for storing documents' text and unique IDs
    """
    def __init__(self):
        self.db = dict()        
    def get(self, id):
        return self.db.get(id, None)
    def add(self, document):
        return self.db.update({document['id']: document['text']})
    def remove(self, document):
        return self.db.pop(document['id'], None)
class InvertedIndex:
    """
    In memory database used to store Inverted Index table
    """
    def __init__(self, db):
        self.index = dict()
        self.db = db
        self.uniqueID = 0

    def index_document(self, documentText, isPdf=False):
        """
        Adds a given document to inverted index table & also updates the database at the same time.

        Arguments:
            documentText -- {str} -- Textual part of a document
            isPDF -- {bool} -- True if a Document submitted is PDF 
        """
        stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
        simplifiedTokens = []
        tokens = [token.lower() for token in documentText.split(' ')]
        for token in tokens:
            if token in stop_words:
                continue
            simplifiedTokens.append(token)
        document = {'id' : self.uniqueID, 'text' : documentText}
        appearances_dict = dict()
        for term in simplifiedTokens:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        self.db.add(document)
        self.uniqueID += 1
        return document
    
    def lookup_query(self, query):
        """
        Converts a query to lower case and returns the results

        Arguments:
            query -- {str} -- Query inputted by the user

        Returns:
            () -- {tuple} -- First element -- {boolean} -- True if result was obtained
                             Second element -- {Dictionary} --  contains the result
        """ 
        query = query.lower()
        if query in self.index:
            return (True, {query: self.index[query]})
        else:
            return (False, None)
