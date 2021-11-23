from pprint import pprint

import dropbox
import csv
import psycopg2
import csv
import datetime
def smart_api(smart_api_picklist_id):
    rds_host = "buymore-2.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com"
    db_name = 'testers'
    #db_name = 'orders'
    #db_name = 'inward'
    name = 'postgres'
    password = 'buymore3'
    conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
    #picklist=input('enter picklist:')
    picklist=smart_api_picklist_id
    cur = conn.cursor()
    quary="UPDATE api_neworders SET pin_code = 577006 where pin_code=0 and pick_list_id='"+picklist+"'"
    cur.execute(quary)
    conn.commit()
    print('updated')

    def lambda_handler(event, content):
        import sys
        import psycopg2
        def db_credential(db_name, typ):
            import requests
            import json
            url = "http://ec2-13-234-21-229.ap-south-1.compute.amazonaws.com/db_credentials/"  #
            payload = json.dumps({
                "data_base_name": db_name
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = dict(requests.post(url, data=payload, headers=headers).json())
            status = response['status']
            print(response)
            if status == True:
                return response['db_detail'][typ]
            else:
                return

        db_creds = db_credential('postgres', 'db_detail_for_psycopg2')
        # db_creds={"endPoint":"buymore-dev-aurora.cluster-cegnfd8ehfoc.ap-south-1.rds.amazonaws.com","userName":"postgres","passWord":"r2DfZEyyNL2VLfg2"}
        rds_host = db_creds['endPoint']
        name = db_creds['userName']
        password = db_creds['passWord']
        try:
            picklist = str(event['picklist'])
        except:
            return {'message': 'picklist is mandatory'}  # 'P300621-E6A879B46C97'

        def get_picklist_id():
            db_name = 'warehouse'
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry = "select id from api_picklist where picklist_id='" + str(picklist) + "'"
            print(qry)
            cur.execute(qry)
            r1 = cur.fetchall()
            cur.close()
            conn.close()
            try:
                return str(r1[0][0])
            except:
                print('picklist - ' + picklist + ' not found in db')
                return None

        picklist_id = get_picklist_id()
        if picklist_id == None:
            return {'message': 'picklist ' + picklist + ' not found in db'}

        def dlmadj(st):
            if st.find("'") > -1:
                s = ''
                for jjm in st:
                    if jjm == "'":
                        s = s + "''"
                    else:
                        s = s + jjm
                st = s
            return st

        def getbskus():
            db_name = "products"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            qry = "select flipkart_portal_unique_id,buymore_sku from flipkart_flipkartproducts f,master_masterproduct m where m.product_id=f.product_id"
            # print(qry)
            cur = conn.cursor()
            cur.execute(qry)
            r1 = cur.fetchall()
            cur.close()
            conn.close()
            ret_data = {}
            for r in r1:
                ret_data[r[0]] = r[1]
            return ret_data
        def update_api_picklistprocessingmonitor():
            db_name = 'warehouse'
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry = "UPDATE api_picklistprocessingmonitor SET items_processed=0 WHERE picklist_id='" + str(picklist_id) + "'"
            print(qry)
            cur.execute(qry)
            qry = "UPDATE api_picklist SET status='Completed' where picklist_id='" + str(picklist) + "'"
            print(qry)
            cur.execute(qry)
            conn.commit()
            cur.close()
            conn.close()

        def insert_to_api_picklistitems(dd_id, binid):
            db_name = 'warehouse'
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry = 'SELECt * FROM api_picklistitems where picklist_id=' + str(
                picklist_id) + ' and portal_new_order_id=' + str(dd_id)
            cur.execute(qry)
            r1 = cur.fetchall()
            if len(r1) > 0:
                cur.close()
                conn.close()
                return
            tem = '(picklist_id,portal_new_order_id,status,found,remarks,updated_at,found_bin)'
            val = "(" + dlmadj(str(picklist_id)) + "," + str(dd_id) + ",'Collected','Found','found',now(),'" + dlmadj(
                str(binid)) + "')"
            qry = "insert into api_picklistitems " + tem + " values" + val + ""
            print(qry, end=' ')
            cur.execute(qry)
            conn.commit()
            cur.close()
            conn.close()

        def getdatetime():
            from datetime import datetime
            cd = datetime.now()
            return cd

        def getproductid(st):
            db_name = "products"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            qry = "select product_id,flipkart_upload_selling_price from flipkart_flipkartproducts where flipkart_portal_unique_id='" + dlmadj(
                str(st)) + "'"
            # print(qry)
            cur = conn.cursor()
            cur.execute(qry)
            r1 = cur.fetchall()
            cur.close()
            conn.close()
            if len(r1) > 0:
                pid = r1[0]
            else:
                pid = ['0', '0']
            return pid

        def getdate(ss):
            if ss != '' and (len(ss) == 21 or len(ss) == 22 or len(ss) == 12):
                if str(ss[0]).isnumeric():
                    s = ss[10:]
                else:
                    s = ss[0:12]
                # print(s)
                i = s.find(',')
                if i != -1:
                    if len(s[i + 2:i + 6]) == 4:
                        try:
                            y = int(s[i + 2:i + 6])
                        except:
                            y = -1
                    else:
                        y = -1
                    if len(s[i - 2:i]) == 2:
                        try:
                            d = int(s[i - 2:i])
                        except:
                            d = -1
                    else:
                        d = -1
                    if s[0:3].lower().startswith('jan'):
                        m = 1
                    elif s[0:3].lower().startswith('feb'):
                        m = 2
                    elif s[0:3].lower().startswith('mar'):
                        m = 3
                    elif s[0:3].lower().startswith('apr'):
                        m = 4
                    elif s[0:3].lower().startswith('may'):
                        m = 5
                    elif s[0:3].lower().startswith('jun'):
                        m = 6
                    elif s[0:3].lower().startswith('jul'):
                        m = 7
                    elif s[0:3].lower().startswith('aug'):
                        m = 8
                    elif s[0:3].lower().startswith('sep'):
                        m = 9
                    elif s[0:3].lower().startswith('oct'):
                        m = 10
                    elif s[0:3].lower().startswith('nov'):
                        m = 11
                    elif s[0:3].lower().startswith('dec'):
                        m = 12
                    else:
                        m = -1
                    if y != -1 and d != -1 and m != -1:
                        import datetime
                        cd = datetime.date(y, m, d)
                        return cd
                    else:
                        return -1
                else:
                    return -1
            else:
                return -1

        def get_product_details(pid, portid):
            db_name = "products"
            conn_products = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur_products = conn_products.cursor()
            qry = "SELECT account_name from master_portalaccountdetails where portal_id_id=" + str(portid)
            cur_products.execute(qry)
            res = cur_products.fetchall()
            if len(res) <= 0:
                conn_products.close()
                cur_products.close()
                return 'portal ' + str(portid) + ' not found in db'
            prt_name = str(res[0][0]).lower()
            qry = "SELECT product_mrp," + prt_name + "_upload_selling_price," + prt_name + "_portal_sku,buymore_sku FROM " + prt_name + "_" + prt_name + "products as a,master_masterproduct as m where m.product_id=a.product_id and a.product_id=" + str(
                pid)
            cur_products.execute(qry)
            res = cur_products.fetchall()
            conn_products.close()
            cur_products.close()
            if len(res) > 0:
                return res[0]
            else:
                return str(pid) + ' not listed in ' + prt_name + "_" + prt_name + 'products or master_masterproduct'

        def getmrpandtaxrate(prdid, selp):
            db_name = "products"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            qry = 'select a.threshold_amount,a.max_rate,a.min_rate,b.product_mrp,b.buymore_sku from calculation_hsncoderate a,master_masterproduct b where a.hsn_rate_id=b.hsn_code_id_id and b.product_id=' + dlmadj(
                str(prdid))
            # print(qry)
            cur = conn.cursor()
            cur.execute(qry)
            r1 = cur.fetchall()
            cur.close()
            conn.close()
            if len(r1) > 0:
                tda = int(r1[0][0])
                maxr = r1[0][1]
                minr = r1[0][2]
                mrp = r1[0][3]
                bmrsku = r1[0][4]
                if int(selp) > tda:
                    return [maxr, mrp, bmrsku]
                else:
                    return [minr, mrp, bmrsku]
            else:
                return -1

        def insertToDispatchdetails(name1, adress, pincode, l_b_h_w, awb, shipid, createdat, updatedat, dd_id,temp_binidlist):
            db_name = "orders"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            tem = '(name,address,pincode,l_b_h_w,picklist_id,is_mark_placed,have_invoice_file,packing_status,is_dispatch,dispatch_confirmed,is_shipment_create,awb,shipment_id,created_at,update_at,dd_id_id,"bin_Id",bin_confirm,fulfillment_model,status,dd_paymentstatus,dd_cancelledpaymentstatus)'
            val = "('" + dlmadj(str(name1)) + "','" + dlmadj(str(adress)) + "','" + dlmadj(str(pincode)) + "','" + dlmadj(
                str(l_b_h_w)) + "'," + str(picklist_id) + ",True,True,True,False,False,True,'" + dlmadj(
                str(awb)) + "','" + dlmadj(str(shipid)) + "','" + dlmadj(str(createdat)) + "','" + dlmadj(
                str(updatedat)) + "'," + dlmadj(str(dd_id)) + ",ARRAY['@@@@@@'],ARRAY[True],'portal','packed',False,False)"
            qry = "insert into api_dispatchdetails " + tem + " values" + val + ""
            # print(qry)
            cur.execute(qry)
            conn.commit()
            for i1 in range(len(temp_binidlist)):
                curbin = "'" + temp_binidlist[i1] + "'"
                if curbin.startswith("'A") or curbin.startswith("'a"):
                    curbinc = "True"
                else:
                    curbinc = "False"
                qry = 'update api_dispatchdetails set "bin_Id"[' + str(i1 + 1) + ']=' + str(curbin) + ',bin_confirm[' + str(
                    i1 + 1) + ']=' + str(curbinc) + ' where dd_id_id=' + str(ddid)
                cur.execute(qry)
                conn.commit()
            cur.close()
            conn.close()

        def insertToNeworder(pid, oid, oiid, od, dbd, poid, psku, quan, sp, mrp, tr, wareid, bmrsku):
            db_name = "orders"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            tem = "(product_id,order_id,order_item_id,order_date,dispatch_by_date,portal_id,portal_sku,qty,selling_price,mrp,tax_rate,warehouse_id,buymore_sku,portal_account_id)"
            val = "(" + dlmadj(str(pid)) + ",'" + dlmadj(str(oid)) + "','" + dlmadj(str(oiid)) + "','" + dlmadj(
                str(od)) + "','" + dlmadj(str(dbd)) + "'," + dlmadj(str(poid)) + ",'" + dlmadj(str(psku)) + "'," + dlmadj(
                str(quan)) + "," + dlmadj(str(sp)) + "," + dlmadj(str(mrp)) + "," + dlmadj(str(tr)) + "," + dlmadj(
                str(wareid)) + ",'" + dlmadj(str(bmrsku)) + "',8)"
            qry = "insert into api_neworder " + tem + " values" + val + "RETURNING dd_id"
            cur = conn.cursor()
            cur.execute(qry)
            # qry = "select dd_id from api_neworder where order_id='" + dlmadj(str(oid)) + "' and order_item_id='" + dlmadj(str(oiid)) + "' and portal_id='" + dlmadj(str(poid)) + "' and warehouse_id='"+dlmadj(str(wareid))+"' order by dd_id DESC"
            # #print(qry)
            # cur.execute(qry)
            # data = cur.fetchall()
            # ddid=''
            ddid = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return ddid

        def updateInneworder(neworderid):
            db_name = "testers"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry = 'update api_neworders set ordersdb_updated=True where new_order_id=' + dlmadj(str(neworderid))
            # print(qry)
            cur.execute(qry)
            conn.commit()
            cur.close()
            conn.close()

        def updateInapimasterstock(productid, warehouseid,qty):
            db_name = "orders"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry = "select orders from api_masterstock where product_id=" + str(productid) + " and warehouse=" + str(
                warehouseid)
            # print(qry)
            cur.execute(qry)
            r1 = cur.fetchall()
            if len(r1) == 0:
                print('no row found for productid=', productid, ' and warehouse=', warehouseid, end=' ')
                return
            order = r1[0][0]
            try:
                # print(order)
                order = int(order) - int(qty)
            except:
                print('value of order is not an int', end=' ')
                return
            qry = "update api_masterstock set orders=" + dlmadj(str(order)) + ",status=True where product_id=" + dlmadj(
                str(productid)) + " and warehouse=" + dlmadj(str(warehouseid))
            # print(qry)
            cur.execute(qry)
            conn.commit()
            cur.close()
            conn.close()

        def update_picklist_id_moved(dd_id_id):
            db_name = "orders"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            # if neworderidlist == []:
            #     qry = "select dd_id from api_neworder where order_id='" + str(oid) + "' and order_item_id='" + str(
            #         oitd) + "'"
            # else:
            #     qry = "select dd_id from api_neworder where order_id='" + str(oid) + "' and order_item_id='" + str(
            #         oitd) + "' and dd_id not in (" + str(neworderidlist)[1:-1] + ")"
            # print(qry)
            # cur.execute(qry)
            # r1 = cur.fetchall()
            qry = "update api_dispatchdetails set picklist_id=" + str(picklist_id) + " where dd_id_id=" + str(dd_id_id)
            print(qry)
            cur.execute(qry)
            conn.commit()
            cur.close()
            conn.close()
            # return r1[0][0]

        def get_flipkart_lid_from_product_id():
            db_name = 'products'
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry = 'SELECT product_id,flipkart_listing_id FROM flipkart_flipkartproducts where flipkart_listing_id is not null'
            cur.execute(qry)
            return_data = {}
            res = cur.fetchall()
            cur.close()
            conn.close()
            for r in res:
                return_data[r[0]] = r[1]
            return return_data

        neworderidlist = []
        from datetime import datetime
        now1 = datetime.now()
        print(now1)
        db_name = "testers"
        conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
        cur = conn.cursor()
        # print('connected')
        qry = "select sku,order_id,order_item_id,order_on,dispatch_by_date,quantity,selling_price_per_item,warehouse_id,buyer_name,address_line_1,address_line_2,pin_code,package_length,package_breadth,package_height,package_weight,tracking_id,shipment_id,new_order_id,fsn,bin_id from api_neworders where tracking_id!=' ' and ordersdb_updated=True and pin_code!=0 and pick_list_id='" + picklist + "' order by new_order_id DESC"
        cur.execute(qry)
        orders = cur.fetchall()
        no_already_moved = len(orders)
        qry = "SELECt * FROM api_neworders where pick_list_id='" + picklist + "'"
        cur.execute(qry)
        total_rows = len(cur.fetchall())
        print('total', total_rows)
        print('already moved', no_already_moved)
        if no_already_moved >= total_rows:
            cur.close()
            conn.close()
            return {'message': 'all ' + str(total_rows) + ' rows of picklist ' + picklist + ' have already moved'}
        cur.close()
        conn.close()
        db_name = 'warehouse'
        conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
        cur = conn.cursor()
        qry = 'DELETE FROM api_picklistitems where picklist_id=' + str(
            picklist_id)
        cur.execute(qry)
        conn.commit()
        cur.close()
        conn.close()
        if total_rows - no_already_moved != 0 and total_rows != 0  and no_already_moved>0:
            db_name = "testers"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry="select distinct(order_id,order_item_id) from api_neworders where tracking_id!=' ' and ordersdb_updated=True and pin_code!=0 and pick_list_id='" + picklist + "'"
            cur.execute(qry)
            orders_1=cur.fetchall()
            cur.close()
            conn.close()
            t_res = []
            for ord1 in orders_1:
                ord=ord1[0][1:-1].split(",")
                print(ord1,ord)
                if (ord[0], ord[1]) not in t_res:
                    t_res.append((ord[0], ord[1]))
            db_name = "orders"
            conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
            cur = conn.cursor()
            qry='SELECT dd_id,"bin_Id" From api_neworder , api_dispatchdetails where dd_id=dd_id_id and (order_id,order_item_id) in ('+str(t_res)[1:-1]+')'
            cur.execute(qry)
            orders_1 = cur.fetchall()
            print(qry)
            cur.close()
            conn.close()
            for ord in orders_1:
                print(ord)
                d_id=ord[0]
                try:
                    bin_id_tem=ord[1]
                except:
                    bin_id_tem='N/A'
                update_picklist_id_moved(d_id)
                insert_to_api_picklistitems(d_id, bin_id_tem)
                neworderidlist.append(d_id)


            # return {'message':str(no_already_moved)+' have already moved kindly check'}
        # if total_rows - no_already_moved != 0 and total_rows != 0:
        #     for o in orders:
        #         d_id = get_dd_id_moved(o[1], o[2])
        #         insert_to_api_picklistitems(d_id, o[20])
        #         print()
        #         neworderidlist.append(d_id)
            # return {'message':'there are '+str(total_rows)+' rows and '+str(no_already_moved)+' already moved for picklist '+picklist+' kindly revert the previously moved entries'}
        access_token = '4joGxl-yofIAAAAAAAAAAW0Wa_qjsmOhQ6NYfWtkG0mNefNaTsIx8hD8BVgkavph'
        dbx = dropbox.Dropbox(access_token)
        picklist_file = '/buymore2/bin_reco/csv_import/' + picklist + '.csv'
        file = picklist + '.csv'
        dbx.files_download_to_file(download_path=file, path=picklist_file)
        with open(file, 'r', newline='') as f:
            fd = list(csv.reader(f))[1:]
        assigned_details = {}
        for row in fd:
            try:
                int(row[5])
            except:
                continue
            try:
                for it in range(int(row[5])):
                    assigned_details[row[1]].append({'binid': row[6], 'assigned': False})
            except:
                assigned_details[row[1]] = []
                for it in range(int(row[5])):
                    assigned_details[row[1]].append({'binid': row[6], 'assigned': False})
        flipkart_product_id_to_fsku = get_flipkart_lid_from_product_id()
        db_name = "testers"
        conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
        cur = conn.cursor()
        qry = "select sku,order_id,order_item_id,order_on,dispatch_by_date,quantity,selling_price_per_item,warehouse_id,buyer_name,address_line_1,address_line_2,pin_code,package_length,package_breadth,package_height,package_weight,tracking_id,shipment_id,new_order_id,fsn,bin_id from api_neworders where tracking_id!=' ' and (ordersdb_updated is NULL or ordersdb_updated=False) and pin_code!=0 and pick_list_id='" + picklist + "' order by new_order_id DESC"
        cur.execute(qry)
        orders = cur.fetchall()
        cur.close()
        conn.close()
        print('retrieved')
        # orders=orders[0:1]
        lenord = len(orders)
        print(lenord)
        now2 = datetime.now()
        all_bskus = getbskus()
        for o in orders:
            from datetime import datetime
            now2 = datetime.now()
            tbinid = str(o[20])
            tsku = o[0]
            if int(str(now2 - now1)[2:4]) < 14:
                if tbinid.startswith('ST-031'):
                    try:
                        tsku=all_bskus[o[19]]
                    except Exception as e1:
                        print(e1)
                        print('no buymore sku for '+o[19])
                        continue
                    temp = tsku.split('_')
                    if len(temp) < 1:
                        print(tsku)
                        continue
                    product_det = []
                    try:
                        for t in temp:
                            temp1 = t.split('-')
                            if len(temp1) != 2:
                                print(tsku)
                                raise Exception('Product id is not as per the format')
                            try:
                                quantity = int(temp1[1])
                                new_update_quantity = o[5] * quantity
                                productid = int(temp1[0])
                                sp = get_product_details(productid, 2)
                                if isinstance(sp, str):
                                    raise Exception(sp)
                                else:
                                    mrp = sp[0] * new_update_quantity
                                    psku = str(sp[2])
                                    bsku = str(sp[3])
                                    sp = sp[1] * new_update_quantity
                                    product_det.append({'new_product_id': productid, 'new_mrp': mrp, 'new_sp': sp,
                                                        'new_qty': new_update_quantity, 'portal_sku': psku,
                                                        'buymore_sku': bsku})
                            except Exception as e1:
                                raise Exception(e1)
                            for current_item in product_det:
                                print(o)
                                tsku = current_item['buymore_sku']
                                tpid = current_item['new_product_id']
                                tsp = current_item['new_sp']
                                tpid = str(tpid)
                                torderid = o[1]
                                titemid = o[2]
                                torderdate = getdate(o[3])
                                tdbd = getdate(o[4])
                                tportal_id = '2'
                                tqty = current_item['new_qty']
                                twid = o[7]
                                tname = o[8]
                                tadress = o[9] + ',' + o[10]
                                tadress = tadress[:200]
                                tpin = o[11]
                                t_l_b_h_w = str(o[12]) + "," + str(o[13]) + "," + str(o[14]) + "," + str(o[15])
                                t_l_b_h_w = t_l_b_h_w[:50]
                                tawb = o[16]
                                ts_d = o[17]
                                tnoid = o[18]
                                gtmrpntrate = getmrpandtaxrate(tpid, tsp)
                                if gtmrpntrate != -1:
                                    tmrp = gtmrpntrate[1]
                                    ttaxrate = gtmrpntrate[0]
                                    tbmrsku = gtmrpntrate[2]
                                if tpid != '0' and torderdate != -1 and tdbd != -1 and gtmrpntrate != -1:
                                    with open(r'split_data.csv','a',newline='') as f:
                                        wrtt=csv.writer(f)
                                        wrtt.writerow([tpid,tsku,tqty,picklist])
                                    print('insert to neworder.....', end=' ')
                                    ddid = insertToNeworder(tpid, torderid, titemid, torderdate, tdbd, tportal_id, tsku,
                                                            tqty, tsp, tmrp,
                                                            ttaxrate, twid, tbmrsku)
                                    print('done', end=' ')
                                    tcreated = getdatetime()
                                    tupdated = getdatetime()
                                    print(ddid, end=' ')
                                    try:
                                        fnsku = flipkart_product_id_to_fsku[current_item['new_product_id']]
                                    except:
                                        fnsku = 'N/A'
                                    binidlist=[]
                                    for n_q in range(0, tqty):
                                        tbid = 'N/A'
                                        if fnsku in assigned_details:
                                            for search_row in assigned_details[fnsku]:
                                                if search_row['assigned'] == False:
                                                    tbid = search_row['binid']
                                                    search_row['assigned'] = True
                                                    binidlist.append(tbid)
                                                    break
                                    print('insert to dispatchdetails.....', tsp, end=' ')
                                    insertToDispatchdetails(tname, tadress, tpin, t_l_b_h_w, tawb, ts_d, tcreated, tupdated,ddid,binidlist)
                                    print('done', end=' ')
                                    print('update api neworders.....', end=' ')
                                    updateInneworder(tnoid)
                                    print('done', end=' ')
                                    print('update api_masterstock.....', end=' ')
                                    updateInapimasterstock(tpid, twid, tqty)
                                    print('done', end=' ')
                                    print('adding to picklistitems', end=' ')
                                    for biid in binidlist:
                                        insert_to_api_picklistitems(ddid, biid)
                                    print('adding to picklistitems done', end=' ')
                                    neworderidlist.append(int(ddid))
                                else:
                                    print('sku=', tsku, ' pid=', tpid, ' oderdate=', torderdate, ' dispatchbydate=', tdbd,
                                          'mrp n rate=',
                                          gtmrpntrate, 'new_oderid=', tnoid)

                    except Exception as em:
                        print(em)
                else:
                    print(o)
                    tsku = o[0]
                    tpid = getproductid(o[19])
                    tsp = tpid[1]
                    tpid = str(tpid[0])
                    torderid = o[1]
                    titemid = o[2]
                    torderdate = getdate(o[3])
                    tdbd = getdate(o[4])
                    tportal_id = '2'
                    tqty = o[5]
                    twid = o[7]
                    tname = o[8]
                    tadress = o[9] + ',' + o[10]
                    tadress = tadress[:200]
                    tpin = o[11]
                    t_l_b_h_w = str(o[12]) + "," + str(o[13]) + "," + str(o[14]) + "," + str(o[15])
                    t_l_b_h_w = t_l_b_h_w[:50]
                    tawb = o[16]
                    ts_d = o[17]
                    tnoid = o[18]
                    gtmrpntrate = getmrpandtaxrate(tpid, tsp)
                    if gtmrpntrate != -1:
                        tmrp = gtmrpntrate[1]
                        ttaxrate = gtmrpntrate[0]
                        tbmrsku = gtmrpntrate[2]
                    if tpid != '0' and torderdate != -1 and tdbd != -1 and gtmrpntrate != -1:
                        print('insert to neworder.....', end=' ')
                        ddid = insertToNeworder(tpid, torderid, titemid, torderdate, tdbd, tportal_id, tsku, tqty, tsp, tmrp,
                                                ttaxrate, twid, tbmrsku)
                        print('done', end=' ')
                        tcreated = getdatetime()
                        tupdated = getdatetime()
                        print(ddid, end=' ')
                        print('insert to dispatchdetails.....', tsp, end=' ')
                        insertToDispatchdetails(tname, tadress, tpin, t_l_b_h_w, tawb, ts_d, tcreated, tupdated, ddid,[tbinid])
                        print('done', end=' ')
                        print('update api neworders.....', end=' ')
                        updateInneworder(tnoid)
                        print('done', end=' ')
                        print('update api_masterstock.....', end=' ')
                        updateInapimasterstock(tpid, twid,tqty)
                        print('done', end=' ')
                        print('adding to picklistitems', end=' ')
                        insert_to_api_picklistitems(ddid, tbinid)
                        print('adding to picklistitems done', end=' ')
                        neworderidlist.append(int(ddid))
                    else:
                        print('sku=', tsku, ' pid=', tpid, ' oderdate=', torderdate, ' dispatchbydate=', tdbd, 'mrp n rate=',
                              gtmrpntrate, 'new_oderid=', tnoid)
                    lenord -= 1
                print('remaining ', lenord)
        if len(neworderidlist) > 0:
            print("updating picklistprocessingmonitor")
            update_api_picklistprocessingmonitor()
            print("done")
        print(now2)
        print(neworderidlist)
        print(len(neworderidlist))
        return {'message': 'picklist ' + picklist + ' processed ',
                'body': {'no_of_entries_retrieved': total_rows, 'no_of_entries_moved': len(neworderidlist),
                         'dd_ids': neworderidlist}}
    pprint(lambda_handler({'picklist':smart_api_picklist_id},''))
smart_api('P241021-F420B240557F')