import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)


client = gspread.authorize(creds)

#sheet = client.open("amazon1").vendor_removal_Bangalore.pysheet1  # Open the spreadhseet
sheet2=client.open('Smart Picklist').worksheet('Bangalore')
#data = sheet.get_all_values()  # Get a list of all records
data2 = list(sheet2.get_all_values())  # Get a list of all records
print(data2)

for i in range(1,len(data2)):
    date=str(data2[i][0])
    Portal=str(data2[i][1])
    Picklist=str(data2[i][2])
    Qty=data2[i][3]
    Status=data2[i][4]
    Automation=data2[i][5]
    Error=data2[i][6]
    warehouse_process=data2[i][7]
    #print(date,Portal,Picklist,Qty,Status,Automation,Error,warehouse_process)
    if (Status=='Done' and Automation!='Done'):
        sheet2.update_cell(i + 1, 6, 'running')
        print('Picklist',Picklist)
        from flipkart_processing_code.mongo_db.dateform import mongo_data
        mongo_data(Picklist)
        time.sleep(1)
        #from flipkart_processing_code.flipkart_picklist_processing_code1 import processing_code
        #processing_code(Picklist)
        # path=r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\failed_records'+'\\failed'+Picklist+'.csv'
        # file=pd.read_csv(path)
        # error_=len(file)
        # if (error_)>0:
        #     error_massage=str(error_)+' records are failed'
        #     sheet2.update_cell(i + 1, 7, error_massage)
        #     sheet2.update_cell(i + 1, 6, 'Done')
        # sheet2.update_cell(i + 1, 6, 'Done')
