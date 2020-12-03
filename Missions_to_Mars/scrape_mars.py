# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News URL page to be scraped

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Collect the latest News Title and Paragraph Text
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL Mars Space Image to be scraped

    space_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(space_image_url)
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    # Retrieve background-image url
    image_path = soup.find_all('img')[3]["src"]
    # Website Url 
    main_url = "https://www.jpl.nasa.gov"
    # Concatenate website url with scrapped route
    featured_image_url = main_url + image_path

    # Mars Facts to be scraped

    

    return mars_dict