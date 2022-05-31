from selenium.webdriver.common.keys import Keys
from urllib.request import Request, urlopen
import socket

from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
from selenium import webdriver


class ImportFromWeb:
    def list_of_document_from_web(self):
        try:

            hdr = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}

            alldata = []
            
            docs_num = 16
           
            for xx in range(1,docs_num):

                url = f"https://covid19.go.id/edukasi/tokoh-agama-dan-masyarakat?page={xx}&search="
                print('url ', url)

                # response = requests.get(url, headers=hdr, timeout=100)
                # print(response.content.decode())

                browser = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver')

                browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
                browser.get(url)
                content = browser.page_source
                browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 

                browser.quit
                browser.close
                # req = Request(url, headers=hdr)
                # page = urlopen(req, timeout=10).read()
                soup = BeautifulSoup(content, 'html.parser')

                data = soup.find_all('a', {'class': 'text-color-dark'})

                for x in tqdm(data, desc='paper', unit='paper'):
                    href = x.get('href')
                    title = x.get_text()

                    # req = Request(href, headers=hdr)
                    print(href)
                    browser = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver')
                    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
                    browser.get(href)
                    content = browser.page_source
                    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
                    browser.quit
                    browser.close

                    soup = BeautifulSoup(content, 'html.parser')

                    try:
                        post_title = soup.find('div', {'class': 'post-title'})
                        print(post_title.get_text())
                        url_article = soup.find_all('div', {'id': 'konten-artikel'})
                        all_article = soup.find_all('p')
                        article = post_title.get_text()

                        for x in all_article:
                            if '#IndonesiaBangkit' in x.get_text():
                                break
                            
                            article += '\n'+x.get_text()

                            
                    except socket.timeout:
                        print("I Failed.")

                        # print(article)
                    # alldata.append({"title": post_title, "article": article})
                    alldata.append(article)
                    # with open(f'Vector Space Model/data/perjalanan_{xx}.txt', 'w') as filehandle:
                    #     filehandle.write(article)

                    

            print(f"Banyaknya Data : {len(alldata)}")
            for x in range(len(alldata)):
                with open(f'Vector Space Model/data/tokoh_agama_dan_masyarakat_{x+1}.txt', 'w') as filehandle:
                    filehandle.write(alldata[x])

        except socket.timeout:
            print("I Failed Again.")



       