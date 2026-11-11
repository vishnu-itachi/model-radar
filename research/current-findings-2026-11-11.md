# Model selection research — 2026-11-11

## What “best” means

Choose by the work to be done, then test the actual provider route and harness. A benchmark rank is a starting signal, not proof that the free endpoint will perform identically. The AA v5.0.1 Intelligence Index includes knowledge work, coding, science, and general reasoning at 25% each. Its coding slice is 15% FrontierCode-AA 2.0 and 10% Terminal-Bench 4.0. This means the raw coding-only blend in `rank_domains.py` uses 60/40 among those two coding scores, while overall Intelligence is not a coding score. [AA v5 methodology](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5/)

## Domain guidance from current evidence

### Coding / agentic software work

Among the six Chinese models compared in the dated AA table, Kimi K3.1 Pro leads Terminal-Bench 4.0 at 67.2%; DeepSeek V4.1 Flash 1017 Max leads FrontierCode-AA 2.0 at 28.5%. AA currently rounds Qwen3.8 Max (0902) component scores to 23% FrontierCode and 39% Terminal-Bench, so the composite uses displayed rounded values for that row. The transparent 60/40 composite ranks Kimi (42.18), DeepSeek (30.62), GLM-5.3 Max (29.72), Qwen3.8 Max (29.60), MiMo V2.6 Pro (28.32), MiniMax M3.1 Flash (22.80). These are benchmark results for named model variants; the advertised free DeepSeek Flash alias is not automatically equivalent to the Max benchmark configuration. [DeepSeek vs GLM AA comparison](https://artificialanalysis.ai/models/comparisons/deepseek-v4-1-flash-1017-vs-glm-5-3) · [AA v5](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5/)

Practical choice: try a free coding route first, but make it pass a small local task suite with tool calls, edits, tests, and repository navigation. Test patch correctness, tool-call success, and latency separately. If ACP is used, it is the agent harness that talks to T3 Code; provider authentication and billing remain with that agent.

### Presentations, documents, and general knowledge work

AA-Briefcase evaluates substantial multi-step knowledge work, including artifacts such as presentations and spreadsheets, and reports rubric outcomes plus Elo ratings for analysis/presentation. In the listed cohort, Kimi K3.1 Pro has the highest Briefcase Elo (1674), followed by Qwen3.8 Max (1605), DeepSeek V4.1 Flash 1017 Max (1570), MiMo V2.6 Pro (1512), GLM-5.3 Max (1503), and MiniMax M3.1 Flash (1474). This is a broad knowledge-work proxy, not a direct PowerPoint-only visual design benchmark. [AA-Briefcase overview](https://artificialanalysis.ai/articles/aa-briefcase) · [Briefcase leaderboard](https://artificialanalysis.ai/evaluations/aa-briefcase?results=elo)

For document and slide artifact generation, GDPval-AA contains professional work-product tasks across occupations, including documents, slides, diagrams, and spreadsheets. AA currently ranks Kimi K3.1 Pro and DeepSeek V4.1 Flash 1017 Max near the top among the models in this comparison set; the exact Elo can move when AA updates/regrades its leaderboard, so this dated sheet preserves DeepSeek’s 1746 and leaves Kimi blank where its page surfaces differing current Elo values. The dated table only includes GDPval values independently verified in the research notes; blank cells mean unverified, not zero. GDPval-AA has been removed from AA Intelligence Index v5 and should be consulted as a separate work-product benchmark. GDP.pdf is useful for document reasoning over long PDFs, but does not measure slide design. [GDPval-AA](https://artificialanalysis.ai/evaluations/gdpval-aa) · [GDP.pdf](https://artificialanalysis.ai/evaluations/gdp-pdf)

Practical choice: for a PowerPoint, run a head-to-head task with the same prompt, source material, slide count, and available tools. Judge factual grounding, story structure, visual hierarchy, layout consistency, and whether the exported PPTX opens and renders. The public benchmark suite does not establish the best free provider route for that precise task.

## Free model candidates that have comparable AA scores

The live catalog snapshot contained these OpenCode free aliases: GLM-5.3-Flash Free, MiniMax M3.1 Flash Free, MiMo V2.6 Flash Free, and DeepSeek V4.1 Flash Free. AA has benchmarked similarly named Flash model variants for the first three. On the coding-only 60/40 blend, GLM Flash scores 23.68, MiniMax Flash 22.80, and MiMo Flash 22.04. On Briefcase Elo, MiMo Flash leads this small matched set at 1487, then MiniMax at 1474 and GLM at 1450. AA does not provide an exact matched score for the catalog's DeepSeek V4.1 Flash Free alias in this snapshot; DeepSeek Max scores must not be substituted. These AA variants are not necessarily the same provider route or free quota as OpenCode's alias. See `data/aa_free_variant_comparables_2026-11-11.csv` and the official pages for [GLM Flash](https://artificialanalysis.ai/models/comparisons/glm-5-3-flash-vs-glm-5-3), [MiniMax Flash](https://artificialanalysis.ai/models/comparisons/minimax-m3-1-flash-vs-glm-5-3), and [MiMo Flash](https://artificialanalysis.ai/models/comparisons/mimo-v2-6-flash-vs-mimo-v2-6-pro).

## Free discovery and monitoring

The tracker queries two catalog sources: models.dev's provider/model catalog and OpenRouter's model listing. It scans all models.dev providers whose input and output price are both explicitly zero, and records modality/tool/context metadata where supplied. It compares exact names against `opencode models`. That match is useful but imperfect because aliases and naming conventions differ.

Limitations:

- A free listing can be rate-limited, waitlisted, geographically restricted, temporary, or unavailable at peak time.
- OpenRouter free route rate limits and model eligibility can change; review its live [free model collection](https://openrouter.ai/collections/free-models/).
- Models.dev metadata may omit provider-specific trial credits and account-level quota. Some APIs have new-account free grants, but those expire or are region/model-dependent.
- A successful HTTP request does not prove tool calling, coding quality, or reliable access. Build a separate authenticated smoke check for providers you rely on, with quotas and privacy in mind.
- `origin_hint` in the data is keyword matching only; verify company/model origin before making claims.

## T3 Code and Chinese model CLIs over ACP

T3 Code supports installed local ACP commands and registered ACP agents. In Settings → Providers → Add provider → Show more → Local ACP command, enter the executable and each argument as its own literal row. The T3 docs explicitly show DeepSeek Harness as executable `dsh`, args `--profile`, `acp`. The locally installed agent handles sign-in and model selection; T3 manages the project/thread interface and communicates through ACP. [T3 ACP provider docs](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-acp.md)

Other official CLIs with ACP entry points:

| Agent | ACP invocation | Setup in T3 | Cost/quota note |
|---|---|---|---|
| DeepSeek Harness | `dsh --profile acp` | `dsh`, `--profile`, `acp` | API credentials/quota are separate. |
| Qwen Code | `qwen --acp` | `qwen`, `--acp` | Alibaba documents limited new-user free quota for eligible models/regions; confirm account, region, expiry. |
| MiniMax Code | `mcode acp` | `mcode`, `acp` | ACP is supported, but account credits/plan or compatible API access may be paid. |
| Kimi Code CLI | `kimi acp` | `kimi`, `acp` | Check current Kimi Code account quota. Older Kimi CLI is archived. |

Sources: [Qwen Code](https://github.com/QwenLM/qwen-code) · [Alibaba Qwen-Coder quota/model info](https://help.aliyun.com/en/model-studio/qwen-coder) · [MiniMax Code](https://github.com/MiniMax-AI/minimax-code) · [MiniMax Token Plan](https://platform.minimax.io/subscribe/coding-plan) · [Kimi ACP reference](https://moonshotai.github.io/kimi-code/en/reference/kimi-acp) · [DeepSeek API docs](https://api-docs.deepseek.com/en/)

This answers whether a CLI can be attached to T3: yes, where it provides ACP. It does not mean all providers are free. Verify the command works in your shell, complete the CLI's own authentication, then add it as a local ACP provider in T3. T3 launches the executable directly, without shell expansion; use a wrapper executable if environment setup is needed.

## Artificial Analysis data constraints

AA's API needs an `x-api-key`. The free plan has request limits, and the `/language/models/free` endpoint returns headline intelligence/capability information rather than the full evaluation matrix. AA notes some detailed per-benchmark fields require Pro access and API use has attribution/usage terms. AA's API docs currently mark coding/agentic index fields null, so don't depend on an API coding score for a domain ranking. `scripts/refresh_aa.py` is key-safe and writes a local dated response only when a key is supplied. [AA Data API docs](https://artificialanalysis.ai/data-api/docs) · [API reference](https://artificialanalysis.ai/data-api/docs/reference)

## Recommendation

For an always-current answer, maintain two layers: (1) catalog and account availability, refreshed frequently; (2) dated task benchmark/quality evidence, refreshed when benchmark versions or model variants change. Decide per job: coding uses coding/agentic evidence plus your own code task suite; PPT/docs use artifact/work-product evidence plus rendered-output inspection; broad reasoning uses the overall index only when a multi-domain balance is appropriate. Keep the exact model ID, provider, region, harness, date, and quota status with every result.
