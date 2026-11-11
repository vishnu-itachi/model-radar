#!/usr/bin/env python3
"""Refresh Artificial Analysis's authenticated free-model endpoint.
Requires AA_API_KEY from Artificial Analysis. Keep the key out of files/CLI args.
"""
import datetime as dt, json, os, pathlib, sys, urllib.error, urllib.request
URL="https://artificialanalysis.ai/api/v2/language/models/free"
def main():
    key=os.environ.get("AA_API_KEY")
    if not key:
        print("Set AA_API_KEY from your Artificial Analysis account; no key is stored by this script.",file=sys.stderr); return 2
    req=urllib.request.Request(URL,headers={"x-api-key":key,"User-Agent":"model-radar/0.1"})
    try:
        with urllib.request.urlopen(req,timeout=40) as r: data=json.load(r)
    except urllib.error.HTTPError as e:
        print(f"AA returned HTTP {e.code}. Check key/plan and endpoint access.",file=sys.stderr); return 1
    out=pathlib.Path("data/aa-free-latest.json"); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"retrieved_at":dt.datetime.now(dt.timezone.utc).isoformat(),"source":URL,"attribution":"Artificial Analysis (artificialanalysis.ai); see API terms","data":data},indent=2)+"\n")
    print(f"Saved {out}. Review AA API attribution/usage terms before sharing this data.")
    return 0
if __name__=="__main__": raise SystemExit(main())
