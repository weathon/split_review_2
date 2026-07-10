Now I have all the information I need. Here is my final consolidated review.

## Summary

This paper proposes MoEP (Modular Expert Paths), a decoder-only architecture that combines dimensional bottlenecking (shrink/grow MoE blocks) with parallel Transformer blocks and top-k routing to achieve sparsity while keeping the total parameter count fixed. The method is evaluated on the BabyLM strict-small track (10M words) across 14 tasks, comparing against GPT-2 and GPT-BERT baselines. The core idea — achieving sparsity without parameter bloat — is a genuine and underexplored design point.

## Strengths

- **Genuine architectural motivation.** The paper identifies a design point that standard MoE does not address: achieving sparsity while keeping total parameters fixed, rather than adding parameters to increase capacity (abstract, Section 1). The combination of dimensional bottlenecking with parallel blocks at reduced dimension is creative.

- **Controlled, multi-task BabyLM evaluation.** The evaluation follows the official BabyLM strict-small pipeline using the same training data, same tokenizer setup, and 14 diverse tasks spanning both zero-shot and finetuned evaluations (Section 4, Table 1). This provides a reasonably rich empirical basis for a small-scale study.

- **Honest limitations section.** Section 6 openly acknowledges that scaling is uncertain, that reduced-dimensional parallel layers may not transfer to more complex data, and that the current setting is limited. This candor is rare and commendable.

## Weaknesses

### Major

1. **Headline claim oversold and depends on an anomalous task (AoA).** The Introduction (line 31) states MoEP "outperforms all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models." This is not supported by the primary metric. On the macro average excluding AoA (Table 1), MoEP scores 49.00, while every GPT-BERT variant scores higher: 54.10 (causal), 53.65 (focus-causal), 52.40 (mixed-causal) — GP-BERT outperforms MoEP by 3.4–5.1 points. MoEP's claim to be "best overall" depends entirely on including the AoA task, where MoEP scores 53.70 while GPT-BERT variants score near zero or negative (−3.90 to 14.50). This 50+ point gap is never explained. Moreover, the paper's own GPT-2 and MoEP-SwiGLU do not report AoA scores at all (shown as "–" in Table 1), so the AoA-based comparison is incomplete even among the paper's own models. The paper does acknowledge the AoA dependency in Section 5.1, but the Introduction's unqualified claim is misleading.

2. **No ablation studies.** The method has multiple independent design choices: number of parallel blocks (P=4), top-k value (k=2), dimensional reduction ratio (d_L to d_P), balancing loss coefficients (λ), and number of parallel layers (N=10). None are ablated (grep confirms zero matches for any ablation variant). It is impossible to determine whether routing and parallelism contribute beyond the dimensional reduction, whether the load-balancing loss prevents expert collapse, or how sensitive results are to specific hyperparameter choices. For a new-method paper, this is a structural weakness.

3. **No compute or efficiency analysis despite efficiency being the core motivation.** The paper motivates MoEP as "adding sparsity while keeping total parameter count fixed" to improve efficiency, yet provides zero measurements: no FLOPs comparison, no training/inference throughput comparison, no wall-clock breakdown per model, no memory usage analysis. Training is reported only as a combined "1-2 hours on an A100" for all models together. For a paper whose entire appeal hinges on efficiency through sparsity, the absence of any compute measurement is a striking gap.

### Minor

4. **MoEP vs. MoEP-SwiGLU comparison confounded by parameter count.** From Table 2, MoEP has 28M parameters and MoEP-SwiGLU has 38M — a 35% increase. The paper claims this shows "lightweight linear experts are more effective at the small scale" (Section 5.1), but the 10M parameter gap makes it impossible to separate activation-function effects from capacity effects.

5. **Improvement over the paper's own GPT-2 is small and uncharacterized.** The paper's own GPT-2 implementation (48.10 excl-AoA) already beats the official BabyLM GPT-2 baseline (46.60) by 1.5 points, suggesting the paper's training setup is itself an improvement. MoEP (49.00) exceeds the paper's own GPT-2 by only 0.9 points. No standard deviations or significance tests are reported, so it is unclear whether this gap exceeds run-to-run variance.

6. **Load-balancing loss choice not justified.** The auxiliary loss uses an entropy regularizer (−Σ p_i log p_i, Eq. 2) rather than the standard auxiliary losses used in most MoE work (coefficient-of-variation or squared-loading terms from Switch Transformers or DeepSeek). The choice is not discussed, and the λ coefficients (Eq. 3) are not reported. Additionally, no routing statistics (e.g., fraction of tokens routed to each parallel block, whether experts collapse) are shown to demonstrate that the loss is working.

