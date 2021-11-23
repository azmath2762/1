import dropbox
import requests
import json


def missing_amazon_new_order_api(order_id):
    url= 'https://ihy3e6yug9.execute-api.ap-south-1.amazonaws.com/missing_amazon_new_order/missing_amazon_new_order'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload= {"order_id": order_id}
    # convert dict to json string by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    #assert resp_body['url'] == url

    # print response full body as text
    #data=resp.text
    print('resp_body',resp_body)
    print('responce:',resp.text)
    #print(len(resp.text))
    for k in resp_body:
        print(k)
missing_amazon_new_order_api('408-9362609-1266735')
#test_post_headers_body_json()

