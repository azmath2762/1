import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import shutil
import csv
import os
import time
import glob
from tika import parser
import dropbox
from selenium.webdriver.support.select import Select
import psycopg2
import pyautogui
from selenium.webdriver.support import expected_conditions as EC
#
new_order_id_list=[-1]
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import psycopg2
import sys

def smart_api_for_moving_orders(picklist):
    import dropbox
    import requests
    import json
    url = 'https://40jww40180.execute-api.ap-south-1.amazonaws.com/s1/movesmartorderstodbfunction'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {"picklist":  ""+picklist+""}
    # convert dict to json string by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    #assert resp.status_code == 200
    resp_body = resp.json()

    print('resp_body', resp_body)
    print('responce:', resp.text)
    # print(len(resp.text))
    for k in resp_body:
        print(k)
#smart_api_for_moving_orders('P231021-9C4B5380C8D8')

def test_post_headers_body_json1(picklist):
    import dropbox
    import requests
    import json
    url = 'https://ruml0ao7qj.execute-api.ap-south-1.amazonaws.com/s1/picklistfunction'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {"picklist_name": ""+picklist+".csv","user_id": 1}
    # convert dict to json string by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    #assert resp.status_code == 200
    resp_body = resp.json()

    print('resp_body', resp_body)
    print('responce:', resp.text)
    # print(len(resp.text))
    for k in resp_body:
        print(k)

#test_post_headers_body_json1('P080921-86A4442AFB53')
def cheking_mongodata(picklist_id):
    from pymongo import MongoClient
    client = MongoClient('mongodb+srv://Counfreedise:buymore123@cluster0-tq9zt.mongodb.net/wms?retryWrites=true&w=majority',tlsAllowInvalidCertificates=True)
    db = client.wms
    #binreco = db.api_binreco.find({'operation':'Order Picklist','picklistId':{'$in':['P250621-09ABAF1EDF5D']}})P290621-96A3194D9C60
    binreco = db.api_binreco.find({'operation':'Order Picklist','picklistId':picklist_id})
    c=0#P031021-881AD5D1555E
    mangao_data=[]
    for item in binreco:
        picklistId=item['picklistId']
        print(picklistId)
        mangao_data.append(picklistId)
    print('len_of mango db',len(mangao_data))
    if len(mangao_data)>0:
        print('run code')
    else:
        test_post_headers_body_json1(picklist_id)
        binreco = db.api_binreco.find({'operation': 'Order Picklist', 'picklistId': picklist_id})
        c = 0  # P031021-881AD5D1555E
        mangao_data = []
        for item in binreco:
            picklistId = item['picklistId']
            print(picklistId)
            mangao_data.append(picklistId)
        print(len(mangao_data))
        if len(mangao_data) > 0:
            print('run code')
        else:
            sys.exit()
# cheking_mongodata(input("enter the picklist id:"))

def getting_order_item_id(order_id_invice):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    name = 'postgres'
    password = 'buymore3'
    db_name = 'testers'
    conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    cur = conn.cursor()
    statement = "SELECT order_id,order_item_id from api_neworders where order_id='" + order_id_invice + "'"
    print(statement)
    print('get the order_item_id from orders db ')
    cur.execute(statement)
    conn.commit()
    data1 = cur.fetchall()
    print(data1)
    order_id = data1[0][0]
    order_item_id = data1[0][1]
    cur.close()
    conn.close()
    return data1


