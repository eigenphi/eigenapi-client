#!/usr/bin/env python3
import time

import requests

from eigenapi_client.endpoints import LatestBlockApi
from eigenapi_client.endpoints.schema import Transaction


class TransactionApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io', max_retry_times: int = 30, waiting_second: int = 30):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'transactions'
        self.latestBlockApi = LatestBlockApi(apikey=apikey, host=host)
        self.max_retry_times = max_retry_times
        self.retry = 0
        self.waiting_second = waiting_second

    def do_request(self, chain: str, filter_type: str = None, start: int = None, end: int = None, limit: int = 100):
        url = f"{self.host}/{self.endpoint}?chain={chain}"
        params = {
            'apikey': self.apikey
        }

        next_end_time = self.latestBlockApi.do_request(chain).blockTimestamp

        if end is not None:
            next_end_time = end

        if start is not None:
            params['start_time'] = start
        else:
            params['start_time'] = next_end_time - 60 * 60

        if limit is not None:
            params['limit'] = limit

        if filter_type is not None:
            params['type'] = filter_type

        params['end_time'] = next_end_time
        result = self.__query_txs__(url, params=params)
        self.retry = 0
        while len(result) > 0:
            next_end_time = result[-1].blockTimestamp
            params['end_time'] = next_end_time
            yield result
            result = self.__query_txs__(url, params=params)

    def __query_txs__(self, url: str, params: dict = None) -> list[Transaction]:
        headers = {
            'Content-Type': 'application/json'
        }
        result = []
        # print(url, params)
        response = requests.request("GET", url, headers=headers, params=params)
        response_result = response.json()
        self.retry = self.retry + 1
        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                for row in response_result['data']:
                    transaction = Transaction(row)
                    result.append(transaction)

        elif response.status_code == 401:
            raise Exception(response_result['errcode'], response_result['err'])
        elif response.status_code == 429:
            if self.retry > self.max_retry_times:
                raise Exception(response_result['errcode'], response_result['err'])
            waiting_second = self.waiting_second * self.retry
            print(response_result['err'], f'sleep {waiting_second} second to retry {self.retry} times')
            time.sleep(waiting_second)
            return self.__query_txs__(url, params=params)
        else:
            raise Exception(response.status_code, response.reason)

        return result
