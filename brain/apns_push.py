#!/usr/bin/env python3
"""
brain/apns_push.py — APNs ActivityKit(Live Activity) push sender. STDLIB ONLY.

pip依存を足さない方針(ui_serverと同じ)。
- ES256 JWT署名: openssl CLI (`openssl dgst -sha256 -sign <p8> -binary`) + stdlibのDER→JOSE変換。
- HTTP/2送信: `curl --http2`。

設定は env or /Users/toma/trench-brain/.env から読む:
  APNS_KEY_ID (必須) / APNS_TEAM_ID (既定 85LF3ZN8C2) / APNS_BUNDLE_ID (既定 com.tomatantan.trenchsurf)
  APNS_KEY_PATH (.p8のパス・必須) / APNS_ENV ("sandbox"|"production"・既定 sandbox)

公開関数:
  send_live_activity_push(push_token, content_state, event="update", dismiss=False) -> (bool, str)

CLI:
  python3 brain/apns_push.py --token <t> --state '{"status":"found","count":1,"lastHook":"x"}'
  python3 brain/apns_push.py --selftest
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

DOTENV_PATH = "/Users/toma/trench-brain/.env"

DEFAULT_TEAM_ID = "85LF3ZN8C2"
DEFAULT_BUNDLE_ID = "com.tomatantan.trenchsurf"
DEFAULT_ENV = "sandbox"

JWT_TTL_SECONDS = 40 * 60  # ~40分キャッシュ

# モジュールレベルJWTキャッシュ (jwtとconfig fingerprintと有効期限)
_jwt_cache = {"jwt": None, "exp": 0.0, "fingerprint": None}


# ---------------------------------------------------------------------------
# .env / config
# ---------------------------------------------------------------------------

def _parse_env_file(path):
    """簡易 KEY=VALUE パーサ (既存 ui_server と同様)。"""
    out = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                # 前後のクォートを剥がす
                if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                    v = v[1:-1]
                out[k] = v
    except OSError:
        pass
    return out


def get_config():
    """env優先 → .env補完 → 既定値、の順で設定を組み立てる。"""
    keys = ["APNS_KEY_ID", "APNS_TEAM_ID", "APNS_BUNDLE_ID", "APNS_KEY_PATH", "APNS_ENV"]
    cfg = {}
    for k in keys:
        if os.environ.get(k):
            cfg[k] = os.environ[k]

    if os.path.exists(DOTENV_PATH):
        file_vals = _parse_env_file(DOTENV_PATH)
        for k in keys:
            if k not in cfg and file_vals.get(k):
                cfg[k] = file_vals[k]

    cfg.setdefault("APNS_TEAM_ID", DEFAULT_TEAM_ID)
    cfg.setdefault("APNS_BUNDLE_ID", DEFAULT_BUNDLE_ID)
    cfg.setdefault("APNS_ENV", DEFAULT_ENV)
    return cfg


# ---------------------------------------------------------------------------
# base64url helpers
# ---------------------------------------------------------------------------

def b64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(s):
    if isinstance(s, bytes):
        s = s.decode("ascii")
    padding = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + padding)


# ---------------------------------------------------------------------------
# DER (ECDSA signature) -> JOSE (r||s, 32 bytes each)
# ---------------------------------------------------------------------------

def _read_der_length(data, idx):
    first = data[idx]
    idx += 1
    if first & 0x80 == 0:
        return first, idx
    num_bytes = first & 0x7F
    length = int.from_bytes(data[idx:idx + num_bytes], "big")
    idx += num_bytes
    return length, idx


def der_to_jose(der):
    """DER `SEQUENCE{INTEGER r, INTEGER s}` -> JOSE r||s, each left-padded to 32 bytes."""
    idx = 0
    if der[idx] != 0x30:
        raise ValueError("DER: expected SEQUENCE (0x30)")
    idx += 1
    _, idx = _read_der_length(der, idx)

    if der[idx] != 0x02:
        raise ValueError("DER: expected INTEGER (0x02) for r")
    idx += 1
    rlen, idx = _read_der_length(der, idx)
    r = der[idx:idx + rlen]
    idx += rlen

    if der[idx] != 0x02:
        raise ValueError("DER: expected INTEGER (0x02) for s")
    idx += 1
    slen, idx = _read_der_length(der, idx)
    s = der[idx:idx + slen]
    idx += slen

    r = r.lstrip(b"\x00").rjust(32, b"\x00")
    s = s.lstrip(b"\x00").rjust(32, b"\x00")
    if len(r) > 32 or len(s) > 32:
        raise ValueError("DER: r/s longer than 32 bytes (not P-256?)")
    return r + s


# ---------------------------------------------------------------------------
# JWT (ES256) build via openssl CLI
# ---------------------------------------------------------------------------

def _sign_der(signing_input, key_path):
    proc = subprocess.run(
        ["openssl", "dgst", "-sha256", "-sign", key_path, "-binary"],
        input=signing_input.encode("ascii"),
        capture_output=True,
        check=True,
    )
    return proc.stdout


def build_jwt(key_id, team_id, key_path):
    header = {"alg": "ES256", "kid": key_id}
    claims = {"iss": team_id, "iat": int(time.time())}

    header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    claims_b64 = b64url_encode(json.dumps(claims, separators=(",", ":")).encode("utf-8"))
    signing_input = header_b64 + "." + claims_b64

    der_sig = _sign_der(signing_input, key_path)
    jose_sig = der_to_jose(der_sig)
    sig_b64 = b64url_encode(jose_sig)

    return signing_input + "." + sig_b64


def get_jwt(cfg):
    """~40分キャッシュしたJWTを返す(設定が変わったら再生成)。"""
    fingerprint = (cfg.get("APNS_KEY_ID"), cfg.get("APNS_TEAM_ID"), cfg.get("APNS_KEY_PATH"))
    now = time.time()
    if (
        _jwt_cache["jwt"] is not None
        and now < _jwt_cache["exp"]
        and _jwt_cache["fingerprint"] == fingerprint
    ):
        return _jwt_cache["jwt"]

    jwt = build_jwt(cfg["APNS_KEY_ID"], cfg["APNS_TEAM_ID"], cfg["APNS_KEY_PATH"])
    _jwt_cache["jwt"] = jwt
    _jwt_cache["exp"] = now + JWT_TTL_SECONDS
    _jwt_cache["fingerprint"] = fingerprint
    return jwt


# ---------------------------------------------------------------------------
# APNs send (curl --http2)
# ---------------------------------------------------------------------------

def send_live_activity_push(push_token, content_state, event="update", dismiss=False):
    """
    Live Activity content-stateの更新をAPNsへ送る。
    戻り値: (成功可否: bool, レスポンス要約/エラー文字列: str)
    鍵未設定/エラー時は例外を投げず (False, "...") を返す。
    """
    try:
        cfg = get_config()
    except Exception as e:
        return False, "設定読み込み失敗: %s" % e

    key_id = cfg.get("APNS_KEY_ID")
    key_path = cfg.get("APNS_KEY_PATH")
    if not key_id or not key_path or not os.path.exists(key_path):
        return False, "APNs未設定"

    try:
        jwt = get_jwt(cfg)
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode("utf-8", "ignore") if isinstance(e.stderr, bytes) else str(e.stderr)
        return False, "JWT署名失敗(openssl): %s" % stderr.strip()
    except Exception as e:
        return False, "JWT生成失敗: %s" % e

    bundle = cfg["APNS_BUNDLE_ID"]
    env_name = cfg.get("APNS_ENV", DEFAULT_ENV)
    host = "api.push.apple.com" if env_name == "production" else "api.sandbox.push.apple.com"
    url = "https://%s/3/device/%s" % (host, push_token)

    aps = {
        "timestamp": int(time.time()),
        "event": event,
        "content-state": content_state,
    }
    if dismiss or event == "end":
        aps["dismissal-date"] = int(time.time())

    body = json.dumps({"aps": aps}, separators=(",", ":"))
    topic = "%s.push-type.liveactivity" % bundle

    headers = [
        "authorization: bearer %s" % jwt,
        "apns-topic: %s" % topic,
        "apns-push-type: liveactivity",
        "apns-priority: 10",
        "apns-expiration: 0",
        "content-type: application/json",
    ]

    cmd = ["curl", "-sS", "--http2", "-i", "-X", "POST"]
    for h in headers:
        cmd += ["-H", h]
    cmd += ["--data-binary", body, url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        return False, "curlタイムアウト"
    except Exception as e:
        return False, "curl実行失敗: %s" % e

    if result.returncode != 0:
        return False, "curl失敗(exit=%d): %s" % (result.returncode, (result.stderr or "").strip())

    output = result.stdout
    m = re.search(r"HTTP/\S+\s+(\d+)", output)
    status = int(m.group(1)) if m else None

    # ヘッダとボディを空行で分離(最後のブロックがボディ)
    if "\r\n\r\n" in output:
        resp_body = output.split("\r\n\r\n")[-1].strip()
    else:
        resp_body = output.split("\n\n")[-1].strip()

    success = status == 200
    summary = "status=%s body=%s" % (status, resp_body[:300])
    return success, summary


# ---------------------------------------------------------------------------
# --selftest
# ---------------------------------------------------------------------------

def _run_selftest():
    tmpdir = tempfile.mkdtemp(prefix="apns_selftest_")
    try:
        ec_pem = os.path.join(tmpdir, "ec.pem")
        p8_path = os.path.join(tmpdir, "test_key.p8")

        subprocess.run(
            ["openssl", "ecparam", "-genkey", "-name", "prime256v1", "-noout", "-out", ec_pem],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["openssl", "pkcs8", "-topk8", "-nocrypt", "-in", ec_pem, "-out", p8_path],
            check=True, capture_output=True,
        )

        jwt = build_jwt("TESTKID123", "TESTTEAMID9", p8_path)
        parts = jwt.split(".")
        assert len(parts) == 3, "JWTは3パートである必要がある(got %d)" % len(parts)

        header = json.loads(b64url_decode(parts[0]))
        claims = json.loads(b64url_decode(parts[1]))
        sig = b64url_decode(parts[2])

        assert header.get("alg") == "ES256", "alg != ES256: %r" % header
        assert header.get("kid") == "TESTKID123", "kid不一致: %r" % header
        assert claims.get("iss") == "TESTTEAMID9", "iss不一致: %r" % claims
        assert "iat" in claims and isinstance(claims["iat"], int), "iat欠落/型不正: %r" % claims
        assert len(sig) == 64, "署名は64バイトである必要がある(got %d)" % len(sig)

        print("[selftest] header decoded: %s" % json.dumps(header, ensure_ascii=False))
        print("[selftest] claims decoded: %s" % json.dumps(claims, ensure_ascii=False))
        print("[selftest] signature bytes: %d" % len(sig))
        print("[selftest] JWT (truncated): %s...%s" % (jwt[:40], jwt[-20:]))
        print("SELFTEST: PASS")
        return True
    except AssertionError as e:
        print("SELFTEST: FAIL (%s)" % e)
        return False
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode("utf-8", "ignore") if isinstance(e.stderr, bytes) else str(e.stderr)
        print("SELFTEST: FAIL (openssl error: %s)" % stderr.strip())
        return False
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="APNs ActivityKit push sender (stdlib only)")
    parser.add_argument("--token", help="push token (device/live-activity token)")
    parser.add_argument("--state", help="content-state JSON string")
    parser.add_argument("--event", default="update", help="aps.event (default: update)")
    parser.add_argument("--dismiss", action="store_true", help="add dismissal-date")
    parser.add_argument("--selftest", action="store_true", help="run JWT self-test (no real APNs call)")
    args = parser.parse_args()

    if args.selftest:
        ok = _run_selftest()
        sys.exit(0 if ok else 1)

    if args.token and args.state:
        try:
            content_state = json.loads(args.state)
        except json.JSONDecodeError as e:
            print("ERROR: --state はJSONである必要がある: %s" % e)
            sys.exit(2)
        ok, msg = send_live_activity_push(args.token, content_state, event=args.event, dismiss=args.dismiss)
        print("%s: %s" % ("OK" if ok else "FAIL", msg))
        sys.exit(0 if ok else 1)

    parser.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
