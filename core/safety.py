import base64
import ipaddress
import os
from dataclasses import dataclass
from urllib.parse import urlparse
import requests

SUSPICIOUS_TLDS: set[str] = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".top", ".xyz",
    ".click", ".work", ".zip", ".mov", ".rest", ".cam",
}

DANGEROUS_EXTENSIONS: tuple[str, ...] = (
    ".exe", ".apk", ".bat", ".cmd", ".scr", ".ps1",
    ".vbs", ".msi", ".dmg", ".sh", ".deb", ".rpm",
)


@dataclass
class SafetyReport:
    level: str          # "AMAN" | "WASPADA" | "BERISIKO"
    color: str          # Warna badge Rich
    findings: list[str]
    vt_summary: str | None = None


def _check_virustotal(url: str, session: requests.Session) -> tuple[str | None, int]:
    api_key = os.environ.get("VT_API_KEY", "").strip()
    if not api_key:
        return None, 0

    url_id = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    try:
        res = session.get(endpoint, headers={"x-apikey": api_key}, timeout=10)
        if res.status_code == 200:
            stats = (
                res.json()
                .get("data", {})
                .get("attributes", {})
                .get("last_analysis_stats", {})
            )
            malicious = int(stats.get("malicious", 0))
            suspicious = int(stats.get("suspicious", 0))
            total = sum(int(v) for v in stats.values())
            summary = f"VirusTotal: {malicious} malicious, {suspicious} suspicious (dari {total} engine)"
            return summary, malicious + suspicious
        if res.status_code == 404:
            return "VirusTotal: URL belum pernah dipindai di database VT", 0
    except requests.RequestException:
        return "VirusTotal: Gagal terhubung ke API", 0

    return None, 0


def check_url_safety(url: str, session: requests.Session) -> SafetyReport:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path_lower = parsed.path.lower()
    findings: list[str] = []
    risk_score = 0

    # 1. Cek protokol tidak terenkripsi
    if parsed.scheme == "http":
        findings.append("Menggunakan HTTP tanpa enkripsi TLS/SSL")
        risk_score += 1

    # 2. Cek teknik phishing '@' pada URL (contoh: https://google.com@evil.com)
    if "@" in parsed.netloc:
        findings.append("Terdeteksi karakter '@' pada host (indikasi spoofing/phishing)")
        risk_score += 3

    # 3. Cek penggunaan alamat IP langsung sebagai host
    try:
        ipaddress.ip_address(host)
        findings.append(f"Host menggunakan alamat IP mentah ({host})")
        risk_score += 2
    except ValueError:
        pass

    # 4. Cek domain Punycode / IDN Homograph Attack
    if "xn--" in host:
        findings.append("Domain menggunakan encoding Punycode (potensi homograph spoofing)")
        risk_score += 2

    # 5. Cek TLD yang sering disalahgunakan
    if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
        findings.append("Menggunakan ekstensi domain (TLD) berisiko tinggi")
        risk_score += 1

    # 6. Cek tautan unduhan file eksekusi langsung
    if any(path_lower.endswith(ext) for ext in DANGEROUS_EXTENSIONS):
        findings.append("Mengarah langsung ke file eksekusi / installer")
        risk_score += 2

    # 7. Cek VirusTotal jika VT_API_KEY tersedia
    vt_summary, vt_hits = _check_virustotal(url, session)
    if vt_hits > 0:
        risk_score += 3

    if risk_score >= 3:
        level, color = "BERISIKO", "bold red"
    elif risk_score >= 1:
        level, color = "WASPADA", "bold yellow"
    else:
        level, color = "AMAN", "bold green"

    if not findings:
        findings.append("Tidak ditemukan pola phishing atau parameter berbahaya")

    return SafetyReport(
        level=level,
        color=color,
        findings=findings,
        vt_summary=vt_summary,
    )
