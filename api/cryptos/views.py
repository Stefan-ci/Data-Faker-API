from fastapi import  Request
from utils.viewset import BaseModelViewSet
from utils.base import StateKeywords, Endpoints
from api.cryptos.models import CryptoModel, CryptoPaginationResponse
from api.cryptos.utils import generate_cryptos_data, generate_cryptos_transactions_data
from api.cryptos.models import CryptoTransactionModel, CryptoTransactionPaginationResponse


class CryptoApiView(BaseModelViewSet):
    model = CryptoModel
    pagination_model = CryptoPaginationResponse
    state_key = StateKeywords.CRYPTOS
    verbose_name = "crypto"
    verbose_name_plural = "cryptos"
    endpoint_prefix = Endpoints.CRYPTOS_BASE_ENDPOINT.endpoint
    tags = "Cryptocurrencies"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_cryptos_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_cryptos_data(length=length))


class CryptoTransactionApiView(BaseModelViewSet):
    model = CryptoTransactionModel
    pagination_model = CryptoTransactionPaginationResponse
    state_key = StateKeywords.CRYPTO_TRANSACTIONS
    verbose_name = "crypto transaction"
    verbose_name_plural = "crypto transactions"
    endpoint_prefix = Endpoints.CRYPTOS_TRANSACTIONS_BASE_ENDPOINT.endpoint
    tags = "Cryptocurrencies"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(
            key=self.state_key, func=generate_cryptos_transactions_data, length=length
        )
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(
            key=self.state_key, value=generate_cryptos_transactions_data(length=length)
        )
