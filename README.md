# Model Radar

[![Live dashboard](https://img.shields.io/badge/dashboard-live-2ea44f)](https://vishnu-itachi.github.io/model-radar/)
[![Daily refresh](https://github.com/vishnu-itachi/model-radar/actions/workflows/daily-pages.yml/badge.svg)](https://github.com/vishnu-itachi/model-radar/actions/workflows/daily-pages.yml)

**A daily-updated directory of advertised free AI model endpoints, with task-specific benchmark comparisons.** Find candidate models for coding, document work, and presentations, then check their source, context window, and advertised tool support.

## Open the dashboard

**[vishnu-itachi.github.io/model-radar](https://vishnu-itachi.github.io/model-radar/)** — public, mobile-friendly, and refreshed every day at 07:00 India Standard Time. The latest scan checks [models.dev](https://models.dev/) and the [OpenRouter model catalog](https://openrouter.ai/docs/api/api-reference/models/list).

A $0 catalog price means the catalog currently lists zero input and output cost. It does **not** guarantee account eligibility, remaining quota, uptime, tool support, or that an endpoint is chat-capable. The dashboard flags missing modality data and separates catalog discovery from benchmark evidence.

## What’s inside

- A searchable view of models with explicitly zero input and output prices across all catalog providers returned by models.dev and OpenRouter.
- Context, modality, advertised tool calling, catalog source, and (for local runs) exact-name visibility in `opencode models`.
- Task-oriented Artificial Analysis (AA) comparisons: a labeled coding blend, AA-Briefcase knowledge-work scores, and matched Flash-family scores where available.
- Notes on connecting Chinese coding CLIs to T3 Code using ACP, including the important distinction between ACP support and free model access.
- A GitHub Actions workflow that refreshes catalogs and republishes the site daily. AA benchmark scores are a dated snapshot and are not automatically refreshed.

## Run locally

Requires Python 3; no third-party packages are needed for the scripts.

```sh
# Refresh public catalog data and compare exact IDs with locally listed OpenCode models
python3 scripts/free_model_tracker.py

# Print the dated task rankings
python3 scripts/rank_domains.py

# Build and preview the dashboard from the latest snapshot
python3 scripts/build_site.py
python3 -m http.server 8000 --directory site
```

Open `http://localhost:8000`. On GitHub Actions, the workflow uses `--skip-local`, since its runner cannot see your local OpenCode installation or account.

To refresh AA’s authenticated free-model endpoint, set your own key in the environment. Do not commit it:

```sh
export AA_API_KEY='…'
python3 scripts/refresh_aa.py
```

The free AA API returns headline fields, not its full benchmark matrix. API limits, attribution, and use terms apply; see the [AA API documentation](https://artificialanalysis.ai/data-api/docs).

## How to read the rankings

There is no single best model for every job. The coding blend uses 60% FrontierCode-AA 2.0 and 40% Terminal-Bench 4.0, mirroring their relative weights inside AA’s coding category; it is an unofficial comparison score. AA-Briefcase is a broad agentic knowledge-work and artifact benchmark, not a PowerPoint-only design score. Benchmarks apply to the exact tested model/configuration and may not transfer to a free alias or a different provider route.

The detailed, dated research is in [`research/current-findings-2026-11-11.md`](research/current-findings-2026-11-11.md). Score data is in [`data/aa_scores_2026-11-11.csv`](data/aa_scores_2026-11-11.csv) and [`data/aa_free_variant_comparables_2026-11-11.csv`](data/aa_free_variant_comparables_2026-11-11.csv).

## Automation

The [daily Pages workflow](.github/workflows/daily-pages.yml) runs at 07:00 IST, on pushes to `main`, or manually from the Actions tab. It refreshes public catalog metadata, builds the dashboard, and deploys it to [GitHub Pages](https://vishnu-itachi.github.io/model-radar/). The repository is public so the dashboard can be opened without signing in.
