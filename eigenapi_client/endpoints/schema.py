class Token(object):
    def __init__(self, data: dict, ):
        self.address: str = data['address']
        self.symbol: str = data['symbol']


class Pool(object):
    def __init__(self, data: dict):
        self.address: str = data['address']
        self.name: str = data['name']
        if 'protocol' in data:
            self.protocol: str = data['protocol']
        self.symbol: str = data['symbol']
        self.tokens = []
        if 'tokens' in data:
            for token in data['tokens']:
                self.tokens.append(Token(token))


class SandwichDetail(object):
    def __init__(self, data: dict):
        self.sandwichRole: str = data['sandwichRole']
        self.transactionIndex: int = data['transactionIndex']
        self.transactionFromAddress: str = data['transactionFromAddress']
        self.transactionHash: str = data['transactionHash']
        self.transactionToAddress: str = data['transactionToAddress']


class LiquidationDetail(object):
    def __init__(self, data: dict):
        self.borrowTokenPrice: float = data['borrowTokenPrice']
        self.borrowTokenVolume: float = data['borrowTokenVolume']
        self.borrower: str = data['borrower']
        self.collateralTokenPrice: float = data['collateralTokenPrice']
        self.collateralTokenVolume: float = data['collateralTokenVolume']
        self.liquidator: str = data['liquidator']
        self.protocol: str = data['protocol']
        self.borrowToken: Token = Token(data['borrowToken'])
        self.collateralToken: Token = Token(data['collateralToken'])


class LendingDetail(object):
    def __init__(self, data: dict):
        self.tokenAmount: float = data['tokenAmount']
        self.tokenVolume: float = data['tokenVolume']
        self.address: str = data['address']
        self.lendingType: str = data['lendingType']
        self.protocol: str = data['protocol']
        self.token: Token = Token(data['token'])


class Transaction(object):
    def __init__(self, transaction: dict):
        self.blockNumber: int = transaction['blockNumber']
        self.blockTimestamp: int = transaction['blockTimestamp']
        self.chain: str = transaction['chain']
        self.cost: float = transaction['cost']
        self.profit: float = transaction['profit']
        self.revenue: float = transaction['revenue']
        self.gasPrice: int = transaction['gasPrice']
        self.transactionFromAddress: str = transaction['transactionFromAddress']
        self.transactionHash: str = transaction['transactionHash']
        self.transactionIndex: int = transaction['transactionIndex']
        self.transactionToAddress: str = transaction['transactionToAddress']
        self.type: str = transaction['type']
        self.tokens = []
        self.id = self.blockNumber * 10000 + self.transactionIndex

        if 'tokens' in transaction:
            for token in transaction['tokens']:
                self.tokens.append(Token(token ))

        self.pools = []
        if 'pools' in transaction:
            for pool in transaction['pools']:
                self.pools.append(Pool(pool))

        self.sandwichDetails = list()
        if 'sandwichDetails' in transaction:
            for sandwichDetail in transaction['sandwichDetails']:
                self.sandwichDetails.append(SandwichDetail(sandwichDetail))

        self.lendingDetails = list()
        if 'lendingDetails' in transaction:
            for lendingDetail in transaction['lendingDetails']:
                self.lendingDetails.append(LendingDetail(lendingDetail))

        self.liquidationDetails = list()
        if 'liquidationDetails' in transaction:
            for liquidationDetail in transaction['liquidationDetails']:
                self.liquidationDetails.append(LiquidationDetail(liquidationDetail))

    def get_id(self) -> int:
        return self.id


class LatestBlock(object):
    def __init__(self, blockNumber: int, blockTimestamp: int):
        self.blockNumber: int = blockNumber
        self.blockTimestamp: int = blockTimestamp


class PoolSandwiched(object):
    def __init__(self, data: dict):
        self.sandwichedTrades: int = data['sandwichedTrades']
        self.trades: int = data['trades']
        self.sandwichedVolume: float = data['sandwichedVolume']
        self.address: str = data['address']
        self.symbol: str = data['symbol']
        self.tokens = []
        if 'tokens' in data:
            for token in data['tokens']:
                self.tokens.append(Token(token))


ERROR_CODE = {
    401: "Please provide valid API key in the apikey query parameter",
    429: "Quota limit exceeded",
    10000: "not_support_chain",
    10001: "not_support_type",
}
