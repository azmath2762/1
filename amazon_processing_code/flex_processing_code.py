import csv
import os
import shutil
import time

import dropbox
import gspread
import pandas as pd
import requests
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import psycopg2
def convert_xps_to_pdf(file_name):
    file1 = open(file_name, "r")
    data = file1.read()
    zpl = data
    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/12dpmm/labels/4x6/0/'
    files = {'file': zpl}
    headers = {'Accept': 'application/pdf'}  # omit this line to get PNG images back
    # headers = {'Accept' : 'application/png'} # omit this line to get PNG images back
    response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('label.pdf', 'wb') as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Error: ' + response.text)


# file_name = "QZ Tray Raw Print.oxps"
# convert_xps_to_pdf(file_name)

# path=r'C:\Users\Administrator\PycharmProjects\pythonProject\chrome_drivers\chromedriver.exe' #path where firefox driver is installed
url='https://www.amazon.in/ap/signin?clientContext=262-0722543-7588645&openid.return_to=https%3A%2F%2Fsellerflex.amazon.in%2F&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_waas_in&openid.mode=checkid_setup&marketPlaceId=A21TJRUUN4KGV&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=Amazon&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=3600&siteState=clientContext%3D258-4741331-3382410%2CsourceUrl%3Dhttps%253A%252F%252Fsellerflex.amazon.in%252F%2Csignature%3Dnull'#url or the targeted website
# driver = webdriver.Chrome(executable_path=path)  # driver object to interact with browser
path = r'C:\Users\Administrator\PycharmProjects\pythonProject\chrome_drivers\chromedriver.exe'  # path where firefox driver is installed
try:
    os.mkdir(r"C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\dd\*")
except:
    pass
chromeOptions2 = Options()
chromeOptions2.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\dd"})
driver = webdriver.Chrome(executable_path=path, options=chromeOptions2)
driver.implicitly_wait(10)
driver.maximize_window()  # miximizes the window size
driver.get(url)  # driver object will fetch the url
action = ActionChains(driver)
time.sleep(2)
# username='buymoreznau@gmail.com'
# passward='buymore@123'
# username='madanmohan.r@sellerbuymore.com'
# passward='Buymore@123'
username='bangalore.dev2@sellerbuymore.com'
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
    d = driver.find_element_by_xpath('(//button[@class="was-form-control was-dropdown-btn"])[1]')
    driver.execute_script("arguments[0].scrollIntoView();", d)
    time.sleep(2)
    try:
        webdriver.ActionChains(driver).move_to_element(d).click(d).perform()
        # d.click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/form/div[1]/div/ul/li[1]').click()
    except:
        webdriver.ActionChains(driver).move_to_element(d).click(d).perform()
        # d.click()
        time.sleep(2)
        driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/form/div[1]/div/ul/li[1]').click()
    #webdriver.ActionChains(driver).move_to_element(d).click(d).perform()
    # sel = Select(d)
    # sel.select_by_index(0)
    driver.find_element_by_xpath('(//button[@class="was-form-control was-dropdown-btn"])[3]').click()
    time.sleep(2)
    driver.find_element_by_xpath('(//li[text()="Microsoft Print to PDF"])[2]').click()
    # webdriver.ActionChains(driver).move_to_element(drop).click(drop).perform()
    driver.find_element_by_xpath('//button[text()="Save"]').click()
    driver.get('https://sellerflex.amazon.in/pack')
    time.sleep(2)

    # sel = Select(drop)
    # sel.select_by_index(3)
login(username,passward)
file=r'mangodb_picklist_details.csv'
with open(file, "r", newline='')as f1:
    r = list(csv.reader(f1))
