from tika import parser
file1= r'C:\Users\Administrator\PycharmProjects\pythonProject\mongodb\Flipkart-Labels-28-Jun-2021-05-08.pdf'
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