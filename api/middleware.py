from fastapi import Request
from api.base import AppStateAccessor, StateKeywords
from starlette.middleware.base import BaseHTTPMiddleware

class LocaleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next): # type: ignore
        accessor = AppStateAccessor(request.app.state)
        locale = self._get_locale(request=request)
        accessor.set(key=StateKeywords.LOCALE_LANG, value=locale)
        response = await call_next(request)
        return response
    
    def _get_locale(self, request: Request):
        locale = (
            request.query_params.get("locale") or
            request.headers.get("Accept-Language") or
            "en_US"
        )
        
        # returns first lang if a list is provided
        if "," in locale:
            locale = locale.split(",")[0].strip()
        return locale
