# -*- coding: utf8 -*-
from os import mkdir
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
    return BeautifulSoup(r.text, 'html.parser')

def get_paper_link(page):
    links = page.select('#content > div > ul > li > div > div a')
    return [link.get('href') for link in links]

def download_wallpaper(base_dir,link, index, total):
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
        open(base_dir+biggest_one['name'], 'wb').write(result.content)

    if index + 1 == total:
        print('Download completed!\n')

def genWallpapper(num):
    if num>=50:
        return
    base_dir = './wallpapers/'
    if not exists(base_dir):
        mkdir(base_dir)  # /wallpapers
    page_start = random.randint(2, 6599)
    page_url = 'http://wallpaperswide.com/page/'
    while num<50:
        print('\nPreparing to download from the {} page of all the  wallpapers...'.format(page_start))
        PAGE_SOURCE = visit_page(page_url + str(page_start))
        WALLPAPER_LINKS = get_paper_link(PAGE_SOURCE)
        page_start = page_start + 1

        for index, link in enumerate(WALLPAPER_LINKS):
            download_wallpaper(base_dir,link, index, len(WALLPAPER_LINKS))
            sleep(1)
        num+=11

def genBanner(imglist):
    out_str="Banner"
    with open('size.csv', 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            out_dir = out_str + "(" + "x".join(row) + ")"
            size=(int(row[0]),int(row[1]))
            print("Start to resize the image to "+"x".join(row)+" Size Banner")
            for img in imglist:
                if not exists(out_dir):
                    mkdir(out_dir)
                resizeBanner(img,out_dir,size)
            print("Successfully get the ", size, "size Banner")

def resizeBanner(jpgfile, outdir,size=(128,128)):
    #open the source image and get the size of image
    img = Image.open(jpgfile)
    (x,y)=img.size

    #resize and crop the image
    try:
        new_img = img.resize((size[0],size[0]*y//x), Image.BILINEAR)
        new_img = new_img.crop((0, 0, size[0], size[1]))
        new_img.save(join(outdir,basename(jpgfile)))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    imglist=glob('./wallpapers/*.jpg')
    num=len(imglist)
    genWallpapper(num)
    genBanner(imglist)