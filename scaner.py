import re
import os
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_html(url):
    '''
    Возвращает HTML код страницы по url
    '''
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')

def processed_page(num):
    ''' .обработка страницы под номером `num`'''
    page_html = get_html(f'https://3game.info/gaming/?page={num}&alias=xbox-key')
    page_html = page_html.replace('\n','').replace('\t','')
    regex = r'>(\s)+'
    page_html = re.sub(regex, '>', page_html, 0, re.MULTILINE)
    page_list = page_html.split('><')
    pass

processed_page(1)
pass