def main_updating(order_id_invice, picklistId_mongo, binId_mongo, awb1):
    # global pick_list_id2, bin_id2, new_order_id2
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    name = 'postgres'
    password = 'buymore3'
    db_name = 'testers'
    data1 = getting_order_item_id(order_id_invice)
    order_id = data1[0][0]
    order_item_id = data1[0][1]
    conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    cur2 = conn2.cursor()
    # statement = "SELECT order_id from api_neworders where pick_list_id='" + picklistId + "' and bin_id='"+binId+"'"# and fsn='"+fsn+"'"
    statement = "SELECT new_order_id,pick_list_id,bin_id,warehouse_id,fsn from api_neworders where order_id='" + order_id_invice + "' and order_item_id='" + order_item_id + "'"  # pick_list_id='" + picklistId + "' or bin_id='" + binId + "' and fsn='" + fsn + "'"
    print(statement)
    cur2.execute(statement)
    conn2.commit()
    data2 = cur2.fetchall()
    cur2.close()
    conn2.close()
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
            conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur2 = conn2.cursor()
            statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "' ,bin_id='" + binId_mongo + "',tracking_id='" + awb1 + "'  where new_order_id=" + str(
                new_order_id1)
            print(statement)
            cur2.execute(statement)
            print('updated the tracking id,bin id and picklist')
            conn2.commit()
            new_order_id_list.append(new_order_id1)
            cur2.close()
            conn2.close()
        elif picklistId1 == picklistId_mongo:
            print('2nd condition picklistId1 == picklistId_mongo')
            print(picklistId1)
            # print('we can update the awb')
            conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur2 = conn2.cursor()
            statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "',bin_id='" + binId_mongo + "',tracking_id='" + awb1 + "'  where new_order_id=" + str(
                new_order_id1)
            cur2.execute(statement)
            print('updated the tracking id,bin id and picklist')
            conn2.commit()
            new_order_id_list.append(new_order_id1)
        elif picklistId1 != picklistId_mongo:
            print('3rd codition picklistId1 != picklistId_mongo')

            conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur2 = conn2.cursor()
            statement = "SELECT new_order_id,pick_list_id,bin_id from api_neworders where pick_list_id='" + picklistId_mongo + "' and warehouse_id=" + str(
                warehouse_id) + " and fsn='" + fsn + "' and order_id!='" + order_id_invice + "' and order_item_id!='" + order_item_id + "' and new_order_id not in (" + str(
                new_order_id_list)[1:-1] + ")"
            print(statement)
            cur2.execute(statement)
            conn2.commit()
            data2 = cur2.fetchall()
            cur2.close()
            conn2.close()
            print(len(data2), 'order id', data2)
            try:
                new_order_id2 = data2[0][0]

                pick_list_id2 = data2[0][1]
                bin_id2 = data2[0][2]
            except Exception as e:
                print('condtion 3 error ', e)
                conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                cur2 = conn2.cursor()
                statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId_mongo + "' ,bin_id='" + binId_mongo + "',tracking_id='" + awb1 + "'  where new_order_id=" + str(
                    new_order_id1)
                print(statement)
                cur2.execute(statement)
                print('updated the tracking id,bin id and picklist')
                conn2.commit()
                new_order_id_list.append(new_order_id1)
                cur2.close()
                conn2.close()
            # bin_id_main=j[1]
            # swaping
            # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            # cur2 = conn2.cursor()
            if len(data2) > 0:
                new_order_id2 = data2[0][0]

                pick_list_id2 = data2[0][1]
                bin_id2 = data2[0][2]
                print('start swaping ')
                conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                cur2 = conn2.cursor()
                statement = "UPDATE api_neworders SET pick_list_id = '" + pick_list_id2 + "',bin_id='" + bin_id2 + "', tracking_id='" + awb1 + "' where new_order_id=" + str(
                    new_order_id1)
                print(statement)
                cur2.execute(statement)
                conn2.commit()

                # conn2 = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
                # cur2 = conn2.cursor()
                statement = "UPDATE api_neworders SET pick_list_id = '" + picklistId1 + "',bin_id='" + bin_id1 + "'  where new_order_id=" + str(
                    new_order_id2)
                print(statement)
                cur2.execute(statement)
                print('done the swaping and update the tracking id')
                conn2.commit()
                new_order_id_list.append(new_order_id1)
                cur2.close()
                conn2.close()
                # Fpdb.set_trace()


