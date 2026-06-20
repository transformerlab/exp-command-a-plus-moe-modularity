# Ablation result data

Causal family-ablation results for the Command A+ modularity study. The **decisive** file is
`consolidation_verdict.json`; `metric_battery.json` shows the same families under every metric we ran
(the measurement-dependence evidence).

| File | Contents | Primary source job |
|---|---|---|
| `consolidation_verdict.json` | Hardened verdict (paper Table 1): per-family on-target effect + 95% CI, random null, worst off-target, under both the point rule and the conservative CI rule. Independent Wikipedia corpus. | `1f061675` |
| `bf16_verdict.json` | Quantization-confound check: the same ablations re-run on the **un-quantized BF16 base model** (8×A100). The verdict reproduces (CI rule 1/6, Arabic), so the negative finding is not a 4-bit artifact. | `3ccba554` |
| `metric_battery.json` | The six families scored under task accuracy, problem-NLL, solution-NLL, FLoRes/Belebele NLL, and the independent-corpus CI run — the evidence that the verdict flips with measurement. | multiple (see file) |

## Provenance and fidelity

The structured JSONs are distilled from the Transformer Lab runs in experiment
`autoresearch-theta-modularity-20260612` (jobs cited per row / in `metric_battery.json`). The
decisive numbers, on-target effects, 95% CIs, null bands, and worst off-targets, are taken verbatim
from the consolidation run `1f061675`. The verdict-level quantities used in the paper are complete and
reproduced in `consolidation_verdict.json`; raw per-condition logs are retained by the authors and
available on request.

Authoritative interpretation: `../FINDINGS.md`.

## Decision rules (both reported, by design)

- **Point rule** (pre-registered): on-target effect > random-null (mean+2σ) AND worst off-target ≤
  on-target/3. → 3/6 modular (ar, es, math); count threshold-sensitive: es passes selectivity by 0.002, code (rejected) fails by 0.009.
- **Conservative CI rule**: lower 95% CI of on-target > null AND upper 95% CI of worst off-target ≤
  (lower 95% CI of on-target)/3. → 1/6 modular (ar only).

We report both because the disagreement *is* part of the finding: modularity verdicts are fragile to
the statistical bar, just as they are to corpus and metric.
