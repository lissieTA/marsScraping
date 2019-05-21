from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from urllib.parse import urljoin

#def scrape():
executable_path = {'executable_path': 'D:\ProgramFiles\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
marsData = {}
#uRL of page to be scraped
url = "https://mars.nasa.gov/news/"
browser.visit(url)
# Scrape page into soup
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())
# save the most recent article, title and date
news = soup.find("div", class_="list_text")
newsDate = news.find("div", class_="list_date").text
#To be added to dict
newsHeader = news.find("div", class_="content_title").text
newsBody = news.find("div", class_="article_teaser_body").text
marsData['newsHeader'] = newsHeader
marsData['newsSummary'] = newsDate
#print(newsDate)
#print(newsHeader)
#print(newsBody)
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())

image = soup.find("article", class_="carousel_item")
imageClass = image.find("a", class_="button fancybox")
#imageURL needs to be in the dict
imageURL = 'https://www.jpl.nasa.gov' +  imageClass['data-fancybox-href']
marsData['imageURL'] = imageURL
#print(imageURL)
browser.visit(imageURL)
tweetURL = "https://twitter.com/marswxreport?lang=en"
browser.visit(tweetURL)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
tweet = soup.find("p", class_="tweet-text")
tweetPost = tweet.text
#tweetPost needs to be in dict
marsData['marsTweet'] = tweetPost
#print(tweetPost)
#print(tweet.text)
factsURL = 'https://space-facts.com/mars/'
browser.visit(factsURL)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
tables = pd.read_html(factsURL)
df = tables[0]
df.columns = ['Property', 'Value']
#print(df)

#html_table needs to be in dict
html_table = df.to_html(index = False)
html_table = html_table.replace('\n', '')
#print(html_table)
marsData['marsProperties'] = html_table


imgList = []
hemisphereURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphereURL)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
container = soup.find('div', 'container').find('div', 'full-content').find('div','result-list')\
    .find('div', 'collapsible results').findAll('div', 'item')
for image in container:
    partialURL = image.find('div','description').find('a').get('href')
    imgUrl = browser.visit(urljoin(hemisphereURL,partialURL))
    imageJPG = browser.find_by_css('.downloads')
    img_href = imageJPG.find_by_css('a')['href']
    print(img_href)
    img_dict = {"title":image.find('div','description').find('h3').text,"img_url":img_href}
    imgList.append(img_dict)

    marsData['imagesURL'] = imgList
 
print(marsData)
    
    
 
