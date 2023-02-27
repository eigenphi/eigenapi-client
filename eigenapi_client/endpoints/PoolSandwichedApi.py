import requests

from eigenapi_client.endpoints.schema import PoolSandwiched


class PoolSandwichedApi(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io'):
        self.apikey = apikey
        self.host = "https://" + host
        self.endpoint = 'pool/sandwiched'

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
        result = []
        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                for row in response_result['data']:
                    pool_sandwiched = PoolSandwiched(row)
                    result.append(pool_sandwiched)

        elif response.status_code == 401 or response.status_code == 419:
            raise Exception(response_result['errcode'], response_result['err'])
        else:
            raise Exception(response.status_code, response.reason)

        return result