print(r)
def amazon_processing():
    for i in range(1,len(r)):
        # picklistId = str(r[i][0])
        # listingId = str(r[i][1])
        # binId_mongo = str(r[i][2])
        # quantity = str(r[i][3])
        # warehouseId_mongo = str(r[i][5])
        # picklistId = str(r[i][0])
        # msku = str(r[i][4])

        picklistId='P1630323233380'
        msku='X0018PRVKV'
        try:
            xps_file = r'C:\Users\Administrator\Documents'
            p = os.listdir(xps_file)
            xps_file += "\\" + str(p[4])
            print(xps_file)
            os.remove(xps_file)
        except:
            pass
        # xps_file = r'C:\Users\Administrator\Documents\*'
        # # p = os.listdir(xps_file)
        # # xps_file += "\\" + str(p[0])
        # def a_remove1(files):
        #
        #     for f in files:
        #         os.remove(f)
        #     print('removed all invoice pdf files from download folder')
        # a_remove1(xps_file)

        url1='https://sellerflex.amazon.in/pack'
        driver.get(url1)
        time.sleep(1)
        p=driver.find_element_by_xpath('//input[@name="scannedPickTaskId"]')
        p.click()
        p.send_keys(picklistId,Keys.ENTER)
        action = ActionChains(driver)
        # double click operation
        action.double_click(p)
        p.send_keys(Keys.ENTER)
        time.sleep(2)
        driver.find_element_by_xpath('//input[@name="scannedSku"]').send_keys(msku,Keys.ENTER)
        try:
            driver.find_element_by_xpath('//input[@id="was-hazmat-confirmation-checkbox"]').click()
        except:
            pass
        try:
            driver.find_element_by_xpath('//button[@id="was-plastic-ban-ok-button"]').click()
        except:
            pass
        try:
            multi=driver.find_element_by_xpath('//label[@id="was-pack-shipment-packed-count"]')
            driver.execute_script("arguments[0].scrollIntoView();", multi)
            multi=multi.text
            multi=int(multi[2])
            print(multi)
            for i in range(1,multi):
                print('in side python')
                try:
                    status=driver.find_element_by_xpath('(//label[@class="was-bold-text was-sku-packed-count"])['+str(i+1)+']').text
                except:
                    status = driver.find_element_by_xpath(
                        '(//label[@class="was-bold-text was-sku-packed-count"])[' + str(i) + ']').text
                status1=int(status[0])
                status2=int(status[2])
                print(status1,status2)
                if status1!=status2:
                    try:
                        sku = driver.find_element_by_xpath('(//label[@id="was-pack-sku-id"])[' + str(i) + ']').text
                    except:
                        sku=driver.find_element_by_xpath('(//label[@id="was-pack-sku-id"])['+str(i+1)+']').text
                    driver.find_element_by_xpath('//input[@name="scannedSku"]').send_keys(sku, Keys.ENTER)

        except Exception as e:
            print('no multi qty',e)


        driver.find_element_by_xpath('//input[@name="scanBoxType"]').send_keys('CUSTOM',Keys.ENTER)
        try:
            driver.find_element_by_xpath('//button[.="CONFIRM AND PRINT"]').click()
        except:
            pass
        xps_file = r'C:\Users\Administrator\Documents'
        p = os.listdir(xps_file)
        xps_file += "\\" + str(p[4])
        print(xps_file)
        # file_name = r'C:\Users\Administrator\Documents'
        # p = os.listdir(file_name)
        # file_name += "\\" + str(p[0])
        convert_xps_to_pdf(xps_file)

        driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[5]/div[4]/div[1]/div/a').click()
        time.sleep(1)
        print(driver.current_url)
        elem = driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[5]/div[4]/div[1]/div/a').get_attribute('href')
        print(elem)
        driver.switch_to.window(driver.window_handles[1])
        #driver.execute_script("window.open(%s, 'new_window')") % elem
        tracking_id = driver.find_element_by_xpath('(//td[@class="was-bold-text"])[4]').text
        order_id=driver.find_element_by_xpath('(//td[@class="was-bold-text"])[5]').text
        driver.close()
        print(tracking_id,order_id)
        driver.switch_to.window(driver.window_handles[0])

        #item_ids=GetItemId(order_id, order_cur)

        #item_id=item_ids[0][0]
        #print('item_id',item_id)
        #drop_box(order_id, item_id)
        #original_pk = picklist_ids[picklistId]
        #print('original_pk',original_pk)

        driver.find_element_by_xpath('//input[@id="was-packScanDeliveryLabel-input"]').send_keys('1234')
        # url1.append(driver.current_url)
        # driver.switch_to_window(driver.window_handles[0])
        # print(url)
amazon_processing()