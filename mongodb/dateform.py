import csv

# with open('mangodb_picklist_details.csv', "w", newline='',encoding="utf-8") as f:
#      thewriter = csv.writer(f)
#      thewriter.writerow(["picklistId","listingId","binId","quantity","fnsku","warehouseId"])
from pymongo import MongoClient
client = MongoClient('mongodb+srv://Counfreedise:buymore123@cluster0-tq9zt.mongodb.net/wms?retryWrites=true&w=majority')
db = client.wms
#binreco = db.api_binreco.find({'operation':'Order Picklist','picklistId':{'$in':['P250621-09ABAF1EDF5D']}})P290621-96A3194D9C60
binreco = db.api_binreco.find({'operation':'Order Picklist','picklistId':input('enter the picklistid:')})
c=0
for item in binreco:
    picklistId=item['picklistId']
    listingId=item['listingId']
    binId=item['binId']
    quantity=item['quantity']
    fnsku=item['fnsku']
    warehouseId=item['warehouseId']
    print('picklistId:',picklistId,'listingId :',listingId,'binId:',binId,'quantity:',quantity,'warehouseId',warehouseId)
    with open('mangodb_picklist_details.csv', "a", newline='', encoding="utf-8") as f:
        thewriter = csv.writer(f)
        thewriter.writerow([picklistId, listingId, binId, quantity, fnsku,warehouseId])
    c=c+1
print(c)

#cancel //span[.="Done"]
#//div[@class="toast-message-container"]    Shipping package size(LBHW) cannot be less than the packaging dimensions mentioned in My Listings tab at the time of order placement