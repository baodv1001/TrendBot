from time import sleep
from turtle import title
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class MyClass(object): 
    def __init__(self, title, views, uploadTime):
        self.title = title
        self.views = views
        self.uploadTime = uploadTime

def main():
    driver = webdriver.Edge()
    driver.get('https://www.youtube.com/feed/trending/vn')
    driver.maximize_window()
    content = driver.page_source.encode('utf-8').strip()

    amount = 10
    titles = []
    views = []
    urls = []
    postedDate = []
    titlesElement = driver.find_elements(by=By.ID, value = 'video-title')

    for i in range(amount): 
        titles.append(titlesElement[i].text)
        urls.append(titlesElement[i].get_attribute('href'))

    res = []
    channels = []
    
    for i in range(amount):
        driver.get(urls[i]) 
        # view = driver.find_element(by=By.CSS_SELECTOR, value = '#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer')
        wait=WebDriverWait(driver,3)
        count=wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer')))
        views.append(count.text)
        date=wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'#info-strings > yt-formatted-string')))
        postedDate.append(date.text)
        # TODO: like, channel
        #channel=wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'yt-simple-endpoint style-scope yt-formatted-string')))
        #channels.append(channel.text)
        # channels.append(driver.find_element(by=By.CLASS_NAME, value='yt-simple-endpoint style-scope yt-formatted-string').text)

    for i in range(amount):
        res.append(
            {
                "title": titles[i],
                "url": urls[i],
                "views": views[i],
                "uploadTime": postedDate[i]
            }
        )

    print(json.dumps(res, ensure_ascii=False))

main()