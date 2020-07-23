import requests
from bs4 import BeautifulSoup
import re
from threading import Thread
import os

class bingImage(Thread):
    def __init__(self,start,end):
        self.url_pre = 'https://www.bizhi.pro/recent/'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
        self.start = start
        self.end = end

    def letGo(self):
        for page in range(self.start,self.end):
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
                path = "BingImage\\"
                if not os.path.exists(path):
                    os.makedirs(path)
                file = path + description + '.jpg'
                time += 1
                with open(file,'wb') as fp:
                    fp.write(pic.content)


    def run(self):
        Threads = []
        for _ in range(15):
            th = Thread(target=self.letGo)
            th.setDaemon(True)
            Threads.append(th)

        for i in Threads:
            i.start()
            i.join()

if __name__ == '__main__':
    start = int(input("你想从第几页开始下载？(请输入数字1-720)\n"))
    assert start>0 and start<721,"开始页数输入错误"
    end = int(input("你想下载到第几页结束？(请输入数字2-720)\n"))
    assert end>1 and end<721,"结束页数输入错误"
    bingImage(start,end).run()


