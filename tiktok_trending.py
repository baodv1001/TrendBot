from distutils.command.build import build
from os import link
from turtle import delay, title
from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import clipboard

value = input("Enter your value: ")
driver = webdriver.Edge()
driver.get('https://www.tiktok.com/')
print('open browser')
sleep(3)
res = []
links=[]
views=[]
titles = []
likes = []
comments = []
shares = []
users = []

def get_video_profile(url):   
    driver.get(url)
    
    for i in range(1,10):
        video = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[{0}]/div[1]/div/div/a'.format(i))
        titles.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[{0}]/div[2]/a'.format(i)).text)
        links.append(video.get_attribute('href'))
        views.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[{0}]/div[1]/div/div/a/div/div[2]/strong'.format(i)).text)
    
    get_info_by_url()

    print(json.dumps(res, ensure_ascii=False))
    delay(5)

def get_video_search():   
    for i in range(1,10):
        video = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[{0}]/div[1]/div/div/a'.format(i+1))
        titles.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[{0}]/div[2]/div/div[1]/div/span[1]'.format(i+1)).text)
        links.append(video.get_attribute('href'))
        views.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[{0}]/div[2]/div/div[2]/div/strong'.format(i+1)).text)

    get_info_by_url()

    print(json.dumps(res, ensure_ascii=False))

    # delay(5)

def get_info_by_url():
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

def get_for_you(count):
    
    driver.get('https://www.tiktok.com/foryou')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    close_button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div[1]');
    close_button.click() 
    sleep(2)
    for i in range(0,count):
        try:
            titles.append(title =driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[1]/div[2]/span[1]'.format(i+1)).text)
        except:
            titles.append("")
        comments.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[2]/div[2]/button[2]/strong'.format(i+1)).text)
        likes.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[2]/div[2]/button[1]/strong'.format(i+1)).text)
        shares.append(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[2]/div[2]/button[3]/strong'.format(i+1)).text)
        users.append(driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[1]/div[1]/a[2]/h4'.format(i+1)).text)
        share_button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[2]/div[2]/button[3]'.format(i+1))
        hover = ActionChains(driver=driver).move_to_element(share_button)
        hover.perform()
        sleep(3)

        copied_link_button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div[1]/div[{0}]/div/div[2]/div[2]/button[3]/div/div/a[5]'.format(i+1))
        copied_link_button.click()
        links.append(clipboard.paste())

    for i in range(0,count):
        res.append(
            {
                "title": titles[i],
                "like": likes[i],
                "comment": comments[i],
                "share": shares[i],
                "user": users[i],
                "url": links[i]
            }
        )
    
    print(json.dumps(res, ensure_ascii=False))

def main():
    

    searchBar = driver.find_element(by=By.CLASS_NAME, value="tiktok-vzysje-InputElement")
    searchBar.send_keys(value)
    print('fill search')
    sleep(3)

    search_button = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/div/form/button')
    search_button.click()
    print('search ok')
    sleep(3)

    try:
        profile_button = driver.find_element(by=By.CSS_SELECTOR, value='#app > div.tiktok-19fglm-DivBodyContainer.etsvyce0 > div.tiktok-mldqij-DivMainContainer.e1l7hzzi0 > div.tiktok-1fwlm1o-DivPanelContainer.e1l7hzzi2 > div.tiktok-1qb12g8-DivThreeColumnContainer.e140s4uj2 > div > div:nth-child(1) > div.tiktok-133zmie-DivLink.e12ixqxa0 > a.tiktok-14p1pn2-StyledDivInfoWrapper.e12ixqxa3')
        url = profile_button.get_attribute('href')
        get_video_profile(url)
    except: 
        get_video_search()
    finally:
        get_for_you(10)

    driver.quit()

main()

