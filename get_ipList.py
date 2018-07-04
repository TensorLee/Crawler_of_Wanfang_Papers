'''
i = 3.14
r = 2
s = i * r * r
print("{:.4f}".format(s))

while True:
    try:
        x = int(input('first number: '))
        y = int(input('second number: '))
        n = x / y
        print('x / y is ', n)
    except:
        print("Invalid input.")
    else:
        break

for i in range(1, 10):
    print(i)
'''
import requests
from bs4 import BeautifulSoup

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

if __name__ == '__main__':

    url = 'http://www.xicidaili.com/nn/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    get_ip_list(url, headers)