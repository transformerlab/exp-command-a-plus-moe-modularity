# Reproducibility — theta (Command A+ modularity)

Everything needed to reproduce the causal modularity test.

## Model (pinned)
- **Repo:** `CohereLabs/command-a-plus-05-2026-w4a4` (W4A4 NVFP4, Apache-2.0). Architecture verified at
  runtime: 128 experts, 8 active/token, +1 shared, 32 layers (text decoder MoE; text-only).
- **Revision:** pin the resolved HF commit SHA at run time (the arch-smoke job logs it).
- **Positive control:** `Qwen/Qwen3-30B-A3B`.

## Hardware / serving
- 1× B200 (RunPod), vLLM ≥0.21 in-process (`VLLM_ENABLE_V1_MULTIPROCESSING=0`, `enforce_eager`,
  `gpu_memory_utilization=0.90`), CUDA-13 + forward-compat shim. NVFP4 kernels via `cohere_melody`.
  Note: NVFP4 requires **Blackwell** (B200); Hopper (H100/H200/GH200) and the RunPod REST `/v1/pods`
  GPU enum (no B300) will not serve this build.
- **Ablation operator:** monkeypatch `vllm…fused_moe.layer.FusedMoE.forward`; set masked experts'
  router logits to `-inf` before top-k+softmax (router-mask + gate renormalization). For Qwen3 the
  capture uses a global gate-output hook.

## Seeds / config
- Generation: `temperature=0` (math/MMLU/Belebele/NLL), `temperature=0.2` (HumanEval code-exec), `seed=0`.
- Random-expert null draws: `RNG_SEED=2026` (s5.5 + consolidation); `RNG_SEED=1234` (s5.2 bands).
- Bootstrap: `N_BOOT=2000`, seeded `np.random.default_rng(2026)`.

## Metrics
- **Accuracy:** MATH-500 (boxed-answer), HumanEval (pass@1, code-exec), MMLU-Pro (MC exact-match).
- **NLL:** mean per-token NLL via vLLM prompt-logprobs (no generation). Problem-NLL = on the problem
  text; solution-NLL = teacher-forced on the gold continuation; language-NLL = on held-out passages.
- **Language corpora (two):** FLoRes-200 passages (reached via `facebook/belebele`, which is built on
  them) for the first powered NLL run, and an independent **Wikipedia** corpus (`wikimedia/wikipedia`,
  streamed) for the decisive consolidation run. (FLoRes was gated as a standalone dataset; its passages
  came through Belebele, so no FLoRes content was lost.) The two corpora disagree on Spanish.

## Decision rules
A family is modular iff its on-target effect beats the size-16 random null (mean+2σ) AND its worst
within-domain off-target effect ≤ ⅓ of on-target. Reported under both the **point** rule (raw effects)
and the **conservative CI** rule (bootstrap 95% bounds). See `results/README.md`.

## Run ledger (experiment `autoresearch-theta-modularity-20260612`)
| Run | Job |
|---|---|
| Mask-mechanism smoke (leak=0) | `3b50d227` |
| Qwen3 positive control | `cf54fcff` |
| Atlas capture → pre-registration | `9a2a6a9f` |
| Control bands (random null, shared-core) | `23dd2b18` |
| Capability accuracy ablation | `e6a67e68` |
| Language ablation (Belebele accuracy) | `6969d6da` |
| Language re-test (FLoRes-200 passage NLL, via Belebele) | `eb4eb07a` |
| Capability problem-NLL control | `11cbdd93` |
| Capability solution-NLL | `d3e27498` |
| **Consolidation (decisive: indep corpus + CIs)** | `1f061675` |

## Known caveats
- W4A4 quantization: results are for the quantized build; a BF16 confirmatory re-run is future work
  (multi-card B200 provisioning was unavailable). The surviving Arabic module argues quantization did
  not uniformly erase specialization.
- n = 80–150 per axis, single seed (bootstrap CIs mitigate); one independent corpus (Wikipedia).
- rag/safety capability families untested.
