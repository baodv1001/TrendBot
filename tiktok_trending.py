from distutils.command.build import build
from os import link
from turtle import delay, title
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

value = input("Enter your value: ")

driver = webdriver.Edge()
driver.get('https://www.tiktok.com/')
print('open browser')
sleep(3)

searchBar = driver.find_element(by=By.CLASS_NAME, value="tiktok-vzysje-InputElement")
searchBar.send_keys(value)
print('fill search')
sleep(3)
search_button = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/div/form/button')
search_button.click()
print('search ok')
sleep(3)

# profile_button = driver.find_element(by=By.CLASS_NAME, value ='tiktok-14p1pn2-StyledDivInfoWrapper e12ixqxa3')
# profile_button = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/a[2]')
profile_button = driver.find_element(by=By.CSS_SELECTOR, value='#app > div.tiktok-19fglm-DivBodyContainer.etsvyce0 > div.tiktok-mldqij-DivMainContainer.e1l7hzzi0 > div.tiktok-1fwlm1o-DivPanelContainer.e1l7hzzi2 > div.tiktok-1qb12g8-DivThreeColumnContainer.e140s4uj2 > div > div:nth-child(1) > div.tiktok-133zmie-DivLink.e12ixqxa0 > a.tiktok-14p1pn2-StyledDivInfoWrapper.e12ixqxa3')

url = profile_button.get_attribute('href')

driver.get(url)
res = []
links=[]
views=[]
titles = []
likes = []
comments = []
shares = []
for i in range(1,10):
    video = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[{0}]/div[1]/div/div/a'.format(i))
    titles.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[{0}]/div[2]/a'.format(i)).text)
    links.append(video.get_attribute('href'))
    views.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[{0}]/div[1]/div/div/a/div/div[2]/strong'.format(i)).text)
    res.append(
        {
            "url": links[i-1],
            "views": views[i-1],
            "title": titles[i-1]
        }
    )

for link in links:
    driver.get(link);
    likes.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[1]/strong').text)
    comments.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[2]/strong').text)
    shares.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[3]/strong').text)
    sleep(3)

for i in range(len(links)):
    res.append(
        {
            "url": links[i],
            "views": views[i],
            "title": titles[i],
            "like": likes[i],
            "comment": comments[i],
            "share": shares[i]
        }
    )

print(res)

delay(5)
    


