from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from math import log10, sqrt
from numpy import true_divide, vectorize
import pandas as pd
import re

from bs4 import BeautifulSoup
import urllib.request
import string
from tqdm import tqdm

# from sklearn.feature_extraction.text import TfidfVectorizer

import itertools
import numpy as np

from socket import timeout, socket


# import nltk
# from nltk import word_tokenize # to create tokens
# from nltk.corpus import stopwords # for stop words

# mendapatkn list dari tiap kata pada tiap dokument
# dimana kata2nya sudah bukan stopword sudah distemming

def get_list_of_word(list_of_document, stopword):
    list_of_word = []
    for sentence in list_of_document:
        for word in sentence.split(" "):
            stemmed_word = stemmer.stem(word)
            if word not in stopword and stemmed_word not in list_of_word:
                list_of_word.append(stemmed_word)
    return list_of_word

def create_term_frequency(list_of_word, length_of_document_with_kk):
    term_frequency = []
    for _ in range(length_of_document_with_kk):
        term_frequency.append(dict(zip(list_of_word, [0 for _ in range(len(list_of_word))])))
    return term_frequency

def create_document_frequency(list_of_word):
    return dict(zip(list_of_word, [0 for _ in range(len(list_of_word))]))

def get_d_df(length_of_document, document_frequency):
    d_df = {}
    for key, value in document_frequency.items():
        try:
            d_df[key] = round((length_of_document / value), 3)
        except:
            d_df[key] = 0

        # print(f"{key} =  {length_of_document} / {value} = {d_df[key]}")
    return d_df

def get_idf(d_df):
    idf = {}
    for key, value in d_df.items():
        try:
            idf[key] = round(log10(value), 3)
        except:
            idf[key] = 0

    return idf

def get_idf_single_dokumen(d_df):
    idf = {}
    for key, value in d_df.items():
        idf[key] = round(1 / value, 3)
    return idf

def get_w_q_t(term_frequency, idf):
    w_q_t = []
    for index, document in enumerate(term_frequency):
        w_q_t.append({})
        for key, value in document.items():
            w_q_t[index][key] = value * idf[key]
    return w_q_t

def get_bobot_kata_kunci(w_q_t, kata_kunci, list_of_word):
    bobot_kata_kunci = []
    total = 0
    for index, document in enumerate(w_q_t):
        if index > 0:
            bobot_kata_kunci.append({})
            total = 0
            for word in stemmer.stem(kata_kunci).split(" "):

                if word in list_of_word:
                    bobot_kata_kunci[index - 1][word] = document[word]
                    total += document[word]

            bobot_kata_kunci[index - 1]['total'] = total
    return bobot_kata_kunci

def get_q_d(w_q_t):
    q_d = []
    for index, document in enumerate(w_q_t):
        q_d.append({})
        total = 0
        for key, value in document.items():
            q_d[index][key] = round(value ** 2, 3)
            total += q_d[index][key]
        q_d[index]["total"] = round(sqrt(total), 3)
    return q_d

def get_bobot_kata_kunci_q_d(q_d, kata_kunci, list_of_word):
    bobot_kata_kunci_q_d = {}

    for word in stemmer.stem(kata_kunci).split(" "):
        if word in list_of_word:
            bobot_kata_kunci_q_d[word] = q_d[0][word]
    return bobot_kata_kunci_q_d

def get_bobot_kk_dan_dokumen(q_d):
    bobot_kk_dan_dokumen = {}
    for index, document in enumerate(q_d):
        for key, value in document.items():
            if key == "total":
                if index == 0:
                    bobot_kk_dan_dokumen["bobot_kata_kunci"] = value
                else:
                    bobot_kk_dan_dokumen[f"bobot_dokumen_{index}"] = value

    return bobot_kk_dan_dokumen

def get_sum_of_tf_q_d(term_frequency, bobot_kata_kunci_q_d, q_d):
    sum_of_tf_q_d = []
    for index, dokument in enumerate(term_frequency):
        if index > 0 :

            sum_of_tf_q_d.append({})
            for key, value in dokument.items():
                if key in bobot_kata_kunci_q_d:
                    sum_of_tf_q_d[index - 1][key] = value * bobot_kata_kunci_q_d[key]

    return sum_of_tf_q_d

def get_bobot_sum_of_tf_q_d(sum_of_tf_q_d):
    bobot_sum_of_tf_q_d = {}
    for index, dokument in enumerate(sum_of_tf_q_d):
        total = 0
        for _, value in dokument.items():
            total += value
        bobot_sum_of_tf_q_d[f"bobot_sum_tf_q_d_{index + 1}"] = total
    return bobot_sum_of_tf_q_d

