import urllib.request
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords_factory = StopWordRemoverFactory()
stopwords = stopwords_factory.get_stop_words()


class QueryExpansion:

    def stateForQueryExpansion(self, kata_kunci):
        words = []
        thesaurus = {}
        words_result = ''

        # for word in kata_kunci.split(" "):
        #     stemmed_word = stemmer.stem(word)
        #     if word not in stopwords and stemmed_word not in words:
        #         words.append(stemmed_word)
        for word in kata_kunci.split(" "):
            # stemmed_word = stemmer.stem(word)
            if word  not in words:
                words.append(word)

        print('words', words)
        words = list(set(words))
        for x in words:
            # print('word on QE ', x)
            name = x
            data = {"q": name}
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            # print('word on QE encoded_data ', encoded_data)


            content = urllib.request.urlopen("https://www.sinonimkata.com/search.php", encoded_data)
            
            soup = BeautifulSoup(content, 'html.parser')
            

            # print(x)

            # print(soup.find_all('a', {'rel': 'nofollow'}))
            words_result += x + ' '
            try:

                for x in soup.find('td', {'width': '90%'}).find_all('a', {'rel': 'nofollow'}):
                    # print("all synonim ", x.get_text())
                    words_result += x.get_text() + ' '

                synonym = soup.find('td', attrs={'width': '90%'}).find_all('a')
                synonym = [x.gettext() for x in synonym]

                thesaurus[x] = [x] + synonym

            except:
                thesaurus[x] = [name]

        return words_result
