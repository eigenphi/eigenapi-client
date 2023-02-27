#!/usr/bin/env python3
import time
import requests
from eigenapi_client.endpoints.schema import LatestBlock


class LatestBlockApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io', max_retry_times: int = 30, waiting_second: int = 30):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'block/latest'
        self.max_retry_times = max_retry_times
        self.retry = 0
        self.waiting_second = waiting_second

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
        self.retry = self.retry + 1
        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                data_ = response_result['data']
                return LatestBlock(data_['blockNumber'], data_['blockTimestamp'])
        elif response.status_code == 401:
            raise Exception(response_result['errcode'], response_result['err'])
        elif response.status_code == 429:
            if self.retry > self.max_retry_times:
                raise Exception(response_result['errcode'], response_result['err'])
            waiting_second = self.waiting_second  * self.retry
            print(response_result['err'], f'sleep {waiting_second} to retry {self.retry} times')
            time.sleep(waiting_second)
            return self.do_request(chain)

        else:
            raise Exception(response.status_code, response.reason)
