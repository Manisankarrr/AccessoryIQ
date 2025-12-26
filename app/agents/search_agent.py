import requests
from urllib.parse import urlparse
from config.settings import settings
import logging


class SearchAgent:
    """
    Tiered Search Agent with confidence scoring.
    """

    OFFICIAL_DOMAINS = {
        "apple.com",
        "support.apple.com",
        "developer.apple.com",
        "samsung.com",
        "sony.com",
        "playstation.com",
        "dell.com",
        "hp.com",
        "asus.com",
        "nvidia.com",
        "amd.com"
    }

    COMMUNITY_DOMAINS = {
        "reddit.com",
        "stackoverflow.com",
        "superuser.com",
        "ifixit.com"
    }

    def search(self, product, accessory):
        logging.info(f"[SEARCH] Triggered for: {product} | {accessory}")

        query = f"{product} {accessory} compatibility"

        headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {"q": query, "num": 10}

        try:
            r = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=payload,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            logging.error(f"[SEARCH ERROR] {e}")
            return self._refusal()

        return self._process_results(data)

    def _process_results(self, data):
        organic = data.get("organic", [])

        official = []
        community = []

        for r in organic:
            url = r.get("link", "")
            domain = urlparse(url).netloc.lower()

            entry = {
                "title": r.get("title", "Accessory"),
                "snippet": r.get("snippet", ""),
                "url": url
            }

            if any(d in domain for d in self.OFFICIAL_DOMAINS):
                official.append(entry)
            elif any(d in domain for d in self.COMMUNITY_DOMAINS):
                community.append(entry)

        if official:
            return self._format(
                official,
                confidence=0.9,
                label="Official documentation"
            )

        if community:
            return self._format(
                community,
                confidence=0.65,
                label="Community-verified sources"
            )

        return self._refusal()

    def _format(self, results, confidence, label):
        lines = ["Recommended:"]

        for r in results[:3]:
            lines.append(f"- {r['title']}")
            lines.append(f"  Reason: {r['snippet']}")
            lines.append(f"  Source: {r['url']}")

        lines.append(f"\nConfidence: {confidence}")
        lines.append(f"Source Type: {label}")

        return "\n".join(lines)

    def _refusal(self):
        return (
            "REFUSAL:\n"
            "No reliable official or community evidence found.\n"
            "Confidence: 0.0"
        )
