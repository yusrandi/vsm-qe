from math import log10, sqrt

class VectorSpaceModel:
    def get_q_d(self,w_q_t):
        print("Q/D WQT dipangkatkn 2 dan diakar")

        q_d = []
        for index, document in enumerate(w_q_t):
            q_d.append({})
            total = 0
            for key, value in document.items():
                q_d[index][key] = round(value ** 2, 3)
                total += q_d[index][key]
            q_d[index]["total"] = round(sqrt(total), 3)
        return q_d
    
    def get_dj_q(self,tfidf):
        print("\nPerhitungan Sum (tfidf * tfidf_query) atau dj.q")
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

    def get_sum_of_qd(self,q_d):
        print("\nPerhitungan |dj|.|q| (jarak dokumen * jarak query)")
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

    def get_sim(self,sumtfidf, sumqd):
        print("Perhitungan dj.q / |dj|.|q|")
        sim = []
        for index, document in enumerate(sumtfidf):
            sim.append({})
            if index > 0 :
                # print(sumtfidf[index]['total'],sumqd[index]['total'])
                # sim[index] = round((sumtfidf[index]['total']/sumqd[index]['total'])*2,3) if sumqd[index]['total'] != 0 else 0
                sim[index] = round((sumtfidf[index]['total']/sumqd[index]['total']),3) if sumqd[index]['total'] != 0 else 0

        return  sim