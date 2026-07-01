Based on the calibration anchors, let me provide my final review.

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| On-Device Transfer Learning (Mixed Precision) | 2.50 | R1 | Much weaker — no real deployment, CNNs only. WASI is stronger. |
| SubZero (4.25) | 4.25 | R1 | Similar memory-efficiency scope, stronger theory but SGD-only limitation. WASI has real deployment advantage. |
| Targeted Low-rank Refinement (4.50) | 4.50 | R1 | Similar experimental concerns. WASI has more comprehensive transformer evaluation. |
| TensorGPT (3.75) | 3.75 | R1 | Training-free compression. WASI addresses a more challenging problem (training). |
| SLiM (3.67) | 3.67 | R2 | One-shot compression. Narrower scope than WASI. |
| Low-Rank Correction for Quantized LLMs (5.00) | 5.00 | R2 | Most comparable — combines known techniques, gaps in analysis. WASI has RPi5 deployment but weaker assumption validation. |
| ROSA (6.00) | 6.00 | R1 | Stronger theory, more thorough experiments. WASI is weaker. |
| AdaRankGrad (7.00) | 7.00 | R1 | Thorough theory + experiments. WASI significantly weaker. |

**Round-1 Bracket:** 4.0–6.0 (between SubZero's fixable gaps and ROSA's stronger execution)

**Score Determination:** The paper sits closest to LRC (5.00) — both combine known techniques into practical solutions, both have experimental gaps. WASI's strengths (RPi5 deployment, joint compression formulation) are offset by its weaker central assumption validation (one layer) and the flawed TinyLlama experiment. Score: **5.0**.

---

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a method that jointly compresses both weights and activations into low-rank subspaces during transformer fine-tuning, targeting on-device deployment. By computing SVD once at the start of fine-tuning and reusing the subspace via iteration, WASI reduces memory and computation during both training and inference. The method is evaluated on ViT, SwinT, and (as an extension) TinyLlama.

## Strengths

1. **Joint compression of weights and activations addresses a genuine gap.** Most prior work (ASI for activations only, SVD-LLM/LoRA for weights only) handles one side. WASI enables inference directly in the compressed space — a practical advantage that neither LoRA (identical inference to full model) nor ASI (leaves weights untouched) achieves.

2. **Real deployment measurement on Raspberry Pi 5 (Section 4.4).** The paper measures actual wall-clock time per iteration on edge hardware (ViT/CIFAR-10, batch size 128), reporting ~1.4× speedup over vanilla training at ε=0.9. This grounds the claims in practice rather than relying purely on simulated FLOPs/memory.

3. **The stability hypothesis is plausible and supported by preliminary evidence.** Fig. 3a shows that singular values of a ViT weight layer remain stable across 40 fine-tuning epochs on Pets. Prior work (Radiya-Dixit & Wang, 2020; Li & Zhang, 2021) also supports the claim that fine-tuned models remain close to their pre-trained parameters.

## Weaknesses

### Major

1. **The central claim about subspace stability is validated on only one layer of one model.** The method's core premise — that the subspace computed at iteration 0 can be reused throughout fine-tuning — is supported by Fig. 3a, which monitors singular values of *layer W6 of ViT on Pets* (Section 4.2: "In these experiments, we focus on fine-tuning ViT model using Pets dataset"). The paper does not examine other layers (shallow vs. deep), SwinT, other datasets, or different learning rate regimes. If subspace drift occurs in unexamined settings, the fixed-rank approximation degrades silently with no detection mechanism. This is a significant evidential gap for a method whose entire computational savings depend on this property.

