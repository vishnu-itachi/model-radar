#!/usr/bin/env python3
"""Print deterministic domain rankings from the dated curated AA score file."""
import csv, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
p=root/"data"/"aa_scores_2026-11-11.csv"
rows=list(csv.DictReader(p.open()))
for r in rows:
    r["coding_composite"]=.6*float(r["frontiercode_aa_2_pct"])+.4*float(r["terminal_bench_4_pct"])
print("Coding (heuristic composite = 60% FrontierCode-AA 2.0 + 40% Terminal-Bench 4.0)")
for r in sorted(rows,key=lambda x:x["coding_composite"],reverse=True): print(f"{r['model']}: {r['coding_composite']:.2f} (FC {r['frontiercode_aa_2_pct']}%; TB {r['terminal_bench_4_pct']}%)")
print("\nKnowledge-work proxy (AA-Briefcase Elo; higher is better)")
for r in sorted(rows,key=lambda x:float(x["briefcase_elo"]),reverse=True): print(f"{r['model']}: {r['briefcase_elo']} Elo")
print("\nDocument / artifact benchmark (GDPval-AA v2.1 score; blank means not verified)")
for r in sorted((x for x in rows if x["gdpval_aa_v2_1"]),key=lambda x:float(x["gdpval_aa_v2_1"]),reverse=True): print(f"{r['model']}: {r['gdpval_aa_v2_1']}")
print("\nFree-catalog Flash family matches (AA evaluates named model variants; provider route may differ)")
free=list(csv.DictReader((root/"data"/"aa_free_variant_comparables_2026-11-11.csv").open()))
for r in sorted((x for x in free if x["coding_composite_60_40"]),key=lambda x:float(x["coding_composite_60_40"]),reverse=True): print(f"{r['catalog_variant']}: coding {float(r['coding_composite_60_40']):.2f}; Briefcase {r['briefcase_elo']} Elo")
print("No AA score found in this snapshot for DeepSeek V4.1 Flash Free's exact variant.")
