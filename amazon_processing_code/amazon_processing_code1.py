import csv
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import glob
with open('amazon_processing_details.csv', "w", newline='', encoding="utf-8") as f:
    thewriter1 = csv.writer(f)
    thewriter1.writerow(['picklist_id','qty','total_item','total_pack','msku'])

path=r'C:\Users\madhanmohan\Desktop\chrome_drivers\chromedriver.exe' #path where firefox driver is installed
url='https://www.amazon.in/ap/signin?clientContext=262-0722543-7588645&openid.return_to=https%3A%2F%2Fsellerflex.amazon.in%2F&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_waas_in&openid.mode=checkid_setup&marketPlaceId=A21TJRUUN4KGV&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=Amazon&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=3600&siteState=clientContext%3D258-4741331-3382410%2CsourceUrl%3Dhttps%253A%252F%252Fsellerflex.amazon.in%252F%2Csignature%3Dnull'#url or the targeted website
driver = webdriver.Chrome(executable_path=path)  # driver object to interact with browser
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
login(username,passward)

driver.get('https://sellerflex.amazon.in/pick')
time.sleep(1)
driver.find_element_by_xpath('(//div[@class="css-1g8dw35"])[2]').click()
time.sleep(1)
table=driver.find_elements_by_xpath('//table[@class="css-1c0jove"]/tbody/tr')
print(len(table))

for i in range(1,len(table)+1):
    driver.get('https://sellerflex.amazon.in/pick')
    driver.find_element_by_xpath('(//div[@class="css-1g8dw35"])[2]').click()
    time.sleep(1)                  #/html/body/div/div/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[3]/div/table/tbody/tr['+str(i)+']/td[2]/span/div/a
    try:
        t=driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div[2]/div/div[3]/div/table/tbody/tr['+str(i)+']/td[2]/span/div/a')
    except:
        t=driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[3]/div/table/tbody/tr['+str(i)+']/td[2]/span/div/a')
    driver.execute_script("arguments[0].scrollIntoView();", t)
    t.click()
    #webdriver.ActionChains(driver).move_to_element(t).click(t).perform()
    time.sleep(1)
    qty = driver.find_element_by_xpath('(//span[@class="was-bold-text"])[4]').text
    picklist_id = driver.find_element_by_xpath('(//span[@class="was-bold-text"])[5]').text
    print(qty,picklist_id)
    qty=int(qty)
    table1=driver.find_elements_by_xpath('//table[@id="was-pick-details-table"]/tbody/tr')
    print('table1 length:',len(table1))
    for j in range(1,len(table1)+1):
        #time.sleep(1)                              #/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr[1]/td[5]
        # print(j)
        total_item=driver.find_element_by_xpath('//table[@id="was-pick-details-table"]/tbody/tr['+str(j)+']/td[5]').text
        total_pack=driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr['+str(j)+']/td[6]').text
        print(total_pack,total_item)
        total=int(total_item)-int(total_pack)
        print(total,type(total))
        if total>0:
            msku=driver.find_element_by_xpath('/html/body/div/div/div[2]/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr['+str(j)+']/td[2]/a').text
            print(msku)

            with open('amazon_processing_details.csv', "a", newline='', encoding="utf-8") as f:
                thewriter1 = csv.writer(f)
                thewriter1.writerow([picklist_id,qty,total_item,total_pack,msku])
