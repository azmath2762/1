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


def drop_box(order_id, order_item_id,awb):
    access_token = '4joGxl-yofIAAAAAAAAAAW0Wa_qjsmOhQ6NYfWtkG0mNefNaTsIx8hD8BVgkavph'
    dbx = dropbox.Dropbox(oauth2_access_token=access_token, max_retries_on_error=2)
    # file1 = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\invoice\\'
    # p = os.listdir(file1)
    # #
    # file1 += str(p[0])
    file_from = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\label.pdf'
    file_to = '/buymore2/orders/invoices/' + order_id + '#' + order_item_id + '.pdf'
    print('file from : ', file_from)
    with open(file_from, 'rb') as f:
        data = dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
    print('written to ', file_to)

    # file22 = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\invoice'
    # p = os.listdir(file22)
    # file22 += "\\" + str(p[0])
    original_invoice = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\label.pdf'
    target_invoice = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\amazon_back_up_invoice\\' + order_id + '&' + order_item_id + '$'+awb+'.pdf'
    shutil.copyfile(original_invoice, target_invoice)

def GetPicklistId():
    picklist_dict={}
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "SELECT id,picklist_id FROM api_picklist"
    picklist_cur.execute(statement)
    data = picklist_cur.fetchall()
    for i in data:
        id=i[0]
        picklist_id = i[1]
        #print(id,picklist_id)
        picklist_dict[picklist_id]=id
    #print(picklist_dict)
    return picklist_dict
picklist_ids=GetPicklistId()
print(picklist_ids)
rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
db_name = 'orders'
name = 'postgres'
password = 'buymore3'

order_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
order_cur = order_conn.cursor()

def GetItemId(order_id,order_cur):

    statement = "SELECT order_item_id,order_id,dd_id FROM api_neworder where order_id='"+order_id+"'"
    order_cur.execute(statement)
    data = order_cur.fetchall()
    return data
# item_ids=GetItemId('403-9643867-9674732',order_cur)
# print('item_ids',item_ids)

def update_ware_house_id(order_id,order_cur):
    statement = "update api_neworder set warehouse_id=3 where order_id='"+order_id+"'"
    print(statement)
    order_cur.execute(statement)
#update_ware_house_id(order_id,order_cur)

