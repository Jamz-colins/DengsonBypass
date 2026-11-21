import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from handlers.base import BaseHandler

META_REFRESH_RE = re.compile(r"url\s*=\s*['\"]?([^'\"\s>]+)", re.IGNORECASE)


class GenericRedirectHandler(BaseHandler):
    def resolve_step(self, url: str) -> tuple[str, int, str, float]:
        """
        Menelusuri satu langkah redirect.
        Mengembalikan (next_url, status_code, method, elapsed_ms).
        """
        start = time.perf_counter()
        response = self.session.get(url, allow_redirects=False, timeout=15)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # 1. HTTP Redirect Header (301, 302, 303, 307, 308)
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location")
            if location:
                next_url = urljoin(url, location.strip())
                return next_url, response.status_code, f"HTTP {response.status_code}", elapsed_ms

        response.raise_for_status()

        # 2. HTML <meta http-equiv="refresh" content="0;url=...">
        content_type = response.headers.get("Content-Type", "").lower()
        if "text/html" in content_type:
            soup = BeautifulSoup(response.text, "html.parser")
            meta = soup.find(
                "meta",
                attrs={"http-equiv": lambda val: val and val.lower() == "refresh"},
            )
            if meta and meta.get("content"):
                match = META_REFRESH_RE.search(meta["content"])
                if match:
                    next_url = urljoin(url, match.group(1).strip())
                    return next_url, response.status_code, "META REFRESH", elapsed_ms

        return url, response.status_code, "FINAL", elapsed_ms

    def resolve(self, url: str) -> str:
        next_url, _, _, _ = self.resolve_step(url)
        return next_url
