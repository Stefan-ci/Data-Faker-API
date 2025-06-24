import random
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
        selected = random.sample(self.cryptos_list, k=min(n, len(self.cryptos_list)))
        return [
            self._build_crypto(i, name, symbol)
            for i, (name, symbol) in enumerate(selected, start=1)
        ]
    
    
    def _build_crypto(self, id: int, name: str, symbol: str):
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


def generate_cryptos_data(length=10):
    return CryptoGenerator().generate(n=length)
