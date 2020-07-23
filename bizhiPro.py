import requests
from bs4 import BeautifulSoup
import re
from threading import Thread
import time,datetime

class bingImage(Thread):
    def __init__(self):
        self.url_pre = 'https://www.bizhi.pro/recent/'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    def letGo(self):
        for page in range(1,721):
            url =self.url_pre + str(page)
            html = requests.get(url=url+'i',headers=self.headers)
            bs = BeautifulSoup(html.text,'lxml')
            get_tag = bs.findAll('img',{'class':'progressive__img progressive--is-loaded'})

            get_h3 = bs.findAll('h3')
            time = 0
            for data in get_tag:
                get_link = data.get('data-progressive')
                pic =requests.get(get_link)
                description = re.findall('<h3>(.*?)\\(',str(get_h3[time]))[0]
                file = "BingImage\\" + description + '.jpg'
                time += 1
                with open(file,'wb') as fp:
                    fp.write(pic.content)


    def run(self):
        for _ in range(15):

            th = Thread(target=self.letGo)
            th.setDaemon(True)
            th.start()
            th.join()
        #print(datetime.datetime.now())

if __name__ == '__main__':
    bingImage().run()





