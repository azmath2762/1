import csv
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import glob
with open('amazon_processing_details.csv', "w", newline='', encoding="utf-8") as f:
    thewriter1 = csv.writer(f)
    thewriter1.writerow(['picklist_id','qty','total_item','total_pack','msku'])

path=r'C:\Users\Administrator\PycharmProjects\pythonProject\chrome_drivers\chromedriver.exe' #path where firefox driver is installed
url='https://www.amazon.in/ap/signin?clientContext=262-0722543-7588645&openid.return_to=https%3A%2F%2Fsellerflex.amazon.in%2F&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_waas_in&openid.mode=checkid_setup&marketPlaceId=A21TJRUUN4KGV&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=Amazon&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=3600&siteState=clientContext%3D258-4741331-3382410%2CsourceUrl%3Dhttps%253A%252F%252Fsellerflex.amazon.in%252F%2Csignature%3Dnull'#url or the targeted website
driver = webdriver.Chrome(executable_path=path)  # driver object to interact with browser
driver.implicitly_wait(10)
driver.maximize_window()  # miximizes the window size
driver.get(url)  # driver object will fetch the url
action = ActionChains(driver)
time.sleep(2)
# username='buymoreznau@gmail.com'
# passward='buymore@123'
username='madanmohan.r@sellerbuymore.com'
passward='Buymore@123'

def login(username,passward):
    driver.find_element_by_xpath('//div/input[@id="ap_email"]').send_keys(username)
    time.sleep(1)
    driver.find_element_by_xpath('//div/input[@id="ap_password"]').send_keys(passward)
    time.sleep(1)
    driver.find_element_by_xpath('//span/input[@id="signInSubmit"]').click()
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//input[@id="ap_password"]').send_keys(passward)
        time.sleep(1)
        driver.find_element_by_xpath('//span/input[@id="signInSubmit"]').click()
    except Exception as e:
        print('login issue :',e)
    #time.sleep(4)
    try:
        driver.find_element_by_xpath('//span[text()="×"]').click()
    except:
        pass
    driver.get('https://sellerflex.amazon.in/printer-settings')
    d=driver.find_element_by_xpath('(//button[@class="was-form-control was-dropdown-btn"])[1]')
    driver.execute_script("arguments[0].scrollIntoView();", d)
    time.sleep(2)
    webdriver.ActionChains(driver).move_to_element(d).click(d).perform()
    # d.click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/form/div[1]/div/ul/li[1]').click()

    # sel = Select(d)
    # sel.select_by_index(0)
    driver.find_element_by_xpath('(//button[@class="was-form-control was-dropdown-btn"])[3]').click()
    time.sleep(2)
    driver.find_element_by_xpath('(//li[text()="Microsoft Print to PDF"])[2]').click()
    #webdriver.ActionChains(driver).move_to_element(drop).click(drop).perform()
    driver.find_element_by_xpath('//button[text()="Save"]').click()
    driver.get('https://sellerflex.amazon.in/pack')
    time.sleep(2)

    # sel = Select(drop)
    # sel.select_by_index(3)
login(username,passward)
