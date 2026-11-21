from urllib.parse import parse_qs, unquote, urlparse
from core.domains import (
    GENERIC_REDIRECT_PARAMS,
    REDIRECT_PATH_HINTS,
    REDIRECT_WRAPPERS,
)
from handlers.base import BaseHandler


class RedirectWrapperHandler(BaseHandler):
    def resolve(self, url: str) -> str:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().removeprefix("www.")
        query_params = parse_qs(parsed.query)

        if not query_params:
            return url

        # 1. Cek domain wrapper yang terdaftar secara spesifik
        candidate_keys: list[str] = []
        if domain in REDIRECT_WRAPPERS:
            candidate_keys.extend(REDIRECT_WRAPPERS[domain])

        # 2. Cek jika path URL mengindikasikan halaman redirect umum
        path_lower = parsed.path.lower()
        if any(hint in path_lower for hint in REDIRECT_PATH_HINTS):
            candidate_keys.extend(GENERIC_REDIRECT_PARAMS)

        for key in candidate_keys:
            values = query_params.get(key)
            if not values:
                continue
            extracted = unquote(values[0]).strip()
            if extracted.startswith(("http://", "https://")):
                return extracted

        return url
