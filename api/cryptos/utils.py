import random
from faker_crypto import CryptoAddress
from utils.base import BaseDataGenerator


class CryptoGenerator(BaseDataGenerator):
    @property
    def cryptos_list(self):
        cryptos = [
            ("Bitcoin", "BTC"),
            ("Ethereum", "ETH"),
            ("Binance Coin", "BNB"),
            ("Solana", "SOL"),
            ("Cardano", "ADA"),
            ("Ripple", "XRP"),
            ("Dogecoin", "DOGE"),
            ("Polkadot", "DOT"),
            ("Litecoin", "LTC"),
            ("Chainlink", "LINK"),
        ]
        return cryptos
    
    
    def generate(self, n=10): # type: ignore
        return [
            self._build_crypto(i)
            for i in range(1, n + 1)
        ]
    
    
    def _build_crypto(self, id: int):
        choice = self.fake.random_element(self.cryptos_list)
        name = choice[0]
        symbol = choice[1]
        
        price = round(random.uniform(0.05, 70000), 2)
        market_cap = round(price * random.uniform(10_000_000, 500_000_000), 2)
        volume = round(market_cap * random.uniform(0.01, 0.25), 2)
        change = round(random.uniform(-15, 15), 2)
        
        return {
            "id": id,
            "uuid": self.fake.uuid4(),
            "name": name,
            "symbol": symbol,
            "price_usd": price,
            "market_cap_usd": market_cap,
            "volume_24h_usd": volume,
            "change_24h": change,
            "last_updated": self.fake.date_time().isoformat(),
        }




class CryptoTransactionGenerator(BaseDataGenerator):
    
    @property
    def cryptos_symbols_list(self):
        return [
            "BTC", "ETH", "BNB", "SOL", "ADA", "XRP", "LTC", "DOGE", "DOT"
        ]
    
    
    def generate(self, n=10):  # type: ignore
        # add a new crypto address provider
        self.fake.add_provider(CryptoAddress)
        return [
            self._build_data(i)
            for i in range(1, n + 1)
        ]
    
    def generate_address(self, crypto_symbol: str):
        if crypto_symbol.upper() == "BTC":
            return self.fake.bitcoin_address()
        elif crypto_symbol.upper() == "ETH":
            return self.fake.ethereum_address()
        elif crypto_symbol.upper() == "BNB":
            return self.fake.binance_smart_chain_address()
        elif crypto_symbol.upper() == "SOL":
            return self.fake.solana_address()
        elif crypto_symbol.upper() == "ADA":
            return self.fake.cardano_address()
        elif crypto_symbol.upper() == "XRP":
            return self.fake.ripple_address()
        elif crypto_symbol.upper() == "LTC":
            return self.fake.litecoin_address()
        elif crypto_symbol.upper() == "DOGE":
            return self.fake.dogecoin_address()
        elif crypto_symbol.upper() == "DOT":
            return self.fake.polygon_address()
        return self.fake.sha256()
    
    
    def _build_data(self, i: int):
        symbol = self.fake.random_element(self.cryptos_symbols_list)
        statuses = ["completed", "pending", "failed"]
        
        return {
            "id": i,
            "uuid": self.fake.uuid4(),
            "sender": self.generate_address(crypto_symbol=symbol),
            "receiver": self.generate_address(crypto_symbol=symbol),
            "crypto_symbol": symbol,
            "amount": round(random.uniform(0.001, 50), 8),
            "fee": round(random.uniform(0.0001, 0.005), 8),
            "timestamp": self.fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
            "status": self.fake.random_element(statuses),
        }







def generate_cryptos_transactions_data(length=10):
    return CryptoTransactionGenerator().generate(n=length)


def generate_cryptos_data(length=10):
    return CryptoGenerator().generate(n=length)
