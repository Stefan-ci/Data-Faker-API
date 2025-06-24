from fastapi import  Request
from utils.base import StateKeywords
from utils.viewset import BaseModelViewSet
from api.cryptos.utils import generate_cryptos_data
from api.cryptos.models import CryptoModel, CryptoPaginationResponse


class CryptoApiView(BaseModelViewSet):
    model = CryptoModel
    pagination_model = CryptoPaginationResponse
    state_key = StateKeywords.CRYPTOS
    verbose_name = "crypto"
    verbose_name_plural = "cryptos"
    endpoint_prefix = "/cryptos"
    
    def get_data_with_length(self, request: Request, length: int):
        return self.get_accessor(request).get_or_generate(key=self.state_key, func=generate_cryptos_data, length=length)
    
    def regenerate_func(self, request: Request, length: int):
        self.get_accessor(request).set(key=self.state_key, value=generate_cryptos_data(length=length))
