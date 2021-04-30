from . import Checksum
from django.conf import settings
import requests
import json

def VerifyPaytmResponse(response):
    response_dict = {}
    if response.method == "POST":
        data_dict = {}
        for key in response.POST:
            data_dict[key] = response.POST[key]
        MID = data_dict['MID']
        ORDERID = data_dict['ORDERID']
        verify = Checksum.verify_checksum(data_dict, settings.PAYTM_MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            STATUS_URL = settings.PAYTM_TRANSACTION_STATUS_URL
            headers = {
                'Content-Type': 'application/json',
            }
            data = '{"MID":"%s","ORDERID":"%s"}'%(MID, ORDERID)
            check_resp = requests.post(STATUS_URL, data=data, headers=headers).json()
            if check_resp['STATUS']=='TXN_SUCCESS':
                response_dict['verified'] = True
                response_dict['paytm'] = check_resp
                return (response_dict)
            else:
                response_dict['verified'] = False
                response_dict['paytm'] = check_resp
                return (response_dict)
        else:
            response_dict['verified'] = False
            return (response_dict)
    response_dict['verified'] = False
    return response_dict