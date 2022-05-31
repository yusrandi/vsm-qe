from collections import OrderedDict

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from math import log10, sqrt
import glob
import urllib.request

from bs4 import BeautifulSoup
import tqdm



factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords_factory = StopWordRemoverFactory()
stopwords = stopwords_factory.get_stop_words()
list_of_dokuments = []
list_of_dokuments_with_kk = []


def listOfDocument(kata_kunci) :
    list_of_dokuments_with_kk.append(kata_kunci)
    list_of_document = [
        "Program studi teknik informatika ada di UDB",
        "Program berbasis web",
        "Web secure, web service dan web socket adalah materi penting dalam program di UDB",
        "UDB memiliki program studi teknik informatika dan ada mata kuliah web programming",
    ]
    return  list_of_document
def give_path(fld_path, kata_kunci):                             #give path of the folder containing all documents
    dic = {}
    dic['kata_kunci'] = kata_kunci
    file_names = glob.glob(fld_path)
    files_150 = file_names
    for file in files_150:
        name = file.split('/')[-1]
        with open(file, 'r', errors='ignore') as f:
            data = f.read()
        dic[name] = data
    return dic
def list_of_document_from_web():
    from urllib.request import Request, urlopen
    import socket
    from bs4 import BeautifulSoup
    import urllib.request
    import string
    from tqdm import tqdm

    try:
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        alldata = []
        docs_num = 5

        for x in range(docs_num):

            url = f"https://covid19.go.id/vaksin-covid19?page={x+1}&search="

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
                       article += f'\n{x.get_text()}'

                except socket.timeout:
                    print("I Failed.")

                alldata.append({"title": title, "article": article})
                list_of_dokuments.append(article)
                list_of_dokuments_with_kk.append(article)

        print(f"Banyaknya Data : {len(alldata)}")
        for x in range(len(alldata)):
            with open(f'dataklasifikasitxt/doc_vaksin_{x+1}.txt', 'w') as filehandle:
                filehandle.write(list_of_dokuments[x])

    except socket.timeout:
        print("I Failed Again.")
def list_of_documents_from_txt(kata_kunci):
    list_of_dokuments_with_kk.append(kata_kunci)
    f = open("listfile.txt", "r")
    for x in f:
        list_of_dokuments.append(x)
        list_of_dokuments_with_kk.append(x)
def get_list_of_word(list_of_document, stopword):
    list_of_word = []
    for sentence in list_of_document.values():
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
def get_w_q_t(term_frequency, idf):
    w_q_t = []
    frekuensi_max = 2
    for index, document in enumerate(term_frequency):
        w_q_t.append({})

        for key, value in document.items():
            if index == 0:
                w_q_t[index][key] = (value/frekuensi_max) * idf[key]
            else:
                w_q_t[index][key] = value * idf[key]

    return w_q_t
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
# sum tfidf*tfidfquery
def get_dj_q(tfidf):
    dj_q = []
    for index, document in enumerate(tfidf):
        dj_q.append({})
        total = 0
        for key, value in document.items():
            if index > 0:
                dj_q[index][key] = value * tfidf[0][key]
                total += dj_q[index][key]
            dj_q[index]["total"] = round(sqrt(total), 3)
    return dj_q
# sum of jarak dokument * jarak query
def get_sum_of_qd(q_d):
    sum_qd = []
    for index, document in enumerate(q_d):
        sum_qd.append({})
        total = 0
        for key, value in document.items():
            if index > 0:
                sum_qd[index][key] = value * q_d[0][key]
                total += sum_qd[index][key]
            sum_qd[index]["total"] = round(sqrt(total), 3)
    return sum_qd
def get_sim(sumtfidf, sumqd):
    sim = []
    for index, document in enumerate(sumtfidf):
        sim.append({})
        if index > 0 :
            # print(sumtfidf[index]['total'],sumqd[index]['total'])
            # sim[index] = round((sumtfidf[index]['total']/sumqd[index]['total'])*2,3) if sumqd[index]['total'] != 0 else 0
            sim[index] = round((sumtfidf[index]['total']/sumqd[index]['total']),3) if sumqd[index]['total'] != 0 else 0

    return  sim

