#!/usr/bin/env python3
"""Build the static dashboard payload from the latest provider snapshot."""
import argparse, csv, datetime as dt, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',default=None,help='catalog snapshot JSON (defaults to latest, then dated snapshot)')
    ap.add_argument('--out',default='site',help='site output directory')
    args=ap.parse_args()
    src=pathlib.Path(args.input) if args.input else ROOT/'data'/'free-models-latest.json'
    if not src.exists(): src=ROOT/'data'/'free-models-2026-11-11.json'
    snapshot=json.loads(src.read_text())
    models=[]
    for key,value in snapshot.get('models',{}).items():
        row=dict(value); row['id']=key; models.append(row)
    aa=[]
    with (ROOT/'data'/'aa_scores_2026-11-11.csv').open(newline='') as f:
        for r in csv.DictReader(f):
            r['coding_composite']=round(.6*float(r['frontiercode_aa_2_pct'])+.4*float(r['terminal_bench_4_pct']),2)
            aa.append(r)
    free=[]
    with (ROOT/'data'/'aa_free_variant_comparables_2026-11-11.csv').open(newline='') as f:
        for r in csv.DictReader(f):
            if r['coding_composite_60_40']:
                r['coding_composite_60_40']=float(r['coding_composite_60_40'])
                free.append(r)
    payload={
      'checked_at':snapshot.get('checked_at'),
      'built_at':dt.datetime.now(dt.timezone.utc).isoformat(),
      'sources':snapshot.get('sources',{}),
      'count':len(models),
      'source_counts':{s:sum(1 for x in models if x.get('source')==s) for s in sorted({x.get('source') for x in models})},
      'modality_missing':sum(1 for x in models if not x.get('modality')),
      'local_visible_count':sum(1 for x in models if x.get('visible_in_local_opencode') is True),
      'models':sorted(models,key=lambda x:(x.get('source',''),x.get('name','').lower(),x['id'])),
      'aa_as_of':'2026-11-11',
      'aa_rankings':{
        'coding':sorted(aa,key=lambda x:x['coding_composite'],reverse=True),
        'knowledge_work':sorted(aa,key=lambda x:int(x['briefcase_elo']),reverse=True),
        'free_flash_comparables':sorted(free,key=lambda x:x['coding_composite_60_40'],reverse=True)
      }
    }
    out=pathlib.Path(args.out); (out/'data').mkdir(parents=True,exist_ok=True)
    (out/'data'/'dashboard.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(f"Built {out/'data'/'dashboard.json'} with {len(models)} catalog candidates")
if __name__=='__main__': main()