### Trivial

None.

## Nice-to-Haves

- Report per-task variance (standard deviations across multiple seeds) to characterize run-to-run stability on the 10M-word dataset.
- Clarify the entropy-based load-balancing loss choice and report the λ values used during training.
- Report routing statistics (expert utilization histograms, auxiliary loss values during training).

## Removed Points

These points are flagged to be removed, treat them with caution:

- "No code or reproducibility check" — the paper states code is released (Section 4 Implementation Environment); the reviewer notes URLs are stripped by the parser, which is a known artifact.
- "Checkpoint selection introduces multiple-comparison problem" — speculative and minor; the paper's approach (best fast-eval checkpoint) is standard practice.
- "GPT-2 outperforming the official baseline means the training setup is itself improved" — the paper already acknowledges this (Section 5.1: "Our GPT-2 version slightly outperformed the BabyLM GPT-2 baseline").
- "Standard MoE increases parameters framing conflates different trade-offs" — a framing preference, not an error.
- Various section-by-section observations about individual task scores (Entity Tracking, EWOK, BoolQ) — these are observations without a clear argument for why they constitute a weakness.

## Novel Insights

None beyond the paper's own contributions. The main insight from the reviewer inputs is that the claim structure in the paper's Introduction outstrips what the evidence supports, and the experimental design lacks the depth (ablations, efficiency measurements, variance reporting) needed to substantiate a new architecture. These are standard reviewer observations, not novel meta-insights.

## Suggestions

1. Revise the headline claim to acknowledge that MoEP outperforms GPT-2 baselines at matched parameter count, but is outperformed by GPT-BERT variants on the primary excl-AoA metric. The fact that MoEP matches or exceeds GPT-2 at the same parameter count is itself a meaningful result and should be presented without overclaiming.
2. Add at least one ablation that isolates the routing/parallelism component from the dimensional reduction (e.g., compare MoEP against a version with a single dense layer of equivalent dimension and parameter count replacing the parallel stack).
3. Provide basic compute numbers: FLOPs per forward pass or tokens/second for MoEP vs. GPT-2.
4. Report routing statistics (e.g., parallel block utilization histograms) to demonstrate that sparsity is actually being achieved.
5. Clarify the MoEP-SwiGLU comparison or re-frame it once the parameter-count confound is addressed.
6. Add standard deviations or confidence intervals to the macro averages in Table 1 to show the results are stable.

## Score and Decision

### Calibration

**Round 1 — Bracketing.** I retrieved anchors from six score bands. The strong-reject band (scores 1.00–1.40) contains papers that are not serious research contributions (systematic reviews, jailbreak demos). The reject band (1.5–3.5) contains relevant MoE/small-scale papers: MOEfication (3.40), NanoMoE (3.00), EfficientSkip (2.50). The borderline-reject band (3.5–5.5) contains papers with stronger experimental methodology: Fantastic Experts (4.33), Efficiently pre-training (4.40), Efficient Expert Pruning (5.25). Bands 5.5+ contain papers with thorough experiments and clear claims (No Need to Talk 7.33, MoE++ 8.00).

Bracket after Round 1: **2.5–3.5** (the paper is clearly stronger than strong-reject papers, but lacks the experimental depth of borderline-reject papers).

**Round 2 — Narrowing.** I retrieved five anchors in the 2.0–4.0 range with a BabyLM-tuned query. The most comparable anchors are:
- **MOEfication (3.40)** — similar MoE-sparsity topic, but with ablations and experiments at 300M/8B scale; the reviewed paper is weaker due to missing ablations and compute analysis.
- **NanoMoE (3.00)** — similar parameter-efficient MoE idea, with theoretical proofs but limited experiments; the reviewed paper has more realistic evaluation (BabyLM) but lacks theoretical grounding. Comparable quality.
- **EfficientSkip (2.50)** — weaker overall evaluation (single model, single benchmark); the reviewed paper has stronger evaluation than this.

**Final score: 3.0**. This places the paper in the "reject" band. The paper has a genuinely interesting architecture and a controlled evaluation setting, but the experimental evidence is too thin: the headline claim is oversold (unqualified claim of beating all models when GPT-BERT outperforms MoEP on the primary metric), there are no ablations to justify the multiple design choices, there is no compute analysis despite efficiency being the central motivation, and the key model comparison (MoEP vs. MoEP-SwiGLU) is confounded by a 35% parameter gap. The core idea has merit, but the paper does not provide sufficient evidence to support its claims at a top-conference level.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>