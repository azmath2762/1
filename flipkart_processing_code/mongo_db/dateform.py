


def mongo_data(picklist):
    import csv
    file_name=r'C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\mongo_db\mangodb_picklist_details.csv'
    with open(file_name, "w", newline='',encoding="utf-8") as f:
         thewriter = csv.writer(f)
         thewriter.writerow(["picklistId","listingId","binId","quantity","fnsku","warehouseId"])

    import csv

    import dropbox

    access_token = '4joGxl-yofIAAAAAAAAAAW0Wa_qjsmOhQ6NYfWtkG0mNefNaTsIx8hD8BVgkavph'
    dbx = dropbox.Dropbox(oauth2_access_token=access_token, max_retries_on_error=2)

    filename = r"C:\Users\Administrator\PycharmProjects\pythonProject\flipkart_processing_code\mongo_db\mangodb_picklist_details1.csv"
    #picklist = 'P031021-6F8E18AF26C3'
    # with open('mangodb_picklist_details.csv', "w", newline='', encoding="utf-8") as f:
    #     thewriter = csv.writer(f)
    #     thewriter.writerow(["picklistId", "listingId", "binId", "quantity", "fnsku", "warehouseId"])
    # dbx = dropbox.Dropbox(access_token)
    # dbx.files_download_to_file(download_path='/tmp/' + filename, path='/buymore2/madan/fk_data.csv')
    dbx.files_download_to_file(download_path=filename, path='/buymore2/bin_reco/csv_import/' + picklist + '.csv')
    with open(filename, "r", newline='')as f1:
        r = list(csv.reader(f1))
    for i in range(1, len(r)):
        listing_id = r[i][1]
        listing_id2 = r[i][2]
        picklist_id = r[i][4]
        qty = r[i][5]
        bin = r[i][6]
        warehouse = r[i][7]
        if int(qty) > 1:
            if len(listing_id2) > 3:
                for j in range(int(qty)):
                    qty = 1
                    with open(file_name, "a", newline='', encoding="utf-8") as f:
                        thewriter = csv.writer(f)
                        thewriter.writerow([picklist_id, listing_id2, bin, qty, "fnsku", warehouse])
            else:
                for j in range(int(qty)):
                    qty = 1
                    with open(file_name, "a", newline='', encoding="utf-8") as f:
                        thewriter = csv.writer(f)
                        thewriter.writerow([picklist_id, listing_id, bin, qty, "fnsku", warehouse])
        elif int(qty) == 1:
            if len(listing_id2) > 3:
                qty = 1
                with open(file_name, "a", newline='', encoding="utf-8") as f:
                    thewriter = csv.writer(f)
                    thewriter.writerow([picklist_id, listing_id2, bin, qty, "fnsku", warehouse])
            else:
                qty = 1
                with open(file_name, "a", newline='', encoding="utf-8") as f:
                    thewriter = csv.writer(f)
                    thewriter.writerow([picklist_id, listing_id, bin, qty, "fnsku", warehouse])
#mongo_data('P041021-7DB610022B1B')
#cancel //span[.="Done"]
#//div[@class="toast-message-container"]    Shipping package size(LBHW) cannot be less than the packaging dimensions mentioned in My Listings tab at the time of order placement