def get_bobot_dokumen_result(bobot_sum_of_tf_q_d, bobot_kata_kunci, bobot_dokumen):
    return round(sqrt(bobot_sum_of_tf_q_d) / (bobot_kata_kunci / bobot_dokumen), 3)

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords_factory = StopWordRemoverFactory()
stopwords = stopwords_factory.get_stop_words()

def stateForIR():
    kata_kunci = "Manajemen transaksi Logistik"

    dokument_1 = "Manajemen Transaksi Logistik"
    dokument_2 = "Pengetahuan Antar Individu"
    dokument_3 = "dalam manajemen pengetahuan terdapat transfer pengetahuan logistik"

    # List yang berisi dokument dan ukurannya

    # df = pd.read_excel('data/use.xls')
    # head  = df['Context'].head(5)
    # response  = df['Text Response'].head(10)
    # kata_kunci = "corona"

    # # init data
    # list_of_context = []
    # list_of_response = []
    # list_of_context_with_kk = []
    # list_of_response_with_kk = []
    # list_of_context_with_kk.append(kata_kunci)
    # list_of_response_with_kk.append(kata_kunci)

    # for value in head:
    #     list_of_context.append(value)
    #     list_of_context_with_kk.append(value)

    # for value in response:
    #     list_of_response.append(value)
    #     list_of_response_with_kk.append(value)

    list_of_document = [dokument_1, dokument_2, dokument_3]
    list_of_document_with_kk = [kata_kunci, dokument_1, dokument_2, dokument_3]
    length_of_document = len(list_of_document)
    length_of_document_with_kk = len(list_of_document_with_kk)

    print("Kata Kunci : " + kata_kunci)
    list_of_word = get_list_of_word(list_of_document, stopwords)

    print("List Of Word")
    print(list_of_word)
    print("-----------------------------------\n")

    term_frequency = create_term_frequency(list_of_word, length_of_document_with_kk)

    for index, sentence in enumerate(list_of_document_with_kk):
        for word in stemmer.stem(sentence).split(" "):
            if word in term_frequency[index]:
                term_frequency[index][word] += 1

    print("Term Frequency")
    print(term_frequency)
    print("-----------------------------------\n")

    document_frequency = create_document_frequency(list_of_word)

    for index, sentence in enumerate(term_frequency):
        if index > 0:
            for key, value in sentence.items():
                if value:
                    document_frequency[key] += 1

    print("Documen Frequency")
    print(document_frequency)
    print("-----------------------------------\n")

    d_df = get_d_df(length_of_document, document_frequency)
    print("D / df")
    print(d_df)
    print("-----------------------------------\n")

    idf = get_idf(d_df)
    print("Idf Log(df)")
    print(idf)
    print("-----------------------------------\n")

    w_q_t = get_w_q_t(term_frequency, idf)

    print("TF-IDF / Wqt")
    print(w_q_t)
    print("-----------------------------------\n")

    bobot_kata_kunci = get_bobot_kata_kunci(w_q_t, kata_kunci, list_of_word)
    print("Bobot Kata Kunci tiap-tiap dokumen")
    print(bobot_kata_kunci)
    print("-----------------------------------\n")

    for x in range(len(bobot_kata_kunci)):
        print(f"Dokumen = {x + 1} Total =  {bobot_kata_kunci[x]['total']}")

    print("\nPROSE SPACE MODEL \n")
    q_d = get_q_d(w_q_t)
    print("Q/D WQT dipangkatkn 2 dan diakar")
    for value in q_d:
        print(value)
    print("-----------------------------------\n")

    bobot_kata_kunci_q_d = get_bobot_kata_kunci_q_d(q_d, kata_kunci, list_of_word)
    print("bobot kata kunci q_d")
    print(bobot_kata_kunci_q_d)
    print("-----------------------------------\n")

    bobot_kk_dan_dokumen = get_bobot_kk_dan_dokumen(q_d)
    print("Total Bobot Kata Kunci dan Dokument q_d")
    print(bobot_kk_dan_dokumen)

    sum_of_tf_q_d = get_sum_of_tf_q_d(term_frequency, bobot_kata_kunci_q_d, q_d)
    print("sum_of_tf_q_d")
    print(sum_of_tf_q_d)

    print("bobot_sum_of_tf_q_d")
    bobot_sum_of_tf_q_d = get_bobot_sum_of_tf_q_d(sum_of_tf_q_d)

    print("\nTotal Bobot dari Dokument Berdasarkan Kata Kunci")
    for key in bobot_sum_of_tf_q_d:
        print(key, bobot_sum_of_tf_q_d[key])

    print("\nHasil Akhir")
    hasil_akhir = []
    for x in range(length_of_document):
        document_result = get_bobot_dokumen_result(bobot_sum_of_tf_q_d[f"bobot_sum_tf_q_d_{x + 1}"],
                                                   bobot_kk_dan_dokumen["bobot_kata_kunci"],
                                                   bobot_kk_dan_dokumen[f"bobot_dokumen_{x + 1}"])
        index = x + 1
        print(f"Document {index}", document_result)
        hasil_akhir.append({"nama": f"Dokument {index}", "nilai": document_result})

    hasil_akhir.sort(key=lambda item: item.get("nilai"), reverse=True)

    # print(hasil_akhir)  
    print('Hasil Akhir')
    print('kata kunci ')
    print(kata_kunci)
    for x in range(len(hasil_akhir)):
        print(hasil_akhir[x])
