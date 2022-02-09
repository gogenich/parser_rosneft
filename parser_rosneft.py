from lxml import html
import requests
import json

"""делаем запрос на первую страничку"""
start_url = 'http://zakupki.rosneft.ru/ru/zakupki/all'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
response = requests.get(start_url, headers=headers)
dom = html.fromstring(response.text)
next_pager = dom.xpath('//li[contains(@class, "pager-next")]/a/@href')
i = 0

"""собираем ссылки первой странички"""
links = dom.xpath("//td[@class = 'views-field views-field-title']/a/@href")

"""собираем ссылки на странички"""
while next_pager:
     response = requests.get(next_pager[0], headers=headers)
     dom = html.fromstring(response.text)
     links = links + dom.xpath("//td[@class = 'views-field views-field-title']/a/@href")
     next_pager = dom.xpath('//li[contains(@class, "pager-next")]/a/@href')
     print(f'страница №: {i}')
     i = i+1
     if i == 100:
         break
"""проходимся по всем страничкам и собираем инфу в словарь инфо"""

rez = []
k = 0
for link in links:
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)

    info_1 = dom.xpath("//div[@class = 'tender-date']/strong/text()")

    # номер заказа
    order_number = info_1[0]

    # дата публикации
    order_data = (info_1[1])

    # предквалификация
    predkvalif = dom.xpath("//span[@class = 'date-display-single']/text()")

    info_2 = dom.xpath('//td[@class = "cont-right"]')

    # организатор
    organizator = info_2[0].xpath('.//strong/text()') + info_2[0].xpath('.//div/text()')[1:-1]

    # общий классификатор закупки
    klassificator_zakupki = info_2[1].xpath('.//strong/text()')

    # цена
    price_data = info_2[2].xpath(".//div[@class = 'info']/text()")

    # ссылка
    link_price = info_2[3].xpath(".//div[@class = 'info']/text()")
    if link_price == []:
        link_price = info_2[3].xpath(".//div[@class = 'info']/a/@href")

    # требования к участникам
    var = dom.xpath("//td[contains(text(),'Требования к участникам')]")
    trebovania = var[0].xpath("..//td[@class = 'cont-right']/text()")


    # контактная информация и процедурные вопросы
    name_data = dom.xpath("//td[@class = 'contact-left']/span/text()")

    adres_data = dom.xpath("//div[@class = 'contact-adress']/span/text()")

    tel_data = dom.xpath("//div[@class = 'contact-tel']/span/text()")


    email_data = dom.xpath("//div[@class = 'contact-email']//@href")


    print(k)
    k = k+1

    rez.append({
        'Номер закупки ': order_number,
        'Дата публикации': order_data,
        'Организатор': organizator,
        'Общий классификатор закупки': klassificator_zakupki,
        'Сведения о начальной (максимальной) цене договора (цене лота)': price_data,
        'Ссылка на закупку на электронной торговой площадке': link_price,
        'Предквалификация': predkvalif,
        'Требования к участникам': trebovania,
        'Контакты (процедурные вопросы) ФИО': name_data,
        'Адрес': adres_data,
        'Телефон': tel_data,
        'E-mail': email_data,
        'Контакты (технические вопросы) ФИО': '',
        'Адрес по техническим вопросам': '',
        'Телефон по техническим вопросам': '',
        'E-mail по техническим вопросам': '',
        'дополнительная ссылка для проверки информации': link
    })

with open("rezult_file.json", "w") as write_file:
    json.dump(rez, write_file)