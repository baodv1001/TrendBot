from turtle import title
from selenium import webdriver
from bs4 import BeautifulSoup
import json

class MyClass(object): 
    def __init__(self, title, views, uploadTime):
        self.title = title
        self.views = views
        self.uploadTime = uploadTime


def main():
    driver = webdriver.Edge()
    driver.get('https://www.youtube.com/feed/trending/vn')
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')
    # titles = soup.findAll('a', class_ = "yt-simple-endpoint style-scope yt-formatted-string")
    titles = soup.findAll('a', id = "video-title")
    views = soup.findAll('span', class_ = "style-scope ytd-video-meta-block")
    count = len(titles)
    my_objects = []
    for i in range(count):
        my_objects.append(
            {
                "title": titles[i].text,
                "views": views[2*i].text,
                "uploadTime": views[2*i+1].text
            }
        )

    print(json.dumps(my_objects, ensure_ascii=False))



main()