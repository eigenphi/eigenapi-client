#!/usr/bin/env python3
from ordered_set import OrderedSet

from eigenapi_client.endpoints.LatestBlockApi import LatestBlockApi
from eigenapi_client.endpoints.PoolSandwichedApi import PoolSandwichedApi
from eigenapi_client.endpoints.TransactionApi import TransactionApi
from eigenapi_client.endpoints.StatusApi import StatusApi
from eigenapi_client.endpoints.Websocket import LivestreamSubscription, OrderedSetQueue
from eigenapi_client.endpoints.schema import LatestBlock, Transaction, ERROR_CODE



class Client(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io', debug: bool = False):
        self.apikey = apikey
        self.host = host
        self.debug = debug
        self._local_subscription_cache = OrderedSetQueue(maxsize=1000)

    def status(self):
        return StatusApi().do_request()

    def block_latest(self, chain: str) -> LatestBlock:
        return LatestBlockApi(self.apikey).do_request(chain=chain)

    def transactions(self, chain: str, filter_type: str = None, start: int = None, end: int = None, limit: int = 100):
        return TransactionApi(self.apikey)\
            .do_request(chain=chain, filter_type=filter_type, start=start, end=end, limit=limit)

    def pool_sandwiched(self, chain: str, duration: int = 30, page: int = 0, limit: int = 100):
        return PoolSandwichedApi(self.apikey).do_request(chain=chain, duration=duration, page=page, limit=limit)

    async def subscribe_transactions(self, chain: str = 'all', filter_type: str = 'all', filter_duplicate: bool = True,
                                     callback=None):

        livestream = LivestreamSubscription(apikey=self.apikey, host=self.host, chain=chain, filter_type=filter_type,
                                            cache=self._local_subscription_cache, filter_duplicate=filter_duplicate,
                                            callback=callback, debug=self.debug)
        await livestream.subscribe()


