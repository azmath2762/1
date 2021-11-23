import csv

with open('failed_records1.csv', "w", newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['listingId', 'picklistId_mongo', 'warehouseId_mongo','bin_id','error massage'])
file=r''
with open(file, "r", newline='')as f1:
    r = list(csv.reader(f1)

for i in range(1,len(r)):
    picklistId_mongo = str(r[i][0])
    listingId = str(r[i][1])
    binId_mongo = str(r[i][2])
    quantity = str(r[i][3])
    warehouseId_mongo = str(r[i][5])

