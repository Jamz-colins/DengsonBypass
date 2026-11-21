from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_PARAMS: set[str] = {
    "fbclid", "gclid", "dclid", "gbraid", "wbraid", "msclkid",
    "yclid", "twclid", "ttclid", "li_fat_id",
    "si", "igshid", "igsh", "feature", "pp",
    "mc_cid", "mc_eid", "_hsenc", "_hsmi", "mkt_tok",
    "ref_src", "ref_url", "spm", "scm", "vero_id",
}

TRACKING_PREFIXES: tuple[str, ...] = (
    "utm_",
    "hsa_",
    "mtm_",
    "pk_",
    "piwik_",
)


def clean_tracking_params(url: str) -> tuple[str, list[str]]:
    """
    Menghapus parameter pelacak dari URL.
    Mengembalikan tuple (url_bersih, daftar_parameter_yang_dihapus).
    """
    parts = urlsplit(url)
    if not parts.query:
        return url, []

    kept_params: list[tuple[str, str]] = []
    removed_params: list[str] = []

    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        key_lower = key.lower()
        if key_lower in TRACKING_PARAMS or key_lower.startswith(TRACKING_PREFIXES):
            removed_params.append(key)
        else:
            kept_params.append((key, value))

    cleaned_query = urlencode(kept_params, doseq=True)
    cleaned_url = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, cleaned_query, parts.fragment)
    )
    return cleaned_url, removed_params
