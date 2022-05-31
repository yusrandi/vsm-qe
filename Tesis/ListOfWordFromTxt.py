import glob

# save list of word on txt

datapath = '../datatxt/list_of_word.txt'

# write to txt
# with open(datapath, 'w') as filehandle:
#     filehandle.write(str(list_of_word))
# datatotxt = ''
# for i in range(len(list_of_word)):
#     if i > 0 :
#         datatotxt += ','
#     datatotxt += list_of_word[i]

# with open(datapath, 'w') as filehandle:
#     filehandle.write(datatotxt)

# read to txt
data_file_names = glob.glob(datapath)
with open(datapath, 'r', errors='ignore') as f:
    data = f.read()

list_of_word = []
list_of_word = data.split(',')


print(len(list_of_word))
