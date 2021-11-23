import os

import requests
import shutil
def convert_xps_to_pdf(file_name):

    file1 = open(file_name,"r")
    data=file1.read()
    zpl = data
    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/12dpmm/labels/4x6/0/'
    files = {'file' : zpl}
    headers = {'Accept' : 'application/pdf'} # omit this line to get PNG images back
    # headers = {'Accept' : 'application/png'} # omit this line to get PNG images back
    response = requests.post(url, headers = headers, files = files, stream = True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('label.pdf', 'wb') as out_file: # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Error: ' + response.text)
xps_file = r'C:\Users\Administrator\Documents'
# os.remove(xps_file)C:\Users\Administrator\Documents\removal.py
p = os.listdir(xps_file)  # C:\Users\Administrator\Documents\removal.py
xps_file += "\\" + str(p[4])
convert_xps_to_pdf(xps_file)
