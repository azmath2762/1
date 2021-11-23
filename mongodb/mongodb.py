import pyautogui
pyautogui.press('esc')


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
    print('cropped_file_path:', cropped_file_path)
    print('pdf crop done')


crop_pdf()