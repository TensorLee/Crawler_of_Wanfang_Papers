import requests
from bs4 import BeautifulSoup
import datetime
import time
import pymongo
# import multiprocessing as mp
import threading
import random

client = pymongo.MongoClient('localhost', 27017)
db = client['wanfang']
finalWanfangPapers = db["finalWanfangPapers"]
# 设置要抓取的总页数 76232
ALL_PAGE_NUMBER = 76232
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
base_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E8%AE%A1%E7%AE%97%E6%9C%BA+%E5%88%86%E7%B1%BB%E5%8F%B7%3a%22TP*%22&f=subjectCatagory&p='
proxy_url = 'http://www.xicidaili.com/nn/'

# def get_ip_list(proxy_url, headers):
#     web_data = requests.get(proxy_url, headers=headers)
#     soup = BeautifulSoup(web_data.text, 'lxml')
#     ips = soup.find_all('tr')
#     proxy_list = []
#     for i in range(1, len(ips)):
#         ip_info = ips[i]
#         tds = ip_info.find_all('td')
#         proxy_list.append(tds[1].text + ':' + tds[2].text)
#     return proxy_list
def get_html(url):
    try:
        # proxy_ip = random.choice(proxy_list)
        # proxies = {'http': proxy_ip}
        html = requests.get(url, headers=headers)
    except:
        time.sleep(10)
        html = get_html(url)
    return html

def startGrab(start_page, end_page):
    current_page = start_page
    for current_page in range(current_page, end_page + 1):
        url = base_url + str(current_page)
        # html, proxies = get_html(proxy_list, url)
        html = get_html(url)
        soup = BeautifulSoup(html.content, "lxml")
        # print("正在使用"+str(proxies) + "爬取" + url)
        print("正在爬取" + url)
        record_item = soup.find_all('div', {'class' : 'record-item'})
        for item in record_item:
            title = item.find('a', {'class' : 'title'}).text.replace(' ', '')
            info = item.find('div', {'class' : 'record-subtitle'})
            try:
                core_list = info.find('span', {'class' : 'core'}).find_all('span')
                cores = []
                for core in core_list:
                    # print(span.text)
                    cores.append(core.text.strip())
            except:
                cores = []
            a_list = info.find_all('a')
            try:
                public = a_list[0].text.strip()  
            except:
                public = ""
            try:
                time = a_list[1].text.strip()
            except:
                time = ""
            authors = []
            try:
                for i in range(2, len(a_list)):
                    authors.append(a_list[i].text)
            except:
                pass
            try:
                abstract = item.find('div', {'class' : 'record-desc'}).text.replace(' ', '').replace('\n', '').replace('\r', '')
            except:
                abstract = ""
            try:
                keywords_list = item.find('div', {'class' : 'record-keyword'}).find_all('span')
                keywords = []
                for keyword in keywords_list:
                    keywords.append(keyword.text.strip())
            except:
                keywords = []
            # try:
            #     read_link = item.find('a', {'class' : 'view'}).get('href').replace(' ', '')
            # except:
            #     read_link = ""
            # try:
            #     download_link = item.find('a', {'class': 'download'}).get('href').replace(' ', '')
            # except:
            #     download_link = ""
            dict = {'标题':title, '期刊':public, '收录': cores, '时间':time, '作者':authors,\
            '摘要':abstract, '关键词':keywords}
            # print(dict)
            db.finalWanfangPapers.insert_one(dict)
