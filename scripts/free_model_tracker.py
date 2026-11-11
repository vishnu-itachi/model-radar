#!/usr/bin/env python3
"""Track advertised zero-price chat models and local OpenCode visibility.

Price is not the same thing as a usable free quota. Sources cover public
catalogs, not every provider, account entitlement, regional limit, or uptime.
"""
from __future__ import annotations
import argparse, datetime as dt, json, pathlib, re, subprocess, sys, urllib.request

MODELS_DEV = "https://models.dev/api.json"
OPENROUTER = "https://openrouter.ai/api/v1/models"
HINTS = re.compile(r"deepseek|qwen|kimi|moonshot|minimax|glm|zhipu|01-ai|baichuan|stepfun|ling|longcat|mimo|xiaomi|hunyuan|tencent|doubao|volc|ernie|wenxin", re.I)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "model-radar/0.1"})
    with urllib.request.urlopen(req, timeout=40) as res: return json.load(res)

def zero(v):
    try: return float(v) == 0
    except (TypeError, ValueError): return False

def local_models():
    try:
        r = subprocess.run(["opencode", "models"], capture_output=True, text=True, timeout=45)
        if r.returncode: return set(), r.stderr.strip() or "opencode models failed"
        return {x.strip() for x in r.stdout.splitlines() if "/" in x}, None
    except (FileNotFoundError, subprocess.TimeoutExpired) as e: return set(), str(e)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", default="data/free-models-latest.json")
    ap.add_argument("--include-non-chat", action="store_true", help="include catalog entries not explicitly marked text-in/text-out")
    args = ap.parse_args()
    path = pathlib.Path(args.state)
    try: old = json.loads(path.read_text()).get("models", {}) if path.exists() else {}
    except Exception: old = {}
    models, status = {}, {}
    try:
        catalog = fetch(MODELS_DEV)
        for pid, provider in catalog.items():
            for mid, m in (provider.get("models") or {}).items():
                cost = m.get("cost") or {}
                if not (zero(cost.get("input")) and zero(cost.get("output"))): continue
                arch = m.get("architecture") or {}
                modality = str(arch.get("modality", ""))
                if not args.include_non_chat and modality and "text" not in modality.lower(): continue
                key = f"{pid}/{mid}"
                models[key] = {"name": m.get("name", mid), "source": "models.dev", "input_cost": cost.get("input"), "output_cost": cost.get("output"), "context": (m.get("limit") or {}).get("context"), "tool_call": m.get("tool_call"), "modality": modality or None, "origin_hint": bool(HINTS.search(key))}
        status["models.dev"] = "ok"
    except Exception as e: status["models.dev"] = f"error: {e}"
    try:
        for m in fetch(OPENROUTER).get("data", []):
            p = m.get("pricing") or {}
            if not (zero(p.get("prompt")) and zero(p.get("completion"))): continue
            arch = m.get("architecture") or {}
            modality = str(arch.get("modality", ""))
            if not args.include_non_chat and modality and "text" not in modality.lower(): continue
            mid = m.get("id", "")
            models[f"openrouter/{mid}"] = {"name": m.get("name", mid), "source": "openrouter", "input_cost": p.get("prompt"), "output_cost": p.get("completion"), "context": m.get("context_length"), "tool_call": None, "modality": modality or None, "origin_hint": bool(HINTS.search(mid))}
        status["openrouter"] = "ok"
    except Exception as e: status["openrouter"] = f"error: {e}"
    local, err = local_models()
    for k,v in models.items(): v["visible_in_local_opencode"] = k in local
    status["local_opencode"] = f"error: {err}" if err else f"ok ({len(local)} models listed)"
    print(f"Checked: {dt.datetime.now().astimezone().isoformat(timespec='seconds')}")
    print("Sources: " + "; ".join(f"{k}={v}" for k,v in status.items()))
    print(f"Advertised zero-price entries: {len(models)}; visible in OpenCode: {sum(x['visible_in_local_opencode'] for x in models.values())}")
    print(f"New entries vs previous snapshot: {len(set(models)-set(old))}; removed: {len(set(old)-set(models))}")
    if any(status.get(s) != "ok" for s in ("models.dev", "openrouter")):
        print("Catalog fetch incomplete; not saving a partial snapshot.", file=sys.stderr); return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"sources":status,"models":models},indent=2,sort_keys=True)+"\n")
    print(f"Saved {path}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
