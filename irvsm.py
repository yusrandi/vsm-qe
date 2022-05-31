from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from math import log10, sqrt

from bs4 import BeautifulSoup
import urllib.request
import string
from tqdm import tqdm

factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords_factory = StopWordRemoverFactory()
stopwords = stopwords_factory.get_stop_words()
list_of_dokuments = []

def listOfDocument() :
    list_of_document = [
        "Program studi teknik informatika ada di UDB",
        "Program berbasis web",
        "Web secure, web service dan web socket adalah materi penting dalam program di UDB",
        "UDB memiliki program studi teknik informatika dan ada mata kuliah web programming",
    ]
    return  list_of_document

def get_list_of_word(list_of_document, stopword):
    list_of_word = []
    for sentence in list_of_document:
        for word in sentence.split(" "):
            stemmed_word = stemmer.stem(word)
            if word not in stopword and stemmed_word not in list_of_word:
                list_of_word.append(stemmed_word)
    return list_of_word

def get_matrix_tf(list_of_word, list_of_document):
    matrix_tf = {}
    for x in list_of_word:
        for i in range(len(list_of_document)):
            jml = list_of_document[i].lower().count(x)
            matrix_tf[(x,i)] = jml
    return  matrix_tf

def get_matrix_idf(matrix_tf, list_of_document):

    matrix_df = {}
    matrix_idf = {}
    for key, value in matrix_tf:
        matrix_df[key] = 0
        for x in range(len(list_of_document)):
           # print(matrix_tf[(key,x)])
           if matrix_tf[(key,x)] > 0:
               matrix_df[key] += 1

    print("\nMatrik df adalah banyaknya dokumen dalam koleksi dimana term/istilah muncul di dalamnya")
    print(matrix_df)

    for key, value in matrix_df.items():
        matrix_idf[key] = round(log10(len(list_of_document)/value), 3) if value != 0 else 0

    return  matrix_idf

def get_matrix_tfidf(matrix_tf, matrix_idf, list_of_word, list_of_document):
    matrix_tfidf = {}
    for key, value in matrix_idf.items():
        for i in range(len(list_of_document)):
            matrix_tfidf[key,i] = matrix_tf[(key,i)] * value
    return  matrix_tfidf

# perhitungan jarak dokumen
def get_matrix_dj(matrix_tfid, list_of_document, list_of_word):
    matrix_w = {}
    matrix_dj = {}

    for x in range(len(list_of_document)):
        matrix_w[x] = 0

    for x in list_of_word:
        for i in range(len(list_of_document)):
            value = matrix_tfid[(x,i)]
            kuadrat = round(value * value, 3)
            matrix_w[i] += kuadrat

    print(matrix_w)
    for x, value in matrix_w.items():
        matrix_dj[x] = round(sqrt(value),3)

    print("\nPerhitungan Jarak Dokumen ( |dj| )")
    print(matrix_dj)
    return matrix_dj

def get_tf_idf_query(kata_kunci, list_of_word, matrix_idf):
    matrik_tf_query = {}
    frequensi_max = 2

    # for x in list_of_word:
    #     jml = kata_kunci.lower().count(x)
    #     matrik_tf_query[x] = jml
    #     if jml > frequensi_max:
    #         frequensi_max = jml

    print("\nMatrik tf dari query/kata kunci")
    print(matrik_tf_query)
    print(f"Frekuensi Maks {frequensi_max}")

    matrik_tfidf_query = {}

    for key, value in matrik_tf_query.items():
        matrik_tfidf_query[key] = (value/frequensi_max) * matrix_idf[key]

    print("\nMatrik tfidf dari query/kata kunci")
    print(matrik_tfidf_query)
    return  matrik_tfidf_query

# Perhitungan Jarak Query ( |q| )
def get_q(matrix_tfidf_query):
    w_query = 0

    for key, value in matrix_tfidf_query.items():
        kuadrat = round(value*value,3)
        w_query += round(kuadrat,3)

    q = round(sqrt(w_query),3)
    print("\nPerhitungan Jarak Query ( |q| )")
    print(q)
    return q

# Perhitungan pengukuran similaritas query document
# Menghitung sum dari (tfidf * tfidf_query) atau dj.q

def get_sum_djq(matrik_tfidf, matrik_tfidf_query, list_of_doc):
    matrik_sum_dj_q = {}
    for x in range(len(list_of_doc)):
        matrik_sum_dj_q[x] = 0

    for key, value in matrik_tfidf_query.items():
        for x in range(len(list_of_doc)):
            WiqXqij = matrik_tfidf[(key,x)] * value
            matrik_sum_dj_q[x] += WiqXqij

    print("\nPerhitungan Sum (tfidf * tfidf_query) atau dj.q ")
    print(matrik_sum_dj_q)
    return matrik_sum_dj_q

# Menghitung dari |dj|.|q| (jarak dokumen * jarak query)
def get_djq(matrik_dj, q):
    matrik_djq = {}
    for key, value in matrik_dj.items():
        matrik_djq[key] = value * q

    print("\nPerhitungan |dj|.|q| (jarak dokumen * jarak query)")
    print(matrik_djq)
    return matrik_djq

# Menghitung dj.q / |dj|.|q|
def get_sim(matrik_sum_dj_q, matrik_djq):
    matrik_sim = {}

    for key, value in matrik_sum_dj_q.items():
        matrik_sim[key] = round(value / matrik_djq[key]) if matrik_djq[key] != 0 else 0

    print("\nPerhitungan dj.q / |dj|.|q|")
    print(matrik_sim)
    return matrik_sim
