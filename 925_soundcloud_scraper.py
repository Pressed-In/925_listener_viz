########## CALL LIBRARIES / PACKAGES TO USE ##########

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd
import time
import re
import urllib.request
from requests_html import HTMLSession

###########

# session = HTMLSession()
# r = session.get('https://soundcloud.com/movin925/tracks')

# r.html.render()

# print(r.text)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

############

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

driver.get("https://soundcloud.com/movin925/tracks")

time.sleep(0.8)

##### SCROLL TO BOTTOM OF PAGE ####

def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(0.8)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        time.sleep(0.8)
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        
        time.sleep(0.8)

scroll_to_bottom(driver)



### PODCAST TITLE SCRAPING ###

podcast_title = []
podcast_plays = []
podcast_date = []


main_page_div = driver.find_elements_by_class_name('userMain__content')

for entire_div in main_page_div:

    scraped_titles = entire_div.find_elements_by_css_selector('.soundTitle__title.sc-link-dark') 
    for i in scraped_titles:
        podcast_title.append(i.text)

    scraped_plays = entire_div.find_elements_by_css_selector('.sound__soundStats')
    for i in scraped_plays:
        podcast_plays.append(i.text)
        
    scraped_date = driver.find_elements_by_tag_name('time')
    for i in scraped_date:
        j = i.get_attribute('datetime')
        podcast_date.append(j)

###### PUTTING SCRAPED DATA INTO DATAFRAME #######

# print(len(podcast_title))
# print(len(podcast_plays))
# print(len(podcast_date))

# print(podcast_title)
# print(podcast_plays)
# print(podcast_date)

df = pd.DataFrame.from_records({'Podcast Title':podcast_title,'Podcast Date':podcast_date,'Plays To Date':podcast_plays})
df = df[['Podcast Title', 'Podcast Date', 'Plays To Date']]
df.to_csv('925_listener_data.csv', index=False, encoding='utf-8')
print(df)