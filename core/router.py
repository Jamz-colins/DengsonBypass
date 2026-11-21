from dataclasses import dataclass
from urllib.parse import urlparse
from core.cleaner import clean_tracking_params
from core.domains import KNOWN_SHORTENERS, REDIRECT_WRAPPERS
from core.safety import SafetyReport, check_url_safety
from core.session import create_session
from handlers.generic import GenericRedirectHandler
from handlers.wrapper import RedirectWrapperHandler

MAX_HOPS = 10


@dataclass
class HopInfo:
    step: int
    url: str
    status_code: int | None
    method: str
    elapsed_ms: float


@dataclass
class ResolutionResult:
    original_url: str
    raw_final_url: str
    final_url: str
    removed_trackers: list[str]
    hops: list[HopInfo]
    safety: SafetyReport


class LinkRouter:
    def __init__(self):
        self.session = create_session()
        self.wrapper_handler = RedirectWrapperHandler(self.session)
        self.generic_handler = GenericRedirectHandler(self.session)

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"https://{url}"
        return url

    def is_supported_domain(self, url: str) -> bool:
        domain = urlparse(self.normalize_url(url)).netloc.lower().removeprefix("www.")
        return domain in KNOWN_SHORTENERS or domain in REDIRECT_WRAPPERS

    def bypass(self, url: str) -> ResolutionResult:
        current_url = self.normalize_url(url)
        visited: set[str] = set()
        hops: list[HopInfo] = []
        step = 1

        for _ in range(MAX_HOPS):
            if current_url in visited:
                break
            visited.add(current_url)

            # Tahap 1: Ekstrak URL wrapper (tanpa request jaringan)
            unwrapped = self.wrapper_handler.resolve(current_url)
            if unwrapped != current_url:
                hops.append(
                    HopInfo(
                        step=step,
                        url=current_url,
                        status_code=None,
                        method="WRAPPER UNWRAP",
                        elapsed_ms=0.0,
                    )
                )
                step += 1
                current_url = unwrapped
                continue

            # Tahap 2: Telusuri HTTP redirect / Meta Refresh
            next_url, status_code, method, elapsed_ms = self.generic_handler.resolve_step(
                current_url
            )
            hops.append(
                HopInfo(
                    step=step,
                    url=current_url,
                    status_code=status_code,
                    method=method,
                    elapsed_ms=elapsed_ms,
                )
            )
            step += 1

            if next_url != current_url:
                current_url = next_url
                continue

            break

        cleaned_url, removed_trackers = clean_tracking_params(current_url)
        safety_report = check_url_safety(cleaned_url, self.session)

        return ResolutionResult(
            original_url=url,
            raw_final_url=current_url,
            final_url=cleaned_url,
            removed_trackers=removed_trackers,
            hops=hops,
            safety=safety_report,
        )
