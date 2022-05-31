import glob
import nltk
nltk.download('popular');
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
from collections import Counter
import numpy as np
from collections import OrderedDict

def give_path(fld_path):                             #give path of the folder containing all documents
    dic = {}
    file_names = glob.glob(fld_path)
    files_150 = file_names[0:10]
    for file in files_150:
        name = file.split('/')[-1]
        with open(file, 'r', errors='ignore') as f:
            data = f.read()
        dic[name] = data
    return dic

def wordList_removePuncs(doc_dict):
    stop = stopwords.words('english') + list(string.punctuation) + ['\n']
    wordList = []
    for doc in doc_dict.values():
        for word in word_tokenize(doc.lower().strip()):
            if not word in stop:
                wordList.append(word)
    return wordList

def termFrequencyInDoc(vocab, doc_dict):
    tf_docs = {}
    for doc_id in doc_dict.keys():
        tf_docs[doc_id] = {}

    for word in vocab:
        for doc_id, doc in doc_dict.items():
            tf_docs[doc_id][word] = doc.count(word)
    return tf_docs
def wordDocFre(vocab, doc_dict):
    df = {}
    for word in vocab:
        frq = 0
        for doc in doc_dict.values():
#             if word in doc.lower().split():
            if word in word_tokenize(doc.lower().strip()):
                frq = frq + 1
        df[word] = frq
    return df
def inverseDocFre(vocab,doc_fre,length):
    idf= {}
    for word in vocab:
        idf[word] = np.log2((length+1) / doc_fre[word])
    return idf
def tfidf(vocab,tf,idf_scr,doc_dict):
    tf_idf_scr = {}
    for doc_id in doc_dict.keys():
        tf_idf_scr[doc_id] = {}
    for word in vocab:
        for doc_id,doc in doc_dict.items():
            tf_idf_scr[doc_id][word] = tf[doc_id][word] * idf_scr[word]
    return tf_idf_scr

def listOfDocument() :
    dic = {}
    list_of_document = [
        "Program studi teknik informatika ada di UDB",
        "Program berbasis web",
        "Web secure, web service dan web socket adalah materi penting dalam program di UDB",
        "UDB memiliki program studi teknik informatika dan ada mata kuliah web programming",
    ]
    for x in range(len(list_of_document)):
        dic[x] = list_of_document[x]

    return  dic


def vectorSpaceModel(query, doc_dict, tfidf_scr):
    query_vocab = []
    for word in query.split():
        if word not in query_vocab:
            query_vocab.append(word)

    query_wc = {}
    for word in query_vocab:
        query_wc[word] = query.lower().split().count(word)

    relevance_scores = {}
    for doc_id in doc_dict.keys():
        score = 0
        for word in query_vocab:
            score += query_wc[word] * tfidf_scr[doc_id][word]
        relevance_scores[doc_id] = score
    sorted_value = OrderedDict(sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True))
    top_5 = {k: sorted_value[k] for k in list(sorted_value)[:5]}
    return top_5

def main():
    path = 'ACL txt/*.txt'
    docs = give_path(path)  # returns a dictionary of all docs
    # docs = listOfDocument()  # returns a dictionary of all docs
    M = len(docs)

    print("\nList Of Word")
    print(M)
    w_List = wordList_removePuncs(docs) #returns a list of tokenized words
    print(w_List)
    vocab = list(set(w_List)) #returns a list of unique words
    print(vocab)

    print("\nTerm Frequency")
    tf_dict = termFrequencyInDoc(vocab, docs)
    print(tf_dict)

    print("\nDocument Frequency")
    df_dict = wordDocFre(vocab, docs)
    print(df_dict)

    print("\nTF-IDF")
    idf_dict = inverseDocFre(vocab, df_dict, M)  # returns idf scores
    tf_idf = tfidf(vocab, tf_dict, idf_dict, docs)  # returns tf-idf socres
    print(tf_idf)

    query1 = 'Text Mining'
    query2 = 'LDA'
    query3 = 'topic modeling'
    query4 = 'Natural language Processing'
    query5 = 'generative models'
    top1 = vectorSpaceModel(query1, docs, tf_idf)  # returns top 5 documents using VSM
    top2 = vectorSpaceModel(query2, docs, tf_idf)  # returns top 5 documents using VSM
    top3 = vectorSpaceModel(query3, docs, tf_idf)  # returns top 5 documents using VSM
    top4 = vectorSpaceModel(query4, docs, tf_idf)  # returns top 5 documents using VSM
    top5 = vectorSpaceModel(query5, docs, tf_idf)  # returns top 5 documents using VSM
    print('Top 5 Documents for Query 1: \n', top1)
    print('\n')
    print('Top 5 Documents for Query 2: \n', top2)
    print('\n')
    print('Top 5 Documents for Query 3: \n', top3)
    print('\n')
    print('Top 5 Documents for Query 4: \n', top4)
    print('\n')
    print('Top 5 Documents for Query 5: \n', top5)

main()