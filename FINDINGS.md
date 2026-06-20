# Findings — Command A+ expert modularity (2026-06-18)

> The authoritative account of the result, accompanying the paper. Every number traces to the
> Transformer Lab job ids cited (experiment `autoresearch-theta-modularity-20260612`); the
> verdict-level data is in [`results/`](results/), and raw per-condition logs are retained by the
> authors and available on request.

## 1. Question and method (one paragraph)

Does a frontier sparse MoE (Command A+: 218B total / 25B active; 128 experts, 8 active, +1 shared;
32 layers; W4A4 NVFP4) organize its experts into **functional modules** — families that each own a
capability or a language, such that ablating a family selectively breaks its own axis while sparing
the others? We build a routing-mass **atlas**, **pre-register** six family→axis hypotheses before any
intervention (math, code, general; Arabic, Chinese, Spanish), and **causally test** each by
inference-time router masking (verified exact, leak=0) against a **size-matched random-16 null**.
A family is **modular** iff its on-target effect beats the null **and** its worst off-target effect
is ≤ ⅓ of on-target (selectivity). A positive control on Qwen3-30B-A3B (recovers its published
disjoint language/task structure: IoU 0.60 vs 0.19) confirms the detector is sensitive.

## 2. The evidence battery

We measured the same six families under **four metrics**, because the result turned out to depend on
the metric — which is itself a finding. All are causal ablations vs the size-16 random null.

| Pass | Metric | Job | What it measures |
|---|---|---|---|
| Capability accuracy | task accuracy (MATH-500/HumanEval/MMLU-Pro) | `e6a67e68` | end-task solving |
| Capability problem-NLL | NLL on the problem text | `11cbdd93` | domain-text familiarity (metric-confound control) |
| Capability solution-NLL | NLL on the gold solution | `d3e27498` | likelihood of the correct output |
| Language accuracy | Belebele MC accuracy | `6969d6da` | near-ceiling — **uninformative (low power)** |
| Language NLL (FLoRes-200) | NLL on FLoRes-200 passages (via Belebele, which is built on them) | `eb4eb07a` | per-language modeling, corpus #1 |
| **Consolidation (hardened)** | **NLL on independent Wikipedia corpus + bootstrap 95% CIs** | `1f061675` | **the decisive test, corpus #2** |

The language leg therefore spans **two distinct corpora**: FLoRes-200 passages (curated parallel
sentences, reached via Belebele) and Wikipedia (natural articles). They disagree on Spanish, which is
the corpus-dependence result itself. (FLoRes was gated as a standalone dataset; the same passages
came through Belebele, so no FLoRes content was lost.)

The consolidation run (`1f061675`) is the one to trust: independent corpus (Wikipedia, not Belebele),
higher n (120/lang; math 80 / code 120 / general 150), and bootstrap CIs with a conservative
CI-based verdict. It is the basis for the headline.

## 3. Headline finding

**Robust functional modularity in this frontier MoE is rare and measurement-fragile.** Of six
pre-registered families, **only the Arabic-language family is a clean causal module** that survives an
independent corpus, a conservative statistical bar, and metric variation. Every other family sits
*at the decision boundary*, and its "modularity" flips depending on the corpus, the metric, or the
statistical treatment. **In Command A+, apparent modularity is therefore largely an artifact of measurement choices** — a claim about this model under this protocol, not a base rate for MoEs in general; what generalizes is the methodological requirement that modularity claims be measurement-controlled.

## 4. The hardened verdict (consolidation run `1f061675`)

Per-language NLL on **independent Wikipedia text**; capabilities via solution-NLL; bootstrap 95% CIs.
We report **both** decision rules, because they disagree and honesty requires showing the fragility:

| family | on-target NLL↑ [95% CI] | null+2σ | beats null | worst off-target | **point rule** (≤⅓) | **conservative CI rule** |
|---|---|---|---|---|---|---|
| **ar** (lang) | **1.80** [1.73, 1.86] | 0.64 | ✓ | 0.43 @en | ✅ modular | ✅ **MODULAR** |
| es (lang) | 1.29 [1.23, 1.36] | 0.58 | ✓ | **0.43 @ar** | ✅ modular *(by 0.002)* | ❌ no |
| zh (lang) | 0.63 [0.59, 0.67] | 0.42 | ✓ | 0.37 @en | ❌ no | ❌ no |
| math (cap) | 0.37 [0.33, 0.41] | 0.15 | ✓ | 0.08 @general | ✅ modular | ❌ no |
| code (cap) | 0.49 [0.39, 0.61] | 0.08 | ✓ | 0.17 @math | ❌ no *(by 0.009)* | ❌ no |
| general (cap) | 0.10 [0.05, 0.16] | 0.19 | ✗ | — | ❌ no | ❌ no |

