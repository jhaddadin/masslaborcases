import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import shutil

def move(src, dest):
    shutil.move(src, dest)

def primepage():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Data\LaborCases\downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "plugins.always_open_pdf_externally": True
    })

    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(10)
    driver.get('https://escheduling.dlr.state.ma.us/pubinfo/Default.aspx?search=advanced')
    time.sleep(5)
    
    agree = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_radioButtonYes"]')
    agree.click()
    time.sleep(5)
    
    caseno = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_txtCaseNo"]')
    caseno.send_keys('SUP-11-5664')
    
    submit = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_btnSearchMore"]')
    submit.click()
    time.sleep(5)
    
    caselink = driver.find_element_by_xpath('//*[@id="ctl00_BodyContent_GridView1_ctl03_lnkCaseNumber"]')
    caselink.click()
    return driver

def fixnames(casenumber):
    filenumber = 1
    downloads = 'C:\Data\LaborCases\downloads'
    for filename in os.listdir(downloads):
        root, ext = os.path.splitext(filename)
        if root.startswith('View'):
            move('{}\{}'.format(downloads,filename), '{}\\renamed\\{}_{}{}'.format(downloads,casenumber,filenumber,ext))
        filenumber = filenumber + 1

def download_docs(driver, startindex):
    print "Downloading files for {} (Index {})".format(casenumbers[startindex], startindex)
    driver.implicitly_wait(10)
    driver.get('https://escheduling.dlr.state.ma.us/pubinfo/documentlink.aspx?case={}'.format(casenumbers[startindex]))
    docs = driver.find_elements_by_link_text('View Document')
    time.sleep(2)
    for doc in docs:
        doc.click()
    time.sleep(8)
    fixnames(casenumbers[startindex])
	
driver = primepage()

text_file = open('cases_2012_2017.txt', 'r')
casenumbers = text_file.read().split('\n')

startindex = 0
while True:
    download_docs(driver, startindex)
    startindex += 1