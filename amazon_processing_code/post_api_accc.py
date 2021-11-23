import dropbox
import requests
import json


def test_post_headers_body_json(picklist):
    url= 'https://vt69hc1o3h.execute-api.ap-south-1.amazonaws.com/s1/api-binreco'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload= { "picklist": picklist }
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
test_post_headers_body_json('P1630390919313')
#test_post_headers_body_json()

access_token = '4joGxl-yofIAAAAAAAAAAW0Wa_qjsmOhQ6NYfWtkG0mNefNaTsIx8hD8BVgkavph'
filename='mangodb_picklist_details.csv'
filename1='mangodb_picklist_details1.csv'
dbx = dropbox.Dropbox(access_token)
dbx.files_download_to_file(download_path=filename, path='/buymore2/madan/' + filename)