- **Pre-registered point rule: 3/6 modular** (ar, es, math). The boundary is crowded: es clears
  selectivity by 0.002 and the *rejected* code family misses by 0.009, so two families straddle it
  from opposite sides and the 3/6 *count* is threshold-sensitive. But of the three admitted, only
  Arabic also survives the conservative CI rule: es fails it (and is corpus-dependent), and math —
  though it clears the point rule by a comfortable 0.04 — collapses under CIs and reverses under task
  accuracy. The point rule's extra positives are exactly what the conservative rule and the
  multi-metric battery are designed to catch.
- **Conservative CI rule: 1/6 modular** (ar only).
- Every family except `general` has a **real causal effect** (beats its null) — the question is
  always *selectivity*, not whether the experts matter.

## 5. The one robust positive: the Arabic module

The Arabic family is a clean module by every standard we applied: ablating it raises Arabic
per-token NLL by +1.80 nats [95% CI 1.73, 1.86] — a ~6× rise in perplexity (8.2 → 49) — against a
random-null band of just 0.64 nats, on an independent corpus, while the worst off-target (English,
+0.43) stays well under the selectivity bar. This is a
genuine, defensible result: **we causally localize a clean Arabic-language expert module in a
frontier MoE.** (Arabic is high-lift in the atlas — 1.95, second only to math — consistent with
routing concentration pointing at it; but routing concentration alone did *not* reliably predict
modularity for the other families, see §7.)

## 6. Why everything else fails — measurement-dependence, with mechanism

The interesting part is *how* the other families fail, because each failure is a different axis of
fragility:

- **Spanish is corpus-dependent.** Clean on the FLoRes-200 passages (`eb4eb07a`: worst-off 0.19), but
  on independent Wikipedia text ablating Spanish bleeds **+0.43 into Arabic** — right at the threshold.
  The es and ar families overlap in only 2 of their 16 experts ({30, 86}; Jaccard 0.067); we report
  the bleed but do not isolate whether those shared experts or broader functional entanglement drive
  it. So "Spanish is modular" held on FLoRes-200 but not on a second, naturalistic corpus.
- **Math is metric-dependent.** Entangled with general reasoning under **accuracy** (ablating math
  drops MMLU-Pro by 0.11, `e6a67e68`); apparently selective under **solution-NLL** point estimates
  (`d3e27498`); not selective once CIs are applied (`1f061675`). The math↔general entanglement is a
  **shared-reasoning** effect that appears only when the off-target metric engages reasoning (task
  accuracy) and recedes when it does not (likelihood of a short answer phrase).
- **Code is metric-dependent the other way.** No detectable **accuracy** effect (0.00 on HumanEval —
  but n=60, single seed, underpowered to separate redundancy from a small real effect), yet the
  *largest* problem-NLL effect of any capability (+1.29, `11cbdd93`) — heavily entangled (bleeds +0.62
  into math) and a real but non-selective solution effect (+0.49). So the code experts demonstrably
  *process* code text and are *not selective*; whether they are dispensable for *solving* is not
  established by the underpowered 0.00 accuracy null.
- **Chinese and general** never clear selectivity / the null under any powered metric.

**Mechanistic summary:** apparent modularity dissolves under (a) an independent corpus (Spanish),
(b) a metric that engages the shared computation (math under accuracy), and (c) a conservative
statistical bar (CIs). Only Arabic is invariant to all three.

## 7. Secondary findings

- **Routing mass is an unreliable guide to modularity.** The routing-defined "universal" shared-core
  is causally **inert/redundant** (dose-response: masking 32 most-shared experts costs only ~0.11
  MMLU, graceful, no cliff — `e6a67e68`). Family **lift** correlates loosely with causal importance
  (the two highest-lift families, math 2.15 and ar 1.95, are the ones with the strongest causal
  effects), but lift does **not** predict *selectivity*: high-lift code/math families are entangled.
