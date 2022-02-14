import requests
from bs4 import BeautifulSoup

url = 'https://flippa.com/'

try:
    r = requests.get(url)
    html = r.content

    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('link')
    imgs = soup.find_all('img')
    anchors = soup.find_all('a')
    scripts = soup.find_all('script')

    for l in links: 
        try:
            lhref = l['href']
        except:
            lhref = None
        if lhref:  
            if l['href'][0] != 'h':
                l['href'] = url + l['href']

    for i in imgs:
        try:
            iscr = i['src']
        except:
            iscr = None
        if iscr:
            if i['src'][0] != 'h':
                i['src'] = url + i['src']

    for a in anchors:
        try:
            ahref = a['href']
        except:
            ahref = None
        if ahref:
            if a['href'][0] != 'h':
                a['href'] = url + a['href']

    for s in scripts:
        try:
            src = s['src']
        except:
            src = None
        if src:
            if s['src'][0] != 'h':
                s['src'] = url + s['src']


    with open("output.html", "w", encoding = 'utf-8') as file: 
        file.write(str(soup.prettify()))

except requests.exceptions.ConnectionError:
    print("Connection timed out")

except:
    print("An error occured")