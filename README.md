# How Modular Is a Frontier Mixture-of-Experts?

Data and reproducibility artifacts for the paper:

> **How Modular Is a Frontier Mixture-of-Experts? A Pre-registered Causal Test in Which
> Apparent Expert Modularity Mostly Dissolves**
> Tony Salomone, Deep Gandhi, Ali Asaria — Transformer Lab.
> arXiv: https://arxiv.org/abs/2606.25092

## TL;DR

We test, causally, whether the experts of **Command A+** (218B total / 25B active; 128 experts,
8 active, +1 shared) form **functional modules** tied to capabilities or languages. We build a
routing-mass **atlas**, **pre-register** six family→axis hypotheses before any intervention, and
ablate each family at inference time against a size-matched random-expert null, measuring whether it
*selectively* breaks its own axis. We score the same ablations under four metrics and a held-out
independent corpus with bootstrap confidence intervals.

**Finding (cautionary): robust functional modularity is rare and measurement-dependent.** Of six
pre-registered families, only **one — the Arabic-language family — is a clean, selective module** that
survives an independent corpus and a conservative statistical bar (1/6; a permissive pre-registered
point rule admits 3/6, but that count is threshold-sensitive: es clears selectivity by only 0.002 and
code misses by 0.009, so families straddle the boundary from both sides). Every other family has a
real causal effect yet fails selectivity, and its apparent modularity **flips with the measurement**:
with the **corpus** (Spanish is selective on one corpus but bleeds into Arabic on a second), the
**metric** (math is entangled with general reasoning under task accuracy but looks selective under
solution-likelihood), or the **statistical bar** (the 1/6-vs-3/6 count). A positive control on
Qwen3-30B-A3B recovers its published disjoint structure, confirming the method detects modularity when
present (a sensitivity check, no negative control); the verdict reproduces on the un-quantized **BF16**
model, ruling out a quantization artifact.

The lesson: **ablation-based modularity claims are not safe unless the corpus, metric, and
statistical bar are controlled** — and, in Command A+ so controlled, only one of six pre-registered
families is a robust module. We make no base-rate claim about MoEs in general from a single model;
what generalizes is the methodological requirement, not the count.

## Repository contents

```
FINDINGS.md                  Authoritative write-up of the result (read this first)
atlas/                       The observational atlas (routing-based)
  atlas_mass.json              Raw per-(layer,expert) routing-mass matrix
  atlas_summary.json           Summary statistics
  prereg_map.json              FROZEN pre-registered family→axis map (the pre-registration)
results/
  consolidation_verdict.json   Hardened verdict (Table 1): independent corpus + bootstrap CIs, both rules
  metric_battery.json          The same families under 4 metrics — the measurement-dependence evidence
  README.md                    Provenance notes
figures/                       The three paper figures + a self-contained regeneration script
  make_figures.py              Regenerates all figures (matplotlib + numpy; no GPU/model/data needed)
```

## Reproducing the figures

```bash
cd figures && python make_figures.py
```

Values are inlined from `FINDINGS.md`, so this needs only `matplotlib` + `numpy`.

## The model

We do **not** redistribute the model. Command A+ is openly available under **Apache-2.0**
(`CohereLabs/command-a-plus-05-2026`; we study the `-w4a4` NVFP4 build). Exact revision pin, seeds,
and the ablation/eval recipe are in `REPRODUCE.md`.

## Harness code

The router-logging, masking, and evaluation **harness is available from the authors on request.**

## Data provenance

Result files are derived from the Transformer Lab runs in experiment
`autoresearch-theta-modularity-20260612`. The decisive run is the consolidation job `1f061675`
(independent corpus + bootstrap CIs). See `FINDINGS.md` §12 for the full job list; raw per-condition
logs are retained by the authors and available on request.

## Citation

```bibtex
@misc{salomone2026modular,
  title         = {How Modular Is a Frontier Mixture-of-Experts? A Pre-registered Causal Test in Which Apparent Expert Modularity Mostly Dissolves},
  author        = {Salomone, Tony and Gandhi, Deep and Asaria, Ali},
  year          = {2026},
  eprint        = {2606.25092},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2606.25092}
}
```

## License

This repository (atlas, ablation data, figures, docs, and the figure script) is licensed under
**[CC BY 4.0](LICENSE)** — reuse freely, including commercially, with attribution. The Command A+
model is not included and is separately under Apache-2.0 (Cohere). See [`LICENSE`](LICENSE) for the
suggested citation.
