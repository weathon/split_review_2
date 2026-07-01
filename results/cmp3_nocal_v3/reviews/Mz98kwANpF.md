## Summary

This paper challenges the prevailing multi-component, diversity-seeking approach to multi-task LoRA. It first shows that a simplified multi-head LoRA (M-LoRA, without a router) with high inter-head similarity outperforms complex diversity-enforcing variants. It then demonstrates that a standard single-adapter LoRA with sufficient rank matches multi-component methods. Based on these findings, the paper proposes Align-LoRA, which adds an alignment loss (KL divergence or MMD) to a standard LoRA to explicitly align task representations in the shared down-projection space, achieving zero inference overhead. A-LoRA-K (the KL variant) consistently outperforms baselines across multiple model scales and benchmarks.

## Strengths

- **Provocative empirical finding (Section 3, Table 1, Figure 2):** M-LoRA (no router, high head similarity ~0.85) outperforms R-LoRA and HydraLoRA on a 5-task benchmark using Qwen2.5-3B. This directly challenges the prevailing assumption that head diversity is essential for multi-task LoRA, making a genuinely useful counterpoint to the literature.

- **Increasing-rank experiment (Section 4, Tables 2–3):** The demonstration that a standard LoRA with sufficient rank (rank 10 on Qwen2.5-7B/14B, rank 30 on LLaMA2) matches or exceeds multi-component methods on the Flanv2→BBH setup is informative and well-executed. It provides concrete evidence that architectural complexity may be unnecessary for good multi-task performance.

- **Zero inference overhead (Section 5.1):** Unlike MoE-based multi-component variants, Align-LoRA's weights can be merged back into the base model post-training. This is a genuine practical advantage correctly emphasized by the paper.

- **A-LoRA-K consistently outperforms baselines with fewer parameters (Tables 4–5):** Across all five model settings (Qwen2.5-3B, 7B, 14B; LLaMA3-8B) and both benchmarks, A-LoRA-K (rank 8, 0.20–0.42% params) outperforms standard LoRA (rank 10, 0.25–0.45% params) and all multi-component baselines. This is the paper's strongest evidence.

- **Breadth of evaluation:** Experiments span Qwen2.5 (3B, 7B, 14B), LLaMA2 (7B, 13B), and LLaMA3-8B, providing reasonable coverage across model families and scales.

## Weaknesses

### Fatal
None.

### Major

1. **Missing same-rank LoRA baseline for Align-LoRA comparisons (Tables 4–5).** This is the most consequential experimental gap. In Table 4, A-LoRA-K uses rank 8 (0.20% params), while the LoRA baseline uses rank 10 (0.25% params). In Table 5, A-LoRA-K again uses fewer parameters than the LoRA baseline. While A-LoRA-K outperforming a *higher-capacity* LoRA is suggestive, it confounds two variables: rank and the alignment loss. Without a same-rank LoRA control (e.g., LoRA rank 8 in Tables 4 and 5), the improvement attributed to representation alignment cannot be isolated from rank effects. The paper has LoRA rank 8 results in Table 3, but those use a different training setup (Flanv2) and cannot fill this gap. This control is necessary to support the core claim that alignment, not rank configuration, drives the improvement.

2. **Factually overclaimed results for A-LoRA-M (line 225).** The paper states "both A-LoRA-K and A-LoRA-M significantly outperform the baselines." This is contradicted by the paper's own data:
   - **Table 4 (Qwen2.5-7B):** A-LoRA-M scores 47.53, *below* LoRA (48.36), R-LoRA (48.32), and M-LoRA (48.44).
   - **Table 4 (Qwen2.5-14B):** A-LoRA-M scores 52.24, *below* M-LoRA (53.78) and LoRA (52.93).
   - **Table 5 (Qwen2.5-3B):** A-LoRA-M scores 78.35, *below* M-LoRA (78.51).
   - **Table 5 (Qwen2.5-7B):** A-LoRA-M scores 82.31, *below* M-LoRA (82.46).
   The MMD variant does not work reliably. The paper should acknowledge this limitation and restrict the outperformance claim to A-LoRA-K.

3. **Theoretical analysis (Section 5.3) is not a novel analysis of Align-LoRA.** The bound presented is a standard multi-task learning / domain-adaptation bound (traceable to Ben-David et al., 2006), with nothing specific to LoRA, the rank-r projection, the KL-based alignment loss in Equation (5), or any structural property of Align-LoRA. The claim that "Align-LoRA actively minimizes Δ(D_i, D_j)" is a restatement of the method's objective, not a derivation showing it achieves a tighter bound than alternatives. The paper should either (a) derive LoRA-specific bounds that connect to the alignment loss, or (b) describe this as a standard MTL bound with the contextual observation that Align-LoRA minimizes the discrepancy term — a useful intuition but not a novel theoretical result.

