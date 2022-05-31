import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf


def step1(x):
    for i in x:
        a=str(i).lower()
        p=re.sub(r'[^a-z0-9]',' ',a)
        print(p)

def get_list_of_word(list_of_document):
    list_of_word = []
    for sentence in list_of_document:
        for word in sentence.split(" "):
                list_of_word.append(word)
                
    return list_of_word
def create_term_frequency(list_of_word, length_of_document_with_kk):
    term_frequency = []
    for _ in range(length_of_document_with_kk):
        term_frequency.append(dict(zip(list_of_word, [0 for _ in range(len(list_of_word))])))
    return term_frequency

df=pd.read_excel('data/use.xls')
x  = df.head(10)
shape = df.shape[0]
# print(df)

# step1(x['Context'])
list_of_document = []
for i in range(shape):
    doc = df['Context'].loc[i]
    list_of_document.append(doc)
    
x = get_list_of_word(list_of_document)
term_frequency = create_term_frequency(x, len(list_of_document))
for index, sentence in enumerate(list_of_document):
    for word in sentence.split(" "):
        if word in term_frequency[index]:
            term_frequency[index][word] += 1
            
for value in term_frequency :
    print(value)