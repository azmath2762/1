import json

from pymongo import MongoClient


def lambda_handler(event, context):
    # TODO implement
    from pymongo import MongoClient
    if 'picklist' in event:
        inp_mon = str(event['picklist'])
    else:
        return {'message': 'picklist is required'}

    client = MongoClient(
        'mongodb+srv://Counfreedise:buymore123@cluster0-tq9zt.mongodb.net/wms?retryWrites=true&w=majority', port=27017)
    db = client.wms
    # binreco = db.api_binreco.find({'operation':'Order Picklist','picklistId':{'$in':['P250621-09ABAF1EDF5D']}})#P290621-96A3194D9C60
    binreco = db.api_binreco.find({'operation': 'Order Picklist', 'picklistId': inp_mon})
    c = 0

    for item in binreco:
        print(item)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
lambda_handler(event='P250621-09ABAF1EDF5D',context=None)


client = MongoClient(
        'mongodb+srv://Counfreedise:buymore123@cluster0-tq9zt.mongodb.net/wms?retryWrites=true&w=majority', port=27017)
db = client.wms
# binreco = db.api_binreco.find({'operation':'Order Picklist','picklistId':{'$in':['P250621-09ABAF1EDF5D']}})#P290621-96A3194D9C60
binreco = db.api_binreco.find({'operation': 'Order Picklist', 'picklistId': 'P250621-09ABAF1EDF5D'})
c = 0

for item in binreco:
    print(item)