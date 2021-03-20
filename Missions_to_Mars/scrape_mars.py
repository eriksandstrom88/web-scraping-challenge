# Mission_to_Mars scrape_mars.py

#import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime as dt
import requests
import os

#Define a function to open the Chrome browser
def init_browser():
    executable_path = {"executable_path":ChromeDriverManager().install()}
    return Browser("chrome",**executable_path, headless=False)

#####Define the scrape function
def scrape():
    #Scrape the latest news headline and teaser
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html_text = browser.html
    soup = BeautifulSoup(html_text,"html.parser")
    headline = soup.find('div',class_='bottom_gradient').find_all('h3')[0].text.strip()
    teaser = soup.find('div',class_='article_teaser_body').get_text()
    mars_dict = {}
    mars_dict['headline'] = headline
    mars_dict['teaser'] = teaser
    browser.quit()
    #Scrape the "featured image" on JPL
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id('filter_Mars').click()
    time.sleep(3)
    browser.find_by_css('.BaseImage').first.click()
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    mars_dict['first_image'] = soup.find('img',class_='BaseImage')['data-src']
    browser.quit()
    #Scrape the Mars Facts
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(url)
    mars_facts = mars_facts_table[0]
    mars_facts = mars_facts.rename(columns = {0:'Fact_Title',1:'Mars_Fact'})
    mars_facts_html = mars_facts.to_html()
    mars_dict['mars_facts'] = mars_facts_html
    browser.quit()
    #Scrape the hemispheres images
    hemispheres_list = []
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    for image in range(4):
        browser.visit(url)
        hemispheres_dict = {}
        browser.find_by_css('h3')[image].click()
        time.sleep(3)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemispheres_dict['hemisphere'] = soup.find('h2', class_='title').get_text()
        hemispheres_dict['image'] = soup.li.find('a')['href']
        hemispheres_list.append(hemispheres_dict)
    mars_dict['hemispheres'] = hemispheres_list
    browser.quit()
    return mars_dict
