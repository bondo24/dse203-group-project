import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


page_url = "https://siccode.com/"


driver = webdriver.Chrome('/Users/dorehkazemisefat/Desktop/amazon-test/scrapyexample4/chromedriver')

company_list = ["Zappos.com ","Woot inc Electronic Shopping and Mail-Order Houses","Whole Foods Market Inc Supermarkets"]

for company in company_list:
    driver.get(page_url)
    searchBox = driver.find_element_by_id("keyword_m")
    searchBox.send_keys(company)
    driver.find_element_by_xpath("/html/body/div[1]/article/section[1]/div/form/div/div[2]/input").click()
    companyCode = driver.find_element_by_xpath("//*[@id='result-naics']/ul/li/a/div").text
    print(companyCode)
    time.sleep(2)