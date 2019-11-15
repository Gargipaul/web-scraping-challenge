#Imports & Dependencies
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
import time
#Site Navigation
def init_browser():
    executable_path = {"executable_path": "Chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)




# Defining scrape & dictionary
def scrape_info():
    # executable_path = {"}
    browser = init_browser()
    
    mars_dict = { 
        'news_t': marsNews(), 
        'image': marsImage(),
        'hem': marsHem(),
        'weth':marsWeather(),
        'facts':marsFacts()
    }
    
    return mars_dict
    
    

# # Mars News

def marsNews():
    browser = init_browser()
    news_url = "https://mars.nasa.gov/news/"
    #browser = init_browser()
    # browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = soup.find("div", class_="content_title")
    news_p = soup.find("div", class_ ="article_teaser_body")
    output = [news_title, news_p]
    return output

# # Mars Space Images - Featured Image
def marsImage():
    browser = init_browser()
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # browser = init_browser()
    browser.visit(featured_image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    feat_img_url = image_soup.find('figure', class_='lede')
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url

# # Mars Weather
def marsWeather():
    browser = init_browser()
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    mars_weather = browser.html
    soup = BeautifulSoup(mars_weather, "html.parser")
    mars_weather = soup.find('P', class_="TweetTextSize")
    return mars_weather

# # Mars Facts
def marsFacts():
    browser = init_browser()
    import pandas as pd
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    table[0]
    df_mars_facts = table[2]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])
    return df_mars_facts.to_html()



# # Mars Hemispheres
def marsHem():
    browser = init_browser()
    import time 
    url_hemesphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemesphere)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
        
    return mars_hemisphere
        