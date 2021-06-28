import requests
from bs4 import BeautifulSoup



HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36', 'accept': '*/*'}

def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def get_linkList(html, URL):
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.select('div.pager.rel.clr > span > a[data-cy="page-link-last"] span')
    page = int(page[0].text)
    linkList = []
    for i in range(1, (page + 1)):
        linkList.append(URL + "&page=" + str(i))
    return linkList

def url(list):
    parseLinks = []
    for i in list:
        name = i['name'].replace(' ', '-')
        min = i['min_price']
        max = i['max_price']
        url = "https://www.olx.ua/list/q-" + name + "/?search%5Bfilter_float_price%3Afrom%5D=" + \
              min + "&search%5Bfilter_float_price%3Ato%5D=" + max
        html = get_html(url)
        if html.status_code == 200:
            try:
                links = get_linkList(html.text, url)
                for link in links:
                    parseLinks.append(link)
            except:
                links = url
                parseLinks.append(links)

    return parseLinks

def send_tg(token, chat_id, data):
    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendPhoto"

    r = requests.post(method, data={
        "chat_id": chat_id,
        "photo": data['img'],
        "caption": data['name'] + "\n" + data['price'] + "\n" + data['link']
    })

    if r.status_code != 200:
        raise Exception("post_text error")