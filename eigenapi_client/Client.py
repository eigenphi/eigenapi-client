#!/usr/bin/env python3

from eigenapi_client.endpoints.LatestBlockApi import LatestBlockApi
from eigenapi_client.endpoints.PoolSandwichedApi import PoolSandwichedApi
from eigenapi_client.endpoints.TransactionApi import TransactionApi
from eigenapi_client.endpoints.StatusApi import StatusApi
from eigenapi_client.endpoints.schema import LatestBlock, Transaction, ERROR_CODE

import asyncio
import json
import ssl
import certifi
import websockets
from websockets.exceptions import InvalidStatusCode


class Client(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io'):
        self.apikey = apikey
        self.host = host

    def status(self):
        return StatusApi().do_request()

    def latest_block(self, chain: str) -> LatestBlock:
        return LatestBlockApi(self.apikey).do_request(chain=chain)

    def transactions(self, chain: str, filter_type: str = None, start: int = None, end: int = None, limit: int = 100):
        return TransactionApi(self.apikey)\
            .do_request(chain=chain, filter_type=filter_type, start=start, end=end, limit=limit)

    def pool_sandwiched(self, chain: str, page: int = 0, limit: int = 100):
        return PoolSandwichedApi(self.apikey).do_request(chain=chain, page=page, limit=limit)

    def subscribe_transactions(self, chain: str = 'all', filter_type: str = 'all', callback=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.__execute_sub__(chain, filter_type, callback))
        finally:
            loop.close()

    async def __execute_sub__(self, chain: str = 'all', filter_type: str = 'all', callback=None):
        url = f"wss://{self.host}/ws?chain={chain}&type={filter_type}&apikey={self.apikey}"
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        try:
            async with websockets.connect(url, ssl=ssl_context) as ws:
                while True:
                    recv_text = await ws.recv()
                    data_dict = json.loads(recv_text)
                    if callback is not None:
                        transaction = Transaction(data_dict)
                        callback(transaction)
        except InvalidStatusCode as e:
            if e.status_code in ERROR_CODE:
                raise Exception(e.status_code, ERROR_CODE[e.status_code])
            else:
                raise Exception(e.status_code, str(e))
        except Exception as e:
            raise Exception(str(e))



