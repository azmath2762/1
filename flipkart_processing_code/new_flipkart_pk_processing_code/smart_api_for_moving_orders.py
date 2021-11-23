def smart_api_for_moving_orders(picklist):
    import dropbox
    import requests
    import json
    url = 'https://40jww40180.execute-api.ap-south-1.amazonaws.com/s1/movesmartorderstodbfunction'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {"picklist":  ""+picklist+""}
    # convert dict to json string by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    #assert resp.status_code == 200
    resp_body = resp.json()

    print('resp_body', resp_body)
    print('responce:', resp.text)
    # print(len(resp.text))
    for k in resp_body:
        print(k)
smart_api_for_moving_orders('P231021-9C4B5380C8D8')