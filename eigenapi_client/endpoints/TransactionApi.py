#!/usr/bin/env python3

import requests

from eigenapi_client.endpoints import LatestBlockApi
from eigenapi_client.endpoints.schema import Transaction


class TransactionApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io', debug: bool = False):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'transactions'
        self.quotaInterval = 10
        self.debug = debug

    def do_request(self, chain: str, filter_type: str = None, start: int = None, end: int = None, limit: int = 100):
        url = f"{self.host}/{self.endpoint}?chain={chain}"
        params = {
            'apikey': self.apikey
        }
        if end is not None:
            params['end_time'] = end

        if start is not None:
            params['start_time'] = start

        if limit is not None:
            params['limit'] = limit

        if filter_type is not None:
            params['type'] = filter_type

        if params['end_time'] is not None and params['start_time'] is not None and \
                params['end_time'] == params['start_time']:
            return []

        return self.__query_txs__(url, params=params)

    def __query_txs__(self, url: str, params: dict = None) -> list[Transaction]:
        headers = {
            'Content-Type': 'application/json'
        }
        result = []
        if self.debug:
            print(url, params)
        response = requests.request("GET", url, headers=headers, params=params)
        response_result = response.json()

        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                for row in response_result['data']:
                    transaction = Transaction(row)
                    result.append(transaction)

        elif response.status_code == 401 or response.status_code == 419:
            raise Exception(response_result['errcode'], response_result['err'])
        else:
            raise Exception(response.status_code, response.reason)

        return result