def get_table_id_list(listing_id,count,picklist_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'
    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()

    #statement = "SELECT id FROM public.original_picklist where order_picklist_fnsku in ("+str(fnsku)[1:-1]+")"
    #statement = "SELECT id FROM public.original_picklist where order_picklist_fnsku='"+fnsku+"'"
    statement = "SELECT id FROM public.original_picklist where order_picklist_listing_id='" + listing_id + "' and picklist_id='"+picklist_id+"' and sequence_number is null and invoice is null limit " + str(count) + ""
    print('statement',statement)
    picklist_cur.execute(statement)
    listing_id = picklist_cur.fetchall()
    print('fnsku_id',listing_id)
    picklist_cur.close()
    picklist_conn.close()
    return listing_id

def updating_in_error(id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "update original_picklist set is_processing=true,status=true where status=false and id="+str(id)+""
    print(statement)
    picklist_cur.execute(statement)
    picklist_conn.commit()
    picklist_cur.close()
    picklist_conn.close()
def cancel_update(picklist_id,id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "update original_picklist set status=true,is_canceled=true,process_time=now() where picklist_id='" + picklist_id + "' and id=" + str(id) + ""
    print('statement', statement)
    picklist_cur.execute(statement)
    picklist_conn.commit()
    picklist_cur.close()
    picklist_conn.close()
def update_details_to_source_table_single(sequence_number,awb,order_id,invoice,status,is_canceled,picklist_id,id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "update original_picklist set sequence_number="+str(sequence_number)+",awb='"+awb+"',order_id='"+order_id+"',invoice='"+invoice+"',status="+status+",is_canceled="+is_canceled+",process_time=now() where picklist_id='"+picklist_id+"' and id="+str(id)+""
    print('statement',statement)
    picklist_cur.execute(statement)
    picklist_conn.commit()
    picklist_cur.close()
    picklist_conn.close()

def get_details_from_source_table(picklist_idd):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "SELECT picklist_id,order_picklist_listing_id,warehouse_id,id FROM public.original_picklist where status!=true and is_processing!=true and warehouse_id=7 and portal_id=2 and picklist_id='"+picklist_idd+"'"
    picklist_cur.execute(statement)
    data = picklist_cur.fetchone()
    try:
        print(data[0])
    except:
        print('no picklists are active')
    statement = "update public.original_picklist set is_processing=true where picklist_id='" + data[0] + "'"
    picklist_cur.execute(statement)
    picklist_conn.commit()
    statement = "SELECT picklist_id,order_picklist_listing_id,warehouse_id,id FROM public.original_picklist where picklist_id='" +data[0] + "' and status!=true"
    picklist_cur.execute(statement)
    picklist_data = picklist_cur.fetchall()
    statement = "SELECT max(sequence_number) FROM public.original_picklist where picklist_id='" + data[0] + "'"
    picklist_cur.execute(statement)
    max_value = picklist_cur.fetchall()
    max_value = max_value[0][0]
    print('max_value:', max_value, type(max_value))
    if max_value == None:
        max_value = 0
    else:
        max_value = max_value
    print('final maxvalue', max_value)
    picklist_cur.close()
    picklist_conn.close()
    return picklist_data, max_value

def finding_sequence_number(picklist_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "SELECT max(sequence_number) FROM public.original_picklist where picklist_id='" + picklist_id + "'"
    picklist_cur.execute(statement)
    max_value = picklist_cur.fetchall()
    max_value = max_value[0][0]
    print('max_value:', max_value, type(max_value))
    if max_value == None:
        max_value = 0
    else:
        max_value = max_value
    print('final maxvalue', max_value)
    picklist_cur.close()
    picklist_conn.close()
    return max_value


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
# username='counfreedise@gmail.com'
# password1='cfdrsl@2012'
username='madanmohan.r@sellerbuymore.com'
password1='Buymore@123'
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
        time.sleep(10)
        driver.get('https://seller.flipkart.com/index.html#dashboard/settings/settingsDetails')
        time.sleep(3)
        driver.find_element_by_xpath('//div[@data-fftype="FBF_LITE_PRINTERS"]').click()
        time.sleep(2)
        drop = driver.find_element_by_xpath('//select[@id="printing"]')
        sel = Select(drop)
        sel.select_by_index(0)
        # sel.select_by_visible_text('Yes, enable thermal printing')
        time.sleep(1)
        driver.find_element_by_xpath('//input[@name="submit"]').click()

        driver.get('https://seller.flipkart.com/index.html#dashboard/fbflite-ff/LOC357548a12e4a4842a1c4177a08648403/nav-ff/processing')
        return True
    except Exception as e:
        print('start smart issue:', str(e))
def drop_box(picklist_id,sequence_number):
    access_token = '4joGxl-yofIAAAAAAAAAAW0Wa_qjsmOhQ6NYfWtkG0mNefNaTsIx8hD8BVgkavph'
    dbx = dropbox.Dropbox(oauth2_access_token=access_token, max_retries_on_error=2)
    file1 = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\croped_file\\'
    p = os.listdir(file1)
    #
    file1 += str(p[0])
    file_from = file1
    file_to = '/buymore2/flex_and_smart_processing_invoices/' + picklist_id + '#' + str(sequence_number) + '.pdf'
    print('file from : ', file_from)
    with open(file_from, 'rb') as f:
        data = dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
    print('written to ', file_to)

def to_take_data_for_processing(picklist_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "SELECT picklist_id,order_picklist_listing_id,warehouse_id,id,source_bin FROM public.original_picklist where picklist_id='" +picklist_id+ "' and status!=true"
    picklist_cur.execute(statement)
    picklist_data = picklist_cur.fetchone()
    picklist_cur.close()
    picklist_conn.close()
    return picklist_data
def to_take_data_for_processing___(picklist_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "SELECT picklist_id,order_picklist_listing_id,warehouse_id,id,source_bin FROM public.original_picklist where picklist_id='" +picklist_id+ "' and status=false"
    print(statement)
    picklist_cur.execute(statement)
    picklist_data = picklist_cur.fetchall()
    picklist_cur.close()
    picklist_conn.close()
    return picklist_data
#d=to_take_data_for_processing('P251021-846A49A0725C')
#print(len(d))

def geting_lbhw():
    main_lbhw={}
    file = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\flipkartlbhw\finalfklbh_new.csv'
    with open(file, "r", newline='') as f1:
        lbhw = csv.DictReader(f1)
        lbhw = list(lbhw)
        for rr in lbhw:
            listingId = rr['Listing ID']
            Length = float(rr['Length'])
            Breadth = float(rr['Breadth'])
            Height = float(rr['height'])
            Weight = float(rr['Weight'])
            main_lbhw[listingId]=[Length,Breadth,Height,Weight]
    return main_lbhw
def update_status_in_for_loop(picklist_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'

    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement = "update original_picklist set status=false where picklist_id='"+picklist_id+"' and sequence_number is null and awb is null and is_canceled is null "
    picklist_cur.execute(statement)
    picklist_conn.commit()
    picklist_cur.close()
    picklist_conn.close()
def final_checkup(picklist_Id,id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'warehouse'
    name = 'postgres'
    password = 'buymore3'
    picklist_conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    picklist_cur = picklist_conn.cursor()
    statement="update public.original_picklist set is_processing=false,status=false where portal_id="+str(id)+" and invoice is null and is_canceled is null and picklist_id='"+picklist_Id+"'"
    print('statement', statement)
    picklist_cur.execute(statement)
    picklist_conn.commit()
    picklist_cur.close()
    picklist_conn.close()
# final_checkup(input('picklist_id:'),input('portal_id:'))
def flipkart_processing_main_code():

    username = 'madanmohan.r@sellerbuymore.com'
    password1 = 'Buymore@123'
    global list1
    ppicklist_id=input('enter the picklist_id:')
    cheking_mongodata(ppicklist_id)
    final_checkup(ppicklist_id,2)
    picklist_data = get_details_from_source_table(ppicklist_id)
    startSmart(username, password1)
    # print('picklist_data',picklist_data)
    pick_data = picklist_data[0]
    max_value = picklist_data[1]
    print('max_value11', max_value)
    print(pick_data)
    # sequence_number = 0
    picklistId_for_api = pick_data[0][0]
    print('picklistId_for_api',picklistId_for_api)
    # cheking_mongodata(picklistId_for_api)
    for loop in range(5):
        loop_len=to_take_data_for_processing___(picklistId_for_api)
        print('loop_len',loop_len)
        print('loop lenth:',len(loop_len))
        #pickk_list=pick_data[0][0]
        #pick_data1 = to_take_data_for_processing(pickk_list)
        update_status_in_for_loop(picklistId_for_api)
        for i in range(0, len(loop_len)):
            try:
                picklistId = pick_data[i][0]
                max_value = finding_sequence_number(picklistId)
                pick_data1 = to_take_data_for_processing(picklistId)
                picklistId_mongo = pick_data1[0]
                listingId = pick_data1[1]
                warehouseId_mongo = pick_data1[2]
                binId_mongo=pick_data1[4]
                print(picklistId_mongo,listingId)
                print(warehouseId_mongo,warehouseId_mongo,warehouseId_mongo,binId_mongo)
                picklist_id_id = pick_data1[3]
                sequnce_num = max_value + 1
                print('sequnce_num:', sequnce_num)
                file111 = glob.glob(r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files\*")
                file222 = glob.glob(r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\croped_file\*")

                def a_remove1(files):

                    for f in files:
                        os.remove(f)
                    print('removed all invoice pdf files from download folder')

                a_remove1(file111)
                a_remove1(file222)

                try:
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div/div[2]/div/div/div[2]/div/div/a/span').click()
                    # time.sleep(1)
                    print(str(warehouseId_mongo) +'=='+'4')
                    if str(warehouseId_mongo) == '4':
                        driver.find_element_by_xpath('//li[.="BANGALORE : 560026"]').click()
                    elif str(warehouseId_mongo) == '10':
                        driver.find_element_by_xpath('//li[.="New Delhi"]').click()
                    elif str(warehouseId_mongo) == '7':
                        driver.find_element_by_xpath('//li[.="HOWRAH : 711302"]').click()
                    elif str(warehouseId_mongo) == '3':
                        driver.find_element_by_xpath('//li[.="BHIWANDI"]').click()
                except Exception as e:
                    print('location error:', e)
                print('select the location from front end')

                time.sleep(1)
                try:
                    driver.find_element_by_xpath('//input[@class="picklistId-input"]').send_keys(picklistId_mongo,
                                                                                                 Keys.ENTER)  # P280621-DCF6D3EA49CD
                    print('enter the picklist id to front end')
                except:
                    print('pass')
                try:
                    driver.find_element_by_xpath('//div[text()="Unable to process picklist. Please check the Picklist ID and try again."]')
                    break
                except:
                    pass
                # time.sleep(2)

                driver.find_element_by_xpath('//input[@class="productId-input"]').send_keys(listingId,
                                                                                            Keys.ENTER)  # LSTFKTFYBHCANHGKSBPBMRW5A
                time.sleep(1)  # //div[@class="toast-message-container"]
                print('enter the listing id id to front end')
                try:
                    if driver.find_element_by_xpath('//div[text()="The scanned shipment item has already been processed."]').is_displayed():
                        driver.refresh()
                        continue
                    else:
                        print('not displayed means not scaned before')
                except:
                    print('not displayed means not scaned before')

                try:
                #if True:
                    cancel = driver.find_element_by_xpath('//span[text()="Order is cancelled"]').text
                    print('cancel',cancel)
                    time.sleep(2)
                    order_id_cancel = driver.find_element_by_xpath('//div[@class="order-id clearfix"]').text
                    print('order_id_cancel',order_id_cancel)
                    time.sleep(1)
                    item_id_cancel = driver.find_element_by_xpath('//div[@class="order-item-id clearfix"]').text
                    print('item_id_cancel',item_id_cancel)
                    time.sleep(2)
                    done=driver.find_element_by_xpath('//span[text()="Done"]').text
                    print('done',done)
                    time.sleep(2)
                    cancel_update(picklistId_mongo,picklist_id_id)

                    try:
                        webdriver.ActionChains(driver).move_to_element(done).click(done).perform()
                    except:
                        print('bhdbvdh')
                        driver.find_element_by_xpath("//section[@class='modalbox-body']/..//span[text()='Done']").click()
                    # driver.find_element_by_xpath('//span[text()="Done"]').click()
                    cancel_update(picklistId_mongo, picklist_id_id)
                    driver.refresh()
                    continue
                except Exception as e:
                    print('cancel error massage:', e)

                try:
                    one_more = driver.find_element_by_xpath('//div[@class="multi-product-warning-container"]').text
                    time.sleep(2)
                    list1 = []
                    l1 = []
                    b1 = []
                    h1 = []
                    w1 = []
                    for i in range(1, 20):
                        try:
                            listing2 = driver.find_element_by_xpath('(//div[@class="product-listing-id clearfix"])[' + str(i) + ']')
                            driver.execute_script("arguments[0].scrollIntoView();", listing2)
                            listingid2 = listing2.text
                            listingid2 = listing2.text
                            listingid2 = listingid2.split()[2]
                            list1.append(listingid2)
                        except Exception as e:
                            print('listting error massge', e)
                            break
                    print('list1:', list1)
                    main_lbhw=geting_lbhw()
                    for p in range(len(list1)):
                        try:
                            l1.append(main_lbhw[list1[p]][0])
                            b1.append(main_lbhw[list1[p]][1])
                            h1.append(main_lbhw[list1[p]][2])
                            w1.append(main_lbhw[list1[p]][3])
                            print('listing labhw table', l1, l1, b1, h1, w1)
                        except:
                            print('listing not present in the lbhw table')
                            l1, b1, h1, w1 = [10, ], [10, ], [10, ], [0.25, ]
                    l = str(float(max(l1)) * 1.05)[:5]
                    b = str(float(max(b1)) * 1.05)[:5]
                    h = str(float(max(h1)) * 1.05)[:5]
                    w = str(float(max(w1)) * 1.05)[:6]
                    print(l1, l, b1, b, h1, h, w1, w)

                    def lbhw(l, b, h, w):
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

                    lbhw(l, b, h, w)
                    enter_list = driver.find_element_by_xpath('//input[@class="productId-input"]')
                    time.sleep(2)
                    driver.execute_script("arguments[0].scrollIntoView();", enter_list)
                    time.sleep(2)
                    for list_id in list1:
                        driver.find_element_by_xpath('//input[@class="productId-input"]').send_keys(list_id,
                                                                                                    Keys.ENTER)
                        time.sleep(1)
                    time.sleep(2)
                    countinue1 = driver.find_element_by_xpath('(//button[text()="Continue"])[2]')
                    driver.execute_script("arguments[0].scrollIntoView();", countinue1)
                    countinue1.click()
                    try:
                        driver.find_element_by_xpath('//button[contains(text()," ×")] ').click()
                    except:
                        pass

                    try:
                        # l1,b1,h1,w1=[10,],[10,],[10,],[0.25,]
                        l = str(float(max(l1)) * 2.5)[:5]
                        b = str(float(max(b1)) * 2.5)[:5]
                        h = str(float(max(h1)) * 2.5)[:5]
                        w = str(float(max(w1)) * 2.5)[:6]
                        wrong_lbhw = driver.find_element_by_xpath('//div[@class="toast-message-container"]').text
                        print('wrong_lbhw:', wrong_lbhw)
                        lbhw(l, b, h, w)
                        countinue1 = driver.find_element_by_xpath('(//button[text()="Continue"])[2]')
                        driver.execute_script("arguments[0].scrollIntoView();", countinue1)
                        countinue1.click()
                    except Exception as e:
                        print('wrong_lbhw error massage')
                        try:
                            # l1,b1,h1,w1=[10,],[10,],[10,],[0.25,]
                            l = str(float(max(l1)) * 3.5)[:5]
                            b = str(float(max(b1)) * 3.5)[:5]
                            h = str(float(max(h1)) * 3.5)[:5]
                            w = str(float(max(w1)) * 3.5)[:6]
                            wrong_lbhw = driver.find_element_by_xpath('//div[@class="toast-message-container"]').text
                            print('wrong_lbhw:', wrong_lbhw)
                            lbhw(l, b, h, w)
                            countinue1 = driver.find_element_by_xpath('(//button[text()="Continue"])[2]')
                            driver.execute_script("arguments[0].scrollIntoView();", countinue1)
                            countinue1.click()
                        except:
                            # l1,b1,h1,w1=[10,],[10,],[10,],[0.25,]
                            l = str(float(max(l1)) * 4.5)[:5]
                            b = str(float(max(b1)) * 4.5)[:5]
                            h = str(float(max(h1)) * 4.5)[:5]
                            w = str(float(max(w1)) * 4.5)[:6]
                            wrong_lbhw = driver.find_element_by_xpath('//div[@class="toast-message-container"]').text
                            print('wrong_lbhw:', wrong_lbhw)
                            lbhw(l, b, h, w)
                            countinue1 = driver.find_element_by_xpath('(//button[text()="Continue"])[2]')
                            driver.execute_script("arguments[0].scrollIntoView();", countinue1)
                            countinue1.click()

                except Exception as e:
                    print('multiple orders error massage1:', e)
                try:
                    driver.find_element_by_xpath('//button[@type="button"]').click()
                except:
                    pass
                time.sleep(1)
                print('donload the invoice')
                file1 = 'C:\\Users\\Administrator\\PycharmProjects\\pythonProject\\flipkart_processing_code\\download_picklist_files\\'
                p = os.listdir(file1)
                print('p=', p)
                file1 += str(p[1])
                raw = parser.from_file(file1)
                data = raw['content']
                data1 = str(data)
                # print(str(data))
                awb = data1.split('Courier AWB No:')
                # print(d,'lenth of d',len(d))
                awb1 = awb[1].split()[0]
                print('awb1 from invoice :', awb1)
                # print(awb1=='519330918214')
                order_id = data1.split('Order ID:')
                order_id_invice = order_id[1].split()[0]
                print('order id from invoice:', order_id_invice)

                # print(order_id_invice=='OD222121632656272000')
                # from projects.flipkart_processing_code.pdfs import pdf_crop
                def crop_pdf():
                    import os

                    from PyPDF2 import PdfFileReader, PdfFileWriter
                    file1 = r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\download_picklist_files'
                    p = os.listdir(file1)
                    # if len(p) == 4:
                    #     file1 +="\\" + str(p[2])
                    # elif len(p) == 2:
                    #     file1 +="\\" + str(p[1])
                    file1 += "\\" + str(p[1])

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
                    print('cropped_file_path:', cropped_file_path)
                    print('pdf crop done')

                crop_pdf()
                drop_box(picklistId_mongo, sequnce_num)
                try:
                    main_updating(order_id_invice, picklistId_mongo, binId_mongo, awb1)
                except Exception as e:
                    print('missing order id error:',e)
                invoice_path = r'/buymore2/flex_and_smart_processing_invoices/' + picklistId_mongo + '#' + str(sequnce_num) + '.pdf'
                res = {}
                for i in list1:
                    count = list1.count(i)
                    # print(i,count)
                    res[i] = count
                print(res)

                ids = {}
                for sku, count in res.items():
                    # print(sku)
                    id = get_table_id_list(sku, count, picklistId_mongo)
                    print('id:', id)
                    print(len(id))
                    pick_id_list = []
                    c = 0
                    for a in range(len(id)):
                        c = c + 1
                        # print(id[a][0])
                        pick_id = id[a][0]
                        pick_id_list.append(pick_id)
                    print(pick_id_list)
                    ids[sku] = pick_id_list
                print(ids)
                for k, v in ids.items():
                    # sequence_number = 0
                    for id_id in range(len(v)):
                        print(v[id_id])
                        final_id = v[id_id]
                        update_details_to_source_table_single(sequence_number=sequnce_num, awb=awb1, order_id=order_id_invice,
                                                              invoice=invoice_path, status='true', is_canceled='false',
                                                              picklist_id=picklistId_mongo, id=final_id)
                # drop_box(picklistId_mongo, sequnce_num)
                handles = driver.window_handles
                ref_window=driver.current_window_handle
                size = len(handles)
                for x in range(size):
                    if handles[x] != driver.window_handles[0]:
                        driver.switch_to.window(handles[x])
                        print(driver.title)
                        driver.close()
                try:
                    driver.switch_to.window(ref_window)
                except:
                    print('switched main window')
                    driver.switch_to.window(driver.window_handles[0])

                driver.find_element_by_xpath('//input[@class="trackingId-input"]').send_keys(awb1, Keys.ENTER)
                time.sleep(2)
                driver.refresh()

            except Exception as e:
                updating_in_error(picklist_id_id)
                handles = driver.window_handles
                ref_window = driver.current_window_handle
                size = len(handles)
                for x in range(size):
                    if handles[x] != driver.window_handles[0]:
                        driver.switch_to.window(handles[x])
                        print(driver.title)
                        driver.close()
                try:
                    driver.switch_to.window(ref_window)
                except:
                    print('switched main window')
                    driver.switch_to.window(driver.window_handles[0])
                print('final error:',e)
                driver.refresh()
    #from flipkart_processing_code.new_flipkart_pk_processing_code.smart_api import smart_api
    smart_api_for_moving_orders(picklistId_for_api)
    driver.close()
flipkart_processing_main_code()