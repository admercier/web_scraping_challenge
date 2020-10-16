import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    
    mars_data = dict()
    
    #set URL
    url = 'https://mars.nasa.gov/news/?order=publish_date+desc&blank_scope=Latest'
    browser.visit(url)

    #scrape page
    html= browser.html
    soup = bs(html, 'html.parser')
    
    #need to get a variable for 'news_title' and 'news_p'
    news_title = soup.find_all('div', class_='content_title')[1].text
    mars_data["news_title"] = news_title
    news_p = soup.find_all('div', class_ = 'article_teaser_body')[1].text
    mars_data["news_p"] = news_p
    ####################################################################
    #set URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #scrape page
    html=browser.html
    soup = bs(html, 'html.parser')

    #get images
    featured_img = soup.find('footer')
    featured_img = featured_img.find('a')['data-fancybox-href']
    featured_img = 'https://www.jpl.nasa.gov' + featured_img
    mars_data["featured_img"] = featured_img
    ####################################################################
    url='https://space-facts.com/mars/'

    #scrape table with pandas as pd
    tables = pd.read_html(url)
    mars_df = tables[0]

    #set index
    #mars_df = mars_df.set_index(0)
    
    #rename column headers
    mars_df = mars_df.rename(columns={0:"Facts",1:"Values"})
    #mars_data["df"] = mars_df
    #convert to HTML
    mars_table = [mars_df.to_html(classes="data", index=False, header = True)]
    #mars_table = mars_table.replace('\n', '')
    mars_data["mars_table"] = mars_table
    
    ####################################################################
    #set URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #scrape page with soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #find hemisphere names
    hems = soup.find_all('h3')
    hemispheres = [result.text[:-9] for result in hems]
    mars_data["hemispheres"] = hemispheres
    
    ####################################################################
    #CERBERUS
    #set URL
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)

    #scrape page with soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #find image URL
    cerberus_url = (soup.find_all('div', class_ = 'downloads')[0].li.a.get('href'))
    
    #SCHIAPARELLI
    #set URL
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)

    #scrape page with soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #find image URL
    schiaparelli_url = (soup.find_all('div', class_ = 'downloads')[0].li.a.get('href'))
    
    #SYRTIS
    #set URL
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)

    #scape page with soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #find image URL
    syrtis_url = (soup.find_all('div', class_ = 'downloads')[0].li.a.get('href'))
    
    #VALLES
    #set URL
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)

    #scrape page with soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #find image URL
    valles_url = (soup.find_all('div', class_ = 'downloads')[0].li.a.get('href'))
    
    #create dict of hemisphere URLs
    hemisphere_dict = [
        {'title': 'Cerberus Hemisphere', 'img_url': cerberus_url},
        {'title': 'Schiaparelli Hemisphere', 'img_url': schiaparelli_url},
        {'title': 'Syrtis Major Hemisphere', 'img_url': syrtis_url},
        {'title': 'Valles Marineris Hemisphere', 'img_url': valles_url},
    ]
    mars_data["hemisphere_dict"] = hemisphere_dict
    
    #return [mars_data, mars_df]
    return mars_data

