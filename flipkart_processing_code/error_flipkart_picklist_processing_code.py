import shutil
import csv
import os
import time
import glob
from tika import parser
import dropbox
import psycopg2
import pyautogui
from selenium.webdriver.support import expected_conditions as EC

with open('failed_records4.csv', "w", newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['listingId', 'picklistId_mongo', 'warehouseId_mongo','bin_id','error massage'])

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
db_name = 'orders'
name = 'postgres'
password = 'buymore3'

def drop_box(order_id,order_item_id):
    access_token = '4joGxl-yofIAAAAAAAAAAW0Wa_qjsmOhQ6NYfWtkG0mNefNaTsIx8hD8BVgkavph'
    dbx = dropbox.Dropbox(oauth2_access_token=access_token, max_retries_on_error=2)
    file1 = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\croped_file\\'
    p = os.listdir(file1)
    #
    file1 += str(p[0])
    file_from = file1
    file_to = '/buymore2/orders/invoices/' + order_id + '#' + order_item_id + '.pdf'
    print('file from : ', file_from)
    with open(file_from, 'rb') as f:
        data = dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
    print('written to ', file_to)

    file11 = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files'
    p = os.listdir(file11)
    file11 += "\\" + str(p[0])
    file_from = file11
    file_to = '/buymore2/madan/invoices/' + order_id + '#' + order_item_id + '.pdf'
    print('file from 2: ', file_from)
    with open(file_from, 'rb') as f:
        data = dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
    print('written to 2:', file_to)

    file22 = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\croped_file'
    p = os.listdir(file22)
    file22 += "\\" + str(p[0])
    original_invoice=file22
    target_invoice=r'C:\Users\Administrator\PycharmProjects\pythonProject\croped_invoice\\'+order_id+'&'+order_item_id+'.pdf'
    shutil.copyfile(original_invoice, target_invoice)


import csv
import pdb

