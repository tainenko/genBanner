# -*- coding: utf8 -*-
from os import mkdir, chdir
from os.path import exists,join,basename
from bs4 import BeautifulSoup
from time import sleep
import requests
import random
from PIL import Image
from glob import glob
import csv

def visit_page(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')

def get_paper_link(page):
    links = page.select('#content > div > ul > li > div > div a')
    return [link.get('href') for link in links]

def download_wallpaper(link, index, total):
    page_domain = 'http://wallpaperswide.com'
    wallpaper_source = visit_page(page_domain + link)
    wallpaper_size_links = wallpaper_source.select('#wallpaper-resolutions > a')
    size_list = [{
        'size': eval(link.get_text().replace('x', '*')),
        'name': link.get('href').replace('/download/', ''),
        'url': link.get('href')
    } for link in wallpaper_size_links]

    biggest_one = max(size_list, key = lambda item: item['size'])
    print('Downloading the ' + str(index + 1) + '/' + str(total) + ' wallpaper: ' + biggest_one['name'])
    result = requests.get(page_domain + biggest_one['url'])

    if result.status_code == 200:
        open(biggest_one['name'], 'wb').write(result.content)

    if index + 1 == total:
        print('Download completed!\n')

def start(page_start,page_end):
    page_url = 'http://wallpaperswide.com/page/'
    while page_start <= page_end:
        print('\nPreparing to download from the {} page of all the  wallpapers...'.format(page_start))
        PAGE_SOURCE = visit_page(page_url + str(page_start))
        WALLPAPER_LINKS = get_paper_link(PAGE_SOURCE)
        page_start = page_start + 1

        for index, link in enumerate(WALLPAPER_LINKS):
            download_wallpaper(link, index, len(WALLPAPER_LINKS),)
            sleep(1)

def genWallpapper():
    base_dir = 'wallpapers'
    if not exists(base_dir):
        mkdir(base_dir)  # /wallpapers
    chdir(base_dir)
    page_start = random.randint(2, 6599)
    page_end = page_start + 2
    start(page_start, page_end)

def genBanner():
    imglist=glob('.\\wallpapers\\*.jpg')
    out_str="Banner"
    with open('size.csv', 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            out_dir = out_str + "(" + "x".join(row) + ")"
            size=(int(row[0]),int(row[1]))
            for img in imglist:
                if not exists(out_dir):
                    mkdir(out_dir)
                resizeBanner(img,out_dir,size)

def resizeBanner(jpgfile, outdir,size=(128,128)):
    img = Image.open(jpgfile)
    try:
        new_img = img.resize(size, Image.BILINEAR)
        new_img.save(join(outdir,basename(jpgfile)))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    num=len(glob('.\\wallpapers\\*.jpg'))
    if num<=50:
        genWallpapper()
    genBanner()
