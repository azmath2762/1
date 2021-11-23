from pprint import pprint


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

    def insertToDispatchdetails(name1, adress, pincode, l_b_h_w, awb, shipid, createdat, updatedat, dd_id):
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

    def updateInapimasterstock(productid, warehouseid):
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
            order = int(order) - 1
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

    def get_dd_id_moved(oid, oitd):
        db_name = "orders"
        conn = psycopg2.connect(host=rds_host, database=db_name, user=name, password=password)
        cur = conn.cursor()
        if neworderidlist == []:
            qry = "select dd_id from api_neworder where order_id='" + str(oid) + "' and order_item_id='" + str(
                oitd) + "'"
        else:
            qry = "select dd_id from api_neworder where order_id='" + str(oid) + "' and order_item_id='" + str(
                oitd) + "' and dd_id not in (" + str(neworderidlist)[1:-1] + ")"
        print(qry)
        cur.execute(qry)
        r1 = cur.fetchall()
        qry = "update api_dispatchdetails set picklist_id=" + str(picklist_id) + " where dd_id_id=" + str(r1[0][0])
        print(qry)
        cur.execute(qry)
        conn.commit()
        cur.close()
        conn.close()
        return r1[0][0]

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
    if no_already_moved == total_rows:
        cur.close()
        conn.close()
        return {'message': 'all ' + str(total_rows) + ' rows of picklist ' + picklist + ' have already moved'}

    if total_rows - no_already_moved != 0 and total_rows != 0:
        for o in orders:
            d_id = get_dd_id_moved(o[1], o[2])
            insert_to_api_picklistitems(d_id, o[20])
            print()
            neworderidlist.append(d_id)
        # return {'message':'there are '+str(total_rows)+' rows and '+str(no_already_moved)+' already moved for picklist '+picklist+' kindly revert the previously moved entries'}

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
    for o in orders:
        from datetime import datetime
        now2 = datetime.now()
        if int(str(now2 - now1)[2:4]) < 14:
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
            tbinid = str(o[20])
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
                insertToDispatchdetails(tname, tadress, tpin, t_l_b_h_w, tawb, ts_d, tcreated, tupdated, ddid)
                print('done', end=' ')
                print('update api neworders.....', end=' ')
                updateInneworder(tnoid)
                print('done', end=' ')
                print('update api_masterstock.....', end=' ')
                updateInapimasterstock(tpid, twid)
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
            'body': {'no_of_entries_retrieved': total_rows, 'no_of_entries_moved': len(orders) + no_already_moved,
                     'dd_ids': neworderidlist}}
pprint(lambda_handler({'picklist':input('Enter picklist id : ')},''))