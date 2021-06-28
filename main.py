#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import datetime
import json
import time

from bs4 import BeautifulSoup
from func import get_html, url, send_tg
from config import TOKEN, CHAT, ITEMS_FOR_OBSERVE


def main():
    Links = url(ITEMS_FOR_OBSERVE)
    print('Получено страниц: ' + str(len(Links)))
    with open('itemList.json', 'r') as f:
        dataListOld = json.load(f)
    print('Успешно открыт файл dataList.json')
    dataList = []
    dataSend = []
    for link in Links:
        content = get_html(link)
        content = content.text
        Csoup = BeautifulSoup(content, 'html.parser')
        items = Csoup.select('table#offers_table > tbody > tr.wrap > td.offer > div.offer-wrapper > table > tbody > tr')
        for i in items:
            item = {}
            photo = i.select('td.photo-cell > a > img')
            name = i.select('td.title-cell > div > h3 > a > strong')
            link = i.select('td.title-cell > div > h3 > a')
            price = i.select('td.td-price > div > p.price > strong')
            if name != [] and link != [] and price != [] and photo != []:
                item['name'] = name[0].text
                item['link'] = link[0].attrs['href']
                item['price'] = price[0].text
                item['img'] = photo[0].attrs['src']
                dataList.append(item)
                if item not in dataListOld:
                    dataSend.append(item)
    with open('itemList.json', 'w') as f:
        json.dump(dataList, f)
    print('Успешно перезаписан itemList.json')
    if dataSend != []:
        print('Для отправки в Телеграм подготовлено: ' + str(len(dataSend)))
        for DATA in dataSend:
            send_tg(TOKEN, CHAT, DATA)
            time.sleep(2)
    else:
        print('Нет новых лотов для отправки в Телеграм')




if __name__ == '__main__':
    i = 0
    while True:
        now = datetime.datetime.now()
        main()
        print('Итерация: ' + str(i))
        print(now.strftime("%d-%m-%Y %H:%M"))
        i += 1
        print('======== ЗАСЫПАЮ ========')
        time.sleep(60)
