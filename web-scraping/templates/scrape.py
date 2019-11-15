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
    browser = Browser("chrome", **executable_path, headless=False)




# Defining scrape & dictionary
def scrape():
    
    Browser = init_browser()
    first_title, first_paragraph = mars_news(Browser)
    
    result = {
    "title": news_title,
    "paragraph": news_p,
    "image_URL": featured_image_url(Browser),
    "weather": url_weather(Browser),
    "facts": mars_facts(),
    "hemispheres": url_hemisphere(Browser),
    }
    
    
    return result

# # NASA Mars News

def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    Browser = init_browser()
    Browser.visit(news_url)
    html = Browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return news_title, news_p

# # JPL Mars Space Images - Featured Image
def marsImage():
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser = init_browser()
    browser.visit(featured_image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url

# # Mars Weather
def marsWeather():
    
    url_weather = "https://twitter.com/marswxreport?lang=en"
    Browser.visit(url_weather)
    mars_weather = Browser.html
    soup = BeautifulSoup(mars_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return mars_weather

# # Mars Facts
def marsFacts():
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
    import time 
    url_hemesphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    Browser.visit(url_hemesphere)
    html = Browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    Browser.visit(image_link)
    html = Browser.html
    soup=BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    hemisphere.append({"title": title, "img_url": image_url})
    
    return mars_hemisphere

    