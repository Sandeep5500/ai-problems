import nltk
import sys
import os
import string
import copy
import math

FILE_MATCHES = 6

SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus = {}

    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name)) as f:
            corpus[file_name] = f.read().replace("\n", " ")

    return corpus

    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    text = []
    text = nltk.word_tokenize(document.lower())
    copytext = copy.deepcopy(text)

    for word in copytext:
        if (word in string.punctuation) or (word in nltk.corpus.stopwords.words("english")):
            text.remove(word)

    return text
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
  
    total = len(documents)
    # print(total)
    idfs = {}
    for content in documents.values():
        for word in content:
            count = 0
            if word not in idfs.keys():
                for filename in documents:
                    if word in documents[filename]:
                        count += 1
                # if word == "connect":
                    # print(count)        
                idfs[word] = math.log(total/count)
    return idfs            
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    file_ti = { filename : 0 for filename in files} #Dict of filename key mapped to td idf values


    for word in query:
        for filename in files:
            tf = files[filename].count(word)
            file_ti[filename] += tf*idfs[word]

    file_ti = [k for k,v in sorted(file_ti.items(),key = lambda item: item[1],reverse=True)]
    # print(file_ti[:n])
    return file_ti[:n]
    # raise NotImplementedError


def term_density(s,query):
    count = 0
    for word in query:
        if word in s:
            count+=1        
    return count/len(s)

# def compare_td(s1,s2,query):
#     if term_density(s1,query) >= term_density(s2,query):
#         return s1
#     else:  
#         return s2  

def second(s_pair):
    return s_pair[1]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # What are the types of supervised learning?

    top_list = [] # List of pairs of sentence and its corresponding idfs

    
    for s in sentences:
        idf = 0
        for word in query:
            if word in sentences[s]:
                idf += idfs[word]

        if idf == 0:
            continue
        if len(top_list) < n:
            top_list.append((s,idf))
            continue

        if idf >= min([item[1] for item in top_list]):
            min_idf = min(sentence[1] for sentence in top_list)
            min_idf_td = 1
            min_s = None
            for item in top_list:
                if item[1] == min_idf and term_density(sentences[item[0]],query) < min_idf_td:
                    min_idf_td = term_density(sentences[item[0]],query)
                    min_s = item     #The sentence with least term density out of the ones with the least idf i.e the sentence with the lowest priority in the current list of top sentences
            
            if idf > min_idf or term_density(sentences[s],query) > min_idf_td:
                top_list.remove(min_s)
                top_list.append((s,idf))

    top_list.sort(key = lambda item: term_density(sentences[item[0]],query),reverse=True)    #Sort by term densities
    top_list.sort(key = second,reverse=True) # Sort by idfs
    top_list = [x[0] for x in top_list] # Convert to list

    return top_list












    # raise NotImplementedError


if __name__ == "__main__":
    main()
