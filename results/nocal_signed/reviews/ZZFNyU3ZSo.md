Now let me assemble the final review.

## Summary

This paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers that handle both generation and understanding. Through empirical analysis of attention weights, layer importance (ARank metric), and task interactions across Show-o and Emu3, the paper identifies that token redundancy varies substantially across tasks and layers, motivating separate routers per task. UniMoD converts selected dense layers into task-specific MoD blocks, reducing training FLOPs by ~15% (Show-o) and ~40% (Emu3) while roughly maintaining benchmark performance.

## Strengths

- **Well-motivated method grounded in multi-perspective empirical analysis (Sections 3.2–3.4).** The paper systematically examines attention weight patterns, ARank-based token redundancy across layers and tasks, and competitive token pruning between tasks, with each observation directly connecting to a specific design decision in UniMoD. This analysis-to-design chain is tighter than the typical "add a module and benchmark" approach. [impact: +9.8]

- **Clean ablation study (Table 5) that isolates the contribution of each component.** Basic MoD, w/o layer switch module, and w/o task-aware router all underperform the full UniMoD, providing direct evidence for the paper's core thesis about the need for task-specific routing. [impact: +9.4]

- **Results on two fundamentally different architectures** (Show-o with diffusion+autoregressive, Emu3 with fully autoregressive), demonstrating generality of the approach. The extension to pure diffusion models (DiT, PixArt) further strengthens this. [impact: +7.0]

- **Honest reporting of limitations**, including transparent disclosure that Emu3 results differ from the original paper because alternative training datasets were used, as official code and data are not publicly available. [impact: +1.7]

## Weaknesses

### Fatal

None.

### Major

- **Large gap between FLOPs reduction and wall-clock training speedup remains insufficiently explained.** For Show-o, FLOPs drop 15.3% (51.1→43.3 TFLOPs) but training cost improves only ~3% (1.30→1.26 x/iter). For Emu3, FLOPs drop 39.9% (89.0→53.5 TFLOPs) but speedup is only 21.3% (3.56→2.80 x/iter). The paper briefly attributes the Show-o-vs-Emu3 difference to tokenizer design but does not explain why the translation from FLOPs to actual speedup is so lossy overall, nor does it provide profiling data (e.g., per-component timing breakdown). This undercuts the paper's headline efficiency claim — the practical gains are meaningfully smaller than the FLOPs numbers suggest. [impact: -6.8]

### Minor

- **Discrepancy between the method description and implementation for layer selection.** Section 4.1 describes an ARank-based procedure that selects "the half of layers with the lowest values," while Section 5.1 states "we transform the last 12 layers into MoD layers." These are not obviously the same; if they happen to coincide because the last 12 layers indeed have the lowest ARank values (plausible from Fig. 3), the paper should state this explicitly. The "w/o layer switch module" ablation then confounds removing ARank-based selection with switching to interleaved layers. [impact: -0.5]

- **The Basic MoD ablation collapses catastrophically on GenEval (0.15 vs. UniMoD's 0.61) while degrading much less on understanding benchmarks** (e.g., MME 960.6 vs. 1093.7). The paper attributes this to a single router struggling to retain important tokens across tasks, but does not explain why generation collapses so disproportionately. Whether this is a genuine limitation of single-router MoD or a tuning artifact / training instability remains unclear. [impact: -0.9]

- **Table 1 shows GQA = 0.0 when skipping layer 3** during inference — a dramatic collapse the paper does not address. This outlier either indicates layer 3 is uniquely critical to the model's function or that the skipping mechanism introduces a confound at that specific layer. [impact: -0.6]

- **The capacity/pruning schedule for Show-o (Section 5.1) is underspecified:** "scale the capacity from 1 down to 0.2" for MMU and "prune 20% of the tokens in the later layers" for T2I. The schedule shape (linear, exponential, etc.) and what constitutes "later layers" are not formally defined. [impact: -0.1]

- **The Emu3 baseline numbers in Table 3 appear to be a re-implementation** — the paper states all Emu3 results differ from the original due to alternative datasets — but this is not explicitly stated for the baseline row, leaving readers unsure whether the "Emu3" row comes from the original codebase or a re-run. [impact: -0.1]

### Trivial

None.

## Nice-to-Haves

- Report variance or confidence intervals for key benchmarks, since several metrics move by small margins (e.g., CLIP score 0.331→0.332) where statistical significance would aid interpretation.
- Provide profiling data (e.g., per-component timing breakdown) to explain why the FLOPs-to-wall-clock translation is lossy.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **"Section 3.2 analysis is descriptive rather than analytical (lines 113–115)"** — REMOVED: The paper reports empirical observations about attention patterns correlating with modeling approaches; it does not claim causal insight, and descriptive analysis is appropriate for motivating design decisions.

2. **"Baselines (Early Exit, Interleaved Layer Skipping) are too naive"** — REMOVED: Partially addressed by the Basic MoD ablation in Table 5, which is a more relevant comparison; the paper's goal is to show simple pruning fails, for which these baselines are adequate.

3. **"Statistical significance / variance not reported"** — MOVED to Nice-to-Haves: Running multiple seeds of 1.4B–8.5B parameter models is expensive; single-run reporting is common in this subfield.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify the relationship between the ARank-based layer selection procedure (Section 4.1) and the fixed "last 12 layers" implementation (Section 5.1), ideally by showing that the last 12 layers indeed have the lowest ARank values.
2. Investigate and explain the GenEval collapse in Basic MoD — e.g., by checking whether the collapse is reproducible with different random seeds or tuning the router learning rate.
3. Formally define the pruning capacity schedule (shape, per-layer values) for both tasks.
4. Clarify whether the Emu3 baseline in Table 3 is from the original paper or a re-implementation.
5. Provide profiling data to bridge the FLOPs-to-wall-clock gap.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>