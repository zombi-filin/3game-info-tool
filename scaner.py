import re
import os
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

end_counter = 5

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
    global end_counter
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
            end_counter -= 1
            break
        product_find = re.findall(product_regex,page_line)
        if len(product_find) == 1:
            id_list.append(product_find[0][0])
            url_list.append(f'https://3game.info/product/{product_find[0][0]}-{product_find[0][1]}')
            title_list.append(product_find[0][2])
            end_counter = 5
        price_find = re.findall(price_regex,page_line)
        if len(price_find)==1:
            price_list.append(price_find[0])
            end_counter = 5
    pass

page_num = 1
while end_counter > 0:
    processed_page(page_num)
    page_num += 1

print(f'{len(id_list)} - {len(price_list)}')

out_file = open('games.html', 'w', encoding='utf-8')

with open('html_begin', 'r', encoding='utf-8') as tmp:
    out_file.write(tmp.read())


for i in range(len(id_list)):
    out_file.write(f'<tr pos="{id_list[i]}" title="{title_list[i]}" price="{price_list[i]}">\n')
    out_file.write(f'<td>{title_list[i]}</td><td>{price_list[i]}</td><td><a href="{url_list[i]}" target="_blank">ПЕРЕЙТИ</a></td></tr>\n')
    out_file.write(f'</tr>\n')

with open('html_end', 'r', encoding='utf-8') as tmp:
    out_file.write(tmp.read())

out_file.close()