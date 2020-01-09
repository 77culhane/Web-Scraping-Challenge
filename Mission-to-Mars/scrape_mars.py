#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def scrape_all():
    browser = Browser('chrome')
    # Step 1.1: NASA Mars News
    #visit webpage
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #establish HTML object and parser
    html = browser.html
    soup = bs(html, "html.parser")
    #find the html snippet containing the article title
    article_code = soup.find("div", class_='list_text')
    #print(article_code)
    news_title = article_code.find("div", class_="content_title").text
    news_p = article_code.find("div", class_ ="article_teaser_body").text

    # Step 1.2 JPL Mars Space Images - Featured Image
    #visit webpage
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #refresh html and soup variables
    html = browser.html
    soup = bs(html, "html.parser")
    #find the html snippet containing the first image
    image_code = soup.find("img", class_="thumb")
    #add webpage URL to create for final image location
    featured_image_url = "https://www.jpl.nasa.gov" + image_code["src"]

    # Step 1.3 Mars Weather
    #visit webpage
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    #refresh html and soup variables
    html = browser.html
    soup = bs(html, "html.parser")
    #find the html snippet containing the first tweet
    mars_weather = soup.find("p", class_="TweetTextSize").text

    # Step 1.4 Mars Facts
    #visit webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    #refresh html and soup variables
    html = browser.html
    soup = bs(html, "html.parser")
    #import tables into pandas
    data = pd.read_html(url)
    #select the mars facts table
    facts_df = data[2]
    facts_df.columns = ['Property', 'Value']
    facts_html = facts_df.to_html()

    # Step 1.5 Mars Hemispheres
    #visit webpage
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #refresh html and soup variables
    html = browser.html
    soup = bs(html, "html.parser")
    #find the html snippet containing the HD hemisphere images
    hemisphere_code = soup.find_all('div', class_='item')
    
    # hemisphere_image_urls; populate later with hemisphere URLS
    hemisphere_image_urls = []
    # Loop through the class=items in the first snippet
    for div_item in hemisphere_code: 
        #find the html snipped containing the title
        title = div_item.find('h3').text
        #find the html snippet containing the image location (sans website URL)
        partial_img_url = div_item.find('a', class_='itemLink product-item')
        #visit webpage 
        browser.visit('https://astrogeology.usgs.gov' + partial_img_url['href'])
        #refresh html and soup variables
        html = browser.html
        soup = bs(html, "html.parser")
        #find the html snippet containing the individual hemisephere image
        hemi_image_code = soup.find('img', class_='wide-image')
        #add webpage URL to create final image location
        img_url = 'https://astrogeology.usgs.gov' + hemi_image_code['src']
        # Append image location to hemisphere_image_urls
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    mars_data = {
    "News_Title": news_title,
    "Paragraph_Text": news_p,
    "Most_Recent_Mars_Image": featured_image_url,
    "Mars_Weather": mars_weather,
    "Mars_Facts": facts_html,
    "mars_h": hemisphere_image_urls
    }

    return mars_data

