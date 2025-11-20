import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from src.logger import get_logger
import re

logger = get_logger('feature_engineering', 'feature_engineering.log')

KEYWORDS = {
    "XSS": [
        r"<script\b",
        r"script\s*injection",
        r"javascript:",
        r"javascript\s*:",
        r"on\w+\s*=",
        r"dom[\s\-]*xss",
        r"html[\s\-]*injection",
        r"raw\s*html",
        r"innerhtml",
        r"outerhtml",
        r"cross[\s\-]*site scripting",
        r"xss\b",
        r"arbitrary\s*(script|javascript)",
        r"event\s*handler",
        r"unescaped\s*html",
        r"reflected\s*xss",
        r"stored\s*xss",
        r"persistent\s*xss",
        r"saniti[sz]ation\s*issue",
    ],

    "SQLi": [
        r"sql",
        r"sql[\s\-]*injection",
        r"injection",
        r"union\s+select",
        r"boolean\s*based",
        r"error\s*based",
        r"time[\s\-]*based",
        r"blind\s*sqli",
        r"unsanitized\s*input",
        r"raw\s*query",
        r"concatenated\s*sql",
    ],

    "RCE": [
        r"remote\s*code",
        r"command\s*execution",
        r"code\s*execution",
        r"execute\s*arbitrary",
        r"system\s*\(",
        r"os[\s\-]*command",
        r"deserialization\s*attack",
        r"unsafe\s*eval",
        r"dynamic\s*code",
        r"template\s*injection",
    ],

    "DoS": [
        r"denial\s*of\s*service",
        r"dos\b",
        r"crash",
        r"resource\s*exhaustion",
        r"infinite\s*loop",
        r"unbounded\s*memory",
        r"cpu\s*exhaustion",
        r"amplification\s*attack",
    ],

    "CSRF": [
        r"csrf",
        r"cross[\s\-]*site[\s\-]*request",
        r"forgery",
        r"missing\s*token",
        r"no\s*csrf",
        r"invalid\s*csrf",
    ],

    "AuthBypass": [
        r"auth\s*bypass",
        r"authentication\s*bypass",
        r"unauthorized",
        r"no\s*auth",
        r"missing\s*auth",
        r"weak\s*authentication",
        r"hardcoded\s*credentials",
        r"default\s*password",
    ],

    "PrivEsc": [
        r"privilege\s*escalation",
        r"elevate\s*privileges",
        r"admin\s*access",
        r"root\s*access",
        r"higher\s*privileges",
        r"insecure\s*permissions",
    ],

    "PathTraversal": [
        r"\.\./",
        r"path\s*traversal",
        r"directory\s*traversal",
        r"arbitrary\s*file\s*read",
        r"file\s*read\s*out\s*of\s*root",
        r"escape\s*directory",
        r"unsanitized\s*path",
    ],

    "SSRF": [
        r"ssrf",
        r"server\s*side\s*request",
        r"internal\s*request",
        r"metadata\s*service",
        r"localhost\s*access",
        r"internal\s*network",
        r"open\s*redirect\s*to\s*internal",
    ],

    "InfoDisclosure": [
        r"information\s*disclosure",
        r"leak",
        r"data\s*leak",
        r"sensitive\s*data",
        r"debug\s*information",
        r"stack\s*trace",
        r"exposes\s*internal",
        r"pii\s*exposed",
    ],

    "Other": [
        r"undefined\s*behavior",
        r"improper\s*validation",
        r"misconfiguration",
        r"unsafe\s*defaults",
        r"improper\s*handling",
        r"weak\s*security",
        r"logic\s*issue",
    ],
}

CVSS_PATTERNS = [
    r"remote",
    r"local",
    r"network",
    r"adjacent",
    r"physical",
    r"low\s*complexity",
    r"high\s*complexity",
    r"privilege",
    r"privileges",
    r"elevated",
    r"admin",
    r"user\s*interaction",
    r"interaction\s*required",
    r"no\s*user\s*interaction",
    r"overflow",
    r"buffer",
    r"use\s*after\s*free",
    r"out\s*of\s*bounds",
    r"oob",
    r"null\s*dereference",
    r"race\s*condition",
    r"memory\s*corruption",
    r"double\s*free",
    r"heap",
    r"stack",
    r"rce",
    r"execute",
    r"arbitrary\s*code",
    r"command\s*execution",
    r"code\s*execution",
    r"execute\s*commands",
    r"bypass",
    r"authentication\s*bypass",
    r"authorization\s*bypass",
    r"denial",
    r"dos\b",
    r"crash",
    r"resource\s*exhaustion",
    r"confidentiality",
    r"integrity",
    r"availability",
    r"high\s*impact",
    r"low\s*impact",
    r"partial",
    r"complete",
    r"access\s*control",
    r"exposure",
    r"leak",
    r"information\s*disclosure",
    r"validation",
    r"sanitization",
    r"unsanitized",
]

class FeatureCreatorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        logger.info("Creating new features...")
        X = X.copy()

        if 'vendor' in X.columns:
            vendor_freq = X['vendor'].value_counts(normalize=True)
            X['vendor_freq'] = X['vendor'].map(vendor_freq)

        if 'product' in X.columns:
            product_freq = X['product'].value_counts(normalize=True)
            X['product_freq'] = X['product'].map(product_freq)

        if 'description' in X.columns:
            desc = X["description"].astype(str)

            X['desc_len'] = desc.apply(len)
            X['desc_word_count'] = desc.apply(lambda x: len(x.split()))
            X['desc_num_count'] = desc.apply(lambda x: sum(c.isdigit() for c in x))
            X['desc_upper_ratio'] = desc.apply(lambda x: sum(c.isupper() for c in x) / max(len(x), 1))
            X['desc_exclamation'] = desc.apply(lambda x: x.count('!'))
            X['desc_question'] = desc.apply(lambda x: x.count('?'))
        else:
            desc = pd.Series([""] * len(X))

        if 'vendor_freq' in X.columns and 'product_freq' in X.columns:
            X['vendor_product_interaction'] = X['vendor_freq'] * X['product_freq']

        for cat, patterns in KEYWORDS.items():
            X[f"{cat}_score"] = desc.apply(
                lambda t: sum(1 for p in patterns if re.search(p, t, flags=re.I))
            )

        X["cvss_keywords_score"] = desc.apply(
            lambda t: sum(1 for p in CVSS_PATTERNS if re.search(p, t, flags=re.I))
        )

        return X

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'logger' in state:
            del state['logger']
        return state