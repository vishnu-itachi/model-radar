# Model Radar

A local, reproducible research kit for discovering advertised free model endpoints and choosing models by task. It separates three questions that are easy to confuse:

1. **Is a model listed at $0?** Public catalog metadata says so.
2. **Can my local agent see it?** Checked against `opencode models`.
3. **Can I use it now, with enough quota and reliable quality?** This depends on provider account, region, rate limits, current capacity, and agent harness. Catalog data cannot answer this alone.

## Quick start

Requires Python 3. No third-party packages.

```sh
python3 scripts/free_model_tracker.py
python3 scripts/rank_domains.py
```

The tracker queries all provider entries in [models.dev](https://models.dev/) and the [OpenRouter models API](https://openrouter.ai/docs/api/api-reference/models/list). It writes `data/free-models-latest.json`; the committed dated snapshot is from 2026-11-11. It uses `opencode models` when installed. `--include-non-chat` retains catalog listings whose modality may be image/audio-only. A price of zero is catalog metadata, not a promise of availability or a provider entitlement. For OpenRouter, check the model page and account limits; free model limits may be restricted.

To refresh Artificial Analysis's authenticated free-model endpoint:

```sh
export AA_API_KEY='…' # use your own key; do not commit it
python3 scripts/refresh_aa.py
```

The free AA endpoint provides headline indices/capability scores, not the full benchmark matrix. API access is rate-limited and subject to AA attribution and internal-use terms. This repo does not include an API key. See the [AA API docs](https://artificialanalysis.ai/data-api/docs).

## Findings as of 2026-11-11

- Current local OpenCode inventory showed 71 model IDs. The captured public catalog snapshot had 66 $0 entries across three free-catalog/provider sources represented in the scan at that time; 12 matched local OpenCode names. These counts change and are not a complete census of every model vendor.
- Chinese-model name detection is a convenience heuristic, not verified model provenance. The Chinese CLIs below do work with T3 Code's local ACP mechanism, but ACP only connects an agent process; it does not give it free credentials, quota, or a free model.
- There is no single best model across domains. For coding among the compared Chinese models, Kimi K3.1 Pro was strongest on Terminal-Bench 4.0 while DeepSeek V4.1 Flash 1017 Max led FrontierCode-AA 2.0. AA's combined intelligence index rewards a wider set of tasks, so it is not a coding-only score.
- For knowledge work and document artifacts, AA-Briefcase and GDPval-AA are useful proxies. They include multi-step work and generated artifacts such as presentations, spreadsheets, and documents. They do not fully measure presentation visual polish or the quality of a specific PowerPoint deliverable.
- The free OpenRouter and OpenCode variants need separate verification. Benchmark scores are for the exact named model/configuration, often a paid or Max/Pro tier, and cannot be assumed to transfer to a free alias/provider route.

## Research and method

See [`research/current-findings-2026-11-11.md`](research/current-findings-2026-11-11.md) for ACP setup, provider limits, benchmark interpretation, and model-by-task analysis. The dated AA table in `data/aa_scores_2026-11-11.csv` supports a clearly labeled heuristic coding composite: 60% FrontierCode-AA 2.0 and 40% Terminal-Bench 4.0 (the 15:10 weight ratio in AA's coding component). It is not an official AA coding index. The `briefcase_elo` and `gdpval_aa_v2_1` columns are separate measures and should not be blended into that composite.

The tracker is a discovery tool, not an uptime monitor. For genuine “is it usable right now?” tracking, add periodic checks using the exact credentials and endpoints you intend to use, record HTTP errors/latency/quota, and never send private code to an untrusted free endpoint.
