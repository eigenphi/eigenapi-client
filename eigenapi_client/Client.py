#!/usr/bin/env python3
import time

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
        self.max_retry_times = 5
        self._local_subscription_cache = OrderedSetQueue(maxsize=1000)

    def quota_retry(self, request, args, interval, retry):
        retry_count = 0
        while True:
            try:
                return request(*args)
            except Exception as e:
                if e.args[0] == 429:
                    retry_count += 1
                    if self.debug:
                        print(f'API Quota reached, waiting for recover. retry {retry_count} time(s)')
                    if retry_count > self.max_retry_times:
                        return None
                    if not retry:
                        return None
                    time.sleep(interval * retry_count)

    def status(self):
        endpoint = StatusApi()
        return self.quota_retry(endpoint.do_request, (), endpoint.quotaInterval, True)

    def block_latest(self, chain: str) -> LatestBlock:
        endpoint = LatestBlockApi(self.apikey)
        return self.quota_retry(endpoint.do_request, (chain,), endpoint.quotaInterval, True)

    def transactions(self, chain: str, filter_type: str = None, start: int = None, end: int = None, limit: int = 100):
        endpoint = TransactionApi(self.apikey, debug=self.debug)
        return self.quota_retry(endpoint.do_request,
                                (chain, filter_type, start, end, limit), endpoint.quotaInterval, True)

    def pool_sandwiched(self, chain: str, duration: int = 30, page: int = 0, limit: int = 100):
        endpoint = PoolSandwichedApi(self.apikey)
        return self.quota_retry(endpoint.do_request, (chain, duration, page, limit), endpoint.quotaInterval, True)

    async def subscribe_transactions(self, chain: str = 'all', filter_type: str = 'all', filter_duplicate: bool = True,
                                     callback=None):

        livestream = LivestreamSubscription(apikey=self.apikey, host=self.host, chain=chain, filter_type=filter_type,
                                            cache=self._local_subscription_cache, filter_duplicate=filter_duplicate,
                                            callback=callback, debug=self.debug)
        await self.quota_retry(livestream.subscribe, (), livestream.quotaInterval, True)


