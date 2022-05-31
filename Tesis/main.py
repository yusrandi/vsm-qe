from urllib.request import Request, urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import socket
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver

from pydoc import importfile
from importtxt import ImportTxt
from queryexpansion import QueryExpansion
from praprocessing import PraProcessing
from importfromweb import ImportFromWeb


# impor = ImportTxt()
# queryExpansion = QueryExpansion()
# praProcess = PraProcessing()
# importFromWeb = ImportFromWeb()



kata_kunci = "pembelajaran tatap muka di masa pandemi covid-19"

# kata_kunci = queryExpansion.stateForQueryExpansion(kata_kunci)
# print('QE Kata Kunci ', kata_kunci)

# path = '../dataklasifikasitxt/*.txt'
# docs = impor.export_from_txt(path, kata_kunci)
# print("\nDocument Length : ", len(docs))

# list_of_word = praProcess.get_list_of_word(docs)
# print('list of word ', len(list_of_word))

# importFromWeb.list_of_document_from_web()
# f = open("Vector Space Model/data/myfile.txt", "w")
# f.write("Woops! I have deleted the content!")
# f.close()


