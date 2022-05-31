import glob

class ImportTxt:
   

    def export_from_txt(self, fld_path, kata_kunci):
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
