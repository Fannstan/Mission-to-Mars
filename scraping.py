# import sys
# sys.path.append("C:\\Users\\fredr\\anaconda3\\envs\\PythonData\\Lib\\site-packages")
# C:\Users\fredr\anaconda3\envs\PythonData\Lib\site-packages
# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    #print("we are in scrape_all()")
    browser = Browser('chrome', **executable_path, headless=False)
    #print(f"browser: {browser}")
    
    news_title, news_paragraph = mars_news(browser)
    

    #Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title, 
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
        
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site 
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')


    # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
    


    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None 

    return news_title, news_p 


# ### JPL Featured Images


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try: 
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

# Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    try:
        #use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)    
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Links for the 4 hemispheres
    hemi_links = browser.find_by_css("a.product-item img") 
    try:
        images = len(hemi_soup.select("div.item"))

        for i in range(images):
            hemispheres = {"img_url": img_url, "title": title}
            browser.find_by_css('a.product-item h3')[i].click()
            element = browser.links.find_by_text('Sample').first
            img_url = element['href']
            title = browser.find_by_css("h2.title").text
            hemispheres['img_url'] = img_url
            hemispheres['title'] = title
                    
            hemisphere_image_urls.append(hemispheres)
            browser.back()
    except BaseException:
        return None

    return hemisphere_image_urls


if __name__ =="__main__":
    #if running as script, print scraped data
    print(scrape_all())