def get_kesimpulan(matrix_sim, list_of_document):
    matrix_kesimpulan = []

    for x in range(len(list_of_document)):
        matrix_kesimpulan.append({"doc": f"Dokument {x+1}","data": list_of_document[x], "nilai": matrix_sim[x]})

    matrix_kesimpulan.sort(key=lambda item: item.get("nilai"), reverse=True)

    return matrix_kesimpulan

def vsmIR():

    kata_kunci = "Program studi teknik informatika"
    list_of_document = listOfDocument()
    list_of_word = get_list_of_word(list_of_document, stopwords)

    print("list Of Word")
    print(list_of_word)

    print("\nTerm Frequency")
    matrix_tf = get_matrix_tf(list_of_word, list_of_document)
    print(matrix_tf)

    matrix_idf = get_matrix_idf(matrix_tf, list_of_document)
    print("\nInverse Document Frequensi")
    print(matrix_idf)

    print("\nMatrik Term Frequency Inverse Document Frequency (tfidf)")
    matrix_tfidf = get_matrix_tfidf(matrix_tf, matrix_idf, list_of_word, list_of_document)
    # for key, value in matrix_idf.items():
    #     for i in range(len(list_of_document)):
    #         print(key,i,matrix_tfidf[(key,i)])

    matrix_dj = get_matrix_dj(matrix_tfidf, list_of_document, list_of_word)

    matrix_tfidf_query = get_tf_idf_query(kata_kunci, list_of_word, matrix_idf)
    q = get_q(matrix_tfidf_query)
    matrix_sum_djq = get_sum_djq(matrix_tfidf, matrix_tfidf_query, list_of_document)
    matrix_djq = get_djq(matrix_dj, q)

    sim = get_sim(matrix_sum_djq,matrix_djq)
    kesimpulan = get_kesimpulan(sim, list_of_document)

    print(f"\nKata Kunci = {kata_kunci}")
    for x in kesimpulan:
        print(x)


def list_of_document_from_web():
    from urllib.request import Request, urlopen
    import socket

    try:
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        alldata = []
        docs_num = 1
        kata_kunci = "Vaksinasi dan Distribusi Vaksin"
        list_of_dokuments_with_kk = [kata_kunci]

        for x in range(docs_num):

            url = "https://covid19.go.id/edukasi/materi-edukasi?page=2&search="

            req = Request(url, headers=hdr)
            page = urlopen(req, timeout=100).read()
            soup = BeautifulSoup(page, 'html.parser')

            data = soup.find_all('a', {'class': 'text-color-dark'})

            for x in tqdm(data, desc='paper', unit='paper'):
                href = x.get('href')
                title = x.get_text()

                req = Request(href, headers=hdr)
                page = urlopen(req, timeout=100).read()
                soup = BeautifulSoup(page, 'html.parser')

                try:
                    url_article = soup.find_all('div', {'id': 'konten-artikel'})
                    all_article = soup.find_all('p')
                    article = title

                    for x in all_article:
                        article += x.get_text()
                except socket.timeout:
                    print("I Failed.")

                    # print(article)
                alldata.append({"title": title, "article": article})
                list_of_dokuments.append(article)
                list_of_dokuments_with_kk.append(article)

        print(f"Banyaknya Data : {len(list_of_dokuments)}")
        with open('listfile.txt', 'w') as filehandle:
            for list in list_of_dokuments:
                filehandle.write('%s\n' % list)

    except socket.timeout:
        print("I Failed Again.")

def list_of_documents_from_txt():
    f = open("listfile.txt", "r")
    for x in f:
        list_of_dokuments.append(x)

    return  list_of_dokuments

def stateForIR():


    from numpy import asarray
    from numpy import savetxt

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stemmer = StemmerFactory().create_stemmer()  

    alldata = []
    docs_num = 1
    kata_kunci = "penyebaran varian delta dan penyebabnya"
    list_of_dokuments = list_of_documents_from_txt()
    list_of_dokuments_with_kk = [kata_kunci]


    list_of_word = get_list_of_word(list_of_dokuments, stopwords)
    print(list_of_word)

    print("\nTerm Frequency")
    matrix_tf = get_matrix_tf(list_of_word, list_of_dokuments)
    print(matrix_tf)

    matrix_idf = get_matrix_idf(matrix_tf, list_of_dokuments)
    print("\nInverse Document Frequensi")
    print(matrix_idf)

    print("\nMatrik Term Frequency Inverse Document Frequency (tfidf)")
    matrix_tfidf = get_matrix_tfidf(matrix_tf, matrix_idf, list_of_word, list_of_dokuments)
    print(matrix_tfidf)

    matrix_dj = get_matrix_dj(matrix_tfidf, list_of_dokuments, list_of_word)
    print(matrix_dj)
    #
    # matrix_tfidf_query = get_tf_idf_query(kata_kunci, list_of_word, matrix_idf)
    # q = get_q(matrix_tfidf_query)
    # matrix_sum_djq = get_sum_djq(matrix_tfidf, matrix_tfidf_query, list_of_dokuments)
    # matrix_djq = get_djq(matrix_dj, q)
    #
    # sim = get_sim(matrix_sum_djq, matrix_djq)
    # kesimpulan = get_kesimpulan(sim, list_of_dokuments)
    #
    # print(f"\nKata Kunci = {kata_kunci}")
    # for x in kesimpulan:
    #     print(x)

# stateForIR()
list_of_document_from_web()