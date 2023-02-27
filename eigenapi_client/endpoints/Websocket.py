import json
import ssl
import certifi
import websockets
from eigenapi_client import Transaction, ERROR_CODE


class OrderedSetQueue(object):
    def __init__(self, maxsize: int = 1000):
        self._max_size = maxsize
        self.data = []

    def put(self, item: Transaction):
        if len(self.data) > self._max_size:
            self.data.pop()
        self.data.append(item.transactionHash)

    def __contains__(self, item: Transaction):
        return self.data.__contains__(item.transactionHash)


class LivestreamSubscription(object):

    def __init__(self, apikey: str, host: str = 'api.eigenapi.io', chain: str = 'all', filter_type: str = 'all',
                 cache: OrderedSetQueue = None, filter_duplicate: bool = True, callback=None, debug: bool = False):
        self.chain = chain
        self.filter_type = filter_type
        self.filter_duplicate = filter_duplicate
        self.callback = callback
        self.apikey = apikey
        self.host = host
        self.debug = debug
        self.url = f"wss://{self.host}/ws?chain={chain}&type={filter_type}&apikey={self.apikey}"
        self._local_subscription_cache = cache
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.load_verify_locations(certifi.where())

    def __auto_remove_duplicate_transactions__(self, transaction: Transaction) -> Transaction or None:
        if not self._local_subscription_cache.__contains__(transaction):
            self._local_subscription_cache.put(transaction)
            return transaction
        else:
            if self.debug:
                print("duplicate transaction received", transaction.transactionHash)
            return None

    def consumer_handler(self, message):
        tx = json.loads(message)
        if tx is None:
            return
        transaction = Transaction(tx)
        if transaction is None:
            return
        if self.filter_duplicate:
            transaction = self.__auto_remove_duplicate_transactions__(transaction)
        if transaction is not None:
            self.callback(transaction)

    async def subscribe(self):
        if self.callback is None:
            print("Setup message callback please")
            return
        try:
            async with websockets.connect(self.url, ssl=self.ssl_context) as websocket:
                while True:
                    response = await websocket.recv()
                    self.consumer_handler(response)
        except websockets.InvalidStatusCode as e:
            if e.status_code in ERROR_CODE:
                raise Exception(e.status_code, ERROR_CODE[e.status_code])
            else:
                raise Exception(e.status_code, str(e))
        except Exception as e:
            raise Exception(str(e))