- **The atlas shows weak structural separation in Command A+** (within-vs-cross family Jaccard gap
  0.09) versus a large gap in the Qwen3 control (0.41) — Command A+ routing does not factor into
  clean families to begin with, foreshadowing the causal result.
- **The detector works** (Qwen3 positive control) — so the failures are about the model, not a broken
  method. (Establishes sensitivity; a negative control remains future work.)

## 8. Proposed thesis for the paper (for co-author decision)

> **Functional modularity in a frontier MoE is rare and measurement-dependent.** Across six
> pre-registered expert families tested causally, only the Arabic-language family is a robust,
> selective module; every other family sits at the decision boundary and its apparent modularity
> flips with corpus, metric, or statistical rigor. The methodological lesson is that ablation-based
> modularity claims are artifacts unless the corpus, metric, and statistical bar are controlled — and
> that, so controlled, only one of six families in this model survives as a clean module — we make no base-rate claim about MoEs in general from one model; the methodological requirement, not the count, is what generalizes.

Contribution = (1) a rigorous, pre-registered, control-anchored causal protocol; (2) one clean
positive (the Arabic module); (3) a cautionary demonstration that, in this model, apparent modularity is fragile to corpus, metric, and statistical choices (measurement-induced), with explicit mechanisms for each failure mode. The base-rate framing is scoped to Command A+; the methodological lesson is what generalizes.

## 9. Scope and claim bounds

- **Bound to:** routing-mass-defined families, 16/128 (12.5%) inference-time ablation, on the **W4A4
  (NVFP4)** build of Command A+.
- **Not claimed:** that no modular structure exists under a different atlas (causal-attribution,
  extreme-deviation), under injection, or under large-fraction ablation. Absence of selectivity under
  this method ≠ absence of modularity in general.

## 10. Limitations

- **Quantization (ADDRESSED — BF16 re-run):** a natural worry is that 4-bit blur manufactures the
  apparent non-selectivity (a false negative). We tested it directly by re-running the identical
  consolidation ablations on the **un-quantized BF16 base model** (8×A100, TP=8). **The verdict
  reproduces:** CI rule 1/6 (Arabic; ar on +1.81 vs W4A4 +1.80, null 0.69), and zh/math/code/general
  non-selective within hundredths of the W4A4 effects. The only mover is the knife-edge **es**, whose
  point-rule selectivity flips from just passing in W4A4 (+0.002) to just failing in BF16 (−0.015) —
  reinforcing that it sits exactly on the boundary. So the negative finding is a property of the
  model, not quantization. (Corroborating: the router is full precision; selectivity is
  condition-dependent, not uniformly smeared.)
- **Power:** n = 120/lang, 80–150/capability, single seed (bootstrap CIs mitigate but do not replace
  multiple seeds). The `general` axis is noisy even at n=150.
- **Corpus:** the language leg spans two corpora (FLoRes-200 passages via Belebele, and Wikipedia);
  a wider sweep of corpora would further probe corpus-dependence. (FLoRes was gated as a standalone
  dataset but its passages were reached through Belebele, so no FLoRes content was lost.)
- **Coverage:** rag and safety capability families never tested; the modularity question for them is
  open (the diffuse/fragile pattern predicts they are not clean modules).
- **n=1 robust module:** with only Arabic surviving, we cannot say *which* languages modularize
  (script-distinctness? resource level?) — a single example, not a class.
- **Metric for "capability":** no single metric cleanly measures a reasoning capability; we triangulate
  with three and report the disagreement rather than picking one.

## 11. Followups (explicitly out of scope, deferred)

- Causal-attribution atlas (define families by ablation impact, not routing) — the natural fix for
  the "routing ≠ causal" limitation.
- Injection (force experts on) and large-fraction dose-response — probe what 16/128 ablation cannot.
- More languages — to test *which* languages form modules and why Arabic does.
- rag/safety capability cells; BF16 confirmatory re-run; multi-seed power.

## 12. Provenance

Atlas `9a2a6a9f` · positive control `cf54fcff` · mask smoke `3b50d227` · control bands `23dd2b18` ·
capability accuracy `e6a67e68` · capability problem-NLL `11cbdd93` · capability solution-NLL
`d3e27498` · language Belebele `6969d6da` · language FLoRes-200 NLL `eb4eb07a` · **consolidation
(hardened) `1f061675`**. Verdict-level data in [`results/`](results/); raw per-condition logs retained
by the authors, available on request. Experiment `autoresearch-theta-modularity-20260612`.