path = r'C:\Users\Administrator\PycharmProjects\pythonProject\chrome_drivers\chromedriver.exe'  # path where firefox driver is installed
try:
    os.mkdir(r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files\*")
except:
    pass
chromeOptions2 = Options()
chromeOptions2.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files"})
driver = webdriver.Chrome(executable_path=path, options=chromeOptions2)
# url='https://buymore2api.sellerbuymore.com/#/login'#url or the targeted website
# driver = webdriver.Chrome(executable_path=path)  # driver object to interact with browser
driver.implicitly_wait(3)
driver.maximize_window()


def startSmart(username, password1):
    try:
        driver.get("https://seller.flipkart.com/")
        driver.maximize_window()
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//span[.='Login for existing sellers']").click()
        except:
            time.sleep(1)
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/span").click()

        driver.find_element_by_xpath(
            "//span[contains(text(),'Username or 10 digit phone number or email')]/../input").send_keys(username)
        time.sleep(2)
        try:
            try:

                ne = driver.find_element_by_xpath("//span[text()='Next']/..")
                webdriver.ActionChains(driver).move_to_element(ne).click(ne).perform()
            except:
                time.sleep(2)
                nex = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[2]/div[2]/div/div[2]/button').click()
                webdriver.ActionChains(driver).move_to_element(nex).click(nex).perform()
        except Exception as e:
            print('login issue:', str(e))

        driver.find_element_by_xpath(
            "//input[@type='password']").send_keys(password1)
        try:
            driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-border"]').click()
            time.sleep(3)
        except:
            pass

        driver.find_element_by_xpath("//span[text()='Login']/..").click()
        time.sleep(4)
        driver.get(
            'https://seller.flipkart.com/index.html#dashboard/fbflite-ff/LOC357548a12e4a4842a1c4177a08648403/nav-ff/processing')
        return True
    except Exception as e:
        print('start smart issue:', str(e))
    #return driver
    # driver.close()


#startSmart(username, password)
import psycopg2

rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
db_name = 'products'

password = 'buymore3'

#order_id_pdf='OD122130185816122000'

#from projects.flipkart_processing_code.mongodb import dateform
username='counfreedise@gmail.com'
password1='cfdrsl@2012'
#P280621-DCF6D3EA49CD
file=r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\flipkartlbhw\finalfklbh_new.csv'

main_lbhw={}
with open(file, "r", newline='') as f1:
    lbhw = csv.DictReader(f1)
    lbhw = list(lbhw)
    for rr in lbhw:
        listingId = rr['Listing ID']
        Length = rr['Length']
        Breadth = rr['Breadth']
        Height = rr['height']
        Weight = rr['Weight']
        main_lbhw[listingId]=[Length,Breadth,Height,Weight]
list1=[]

#print(main_lbhw)
#pdb.set_trace()

file=r'failed_records1.csv'
#file=r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\mongo_db\mangodb_picklist_details.csv'
with open(file, "r", newline='')as f1:
    r = list(csv.reader(f1))
    print('start the login')
    startSmart(username, password1)
    for i in range(1,len(r)):

        multilisting_id_list=[]
        try:
            #fail
            picklistId_mongo = str(r[i][1])
            listingId = str(r[i][0])
            binId_mongo = str(r[i][3])
            #quantity = str(r[i][3])
            warehouseId_mongo = str(r[i][2])
            #originaal
            # picklistId_mongo = str(r[i][0])
            # listingId = str(r[i][1])
            # binId_mongo =str(r[i][2])
            # quantity = str(r[i][3])
            # warehouseId_mongo=str(r[i][5])
            # picklistId_mongo='P020721-219F439F334D'
            # listingId='LSTFKTFYBHCANHGKSBPBMRW5A'
            print('get the data from the mongo db')
            print('picklistId_mongo',picklistId_mongo,'listingId:',listingId,'binId_mongo:',binId_mongo,'warehouseId_mongo:',warehouseId_mongo)
            #pdb.set_trace()
            #try:
            if listingId in list1:
                try:
                    list1.pop()
                except:
                    print('list1 is empty')
                continue
            time.sleep(5)
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div/div[2]/div/div/div[2]/div/div/a/span').click()
                #time.sleep(1)
                if warehouseId_mongo=='4':
                    driver.find_element_by_xpath('//li[.="BANGALORE : 560026"]').click()
                elif warehouseId_mongo=='10':
                    driver.find_element_by_xpath('//li[.="New Delhi"]').click()
                elif warehouseId_mongo=='7':
                    driver.find_element_by_xpath('//li[.="HOWRAH : 711302"]').click()
                elif warehouseId_mongo=='3':
                    driver.find_element_by_xpath('//li[.="BHIWANDI"]').click()
            except Exception as e:
                print('location error:',e)
            print('select the location from front end')

            time.sleep(1)
            try:
                driver.find_element_by_xpath('//input[@class="picklistId-input"]').send_keys(picklistId_mongo,Keys.ENTER)#P280621-DCF6D3EA49CD
                print('enter the picklist id to front end')
            except:
                print('pass')
            #time.sleep(2)
            driver.find_element_by_xpath('//input[@class="productId-input"]').send_keys(listingId,Keys.ENTER)#LSTFKTFYBHCANHGKSBPBMRW5A
            time.sleep(1)#//div[@class="toast-message-container"]
            print('enter the listing id id to front end')
            try:
                cancel=driver.find_element_by_xpath('//span[text()="Order is cancelled"]').text
                time.sleep(2)
                order_id_cancel=driver.find_element_by_xpath('//div[@class="order-id clearfix"]').text
                time.sleep(1)
                item_id_cancel=driver.find_element_by_xpath('//div[@class="order-item-id clearfix"]').text
                time.sleep(2)
                driver.find_element_by_xpath('//span[.="Done"]').click()
                # pdb.set_trace()
                awb1='Canceled_product'
                name = 'postgres'
                rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
                db_name = 'products'
                password = 'buymore3'
                conn1 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                cur1 = conn1.cursor()

                statement = "SELECT flipkart_portal_unique_id from flipkart_flipkartproducts where flipkart_listing_id='" + listingId + "'"
                cur1.execute(statement)
                conn1.commit()
                data = cur1.fetchall()
                dd_length = len(data)
                #fsn_mongo = data[0][0]
                #print(len(data), fsn_mongo)

                rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
                db_name = 'products'
                password = 'buymore3'
                db_name = 'testers'
                conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                cur2 = conn2.cursor()
                # statement = "SELECT order_id from api_neworders where pick_list_id='" + picklistId + "' and bin_id='"+binId+"'"# and fsn='"+fsn+"'"
                statement = "SELECT new_order_id,pick_list_id,bin_id,warehouse_id,fsn from api_neworders where order_id='" + order_id_cancel + "' and order_item_id='" + item_id_cancel + "'"  # pick_list_id='" + picklistId + "' or bin_id='" + binId + "' and fsn='" + fsn + "'"
                cur2.execute(statement)
                conn2.commit()
                data2 = cur2.fetchall()
                dd_length3 = len(data2)
                print(len(data2), 'order id', data2)
                for j in data2:
                    new_order_id1 = j[0]
                    picklistId1 = j[1]
                    bin_id1 = j[2]
                    warehouse_id = j[3]
                    fsn = j[4]
                    print(picklistId1, picklistId_mongo, bin_id1, warehouse_id)
                    # pdb.set_trace()
                    if picklistId1 == ' ' and bin_id1 == ' ':
                        # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                        # cur2 = conn2.cursor()
                        statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "',bin_id='" + binId_mongo + "',tracking_id='" + awb1 + "'  where new_order_id=" + str(new_order_id1)
                        cur2.execute(statement)
                        conn2.commit()
                    elif picklistId1 == picklistId_mongo:
                        print(picklistId1)
                        print('we can update the awb')
                        # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                        # cur2 = conn2.cursor()
                        statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "',bin_id='" + binId_mongo + "',tracking_id='" + awb1 + "'  where new_order_id=" + str(new_order_id1)
                        cur2.execute(statement)
                        conn2.commit()
                    elif picklistId1 != picklistId_mongo:
                        # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                        # cur2 = conn2.cursor()
                        statement = "SELECT new_order_id,pick_list_id,bin_id from api_neworders where pick_list_id='" + picklistId_mongo + "' and warehouse_id=" + str(warehouse_id) + " and fsn='" + fsn + "'"
                        cur2.execute(statement)
                        conn2.commit()
                        data2 = cur2.fetchall()
                        print(len(data2), 'order id', data2)
                        new_order_id2 = data2[0][0]
                        pick_list_id2 = data2[0][1]
                        bin_id2 = data2[0][2]
                        # bin_id_main=j[1]
                        # swaping
                        # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                        # cur2 = conn2.cursor()
                        statement = "UPDATE api_neworders SET pick_list_id = '" + pick_list_id2 + "',bin_id='" + bin_id2 + "', tracking_id='" + awb1 + "' where new_order_id=" + str(new_order_id1)
                        cur2.execute(statement)
                        conn2.commit()

                        # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                        # cur2 = conn2.cursor()
                        statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId1 + "',bin_id='" + bin_id1 + "'  where new_order_id=" + str(new_order_id2)
                        cur2.execute(statement)
                        conn2.commit()
                        # pdb.set_trace()
                continue
            except Exception as e:
                print('cancel error massage:',e)
            try:
                one_more=driver.find_element_by_xpath('//div[@class="multi-product-warning-container"]').text
                time.sleep(2)
                list1=[]
                l1 = []
                b1 = []
                h1 = []
                w1 = []
                listing2 = driver.find_element_by_xpath('(//div[@class="product-listing-id clearfix"])[2]')
                driver.execute_script("arguments[0].scrollIntoView();", listing2)
                listingid2 = listing2.text
                listingid2 = listing2.text
                listingid2 = listingid2.split()[2]
                list1.append(listingid2)
                listing1 = driver.find_element_by_xpath('(//div[@class="product-listing-id clearfix"])[1]')
                driver.execute_script("arguments[0].scrollIntoView();", listing1)
                listingid1=listing1.text
                listingid1=listingid1.split()[2]
                multilisting_id_list.append(listingid1)
                list1.append(listingid1)
                print(listingid1)
                try:
                    listing3 = driver.find_element_by_xpath('(//div[@class="product-listing-id clearfix"])[3]')
                    driver.execute_script("arguments[0].scrollIntoView();", listing3)
                    listingid3 = listing3.text
                    listingid3 = listingid3.split()[2]
                    list1.append(listingid3)
                except Exception as e:
                    print('error massage for listing3',e)
                try:
                    listing4 = driver.find_element_by_xpath('(//div[@class="product-listing-id clearfix"])[4]')
                    driver.execute_script("arguments[0].scrollIntoView();", listing4)
                    listingid4 = listing4.text
                    listingid4 = listingid4.split()[2]
                    list1.append(listingid4)
                except Exception as e:
                    print('error massage for listing4',e)
                try:
                    listing5 = driver.find_element_by_xpath('(//div[@class="product-listing-id clearfix"])[5]')
                    driver.execute_script("arguments[0].scrollIntoView();", listing5)
                    listingid5 = listing5.text
                    listingid5 = listingid5.split()[2]
                    list1.append(listingid5)
                except Exception as e:
                    print('error massage for listing5',e)
                print('list1:',list1)
                for p in range(len(list1)):
                    try:
                        l1.append(main_lbhw[list1[p]][0])
                        b1.append(main_lbhw[list1[p]][1])
                        h1.append(main_lbhw[list1[p]][2])
                        w1.append(main_lbhw[list1[p]][3])
                        print('listing labhw table',l1,l1,b1,h1,w1)
                    except:
                        print('listing not present in the lbhw table')
                        l1,b1,h1,w1=[10,],[10,],[10,],[0.25,]
                l = str(float(max(l1)) * 1.05)[:5]
                b = str(float(max(b1)) * 1.05)[:5]
                h = str(float(max(h1)) * 1.05)[:5]
                w = str(float(max(w1)) * 1.05)[:6]
                print(l1,l,b1,b,h1,h,w1,w)
                def lbhw(l,b,h,w,listingid):
                    driver.find_element_by_xpath('//input[@class="length-input"]').clear()
                    driver.find_element_by_xpath('//input[@class="length-input"]').send_keys(l)
                    time.sleep(1)
                    driver.find_element_by_xpath('//input[@class="breadth-input"]').clear()
                    driver.find_element_by_xpath('//input[@class="breadth-input"]').send_keys(b)
                    time.sleep(1)
                    driver.find_element_by_xpath('//input[@class="height-input"]').clear()
                    driver.find_element_by_xpath('//input[@class="height-input"]').send_keys(h)
                    time.sleep(1)
                    driver.find_element_by_xpath('//input[@class="weight-input"]').clear()
                    driver.find_element_by_xpath('//input[@class="weight-input"]').send_keys(w)
                    time.sleep(1)
                    enter_list=driver.find_element_by_xpath('//input[@class="productId-input"]')
                    time.sleep(2)
                    driver.execute_script("arguments[0].scrollIntoView();", enter_list)
                    time.sleep(2)
                    driver.find_element_by_xpath('//input[@class="productId-input"]').send_keys(listingid,Keys.ENTER)
                    time.sleep(2)
                    #driver.find_element_by_xpath('//input[@class="productId-input"]').send_keys(listingid2,Keys.ENTER)
                    time.sleep(2)
                    countinue1=driver.find_element_by_xpath('(//button[text()="Continue"])[2]')
                    driver.execute_script("arguments[0].scrollIntoView();", countinue1)
                    countinue1.click()

                lbhw(l,b,h,w,listingid2)
                try:
                    l1,b1,h1,w1=[10,],[10,],[10,],[0.25,]
                    wrong_lbhw = driver.find_element_by_xpath('//div[@class="toast-message-container"]').text
                    if wrong_lbhw=='Shipping package size(LBHW) cannot be less than the packaging dimensions mentioned in My Listings tab at the time of order placement':
                        lbhw(l, b, h, w, listingid2)
                except Exception as e:
                    print('wrong_lbhw error massage')


            except Exception as e:
                print('multiple orders error massage1:',e)


            time.sleep(3)
            alrert_o=driver.switch_to.alert
            mas=alrert_o.dismiss()
            #pyautogui.press('esc')
            # pyautogui.press('enter')
            time.sleep(2)
            file1 = glob.glob(r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files\*")
            file2=glob.glob(r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\croped_file\*")
            def a_remove1(files):


                for f in files:
                    os.remove(f)
                print('removed all invoice pdf files from download folder')
            a_remove1(file1)
            a_remove1(file2)

            try:
                driver.find_element_by_xpath('//button[@type="button"]').click()
            except:
                pass
            time.sleep(2)
            print('donload the invoice')
            driver.find_element_by_xpath('//a[.="Reprint Label"]').click()
            time.sleep(5)
            # #pyautogui.keyUp('esc')
            #pdb.set_trace()

            # for k in multilisting_id_list:
            #
            #     print(k)
            #time.sleep(2)
            file1='C:\\Users\\Administrator\\PycharmProjects\\pythonProject\\flipkart_processing_code\\download_picklist_files\\'
            p=os.listdir(file1)
            print('p=',p)
            file1+=str(p[0])

             # pip install tika 519330743273 519330918214
            raw = parser.from_file(file1)
            data=raw['content']
            data1=str(data)
            #print(str(data))
            awb=data1.split('Courier AWB No:')
            #print(d,'lenth of d',len(d))
            awb1=awb[1].split()[0]
            print('awb1 from invoice :',awb1)
            #print(awb1=='519330918214')
            order_id=data1.split('Order ID:')
            order_id_invice=order_id[1].split()[0]
            print('order id from invoice:',order_id_invice)
            #print(order_id_invice=='OD222121632656272000')
            #from projects.flipkart_processing_code.pdfs import pdf_crop
            def crop_pdf():
                import os

                from PyPDF2 import PdfFileReader, PdfFileWriter
                file1 = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files'
                p = os.listdir(file1)
                file1 += "\\" + str(p[0])

                original_file_path = file1
                cropped_file_path = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\croped_file\cropped.pdf'
                reader = PdfFileReader(original_file_path, 'r')
                page = reader.getPage(0)
                writer = PdfFileWriter()
                page.cropBox.setLowerLeft((174, 470))
                page.cropBox.setUpperLeft((174, 813))
                page.cropBox.setUpperRight((421, 813))
                page.cropBox.setLowerRight((421, 470))
                writer.addPage(page)
                outstream = open(cropped_file_path, 'wb')
                writer.write(outstream)
                outstream.close()

                print('original_file_path:', original_file_path)
                print('cropped_file_path:',cropped_file_path)
                print('pdf crop done')


            crop_pdf()

            db_name='testers'
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            statement = "SELECT order_id,order_item_id from api_neworders where order_id='"+order_id_invice+"'"
            print(statement)
            print('get the order_item_id from orders db ')
            cur.execute(statement)
            conn.commit()
            data1 = cur.fetchall()
            print(data1)
            order_id=data1[0][0]
            order_item_id=data1[0][1]
            #time.sleep(3)
            # pdb.set_trace()
            # driver.find_element_by_xpath('//input[@class="trackingId-input"]').send_keys(awb1,Keys.ENTER)
            print('start save the invioce file to drop box')

            #time.sleep(2)
            drop_box(order_id_invice,order_item_id)
            print('successfully saved the invioce file to drop box')
            #add to drop box the invice
            # pdb.set_trace()
            name = 'postgres'
            rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
            db_name = 'products'
            password = 'buymore3'
            conn1 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur1 = conn1.cursor()

            statement = "SELECT flipkart_portal_unique_id from flipkart_flipkartproducts where flipkart_listing_id='" + listingId + "'"
            print(statement)
            cur1.execute(statement)
            # conn1.commit()
            data = cur1.fetchall()
            print('data flipkart_flipkartproducts:',data)
            #fsn_mongo = data[0][0]
            print(len(data))

            rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
            db_name = 'products'
            password = 'buymore3'
            db_name = 'testers'
            conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur2 = conn2.cursor()
            # statement = "SELECT order_id from api_neworders where pick_list_id='" + picklistId + "' and bin_id='"+binId+"'"# and fsn='"+fsn+"'"
            statement = "SELECT new_order_id,pick_list_id,bin_id,warehouse_id,fsn from api_neworders where order_id='" + order_id_invice + "' and order_item_id='" + order_item_id + "'"  # pick_list_id='" + picklistId + "' or bin_id='" + binId + "' and fsn='" + fsn + "'"
            print(statement)
            cur2.execute(statement)
            conn2.commit()
            data2 = cur2.fetchall()
            dd_length3 = len(data2)
            print(len(data2), 'order id', data2)
            for j in data2:
                new_order_id1 = j[0]
                picklistId1 = j[1]
                bin_id1 = j[2]
                warehouse_id = j[3]
                fsn = j[4]
                print('get the data from the testers db picklistId1, picklistId_mongo, bin_id1, warehouse_id')
                print(picklistId1, picklistId_mongo, bin_id1, warehouse_id)
                # pdb.set_trace()
                if picklistId1 == ' ' and bin_id1 == ' ':
                    print('1st condition if picklistId1 == ' ' and bin_id1 == ' ': ')
                    # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                    # cur2 = conn2.cursor()
                    statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "' ,bin_id='" + binId_mongo + "',tracking_id='" +awb1+"'  where new_order_id=" + str(new_order_id1)
                    print(statement)
                    cur2.execute(statement)
                    print('updated the tracking id,bin id and picklist')
                    conn2.commit()
                elif picklistId1 == picklistId_mongo:
                    print('2nd condition picklistId1 == picklistId_mongo')
                    print(picklistId1)
                    #print('we can update the awb')
                    # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                    # cur2 = conn2.cursor()
                    statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "',bin_id='" + binId_mongo + "',tracking_id='" +awb1+"'  where new_order_id=" + str(new_order_id1)
                    cur2.execute(statement)
                    print('updated the tracking id,bin id and picklist')
                    conn2.commit()
                elif picklistId1 != picklistId_mongo:
                    print('3rd codition picklistId1 != picklistId_mongo')

                    # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                    # cur2 = conn2.cursor()
                    statement = "SELECT new_order_id,pick_list_id,bin_id from api_neworders where pick_list_id='" + picklistId_mongo + "' and warehouse_id=" +str( warehouse_id )+ " and fsn='" + fsn + "' and order_id!='"+order_id_invice+"' and order_item_id!='"+order_item_id+"'"
                    print(statement)
                    cur2.execute(statement)
                    conn2.commit()
                    data2 = cur2.fetchall()
                    print(len(data2), 'order id', data2)
                    try:
                        new_order_id2 = data2[0][0]

                        pick_list_id2 = data2[0][1]
                        bin_id2 = data2[0][2]
                    except Exception as e:
                        print('condtion 3 error ',e)
                        statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "' ,bin_id='" + binId_mongo + "',tracking_id='" + awb1 + "'  where new_order_id=" + str(
                            new_order_id1)
                        print(statement)
                        cur2.execute(statement)
                        print('updated the tracking id,bin id and picklist')
                        conn2.commit()

                    # bin_id_main=j[1]
                    # swaping
                    # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                    # cur2 = conn2.cursor()
                    print('start swaping ')
                    statement = "UPDATE api_neworders SET pick_list_id = '" + pick_list_id2 + "',bin_id='" + bin_id2 + "', tracking_id='"+awb1+"' where new_order_id=" + str(new_order_id1)
                    print(statement)
                    cur2.execute(statement)
                    conn2.commit()

                    # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                    # cur2 = conn2.cursor()
                    statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId1 + "',bin_id='" + bin_id1 + "'  where new_order_id="+str(new_order_id2)
                    print(statement)
                    cur2.execute(statement)
                    print('done the swaping and update the tracking id')
                    conn2.commit()
                    #Fpdb.set_trace()
                conn2.commit()
            #time.sleep(2)
            driver.find_element_by_xpath('//input[@class="trackingId-input"]').send_keys(awb1, Keys.ENTER)
            time.sleep(2)
            driver.refresh()
            time.sleep(1)
        except Exception as e:
            print('final error massage for :',listingId,e)
            with open('failed_records4.csv', "a", newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([listingId, picklistId_mongo, warehouseId_mongo,binId_mongo,e])
                driver.refresh()
                time.sleep(1)
                continue
        # except Exception as e:
        #     print('total error:',e)

#update_awb(order_id,awb1)


