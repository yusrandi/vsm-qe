from math import log10, sqrt

class TfIdf:
    def create_term_frequency(self, list_of_word, length_of_document_with_kk):
        term_frequency = []
        for _ in range(length_of_document_with_kk):
            term_frequency.append(dict(zip(list_of_word, [0 for _ in range(len(list_of_word))])))
        return term_frequency
    def create_document_frequency(self, list_of_word):
        return dict(zip(list_of_word, [0 for _ in range(len(list_of_word))]))
    
    def get_d_df(self, length_of_document, document_frequency):
        d_df = {}
        for key, value in document_frequency.items():
            try:
                d_df[key] = round((length_of_document / value), 3)
            except:
                d_df[key] = 0

            # print(f"{key} =  {length_of_document} / {value} = {d_df[key]}")
        return d_df

    def get_idf(self, d_df):
        idf = {}
        for key, value in d_df.items():
            try:
                idf[key] = round(log10(value), 3)
            except:
                idf[key] = 0

        return idf
        
    def get_w_q_t(self, term_frequency, idf):
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