def stateForChatBot():
    print("stateForChatBot")
    df = pd.read_excel('data/use.xls')
    head = df['Context'].head(11)
    response = df['Text Response'].head(11)
    kata_kunci = "bagaimana penyebaran virus corona"

    # init data
    list_of_context = []
    list_of_response = []
    list_of_context_with_kk = []
    list_of_context_with_kk.append(kata_kunci)

    for value in head:
        list_of_context.append(value)
        list_of_context_with_kk.append(value)

    for value in response:
        list_of_response.append(value)

    list_of_word = get_list_of_word(list_of_context, stopwords)

    term_frequency = create_term_frequency(list_of_word, len(list_of_context_with_kk))

    for index, sentence in enumerate(list_of_context_with_kk):
        for word in stemmer.stem(sentence).split(" "):
            if word in term_frequency[index]:
                term_frequency[index][word] += 1

    print("Term Frequency")
    print("-----------------------------------")
    print(term_frequency)

    document_frequency = create_document_frequency(list_of_word)
    for index, sentence in enumerate(term_frequency):
        if index > 0:
            for key, value in sentence.items():
                if value:
                    document_frequency[key] += 1

    print("\nDocumen Frequency")
    print("-----------------------------------")
    print(document_frequency)

    d_df = get_d_df(len(list_of_context), document_frequency)
    print("\nD / df")
    print("-----------------------------------")
    print(d_df)

    idf = get_idf(d_df)
    print("\nIdf Log(df)")
    print(idf)
    print("-----------------------------------")

    w_q_t = get_w_q_t(term_frequency, idf)

    print("\nTF-IDF / Wqt")
    print(w_q_t)
    print("-----------------------------------")

    bobot_kata_kunci = get_bobot_kata_kunci(w_q_t, kata_kunci, list_of_word)
    print("\nBobot Kata Kunci tiap-tiap dokumen")
    # print(bobot_kata_kunci)
    for x in range(len(bobot_kata_kunci)):
        print(bobot_kata_kunci[x])
    print("-----------------------------------")

    hasil_akhir = []
    for x in range(len(bobot_kata_kunci)):
        index = x + 1
        print(f"Dokumen {x + 1} value = {bobot_kata_kunci[x]['total']}")
        total = bobot_kata_kunci[x]['total']
        hasil_akhir.append({"nama": f"Dokument {index}", "index": x, "nilai": total})

    hasil_akhir.sort(key=lambda item: item.get("nilai"), reverse=True)

    for value in hasil_akhir:
        print(value)

    print("\nHASIL")
    print(kata_kunci)
    print(list_of_context[hasil_akhir[0]['index']])
    print(list_of_response[hasil_akhir[0]['index']])
