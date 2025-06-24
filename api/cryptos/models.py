from pydantic import Field
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class CryptoModel(CustomBaseModel):
    name: str
    symbol: str
    price_usd: float
    market_cap_usd: float
    volume_24h_usd: float
    change_24h: float
    last_updated: datetime


class CryptoTransactionModel(CustomBaseModel):
    sender: str
    receiver: str
    crypto_symbol: str
    amount: float
    fee: float
    timestamp: datetime
    status: str = Field(..., description="e.g. 'completed', 'pending', 'failed'")


class CryptoPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated cryptos list """
    results: list[CryptoModel] = Field(default_factory=list)


class CryptoTransactionPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated crypto transactions list """
    results: list[CryptoTransactionModel] = Field(default_factory=list)
