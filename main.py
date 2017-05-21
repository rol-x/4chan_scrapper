import requests
import urllib.request
import os
import random
from bs4 import BeautifulSoup



####HOW TO USE####
#1. Make an input.txt file with links to threads that you want to downlaod (each one in a separate line)#
#2. Place it in the same folder as main.py#
#2. Run this code with any python compiler (PyCharm pref)#
#3. All gifs, webms, pngs, jpgs etc. will be in thread-named folder in your main.py script directory#

####Made by Karol Latos 2016####

def create_folder(soup, board):
    thread_name = ""
    for name in soup.findAll('span', {'class': 'subject'}):
        if name.string:
            thread_name = name.string
        else:
            r = random.randrange(1,100)
            thread_name = str(r)
        thread_name = (board + '_' + thread_name)
        thread_name = str.replace(thread_name, "/", "")
        thread_name = str.replace(thread_name, " ", "-")
    try:
        os.makedirs(thread_name)
    except OSError:
        pass
    os.chdir(thread_name)


def download_images(thread_url):
    board = str.replace(thread_url, "thread", '/////thread')
    board = str.replace(board, 'http://boards.4chan.org/', "")
    board = board[0:4]
    board = str.replace(board, "/", "")
    source_code = requests.get(thread_url)
    raw_text = source_code.text
    soup = BeautifulSoup(raw_text, "html.parser")
    create_folder(soup, board)
    for url in soup.findAll('a', {'class': 'fileThumb'}):
        image_url = url.get('href')
        image_url = ('http:' + image_url)
        image_name = image_url
        image_name = str.replace(image_name, 'http://i.4cdn.org/', "")
        image_name = str.replace(image_name, '/', "")
        image_name = str.replace(image_name, board, "")
        if board == 'gif' and image_name[len(image_name)-1] == '.':
            image_name = (image_name + 'gif')
        urllib.request.urlretrieve(image_url, image_name)



##Also, if it is only one link, you can unhash the following line and paste the link in the compiler (after running the code)##

#link = input()
input_file = open("input.txt", "r")
input_list = input_file.readlines()
for line_n in range(0, input_list.__len__()):
    link = input_list.__getitem__(line_n)
    download_images(link)
input_file.close()