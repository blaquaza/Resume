#!/usr/bin/env python3
"""
Phishing URL Analyzer
Scores URLs for common phishing red flags using heuristics —
no external services or network calls required. Standard library only.
"""

import re
import argparse
from urllib.parse import urlparse

SUSPICIOUS_TLDS = {
    "zip", "mov", "xyz", "top", "gq", "tk", "ml", "cf", "work", "click",
}

BRAND_KEYWORDS = {
    "paypal", "microsoft", "apple", "google", "amazon", "netflix",
    "bank", "facebook", "instagram", "outlook", "office365", "icloud",
}

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly",
}


def looks_like_ip(hostname: str) -> bool:
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname))


def has_homoglyph_risk(hostname: str) -> bool:
    """Flag mixed-script or lookalike-character domains."""
    return bool(re.search(r"[а-яА-Я]", hostname)) or "xn--" in hostname


def contains_brand_but_wrong_domain(hostname: str, full_url: str) -> list[str]:
    flags = []
    parts = hostname.split(".")
    registrable = ".".join(parts[-2:]) if len(parts) >= 2 else hostname
    for brand in BRAND_KEYWORDS:
        if brand in full_url.lower() and brand not in registrable.lower():
            flags.append(f"Mentions '{brand}' but domain is '{registrable}'")
    return flags


def analyze_url(url: str) -> dict:
    issues = []
    score = 0

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    full = url.lower()

    if parsed.scheme == "http":
        issues.append("Uses unencrypted HTTP instead of HTTPS")
        score += 1

    if looks_like_ip(hostname):
        issues.append("Hostname is a raw IP address, not a domain name")
        score += 3

    if has_homoglyph_risk(hostname):
        issues.append("Contains non-Latin characters or punycode (possible lookalike domain)")
        score += 3

    if hostname in URL_SHORTENERS:
        issues.append("Uses a URL shortener, which can hide the real destination")
        score += 2

    tld = hostname.split(".")[-1] if "." in hostname else ""
    if tld in SUSPICIOUS_TLDS:
        issues.append(f"Uses a TLD often associated with abuse ('.{tld}')")
        score += 2

    if hostname.count("-") >= 3:
        issues.append("Domain has an unusually high number of hyphens")
        score += 1

    if hostname.count(".") >= 4:
        issues.append("Domain has an unusually deep subdomain structure")
        score += 1

    if len(url) > 90:
        issues.append("URL is unusually long")
        score += 1

    issues.extend(contains_brand_but_wrong_domain(hostname, full))
    if any("Mentions" in i for i in issues):
        score += 3

    if re.search(r"(login|verify|secure|account|update|confirm).{0,20}(paypal|bank|apple|microsoft)", full):
        issues.append("Combines urgency/login keywords with a brand name")
        score += 2

    if score >= 6:
        risk = "High"
    elif score >= 3:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "url": url,
        "hostname": hostname,
        "risk": risk,
        "score": score,
        "issues": issues or ["No red flags detected"],
    }


def print_report(result: dict) -> None:
    print(f"\nURL:      {result['url']}")
    print(f"Hostname: {result['hostname']}")
    print(f"Risk:     {result['risk']}  (score: {result['score']})")
    print("Flags:")
    for issue in result["issues"]:
        print(f"  - {issue}")


def main():
    parser = argparse.ArgumentParser(
        description="Score URLs for common phishing heuristics (no network calls)."
    )
    parser.add_argument("urls", nargs="*", help="One or more URLs to check")
    parser.add_argument("-f", "--file", help="Path to a file with one URL per line")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.file:
        with open(args.file) as f:
            urls.extend(line.strip() for line in f if line.strip())

    if not urls:
        print("No URLs provided. Use positional args or --file.")
        return

    for url in urls:
        result = analyze_url(url)
        print_report(result)
    print()


if __name__ == "__main__":
    main()