2. **The TinyLlama experiment (Section 4.3) has critical methodological problems.** (a) *Selective resource logging*: "For comparison, we log the resource consumption only at the layers that are fine-tuned" (line 227). When only the last 1–5 layers are fine-tuned, measuring only those layers inflates the reported savings (953.86× activation memory, 30.12× weight memory) relative to what the full model actually consumes. (b) *Incomparable regime*: ε=0.1 is used here while all other experiments use ε∈[0.4, 0.9] — preserving 10% of variance is far more aggressive, making FLOPs reductions (13.11× training, 30.27× inference) incomparable to the main results. (c) *Thin evaluation*: Only BoolQ is tested, with accuracy in a narrow 64–66% range; insufficient to demonstrate generality to language models.

### Minor

3. **LoRA is critiqued in related work but never included as an empirical baseline.** The paper argues LoRA has "two notable drawbacks" (Section 2) and states WASI "avoids LoRA adapters" (line 221), yet standard LoRA fine-tuning is absent from all experiments. While SVD-LLM uses LoRA-style adapters, a direct comparison against standard LoRA is needed to substantiate the claimed advantages.

4. **SVD-LLM is applied as a vision transformer baseline despite the paper stating it "cannot be directly applied to all vision transformer-based models" (line 47).** The mismatch between SVD-LLM's design target (LLMs) and the evaluation context (ViT/SwinT) weakens the informativeness of this comparison, even if the adaptation was reasonable.

5. **Key quantitative results are presented only in figures, not tables.** Figures 5 and 6 show accuracy vs. resource curves, but the paper never provides a table with exact top-1 accuracy, memory, and FLOPs for each method at each compression level. This makes precise verification of claims like "matches vanilla accuracy at ε=0.9" unnecessarily difficult.

6. **The abstract's headline claims mix theoretical projections with empirical measurements.** The abstract states "reducing... computational cost (FLOPs) by up to 2×." The 2× figure does not appear as a measured result in the main text — the SwinT experiment shows 1.5× FLOPs reduction (line 225), the Raspberry Pi wall-clock speedup is 1.4× (line 245). The 2× appears to be a theoretical maximum from the complexity analysis (Section 3.4). Conflating a theoretical upper bound with empirical measurements in the same sentence is misleading.

### Trivial

7. **The complexity analysis (Section 3.4) assumes the same optimal rank for weights and activations** — acknowledged as a simplification, but limits the practical relevance of the theoretical projections since optimal ranks likely differ.

## Nice-to-Haves

- Broader validation of subspace stability across multiple layers, architectures (SwinT), and datasets would substantially strengthen the paper's core assumption.
- A direct LoRA baseline (standard LoRA fine-tuning) would make the comparison more complete.
- Accuracy tables showing exact top-1 accuracy for each method/compression level would improve reproducibility.
- For the TinyLlama experiment, measuring full-model resources and using ε values within [0.4, 0.9] would make results comparable to the main experiments.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **"Core technical novelty is the combination of two existing techniques"** — References the dynamic programming improvement and 3D tensor support as "relegated to the appendix without evaluation." The appendix was stripped by the paper parser; evaluating content that existed in the original submission is not appropriate.
- **"No statistical significance/variance"** — Single-run evaluation is standard for large-scale benchmarks in this setting.
- **"No discussion of subspace iteration convergence"** — Nice-to-have for an empirical systems paper.
- **"Missing related works"** / **"Overstating limitations of prior methods"** — Cannot be verified or is subjective.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Broaden stability validation.** Show rank stability across at least 3–5 layers of varying depth, on both ViT and SwinT, on at least two datasets. A table of rank(K_i) at epochs 0, 10, 20, 30, 40 would suffice.
2. **Fix the TinyLlama experiment.** Measure full-model resources, use ε∈[0.4, 0.9], and include at least one additional dataset. Or de-emphasize these results.
3. **Add accuracy tables.** Provide exact top-1 accuracy, memory, and FLOPs for each method/compression level.
4. **Clarify the 2× FLOPs claim.** Source it to a specific experiment or acknowledge it as a theoretical upper bound distinct from empirical measurements.
5. **Add LoRA as a baseline** to substantiate the claimed advantages discussed in related work.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>