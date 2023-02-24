#!/usr/bin/env python3

import requests
from eigenapi_client.endpoints.schema import LatestBlock


class LatestBlockApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io'):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'block/latest'

    def do_request(self, chain: str) -> LatestBlock:
        url = f"{self.host}/{self.endpoint}?chain={chain}"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'apikey': self.apikey
        }
        response = requests.request("GET", url, headers=headers, params=params)
        response_result = response.json()
        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                data_ = response_result['data']
                return LatestBlock(data_['blockNumber'], data_['blockTimestamp'])
        elif response.status_code == 401 or response.status_code == 419:
            raise Exception(response_result['errcode'], response_result['err'])
        else:
            raise Exception(response.status_code, response.reason)
