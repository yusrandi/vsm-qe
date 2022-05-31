from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords_factory = StopWordRemoverFactory()
stopwords = stopwords_factory.get_stop_words()

class PraProcessing:
    def get_list_of_word(self, list_of_document):
        list_of_word = []
        for sentence in list_of_document.values():
            for word in sentence.split(" "):
                stemmed_word = stemmer.stem(word)
                if word not in stopwords and stemmed_word not in list_of_word:
                    list_of_word.append(stemmed_word)
        return list_of_word