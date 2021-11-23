#xps_file = r'C:\Users\Administrator\Documents\*'
# p = os.listdir(xps_file)
# xps_file += "\\" + str(p[0])
import os

def a_remove1(files):

    for f in files:
        os.remove(f)
    print('removed all invoice pdf files from download folder')
#a_remove1(xps_file)