def stateForQueryExpansion(kata_kunci):
    
    words = []
    thesaurus = {}
    words_result = ''

    for word in kata_kunci.split(" "):
            stemmed_word = stemmer.stem(word)
            if word not in stopwords and stemmed_word not in words:
                words.append(stemmed_word)

    print(words)
    words = list(set(words))
    for x in words:
        name = x
        data = {"q": name}
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        content = urllib.request.urlopen("http://sinonimkata.com/search.php", encoded_data)
        soup = BeautifulSoup(content, 'html.parser')

        print(x)

        # print(soup.find_all('a', {'rel': 'nofollow'}))

        try:

            for x in soup.find('td', {'width': '90%'}).find_all('a', {'rel': 'nofollow'}):
                # print(x.get_text())
                words_result += x.get_text()+' '

            synonym = soup.find('td', attrs={'width': '90%'}).find_all('a')
            synonym = [x.gettext() for x in synonym]

            thesaurus[x] = [x] + synonym

        except:
            thesaurus[x] = [name]

    return words_result
    

def stateOfIR(kata_kunci):

    print(kata_kunci)

    query_expansion = stateForQueryExpansion(kata_kunci)
    # print(query_expansion)
    
    path = 'dataklasifikasitxt/*.txt'
    docs = give_path(path, query_expansion)
    print("\nDocument Length")
    print(len(docs))

    # print("\nList Of Document")
    # print(docs)


    # print("\nList Of Word in Documents")
    list_of_word = get_list_of_word(docs, stopwords)
    # print(list_of_word)

    # print("\nTerm Frequency")
    term_frequency = create_term_frequency(list_of_word, len(docs))
    for index, sentence in enumerate(docs.values()):
        for word in stemmer.stem(sentence).split(" "):
            if word in term_frequency[index]:
                term_frequency[index][word] += 1
    
    # print("-----------------------------------\n")

    # print("Document Frequency")

    document_frequency = create_document_frequency(list_of_word)
    for index, sentence in enumerate(term_frequency):
        if index > 0:
            for key, value in sentence.items():
                if value:
                    document_frequency[key] += 1

    
    # print("-----------------------------------\n")

    # print("D / df")
    d_df = get_d_df(len(docs)-1, document_frequency)
    # print("-----------------------------------\n")
    
    idf = get_idf(d_df)
    # print("Idf Log(df)") 
    # print("-----------------------------------\n")
    
    w_q_t = get_w_q_t(term_frequency, idf)
    
    # print("TF-IDF / Wqt")
    # for x in range(len(w_q_t)):
        # print(x, w_q_t[x])
    # print("-----------------------------------\n")

    
    print("\nPROSES SPACE MODEL \n")
    q_d = get_q_d(w_q_t)
    # print("Q/D WQT dipangkatkn 2 dan diakar")
    # print(q_d)
    # for x in q_d:
    #     print(x['total'])
    # print("-----------------------------------\n")

    # print("\nPerhitungan Sum (tfidf * tfidf_query) atau dj.q")
    sum_dj_q = get_dj_q(w_q_t)
    # for x in sum_dj_q:
    #     print(x['total'])

    # print("\nPerhitungan |dj|.|q| (jarak dokumen * jarak query)")
    sum_qd = get_sum_of_qd(q_d)
    # for x in sum_qd:
        # print(x['total'])

    kesimpulan = {}
    # print("Perhitungan dj.q / |dj|.|q|")
    sim = get_sim(sum_dj_q, sum_qd)

    i = 0
    for x in docs.keys():
        if x != 'kata_kunci':
            kesimpulan[x] = sim[i]
        i += 1

    sorted_value = OrderedDict(sorted(kesimpulan.items(), key=lambda x: x[1], reverse=True))

    print(sorted_value)
    # i = 1
    # for x in list(sorted_value)[:60]:
    #     if kesimpulan[x] >= 0 :
    #         print(i, x, kesimpulan[x])
    #     i += 1

# list_of_document_from_web()
stateOfIR("dan Tenaga Kesehatan")