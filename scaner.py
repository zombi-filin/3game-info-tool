import re
import os
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

id_list = []
title_list = []
url_list = []
price_list = []

def get_html(url):
    '''
    Возвращает HTML код страницы по url
    '''
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')

def processed_page(num):
    ''' Обработка страницы под номером `num`'''
    print(f'Page #{num}')
    page_html = get_html(f'https://3game.info/gaming/?page={num}&alias=xbox-key')
    page_html = page_html.replace('\n','').replace('\t','')
    regex = r'>(\s)+'
    page_html = re.sub(regex, '>', page_html, 0, re.MULTILINE)
    page_list = page_html.split('><')
    
    product_regex = r'href=\"https://3game\.info/product/(\d+)-(.+)\"\sonclick(?:.+)>(.+)</'
    price_regex = r'itemprop=\"price\"(?:.+)>([0-9]+)<'

    for page_line in page_list:
        if page_line == 'p class="otstup-pop"':
            break
        product_find = re.findall(product_regex,page_line)
        if len(product_find) == 1:
            id_list.append(product_find[0][0])
            url_list.append(f'https://3game.info/product/{product_find[0][0]}-{product_find[0][1]}')
            title_list.append(product_find[0][2])
        price_find = re.findall(price_regex,page_line)
        if len(price_find)==1:
            price_list.append(price_find[0])
        
    pass

for page_num in range(1,200):
    processed_page(page_num)


print(f'{len(id_list)} - {len(price_list)}')

f = open('out.txt', 'w', encoding='utf-8')
for i in range(len(id_list)):
    f.write(f'{title_list[i]}\t{price_list[i]}\n')
f.close()