# picklist_id_wms='P1630038209188'
# original_pk=picklist_ids[picklist_id_wms]
# print('original_pk',original_pk)
def UpadateAwbBin(picklist_id,bin_id,awb,dd_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'orders'
    name = 'postgres'
    password = 'buymore3'

    order_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    order_cur = order_conn.cursor()
    #statement1='UPDATE api_dispatchdetails SET "bin_Id" = "'+bin_id+'",awb="'+awb+'" where picklist_id='+ str(picklist_id)
    statement1 = 'update api_dispatchdetails set "bin_Id"[0]=\'' + str(
        bin_id) + '\',awb=' + str(awb) + ',picklist_id=' + str(picklist_id) + ' where dd_id_id=' + str(dd_id)
    print(statement1)
    #statement1 = 'update api_dispatchdetails set "bin_Id"[0]=\'' + str(bin_id) + '\',awb="'+awb+'" where picklist_id='+ str(picklist_id)+' and dd_id_id='+str(dd_id)
    #statement1 = 'SELECT "bin_Id",awb FROM api_dispatchdetails where picklist_id=' + str(picklist_id)
    order_cur.execute(statement1)
    # data = order_cur.fetchall()
    # return data
# dispatch_details=UpadateAwbBin(order_cur,)
# print('dispatch_details',dispatch_details)


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
# passward='Delhi@123'
# username='madanmohan.r@sellerbuymore.com'
# passward='Buymore@123'
username='bangalore.dev2@sellerbuymore.com'
passward='Buymore@123'
# username='mumbai.test3@sellerbuymore.com'
# passward='Buymore@123'

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


def amazon_processing(picklist):
    faild_file_name = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\complete_and_fail_files\\failed' + picklist + '.csv'
    completed_file_name = r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\complete_and_fail_files\\completed' + picklist + '.csv'
    with open(faild_file_name, "w", newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(
            ['picklistId', 'listingId', 'binId', 'quantity', 'fnsku', 'warehouseId', 'tracking_id', 'order_id',
             'error massage'])
    with open(completed_file_name, "w", newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(
            ['picklistId', 'listingId', 'binId', 'quantity', 'fnsku', 'warehouseId', 'tracking_id', 'order_id'])

    file = r'mangodb_picklist_details.csv'
    with open(file, "r", newline='')as f1:
        r = list(csv.reader(f1))
    for i in range(1,len(r)):

        picklistId = str(r[i][0])
        listingId = str(r[i][1])
        binId_mongo = str(r[i][2])
        quantity = str(r[i][3])
        warehouseId_mongo = str(r[i][5])
        # picklistId = str(r[i][0])
        msku = str(r[i][4])

        # picklistId='P1630308093186'
        #msku='X0018POFCN'
        try:
            xps_file = r'C:\Users\Administrator\Documents'
            p = os.listdir(xps_file)
            xps_file += "\\" + str(p[4])
            print(xps_file)
            os.remove(xps_file)
        except Exception as e:
            print('remove error',e)

        # xps_file = r'C:\Users\Administrator\Documents\*'
        # # p = os.listdir(xps_file)
        # # xps_file += "\\" + str(p[0])
        # def a_remove1(files):
        #
        #     for f in files:
        #         os.remove(f)
        #     print('removed all invoice pdf files from download folder')
        # a_remove1(xps_file)
        try:
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
                multi = driver.find_element_by_xpath('//label[@id="was-pack-shipment-packed-count"]')
                driver.execute_script("arguments[0].scrollIntoView();", multi)
                multi = multi.text
                multi = int(multi[2])
                print(multi)
                for i in range(1, multi):
                    print('in side python')
                    try:
                        status = driver.find_element_by_xpath(
                            '(//label[@class="was-bold-text was-sku-packed-count"])[' + str(i + 1) + ']').text
                    except:
                        status = driver.find_element_by_xpath(
                            '(//label[@class="was-bold-text was-sku-packed-count"])[' + str(i) + ']').text
                    status1 = int(status[0])
                    status2 = int(status[2])
                    print(status1, status2)
                    if status1 != status2:
                        try:
                            sku = driver.find_element_by_xpath('(//label[@id="was-pack-sku-id"])[' + str(i) + ']').text
                        except:
                            sku = driver.find_element_by_xpath('(//label[@id="was-pack-sku-id"])[' + str(i + 1) + ']').text
                        driver.find_element_by_xpath('//input[@name="scannedSku"]').send_keys(sku, Keys.ENTER)

            except Exception as e:
                print('no multi qty', e)


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

            item_ids=GetItemId(order_id, order_cur)
            if len(item_ids)>0:
                item_id_=[]
                order_id_=[]

                for j in item_ids:
                    item_id = j[0]
                    order_id = j[1]
                    dd_id=j[2]
                    item_id_.append(item_id)
                    order_id_.append(order_id)
                    # item_id_details.append(dd_id)
                    print('item_id',item_id)
                    original_pk = picklist_ids[picklistId]
                    print('original_pk', original_pk)
                    UpadateAwbBin(original_pk,binId_mongo,tracking_id,dd_id)

                print(order_id_[0],'#', item_id_[0])
                drop_box(order_id_[0], item_id_[0],tracking_id)
            if len(item_ids)==0:
                from amazon_processing_code.missing_order_api import missing_amazon_new_order_api
                missing_amazon_new_order_api(order_id)
                update_ware_house_id(order_id, order_cur)
                item_ids = GetItemId(order_id, order_cur)
                print('nees to update warehouse id in orders table')
                if len(item_ids) > 0:
                    item_id_ = []
                    order_id_ = []

                    for j in item_ids:
                        item_id = j[0]
                        order_id = j[1]
                        dd_id = j[2]
                        item_id_.append(item_id)
                        order_id_.append(order_id)
                        # item_id_details.append(dd_id)
                        print('item_id', item_id)
                        original_pk = picklist_ids[picklistId]
                        print('original_pk', original_pk)
                        UpadateAwbBin(original_pk, binId_mongo, tracking_id, dd_id)

                    print(order_id_[0], '#', item_id_[0])
                    drop_box(order_id_[0], item_id_[0], tracking_id)
                if len(item_ids)==0:
                    continue
            driver.find_element_by_xpath('//input[@id="was-packScanDeliveryLabel-input"]').send_keys('1234')
            # url1.append(driver.current_url)
            # driver.switch_to_window(driver.window_handles[0])
            # print(url)

            with open(completed_file_name, "a", newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(
                    [picklistId, listingId, binId_mongo, quantity, msku, warehouseId_mongo, tracking_id, order_id])
        except Exception as e:
            print('final error msg',e)
            with open(faild_file_name, "a", newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([picklistId, listingId, binId_mongo, quantity, msku, warehouseId_mongo,e])





scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)


client = gspread.authorize(creds)

#sheet = client.open("amazon1").vendor_removal_Bangalore.pysheet1  # Open the spreadhseet
sheet2=client.open('Flex Picklist').worksheet('bangalore')
#data = sheet.get_all_values()  # Get a list of all records
data2 = list(sheet2.get_all_values())  # Get a list of all records
print('data2',data2)

for i in range(1,len(data2)):
    date=str(data2[i][0])
    Portal=str(data2[i][1])
    Picklist=str(data2[i][2])
    Qty=data2[i][3]
    Status=data2[i][4]
    Automation=data2[i][5]
    Error=data2[i][6]
    warehouse_process=data2[i][7]
    print(date,Portal,Picklist,Qty,Status,Automation,Error,warehouse_process)
    if (Status=='Done' and Automation!='Done'):
        sheet2.update_cell(i + 1, 6, 'running')
        print('Picklist',Picklist)
        from amazon_processing_code.dateform import mongo_details

        print('stop')
        mongo_details(Picklist)
        time.sleep(1)
        print('stop')
        amazon_processing(Picklist)
        path=r'C:\Users\Administrator\PycharmProjects\pythonProject\amazon_processing_code\complete_and_fail_files\failed'+Picklist+'.csv'
        file=pd.read_csv(path)
        error_=len(file)
        if (error_)>0:
            error_massage=str(error_)+' records are failed'
            sheet2.update_cell(i + 1, 7, error_massage)
            sheet2.update_cell(i + 1, 6, 'Done')
        sheet2.update_cell(i + 1, 6, 'Done')