### Minor

4. **No variance or statistical significance reported.** Every result in every table comes from a single run with no standard deviations, confidence intervals, or mention of random seeds. Many claimed improvements are small (e.g., Table 1: M-LoRA 75.45 vs. R-LoRA 74.67, a 0.78-point gap on one 3B model). Without variance estimates, the reader cannot assess whether these differences are stable or within training noise. While single-run evaluation is common in LLM fine-tuning, the paper would be substantially strengthened by reporting variance across seeds for the key comparisons.

5. **Cross-experiment setups weaken the cumulative narrative.** Section 3 (M-LoRA) uses Qwen2.5-3B on a 5-task benchmark with same-task evaluation. Section 4 (increasing rank) uses Flanv2 training → BBH evaluation. Section 5 (Align-LoRA) uses the 5-task training → BBH evaluation (Table 4) plus an 8-task benchmark (Table 5). The claim that "increasing rank matches multi-component methods" is established on a different training distribution (Flanv2) than the M-LoRA finding (5-task set), so the chain of reasoning is less tight than presented. This does not invalidate the individual results but makes the cumulative argument harder to follow.

6. **Strong distributional assumption in alignment loss not discussed (Equation 5).** The alignment loss models each task's representations as a diagonal-covariance Gaussian estimated from a batch. The paper does not discuss: (a) whether the low-dimensional representations are approximately Gaussian, (b) sensitivity to batch size in estimating per-task parameters, or (c) whether the diagonal covariance assumption is reasonable for the rank-r latent space. These are not fatal gaps but merit brief discussion.

### Trivial
None.

## Nice-to-Haves

- Ablation comparing alignment applied to the A matrix vs. the B matrix (or both). The paper's justification for operating on A is plausible and cited, but a direct comparison would strengthen the claim.
- Batch-size sensitivity analysis for the alignment loss, since batch-level Gaussian estimates may be noisy for small batches.
- Analysis of why A-LoRA-M (MMD variant) underperforms relative to A-LoRA-K (KL variant), e.g., sensitivity to kernel choice or weaker gradient signal.
- The feature visualizations relegated to the appendix would strengthen the main paper's core thesis about shared representations if space permits.

## Removed Points

These points were flagged for removal because they are factually incorrect, misunderstand the paper, or lack substance.

1. **"The HydraLoRA 'w/o Router' ablation is not a clean ablation of M-LoRA's mechanism"** — The reviewer claimed the ablation removes the router but does not add multi-head dropout, making it not a clean comparison. However, the paper is using HydraLoRA (which lacks multi-head dropout) precisely to isolate the effect of dropout: removing the router *without* dropout causes performance to drop, confirming that dropout is the critical factor. The reviewer's criticism misunderstands the ablation's purpose. **REMOVED** (factually incorrect criticism).

2. **"Figure 3 showing baselines as flat lines is potentially misleading"** — Showing λ-independent baselines as constant reference lines on a λ-sensitivity plot is standard practice. **REMOVED** (nitpick without substance).

## Novel Insights

The input review surfaces an important meta-observation beyond the paper's own claims: the paper's strongest evidence (A-LoRA-K) and its weakest evidence (A-LoRA-M) are presented as equally supportive in the text, but the data only supports one variant consistently. The reviewer's central methodological point — that the missing same-rank baseline prevents isolating alignment's contribution from rank effects — is the single most important gap that the authors should address. The theoretical analysis being a standard bound with no LoRA-specific derivation is another gap obscured by the paper's confident framing.

## Suggestions

1. **Add a LoRA rank 8 baseline to Tables 4 and 5.** This is the single highest-leverage improvement. If A-LoRA-K (rank 8) outperforms LoRA (rank 8) at the same parameter budget, the core claim that alignment adds value is directly supported.

2. **Correct the overstatement about A-LoRA-M.** Acknowledge that the MMD variant does not consistently outperform baselines, and either remove the claim or restrict it to A-LoRA-K only.

3. **Qualify the theoretical analysis.** Describe it as a framing device that connects standard MTL bounds to the alignment objective, rather than a "novel generalization bound for MTL" specific to Align-LoRA.

4. **Report variance across random seeds** for at least the key comparisons (Tables 1, 4, 5) to establish the stability of the reported improvements.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>