def stateForQueryExpansion():
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stemmer = StemmerFactory().create_stemmer()

    docs_num = 1
    digilib_url = "http://digilib.its.ac.id/publisher/51100"
    paper = []

    for x in range(0, docs_num, 3):
        page = urllib.request.urlopen(digilib_url)
        soup = BeautifulSoup(page, 'html.parser')
        docs = soup.find_all('span', attrs={'class': 'style5'})

        link = []
        for x in docs:
            try:
                link.append(x.find('a').get('href'))
            except:
                pass

        for x in tqdm(link[:3], desc='paper', unit='paper'):

            page = urllib.request.urlopen(x)
            soup = BeautifulSoup(page, 'html.parser')

            try:
                title = soup.title.string
                abstract = soup.find('span', {'class': 'teks'}).find('p').get_text()
                paper.append([x, title, abstract])

            except:
                pass

    words = []
    processed_paper = []
    print(paper)

    for x in tqdm(paper, desc='paper', unit='paper'):
        text = x[2]
        text = text.lower()
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        text = text.translate(remove_punctuation_map)
        text = stopword.remove(text)
        text = text.split()
        text = [stemmer.stem(x) for x in text]
        processed_paper.append(' '.join(text))
        text = list(set(text))
        words += text

    print("words")
    print(words)
    thesaurus = {}

    words = list(set(words))
    for x in tqdm(words, desc='word', unit='word'):
        name = x
        data = {"q": name}
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        content = urllib.request.urlopen("http://sinonimkata.com/search.php", encoded_data)
        soup = BeautifulSoup(content, 'html.parser')

        print(x)

        # print(soup.find_all('a', {'rel': 'nofollow'}))

        try:

            for x in soup.find('td', {'width': '90%'}).find_all('a', {'rel': 'nofollow'}):
                print(x.get_text())

            synonym = soup.find('td', attrs={'width': '90%'}).find_all('a')
            synonym = [x.gettext() for x in synonym]

            thesaurus[x] = [x] + synonym

        except:
            thesaurus[x] = [name]

    # vectorizer = TfidfVectorizer(use_idf=True)
    # query = input("Masukkan Query  = ")
    # query = query.lower()
    # remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    # query = query.translate(remove_punctuation_map)
    # query = stopword.remove(query)
    # query = query.split()
    # query = [stemmer.stem(x) for x in query]

    product_query = []
    list_synonym = []

    # for x in query :
    #     if x in words :
    #         list_synonym.append(thesaurus[x])
    #     else : 
    #         name = x
    #         data = {"q": name}
    #         encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    #         content = urllib.request.urlopen("http://sinonimkata.com/search.php", encoded_data)
    #         soup = BeautifulSoup(content, 'html.parser')

    #         try: 
    #             synonym  = soup.find('td', attrs= {'width': '90%'}).find_all('a')
    #             synonym = [x.gettext() for x in synonym] 
    #             thesaurus[x] = [x] + synonym
    #             list_synonym.append(thesaurus[x])
    #         except:
    #             list_synonym.append(x)

    # qs = []
    # for x in itertools.product(*list_synonym):
    #     x = [stemmer.stem(y) for y in x]
    #     qs.append([' '.join(x)])

    # max_result = []

    # print(processed_paper)

    # for x in qs :
    #     paper_tfidf = vectorizer.fit_transform(x + processed_paper)
    #     q = paper_tfidf[0]
    #     result = cosine_similarity(paper_tfidf, q)
    #     idx = np.argsort(-result, axis=0).flatten()
    #     final = [[num, y[0], x] for num, y in enumerate(result) if y[0] > 0.0]
    #     max_result += final