if __name__ == '__main__':
    # proxy_list = get_ip_list(proxy_url, headers)
    # proxy_list = ['111.13.7.42:80', '123.56.169.22:3128', '122.49.35.168:33128', '123.103.93.38:80', \
    #       '120.24.208.42:9999']
    # q = mp.Queue()
    '''
    db.wanfang_papers.remove({})
    starttime0 = datetime.datetime.now()
    startGrab(1,8,)
    endtime0 = datetime.datetime.now()
    print("normal执行时间：", (endtime0 - starttime0).seconds, "s")

    db.wanfang_papers.remove({})
    starttime = datetime.datetime.now()
    p1 = mp.Process(target=startGrab, args=(1,2,))
    p2 = mp.Process(target=startGrab, args=(3,4,))
    p3 = mp.Process(target=startGrab, args=(5,6,))
    p4 = mp.Process(target=startGrab, args=(7,8,))
    # startGrab(1, 2)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    endtime = datetime.datetime.now()
    print ("multiprocessing执行时间: ", (endtime - starttime).seconds, "s")
    '''
    # db.wanfang_papers.remove({})
    threads = []
    starttime = datetime.datetime.now()
    for i in [2801, 2901, 3001, 3101]:
        threads.append(threading.Thread(target=startGrab, args=(i, i+99)))
    for thread in threads:
        thread.start()
        thread.join()
    # t1 = threading.Thread(target=startGrab, args=(1,2,))
    # t2 = threading.Thread(target=startGrab, args=(3,4,))
    # t3 = threading.Thread(target=startGrab, args=(5,6,))
    # t4 = threading.Thread(target=startGrab, args=(7,8,))
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    endtime = datetime.datetime.now()
    print ("threading执行时间: ", (endtime - starttime).seconds, "s")
"""
        for sc_content in sc_contents:
            title = sc_content.find('a').text
            # print(title)
            # abstract = sc_content.find('div', {'class': 'c_abstract'})
            spans = sc_content.find_all('span')
            authors = spans[0].find_all('a')
            author = ''      
            for i in authors:
                # print(i.text, ',', end='')
                author = author  + i.text + ' '
                # author.append(i.text)
                # print(author)
                # file.write(i.text+',')
            book = spans[1].text.strip()
            # print(book)
            # print(book.strip(), end=',')
            # file.write(book.strip()+',')
            time = spans[2].text.strip()
            # print(time)
            # print(time.strip(), end=', ')
            # file.write(time.strip()+', ')
            try:
                quote = spans[3].find('a').text.strip()
                # print(quote)
            except:
                pass
            dict = {'论文题目': title, '作者': author, '期刊': book, '发表时间': time, '被引量': quote}
            db.collection.insert_one(dict)
        page = page + 10
    for item in db.collection.find():
        print(item)
    print(db.collection.count())
        # print(quote.strip(), end='\n')
        # file.write(quote.strip()+'\n\n')
    for item in test:
        p = item.contents[3].find('p').text.strip()
        print(p)
        file.write(p)
        file.write('\n')
    file.close()
"""
"""
    while page_number <= ALL_PAGE_NUMBER:
        url = base_url + str(page_number)
        print (">>>>>>>>>>>将要抓取", url)

        # 可能因为超时等网络问题造成异常，需要捕获并重新抓取
        try:
            page = requests.get(url)
        except:
            print ("重新抓取 ", url)
            continue

        # 使用BeautifulSoup规范化网页并生成对象
        soup = BeautifulSoup(page.content, "lxml")

        lesson_data = soup.find("li")
        print(lesson_data)
        # output_txt = open('output.txt', 'w')
        for item in lesson_data:
            try:
                if (item.contents[1].find("a").text):
                    name = item.contents[1].find("a").text
                    link = item.contents[1].find("a").get("href")
                    des = item.contents[1].find("p").text
                    number = item.contents[1].find("em", {"class": "learn-number"}).text
                    time = item.contents[1].find("dd", {"class": "mar-b8"}).contents[1].text
                    degree = item.contents[1].find("dd", {"class": "zhongji"}).contents[1].text
                    output_list = [name, link, des, number, time, degree]
                    for content in output_list:
                        output_txt.write(content)
                    output_txt.write('\n')
                    lesson_info = {"name": name, "link": link, "des": des, "number": number, "time": time, "degree": degree}
                    saveToSqlite(lesson_info)
                    print ("课程名称: ", item.contents[1].find("a").text)
                    print ("课程链接: ", item.contents[1].find("a").get("href"))
                    print ("课程简介: ", item.contents[1].find("p").text)
                    print ("学习人数: ", item.contents[1].find("em", {"class": "learn-number"}).text)
                    print ("课程时间: ", item.contents[1].find("dd", {"class": "mar-b8"}).contents[1].text)
                    print ("课程难度: ", item.contents[1].find("dd", {"class": "zhongji"}).contents[1].text)
                    print ("-----------------------------------------------")
            except:
                pass
        output_txt.close()
        page_number = page_number + 1
"""