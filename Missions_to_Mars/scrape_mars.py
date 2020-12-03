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

    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    mars_facts_df = table[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html.replace('\n', "")

    # Mars Hemisphere to be scraped

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html_hemi = browser.html
    soup = bs(html_hemi, 'html.parser')
    # Collect all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # List for hemisphere urls 
    hemi_image_urls = []
    # Store the main_ul 
    hemi_main_url = 'https://astrogeology.usgs.gov'
    # Loop through the items
    for item in items: 
        title = item.find('h3').text
        # Link that leads to full image website
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        # Beautiful Soup
        browser.visit(hemi_main_url + partial_img_url) 
        partial_img_html = browser.html 
        soup = bs( partial_img_html, 'html.parser')
        # Full image source 
        img_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
        # Append list 
        hemi_image_urls.append({"title" : title, "img_url" : img_url})

    # Mars Dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_facts_html),
        "hemisphere_images": hemi_image_urls
    }

    return mars_dict