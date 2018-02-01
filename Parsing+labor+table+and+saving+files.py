
# coding: utf-8

# In[1]:

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re


# In[2]:

def getlinks(driver):
    links = driver.find_elements_by_css_selector(".footable-loaded.phone")
    for i in links:
        if links.index(i) % 3 == 0:
            casenumbers.append(i.text)


# In[3]:

def scrapecasenumbers(driver):
    morepages = True
    pagecount = 0
    lastpage = None
    while morepages == True:
        pagenav = driver.find_elements_by_class_name('gridviewPagerCss') # Capture the range of page numbers on the bottom
        pagenav = pagenav[0].text.split(" ")

        if pagenav[0] == "...": # Remove '...' from the first value in the list
            del pagenav[0]

        if pagenav[-1] == "...": # Check if there are multiple pages to load
            lastpage = str(int(pagenav[-2]) + 1).encode("utf-8").decode("utf-8")  # Calculate the final page
            pagenav[-1] = lastpage # Change last value to string

            for index, page in enumerate(pagenav):
                if index == 0: # Scrape links for the first page
                    print ">> Scraping page {}".format(page)
                    getlinks(driver)
                    pagecount = pagecount + 1
                else:
                    href = "javascript:__doPostBack('ctl00$BodyContent$GridView1','Page${}')".format(page)
                    pagelink = driver.find_element_by_xpath('//a[@href="{}"]'.format(href))
                    pagelink.click()
                    print ">> Scraping page {}".format(page)
                    getlinks(driver) # Scrape the links
                    pagecount = pagecount + 1 
        else:
            morepages = False
            if lastpage == None:
                for index, page in enumerate(pagenav):
                    if index == 0: # Scrape links for the first page
                        print ">> Scraping page {}".format(page)
                        getlinks(driver)
                        pagecount = pagecount + 1
                    else:
                        pagelink = driver.find_element_by_link_text(page) # Click the link for the next page number
                        pagelink.click()
                        print ">> Scraping page {}".format(page)
                        getlinks(driver) # Scrape the links
                        pagecount = pagecount + 1
            else:
                for index, page in enumerate(pagenav):
                    if page == u'...':
                        pass
                    elif int(page) <= int(lastpage):
                        pass
                    else:
                        pagelink = driver.find_element_by_link_text(page) # Click the link for the next page number
                        pagelink.click()
                        print ">> Scraping page {}".format(page)
                        getlinks(driver) # Scrape the links
                        pagecount = pagecount + 1
            print "Total pages scraped: {}".format(pagecount)
            print "Total cases scraped: {}".format(len(casenumbers))
            print ""


# In[4]:

def loadbrowser():
    driver = webdriver.Chrome()
    driver.get("https://escheduling.dlr.state.ma.us/pubinfo/")
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_radioButtonYes"]').click()
    return driver


# In[5]:

casenumbers = []


# In[6]:

years = ['2011']


# In[9]:

quarters = {'1/01/':'8/31/',
            '9/01/':'12/31/'}


# In[10]:

for year in years:
    for start, end in quarters.iteritems():
        driver = loadbrowser()
        driver.implicitly_wait(10)
        date_start = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_txtDateFileFrom"]')
        date_end = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_txtDateFileTo"]')
        submit = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_btnSearchMore"]')
        date_start.clear()
        date_end.clear()
        print "Scraping case numbers for {}: {} through {}".format(year, start, end)
        date_start.send_keys(start + year)
        date_end.send_keys(end + year)
        submit.click()
        scrapecasenumbers(driver)
        driver.quit()


# In[11]:

# Save the case numbers to a text file
thefile = open('cases_2011.txt', 'w')
for item in casenumbers:
  thefile.write("%s\n" % item)
thefile.close()


# In[ ]:



