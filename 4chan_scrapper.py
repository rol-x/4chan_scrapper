### Made in 2016 ###
### Refactored in 2024 ###
import requests
import urllib.request
import os
import re
import random
from bs4 import BeautifulSoup


def get_subject(soup) -> str | None:
    subject_parent = soup.find('div', {'class': 'postInfo desktop'})
    return subject_parent.find('span', {'class': 'subject'}).string


def create_thread_dir_name(subject: str | None, board: str) -> str:
    if subject:
        thread_dir = f"{board}_{subject}".replace(" ", "")
        return re.sub(r'\W+', '', thread_dir)
    else:
        return str(random.randint(10000, 100000))


def create_thread_folder(subject: str | None, board: str) -> None:
    thread_dir = create_thread_dir_name(subject, board)
    print(f"Thread directory: {thread_dir}")
    try:
        if not os.path.exists(thread_dir):
            os.makedirs(thread_dir)
        os.chdir(thread_dir)
    except OSError as error:
        print(f"Couldn't create the thread folder: {error}")
        exit()


def download_images(thread_url: str) -> None:
    board_name = thread_url.split(".org/")[1].split("/")[0]
    page_content = requests.get(thread_url)
    soup = BeautifulSoup(page_content.text, "html.parser")
    subject = get_subject(soup)
    create_thread_folder(subject, board_name)
    for url_parent in soup.findAll('div', {'class': 'fileText'}):
        file_url = 'http:' + url_parent.find('a').get('href')
        file_name = file_url.split('/')[-1]
        if file_name in os.listdir():
            continue
        print(f"Downloading: {file_name}")
        urllib.request.urlretrieve(file_url, file_name)
    os.chdir('..')

def scrape_from_file():
    with open("threads.txt") as threads_file:
        threads = threads_file.readlines()
        for thread_url in threads:
            print(f"Scraping: {thread_url[:-1]}")
            download_images(thread_url)

scrape_from_file()