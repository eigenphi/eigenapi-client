import time

import requests

from eigenapi_client.endpoints.schema import PoolSandwiched


class PoolSandwichedApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io', max_retry_times: int = 30, waiting_second: int = 30):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'pool/sandwiched'
        self.max_retry_times = max_retry_times
        self.retry = 0
        self.waiting_second = waiting_second

    def do_request(self, chain: str, duration: int = 30, page: int = 0, limit: int = 100):
        url = f"{self.host}/{self.endpoint}?chain={chain}"
        params = {
            'apikey': self.apikey
        }

        if page is not None:
            params['page'] = page

        if limit is not None:
            params['limit'] = limit

        if duration is not None:
            params['duration'] = duration

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, params=params)
        response_result = response.json()
        self.retry = self.retry + 1
        result = []
        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                for row in response_result['data']:
                    pool_sandwiched = PoolSandwiched(row)
                    result.append(pool_sandwiched)

        elif response.status_code == 401:
            raise Exception(response_result['errcode'], response_result['err'])
        elif response.status_code == 429:
            if self.retry > self.max_retry_times:
                raise Exception(response_result['errcode'], response_result['err'])
            waiting_second = self.waiting_second * self.retry
            print(response_result['err'], f'sleep {waiting_second} to retry {self.retry} times')
            time.sleep(waiting_second)
            return self.do_request(chain)
        else:
            raise Exception(response.status_code, response.reason)

        return result
