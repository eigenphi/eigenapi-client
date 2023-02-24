#!/usr/bin/env python3

import requests

from eigenapi_client.endpoints import LatestBlockApi
from eigenapi_client.endpoints.schema import Transaction


class TransactionApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io'):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'transactions'
        self.latestBlockApi = LatestBlockApi(apikey=apikey, host=host)

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
