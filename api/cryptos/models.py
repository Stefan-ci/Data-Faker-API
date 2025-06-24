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


class CryptoPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated cryptos list """
    results: list[CryptoModel] = Field(default_factory=list)
