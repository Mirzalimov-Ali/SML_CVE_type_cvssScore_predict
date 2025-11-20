import requests, json, gzip, io, time, random
from dateutil import parser as dp
from tqdm import tqdm
from src.logger import get_logger

logger = get_logger('data_extraction', 'data_extraction.log')

class DataExtractor:
    def __init__(self, years=None):
        self.years = years or []

    def safe_get(self, url, api_key=None, params=None):
        headers = {"User-Agent": "Mozilla/5.0"}
        if api_key:
            headers["apiKey"] = api_key
        for i in range(6):
            try:
                r = requests.get(url, params=params, headers=headers, timeout=30)
                if r.status_code == 429:
                    logger.warning(f"Rate limit hit, retrying in {2**i:.1f}s...")
                    time.sleep((2 ** i) + random.random())
                    continue
                r.raise_for_status()
                logger.info(f"Successfully fetched: {url}")
                return r
            except requests.RequestException as e:
                logger.warning(f"Request failed: {e}, retrying in {2**i:.1f}s...")
                time.sleep((2 ** i) + random.random())
        raise RuntimeError(f"Failed GET {url}")

    def parse_cve(self, cve):
        d = next((x["value"] for x in cve.get("descriptions", []) if x.get("lang") == "en"), "")
        if not d and cve.get("descriptions"):
            try:
                d = cve["descriptions"][0].get("value", "")
            except Exception:
                d = ""

        s = None
        for k in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2", "cvssMetricV4"):
            m = cve.get("metrics", {}).get(k)
            if m:
                try:
                    s = float(m[0].get("cvssData", {}).get("baseScore"))
                except Exception:
                    pass
                if s is not None:
                    break

        # CVSS kategoriyasi
        cvss_category = None
        if s is not None:
            if 0 <= s <= 3.9:
                cvss_category = "Low"
            elif 4 <= s <= 6.9:
                cvss_category = "Medium"
            elif 7 <= s <= 8.9:
                cvss_category = "High"
            elif 9 <= s <= 10:
                cvss_category = "Critical"

        w = ""
        try:
            if cve.get("weaknesses"):
                w = cve["weaknesses"][0]["description"][0].get("value", "")
        except Exception:
            w = ""

        v, p = "", ""
        try:
            nodes = cve.get("configurations", [])[0].get("nodes", [])
            if nodes and "cpeMatch" in nodes[0]:
                uri = nodes[0]["cpeMatch"][0].get("criteria", "")
                parts = uri.split(":")
                if len(parts) >= 5:
                    v, p = parts[3], parts[4]
        except Exception:
            pass

        pub = cve.get("published", "")
        try:
            pub = dp.parse(pub).strftime("%Y-%m-%d")
        except Exception:
            pass

        return {
            "cve_id": cve.get("id", "") or cve.get("CVE_data_meta", {}).get("ID", ""),
            "description": d,
            "cvss_score": cvss_category,
            "cwe": w,
            "vendor": v,
            "product": p,
            "publish_date": pub
        }

    @staticmethod
    def classify(cwe, desc):
        t = (desc or "").lower()
        if "xss" in t or str(cwe).startswith("CWE-79"): return "XSS"
        if "sql injection" in t or str(cwe).startswith("CWE-89"): return "SQLi"
        if "code execution" in t or str(cwe).startswith("CWE-94"): return "RCE"
        if "traversal" in t or str(cwe).startswith("CWE-22"): return "PathTraversal"
        if "privilege escalation" in t or cwe in ("CWE-269","CWE-264"): return "PrivEsc"
        if "authentication bypass" in t or str(cwe).startswith("CWE-287"): return "AuthBypass"
        if "information disclosure" in t or str(cwe).startswith("CWE-2"): return "InfoDisclosure"
        if "ssrf" in t or str(cwe).startswith("CWE-918"): return "SSRF"
        if "csrf" in t: return "CSRF"
        if "denial of service" in t or "dos" in t: return "DoS"
        return "Other"

    def fetch_feed_year(self, year, feed_url, api_key=None):
        rows = []
        logger.info(f"Fetching feed for {year}...")
        url = feed_url + f"nvdcve-2.0-{year}.json.gz"
        r = self.safe_get(url, api_key=api_key)
        if r.status_code != 200:
            logger.error(f"Failed to fetch feed for {year}")
            return rows
        with gzip.GzipFile(fileobj=io.BytesIO(r.content)) as f:
            try:
                j = json.load(f)
            except Exception as e:
                logger.error(f"Failed to parse JSON for {year}: {e}")
                return rows

        items = j.get("vulnerabilities") or j.get("CVE_Items") or []
        for v in tqdm(items, desc=f"CVE {year}"):
            c = v.get("cve") if isinstance(v, dict) and v.get("cve") else v
            try:
                rows.append(self.parse_cve(c))
            except Exception as e:
                logger.warning(f"Skipping item due parse error: {e}")
        logger.info(f"Finished fetching {len(rows)} CVEs for {year}")
        time.sleep(1 + random.random())
        return rows