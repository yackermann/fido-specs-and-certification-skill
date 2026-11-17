#!/usr/bin/env python3
"""Browse the FIDO Metadata Service (MDS3) BLOB from a local cache.

  python3 scripts/mds.py update [--force]       download the BLOB (max 2 pulls per 24 h), verify, cache
  python3 scripts/mds.py info                    BLOB number, nextUpdate, verification, pull budget, stats
  python3 scripts/mds.py search TERMS... [--status S] [--protocol fido2|uaf|u2f] [--limit N]
  python3 scripts/mds.py show ID [--json] [--icon]   one entry: AAGUID, AAID, key identifier or name

FIDO limits BLOB downloads to two per day, so the BLOB is downloaded only by `update`, which
refuses when the limit is reached. Every other command reads the cached copy.

The JWT signature and certificate chain are checked against GlobalSign Root R46, the root FIDO
publishes for the BLOB (https://fidoalliance.org/metadata/). The root is embedded below; no system
certificate store is used. Only the standard library is needed. CRLs are not checked.

Cache: $FIDO_SPEC_CACHE/mds or ~/.cache/fido-spec-and-certification/mds
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

CACHE = Path(os.environ.get("FIDO_SPEC_CACHE", Path.home() / ".cache" / "fido-spec-and-certification")) / "mds"
# No temp-folder fallback here: the pull log must persist, or the two-per-day limit could be exceeded.
UA = "fido-spec-and-certification-skill/0.1 (mds)"
MDS_URL = "https://mds.fidoalliance.org/"
LEGAL = "https://fidoalliance.org/metadata/metadata-legal-terms/"
MAX_PULLS, WINDOW = 2, dt.timedelta(hours=24)
BLOB, META, LOG = CACHE / "blob.jwt", CACHE / "meta.json", CACHE / "pulls.json"
LEAF_CN = "mds.fidoalliance.org"

# GlobalSign Root R46 (self-signed, valid 2019-03-20 to 2046-03-20), the MDS3 trust anchor named on
# https://fidoalliance.org/metadata/. Source: https://secure.globalsign.com/cacert/rootr46.crt
ROOT_R46 = """
MIIFWjCCA0KgAwIBAgISEdK7udcjGJ5AXwqdLdDfJWfRMA0GCSqGSIb3DQEBDAUAMEYxCzAJBgNV
BAYTAkJFMRkwFwYDVQQKExBHbG9iYWxTaWduIG52LXNhMRwwGgYDVQQDExNHbG9iYWxTaWduIFJv
b3QgUjQ2MB4XDTE5MDMyMDAwMDAwMFoXDTQ2MDMyMDAwMDAwMFowRjELMAkGA1UEBhMCQkUxGTAX
BgNVBAoTEEdsb2JhbFNpZ24gbnYtc2ExHDAaBgNVBAMTE0dsb2JhbFNpZ24gUm9vdCBSNDYwggIi
MA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQCsrHQy6LNl5brtQyYdpokNRbopiLKkHWPd08Es
CVeJOaFV6Wc0dwxu5FUdUiXSE2te4R2pt32JMl8Nnp8semNgQB+msLZ4j5lUlghYruQGvGIFAha/
r6gjA7aUD7xubMLL1aa7DOn2wQL7Id5m3RerdELv8HQvJfTqa1VbkNud316HCkD7rRlr+/fKYIje
2sGP1q7Vf9Q8g+7XFkyDRTNrJ9CG0Bwta/OrffGFqfUo0q3v84RLHIf8E6M6cqJaESvWJ3En7YEt
bWaBkoe0G1h6zD8K+kZPTXhc+CtI4wSEy132tGqzZfxCnlEmIyDLPRT5ge1lFgBPGmSXZgjPjHvj
K8Cd+RTyG/FWaha/LIWFzXg4mutCagI0GIMXTpRW+LaCtfOW3T3zvn8gdz57GSNrLNRyc0NXfeD4
12lPFzYE+cCQYDdF3uYM2HSNrpyibXRdQr4G9dlkbgIQrImwTDsHTUB+JMWKmIJ5jqSngiCNI/on
ccnfxkF0oE32kRbcRoxfKWMxWXEM2G/CtjJ9++ZdU6Z+Ffy7dXxd7Pj2Fxzsx2sZy/N78CsHpdls
eVR2bJ0cpm4O6XkMqCNqo98bMDGfsVR7/mrLZqrcZdCinkqaByFrgY/bxFn63iLABJzjqls2k+g9
vXqhnQt2sQvHnf3PmKgGwvgqo6GDoLclcqUC4wIDAQABo0IwQDAOBgNVHQ8BAf8EBAMCAYYwDwYD
VR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA1yrc4GHqMywptWU4jaWSf8FmSwwDQYJKoZIhvcNAQEM
BQADggIBAHx47PYCLLtbfpIrXTncvtgdokIzTfnvpCo7RGkerNlFo048p9gkUbJUHJNOxO97k4Vg
JuoJSOD1u8fpaNK7ajFxzHmuEajwmf3lH7wvqMxX63bEIaZHU1VNaL8FpO7XJqti2kM3S+LGteWy
gxk6x9PbTZ4IevPuzz5i+6zoYMzRx6Fcg0XERczzF2sUyQQCPtIkpnnpHs6i58FZFZ8d4kuaPp92
CC1r2LpXFNqD6v6MVenQTqnMdzGxRBF6XLE+0xRFFRhiJBPSy03OXIPBNvIQtQ6IbbjhVp+J3pZm
OUdkLG5NrmJ7v2B0GbhWrJKsFjLtrWhV/pi60zTe9Mlhww6G9kuEYO4Ne7UyWHmRVSyBQ7N0H3qq
JZ4d16GLuc1CLgSkZoNNiTW2bKg2SnkheCLQQrzRQDGQob4Ez8pn7fXwgNNgyYMqIgXQBztSvwye
qiv5u+YfjyW6hY0XHgL+XVAEV8/+LbzvXMAaq7afJMbfc2hIkCwU9D9SGuTSyxTDYWnP4vkYxboz
nxSjBF25cfe1lNj2M8FawTSLfJvdkzrnE6JwYZ+vj+vYxXX4M2bUdGc6N3ec592kD3ZDZopD8p/7
DEJ4Y9HiD2971KE9dJeFt0g5QdYg/NA6s/rob8SKunE3vouXsXgxT7PntgMTzlSdriVZzH81Xwj3
QEUxeCp6
"""
ROOT_SHA256 = "4fa3126d8d3a11d1c4855a4f807cbad6cf919d3a5a88b03bea2c6372d93c40c9"


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def b64url(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


# ---------- minimal DER / X.509 / RSA (enough to verify the MDS chain) ----------

def tlv(b: bytes, i: int = 0):
    """Return (tag, value_start, value_end) of the DER element at offset i."""
    tag, ln = b[i], b[i + 1]
    i += 2
    if ln & 0x80:
        n = ln & 0x7F
        ln = int.from_bytes(b[i:i + n], "big")
        i += n
    return tag, i, i + ln


def children(b: bytes, start: int, end: int):
    out, i = [], start
    while i < end:
        t, s, e = tlv(b, i)
        out.append((t, s, e, i))  # i = element start (header included)
        i = e
    return out


SIG_ALGS = {  # OID bytes -> (hashlib name, DigestInfo prefix)
    bytes.fromhex("2a864886f70d01010b"): ("sha256", "3031300d060960864801650304020105000420"),
    bytes.fromhex("2a864886f70d01010c"): ("sha384", "3041300d060960864801650304020205000430"),
    bytes.fromhex("2a864886f70d01010d"): ("sha512", "3051300d060960864801650304020305000440"),
}
OID_CN = bytes.fromhex("550403")
OID_BASIC = bytes.fromhex("551d13")


def rsa_verify(n: int, e: int, data: bytes, sig: bytes, hname: str, prefix: str) -> bool:
    k = (n.bit_length() + 7) // 8
    if len(sig) != k:
        return False
    em = pow(int.from_bytes(sig, "big"), e, n).to_bytes(k, "big")
    t = bytes.fromhex(prefix) + hashlib.new(hname, data).digest()
    return em == b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t


def parse_time(b: bytes, t: int) -> dt.datetime:
    s = b.decode()
    fmt = "%y%m%d%H%M%SZ" if t == 0x17 else "%Y%m%d%H%M%SZ"
    return dt.datetime.strptime(s, fmt).replace(tzinfo=dt.timezone.utc)


def parse_cert(der: bytes) -> dict:
    _, s, e = tlv(der)
    tbs, alg, sig = children(der, s, e)[:3]
    tbs_raw = der[tbs[3]:tbs[2]]
    f = children(der, tbs[1], tbs[2])
    if f[0][0] == 0xA0:  # explicit version
        f = f[1:]
    _serial, _alg, issuer, validity, subject, spki = f[:6]
    exts = [x for x in f[6:] if x[0] == 0xA3]
    oid = der[slice(*children(der, alg[1], alg[2])[0][1:3])]
    nb, na = children(der, validity[1], validity[2])
    # SPKI -> BIT STRING -> RSAPublicKey
    bits = children(der, spki[1], spki[2])[1]
    _, rs, re_ = tlv(der, bits[1] + 1)
    n_, e_ = children(der, rs, re_)
    cn = None
    for rdn in children(der, subject[1], subject[2]):
        for atv in children(der, rdn[1], rdn[2]):
            o, v = children(der, atv[1], atv[2])
            if der[o[1]:o[2]] == OID_CN:
                cn = der[v[1]:v[2]].decode(errors="replace")
    is_ca = False
    for x in exts:
        seq = children(der, x[1], x[2])[0]
        for ext in children(der, seq[1], seq[2]):
            parts = children(der, ext[1], ext[2])
            if der[parts[0][1]:parts[0][2]] == OID_BASIC:
                val = parts[-1]  # OCTET STRING wrapping BasicConstraints SEQUENCE
                _, bs, be = tlv(der, val[1])
                inner = children(der, bs, be)
                is_ca = bool(inner) and inner[0][0] == 0x01 and der[inner[0][1]] != 0
    return {
        "tbs": tbs_raw, "alg": oid, "sig": der[sig[1] + 1:sig[2]],
        "issuer": der[issuer[3]:issuer[2]], "subject": der[subject[3]:subject[2]],
        "not_before": parse_time(der[nb[1]:nb[2]], nb[0]), "not_after": parse_time(der[na[1]:na[2]], na[0]),
        "n": int.from_bytes(der[n_[1]:n_[2]], "big"), "e": int.from_bytes(der[e_[1]:e_[2]], "big"),
        "cn": cn, "ca": is_ca,
    }


def verify_jwt(jwt: str) -> str:
    """Raise ValueError if the BLOB signature or chain is not valid; return a short description."""
    h64, p64, s64 = jwt.split(".")
    header = json.loads(b64url(h64))
    if header.get("alg") != "RS256":
        raise ValueError(f"unexpected JWT alg {header.get('alg')}")
    chain = verify_chain(header["x5c"])
    leaf = chain[0]
    if not rsa_verify(leaf["n"], leaf["e"], f"{h64}.{p64}".encode(), b64url(s64), *SIG_ALGS[bytes.fromhex("2a864886f70d01010b")]):
        raise ValueError("bad JWT signature")
    return " <- ".join(c["cn"] or "?" for c in chain)


def verify_chain(x5c: list[str]) -> list[dict]:
    """Validate x5c up to the pinned root; return [leaf, ..., root] or raise ValueError."""
    root_der = base64.b64decode("".join(ROOT_R46.split()))
    if hashlib.sha256(root_der).hexdigest() != ROOT_SHA256:
        raise ValueError("embedded root certificate is corrupted")
    root = parse_cert(root_der)
    chain = []
    for c in x5c:
        cert = parse_cert(base64.b64decode(c))
        if cert["subject"] == root["subject"]:
            break  # a copy of the root (possibly cross-signed): the pinned root replaces it
        chain.append(cert)
    if not chain:
        raise ValueError("x5c has no signing certificate")
    chain.append(root)
    t = now()
    leaf = chain[0]
    if leaf["cn"] != LEAF_CN:
        raise ValueError(f"signing certificate is for {leaf['cn']!r}, not {LEAF_CN}")
    for i, c in enumerate(chain[:-1]):
        issuer = chain[i + 1]
        if c["issuer"] != issuer["subject"]:
            raise ValueError(f"chain broken at certificate {i} ({c['cn']})")
        if not issuer["ca"]:
            raise ValueError(f"issuer {issuer['cn']} is not a CA certificate")
        if not (c["not_before"] <= t <= c["not_after"]):
            raise ValueError(f"certificate {c['cn']} is outside its validity period")
        if c["alg"] not in SIG_ALGS or not rsa_verify(issuer["n"], issuer["e"], c["tbs"], c["sig"], *SIG_ALGS[c["alg"]]):
            raise ValueError(f"bad signature on certificate {c['cn']}")
    return chain


# ---------- cache, pull budget ----------

def pulls() -> list[dt.datetime]:
    try:
        return [dt.datetime.fromisoformat(x) for x in json.loads(LOG.read_text())]
    except (OSError, ValueError):
        return []


def recent_pulls() -> list[dt.datetime]:
    return [p for p in pulls() if now() - p < WINDOW]


def log_pull() -> dt.datetime:
    t = now()
    LOG.write_text(json.dumps([p.isoformat(timespec="seconds") for p in recent_pulls() + [t]]))
    return t


def unlog_pull(t: dt.datetime) -> None:
    LOG.write_text(json.dumps([p.isoformat(timespec="seconds") for p in recent_pulls()
                               if p.isoformat(timespec="seconds") != t.isoformat(timespec="seconds")]))


def meta() -> dict:
    try:
        return json.loads(META.read_text())
    except (OSError, ValueError):
        return {}


def load_blob() -> dict:
    if not BLOB.exists():
        die("no cached MDS BLOB. Run `python3 scripts/mds.py update` first "
            f"(downloading it means accepting FIDO's MDS terms: {LEGAL}).")
    return json.loads(b64url(BLOB.read_text().strip().split(".")[1]))


def cmd_update(a) -> None:
    try:
        CACHE.mkdir(parents=True, exist_ok=True)
        (CACHE / ".write-test").write_text("")
        (CACHE / ".write-test").unlink()
    except OSError as e:
        die(f"cannot write to {CACHE} ({e}); a sandbox may be blocking it. Options: allow writes there "
            "(Codex: add the folder to sandbox_workspace_write.writable_roots, or approve running this command "
            "outside the sandbox), or set FIDO_SPEC_CACHE to a persistent writable folder. The pull log lives in "
            "this folder, so a new folder starts a new count: FIDO's limit of two downloads per day still applies.")
    m = meta()
    if m.get("pulled") and not a.force:
        age = now() - dt.datetime.fromisoformat(m["pulled"])
        if age < WINDOW:
            ago = f"{age.seconds // 3600} h" if age.seconds >= 3600 else f"{age.seconds // 60} min"
            print(f"Cached BLOB no. {m.get('no')} was downloaded {ago} ago "
                  f"(nextUpdate {m.get('nextUpdate')}); not downloading again. Use --force to override.")
            return
    rp = recent_pulls()
    if len(rp) >= MAX_PULLS:
        nxt = min(rp) + WINDOW
        die(f"MDS download limit reached ({MAX_PULLS} per 24 h). Next download allowed after "
            f"{nxt:%Y-%m-%d %H:%M} UTC." + (" The cached BLOB is still usable." if BLOB.exists() else ""))
    attempt = log_pull()  # count the attempt before sending, so failed or partial downloads also count
    print(f"Downloading {MDS_URL} (pull {len(rp) + 1} of {MAX_PULLS} in 24 h)…", file=sys.stderr)
    req = urllib.request.Request(MDS_URL, headers={"User-Agent": UA})
    try:
        r = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:  # the server answered: counts as a pull
        die(f"download failed: HTTP {e.code} {e.reason}")
    except (urllib.error.URLError, OSError) as e:  # no answer (offline, DNS, sandbox): doesn't count
        unlog_pull(attempt)
        die(f"download failed before reaching the server: {e}. This attempt was not counted. "
            "If you are in a sandbox (for example Codex's default workspace-write mode), network access may be "
            "off: rerun outside the sandbox with the user's approval, or have the user enable network access.")
    try:
        with r:
            jwt = r.read().decode().strip()
    except Exception as e:  # noqa: BLE001  (connection dropped mid-download: counts)
        die(f"download interrupted: {e}")
    try:
        chain = verify_jwt(jwt)
    except (ValueError, KeyError, IndexError) as e:
        (CACHE / "blob.rejected.jwt").write_text(jwt)
        die(f"BLOB verification failed: {e}. Kept the previous cached BLOB; rejected file saved as blob.rejected.jwt.")
    body = json.loads(b64url(jwt.split(".")[1]))
    tmp = BLOB.with_suffix(".part")
    tmp.write_text(jwt)
    tmp.replace(BLOB)
    META.write_text(json.dumps({
        "pulled": now().isoformat(timespec="seconds"), "no": body.get("no"), "nextUpdate": body.get("nextUpdate"),
        "entries": len(body.get("entries", [])), "sha256": hashlib.sha256(jwt.encode()).hexdigest(),
        "verified": chain,
    }, indent=1))
    print(f"BLOB no. {body.get('no')} ({len(body['entries'])} entries, nextUpdate {body.get('nextUpdate')}) "
          f"verified ({chain}) and cached at {BLOB}")
    print(body.get("legalHeader", ""))


# ---------- browsing ----------

def ident(e: dict) -> str:
    if e.get("aaguid"):
        return e["aaguid"]
    if e.get("aaid"):
        return e["aaid"]
    return ",".join(e.get("attestationCertificateKeyIdentifiers", [])[:1]) or "?"


def protocol(e: dict) -> str:
    return e.get("metadataStatement", {}).get("protocolFamily", "?")


def reports(e: dict) -> list[dict]:
    return sorted(e.get("statusReports", []), key=lambda r: r.get("effectiveDate", ""), reverse=True)


def latest(e: dict) -> dict:
    r = reports(e)
    return r[0] if r else {}


def name(e: dict) -> str:
    return e.get("metadataStatement", {}).get("description", "")


def norm(s: str) -> str:
    return re.sub(r"[^0-9a-z]", "", s.lower())


def keys_of(e: dict) -> list[str]:
    return [norm(k) for k in [e.get("aaguid", ""), e.get("aaid", ""), *e.get("attestationCertificateKeyIdentifiers", [])] if k]


def find(blob: dict, q: str) -> dict:
    nq = norm(q)
    exact = [e for e in blob["entries"] if nq in keys_of(e)]
    if exact:
        return exact[0]
    by_name = [e for e in blob["entries"] if q.lower() in name(e).lower()]
    if len(by_name) == 1:
        return by_name[0]
    if not by_name:
        die(f"no MDS entry matches {q!r}. Try `mds.py search`.")
    die(f"{len(by_name)} entries match {q!r}" + (" (first 20 shown)" if len(by_name) > 20 else "")
        + "; use the AAGUID, AAID or key identifier:\n"
        + "\n".join(f"  {ident(e):40} {protocol(e):6} {latest(e).get('status', '?'):22} {name(e)}" for e in by_name[:20]))


def cmd_info(a) -> None:
    blob, m = load_blob(), meta()
    from collections import Counter
    st = Counter(latest(e).get("status", "?") for e in blob["entries"])
    pf = Counter(protocol(e) for e in blob["entries"])
    stale = blob.get("nextUpdate", "9999") < now().strftime("%Y-%m-%d")
    rp = recent_pulls()
    print(f"MDS BLOB no. {blob.get('no')}, nextUpdate {blob.get('nextUpdate')}"
          + ("  (PAST: a newer BLOB should exist; run `update`)" if stale else ""))
    print(f"Downloaded {m.get('pulled', '?')} UTC; signature: {m.get('verified', 'not recorded')}")
    print(f"Pull budget: {MAX_PULLS - len(rp)} of {MAX_PULLS} left in the last 24 h")
    print(f"Entries: {len(blob['entries'])}  by protocol: {dict(pf)}")
    print("Latest status: " + ", ".join(f"{k} {v}" for k, v in st.most_common()))
    print(f"Legal: {blob.get('legalHeader', '')}")


def cmd_search(a) -> None:
    blob = load_blob()
    terms = [t.lower() for t in a.terms]
    hits = []
    for e in blob["entries"]:
        ms = e.get("metadataStatement", {})
        hay = " ".join([name(e), json.dumps(ms.get("friendlyNames", {})), ident(e),
                        *e.get("attestationCertificateKeyIdentifiers", []),
                        *[r.get("certificateNumber", "") for r in e.get("statusReports", [])]]).lower()
        if not all(t in hay or norm(t) in norm(hay) for t in terms):
            continue
        if a.status and a.status.lower() not in latest(e).get("status", "").lower():
            continue
        if a.protocol and a.protocol.lower() != protocol(e).lower():
            continue
        hits.append(e)
    for e in hits[: a.limit]:
        r = latest(e)
        print(f"{ident(e):38} {protocol(e):6} {r.get('status', '?'):22} {r.get('effectiveDate', ''):10}  {name(e)}")
    print(f"{len(hits)} match(es)" + (f", showing {a.limit}" if len(hits) > a.limit else ""), file=sys.stderr)


def cmd_show(a) -> None:
    blob = load_blob()
    e = find(blob, a.id)
    if a.json:
        def strip(x):
            if isinstance(x, dict):
                return {k: strip(v) for k, v in x.items()}
            if isinstance(x, list):
                return [strip(v) for v in x]
            if isinstance(x, str) and x.startswith("data:image"):
                return "<image data URI omitted; use --icon>"
            return x
        print(json.dumps(e if a.icon else strip(e), indent=1))
        return
    ms = e.get("metadataStatement", {})
    gi = ms.get("authenticatorGetInfo", {})
    print(f"# {name(e)}")
    print(f"BLOB no. {blob.get('no')} (nextUpdate {blob.get('nextUpdate')})")
    for k in ("aaguid", "aaid"):
        if e.get(k):
            print(f"{k}: {e[k]}")
    if e.get("attestationCertificateKeyIdentifiers"):
        print("attestationCertificateKeyIdentifiers: " + ", ".join(e["attestationCertificateKeyIdentifiers"]))
    print(f"protocolFamily: {protocol(e)}   authenticatorVersion: {ms.get('authenticatorVersion')}   "
          f"schema: {ms.get('schema')}")
    if ms.get("friendlyNames"):
        print("friendlyNames: " + "; ".join(f"{k}: {v}" for k, v in ms["friendlyNames"].items()))
    print(f"timeOfLastStatusChange: {e.get('timeOfLastStatusChange')}")
    print("\nStatus reports (newest first):")
    for r in reports(e):
        extra = ", ".join(f"{k}={v}" for k, v in r.items() if k not in ("status", "effectiveDate") and v)
        print(f"  {r.get('effectiveDate', '?'):10}  {r.get('status')}" + (f"  ({extra})" if extra else ""))
    print("\nStatement:")
    for k in ("upv", "authenticationAlgorithms", "publicKeyAlgAndEncodings", "attestationTypes", "keyProtection",
              "matcherProtection", "cryptoStrength", "attachmentHint", "tcDisplay", "isKeyRestricted",
              "isFreshUserVerificationRequired", "multiDeviceCredentialSupport"):
        if k in ms:
            print(f"  {k}: {json.dumps(ms[k])}")
    if ms.get("userVerificationDetails"):
        alts = [" + ".join(m.get("userVerificationMethod", "?") for m in combo) for combo in ms["userVerificationDetails"]]
        print("  userVerificationDetails: " + " | ".join(alts))
    print(f"  attestationRootCertificates: {len(ms.get('attestationRootCertificates', []))}")
    if gi:
        print("\nauthenticatorGetInfo:")
        for k in ("versions", "extensions", "transports", "options", "algorithms", "maxMsgSize", "pinUvAuthProtocols",
                  "minPINLength", "firmwareVersion", "certifications"):
            if k in gi:
                print(f"  {k}: {json.dumps(gi[k])}")
    print("\nFull entry: add --json. Field meanings: Metadata Statement 3.1.1 and MDS 3.1.1 specs in the catalog.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("update"); s.add_argument("--force", action="store_true",
                                                 help="download even if the cache is less than 24 h old (limit still applies)")
    sub.add_parser("info")
    s = sub.add_parser("search"); s.add_argument("terms", nargs="+"); s.add_argument("--status")
    s.add_argument("--protocol"); s.add_argument("--limit", type=int, default=40)
    s = sub.add_parser("show"); s.add_argument("id"); s.add_argument("--json", action="store_true")
    s.add_argument("--icon", action="store_true", help="keep icon and logo images in --json output")
    a = p.parse_args()
    {"update": cmd_update, "info": cmd_info, "search": cmd_search, "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    main()