def stateForPaperIR():
    from threading import Timer

    from urllib.request import Request, urlopen

    journals_url = "https://journals.sagepub.com/coronavirus"
    science_url = "https://www.sciencedirect.com/articlelist/covid"
    digilib_url = "http://digilib.its.ac.id/publisher/51100"
    main_url = "https://www.sciencedirect.com"
    satgas_covid19_url = "https://covid19.go.id/edukasi/materi-edukasi"

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stemmer = StemmerFactory().create_stemmer()

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    # page = urllib.request.urlopen(journals_url)
    # soup = BeautifulSoup(page, 'html.parser')

    try:
        # page = urllib.request.urlopen(journals_url, headers={'User-Agent': 'Mozilla/5.0'})
        # soup = BeautifulSoup(page, 'html.parser')

        # req = Request(satgas_covid19_url, headers=hdr)
        # page = urlopen(req, timeout=10).read()
        # soup = BeautifulSoup(page, 'html.parser')

        # data = soup.find_all('a', {'class': 'text-color-dark'})

        alldata = []
        docs_num = 10
        kata_kunci = "Panduan Penyelenggaraan Ibadah"
        list_of_dokuments = []
        list_of_dokuments_with_kk = [kata_kunci]

        for x in range(docs_num):

            url = f"https://covid19.go.id/edukasi/materi-edukasi?page={x + 1}"

            req = Request(url, headers=hdr)
            page = urlopen(req, timeout=100).read()
            soup = BeautifulSoup(page, 'html.parser')

            data = soup.find_all('a', {'class': 'text-color-dark'})

            for x in tqdm(data, desc='paper', unit='paper'):
                href = x.get('href')
                title = x.get_text()

                # print(title)

                #     print(href)
                req = Request(href, headers=hdr)
                page = urlopen(req, timeout=10).read()
                soup = BeautifulSoup(page, 'html.parser')

                url_article = soup.find_all('div', {'id': 'konten-artikel'})
                all_article = soup.find_all('p')
                article = title
                for x in all_article:
                    article += x.get_text()

                # print(article)
                alldata.append({"title": title, "article": article})
                list_of_dokuments.append(article)
                list_of_dokuments_with_kk.append(article)

        print(f"Banyaknya Data : {len(list_of_dokuments)}")

        list_of_word = get_list_of_word(list_of_dokuments, stopwords)
        # print(list_of_word)
        # print(len(list_of_word))

        term_frequency = create_term_frequency(list_of_word, len(list_of_dokuments_with_kk))
        for index, sentence in enumerate(list_of_dokuments_with_kk):
            for word in stemmer.stem(sentence).split(" "):
                if word in term_frequency[index]:
                    term_frequency[index][word] += 1

        # print("Term Frequency")
        # print(term_frequency)
        # # print("-----------------------------------\n")

        document_frequency = create_document_frequency(list_of_word)

        for index, sentence in enumerate(term_frequency):
            if index > 0:
                for key, value in sentence.items():
                    if value:
                        document_frequency[key] += 1

        # print("Documen Frequency")
        # print(document_frequency)
        # # print("-----------------------------------\n")

        d_df = get_d_df(len(list_of_dokuments), document_frequency)
        # # print("D / df")
        # # print(d_df)
        # # print("-----------------------------------\n")

        idf = get_idf(d_df)
        # # print("Idf Log(df)")
        # # print(idf)
        # # print("-----------------------------------\n")

        w_q_t = get_w_q_t(term_frequency, idf)

        # print("TF-IDF / Wqt")
        # print(w_q_t)
        # print("-----------------------------------\n")

        bobot_kata_kunci = get_bobot_kata_kunci(w_q_t, kata_kunci, list_of_word)
        # print("Bobot Kata Kunci tiap-tiap dokumen")
        # for x in bobot_kata_kunci:
        #     print(x)
        # print("-----------------------------------\n")

        # print(f"Kata Kunci  = {kata_kunci}")
        # for x in range(len(bobot_kata_kunci)) :
        #     title = alldata[x]['title']
        #     print(f"Dokumen ke - {x+1} = {title} Total =  {bobot_kata_kunci[x]['total']}")

        print("\nPROSE SPACE MODEL \n")
        q_d = get_q_d(w_q_t)
        # print("Q/D WQT dipangkatkn 2 dan diakar")
        # print(q_d)
        # print("-----------------------------------\n")

        bobot_kata_kunci_q_d = get_bobot_kata_kunci_q_d(q_d, kata_kunci, list_of_word)
        # print("bobot kata kunci q_d")
        # print(bobot_kata_kunci_q_d)
        # print("-----------------------------------\n")

        bobot_kk_dan_dokumen = get_bobot_kk_dan_dokumen(q_d)
        # print("Total Bobot Kata Kunci dan Dokument q_d")
        # print(bobot_kk_dan_dokumen)

        sum_of_tf_q_d = get_sum_of_tf_q_d(term_frequency, bobot_kata_kunci_q_d)
        print("sum_of_tf_q_d")
        # print(sum_of_tf_q_d)
        for x in range(len(list_of_dokuments)):
            data = sum_of_tf_q_d[x]
            printdata = f"Doc {x + 1}, Hasil = {data}"
            print(printdata)

        bobot_sum_of_tf_q_d = get_bobot_sum_of_tf_q_d(sum_of_tf_q_d)

        # print("bobot_sum_of_tf_q_d")

        # print("\nTotal Bobot dari Dokument Berdasarkan Kata Kunci")
        # for key in bobot_sum_of_tf_q_d:
        #     print(key, bobot_sum_of_tf_q_d[key])  

        # print("\nHasil Akhir")
        hasil_akhir = []
        for x in range(len(list_of_dokuments)):
            document_result = get_bobot_dokumen_result(bobot_sum_of_tf_q_d[f"bobot_sum_tf_q_d_{x + 1}"],
                                                       bobot_kk_dan_dokumen["bobot_kata_kunci"],
                                                       bobot_kk_dan_dokumen[f"bobot_dokumen_{x + 1}"])
            index = x + 1
            title = alldata[x]['title']

            hasil_akhir.append({"doc": f"{index}, {title}", "nilai": document_result})

        hasil_akhir.sort(key=lambda item: item.get("nilai"), reverse=True)

        print(kata_kunci)
        for x in hasil_akhir:
            print(x)

        print("I tried.")
    except Exception as exc:
        print("I Failed.")
        print(exc)


# stateForChatBot()
# stateForIR()
stateForQueryExpansion()
# stateForPaperIR()
