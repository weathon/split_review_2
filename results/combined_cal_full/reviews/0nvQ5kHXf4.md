Now I have enough information for a well-calibrated review. Let me produce the final output.

## Summary

This paper introduces Weight-Activation Subspace Iteration (WASI), a method for resource-constrained fine-tuning of transformers that jointly compresses weight matrices and activation maps into low-rank subspaces using a combination of SVD and warm-started subspace iteration. The core insight is that parameter subspaces remain stable during fine-tuning, enabling efficient reuse of the subspace across training iterations. Experiments on ViT, SwinT, and TinyLlama across multiple datasets show memory savings up to 62× and a ~1.4× wall-clock speedup on a Raspberry Pi 5 compared to vanilla training.

## Strengths

- **Novel joint compression of weights and activations.** Prior work compresses either weights (SVD-LLM, ASVD) or activations (ASI, AMC) but not both simultaneously in a unified training loop. WASI's combination of Weight Subspace Iteration (WSI) and Activation Subspace Iteration (ASI) is clearly motivated by the observation that both are bottlenecks (Sec. 3.1).

- **Empirical validation of the subspace stability assumption.** Fig. 3a directly measures singular value evolution over 40 epochs and confirms that weight subspaces remain stable during fine-tuning. This distinguishes WASI from methods like ASVD/FWSVD that lack a theoretical grounding for truncation choices.

- **Real hardware deployment validation.** The Raspberry Pi 5 experiments (Fig. 8) demonstrate ~1.4× wall-clock speedup, showing that savings translate beyond simulated FLOP counts to actual resource-constrained hardware. Many papers in this area stop at GPU simulations.

- **Substantial memory savings on vision transformers.** The reported 62× memory reduction (SwinT, Fig. 6) and 953.86× activation memory reduction (TinyLlama, Fig. 7) demonstrate that joint weight-activation compression can dramatically reduce the memory footprint of transformer fine-tuning.

## Weaknesses

### Fatal
None.

### Major

- **Missing LoRA baseline despite extensive discussion.** The paper discusses LoRA at length in Related Work (Section 2), explicitly frames WASI as overcoming LoRA's limitations (frozen weights co-existing with adapters, inference reverts to full model), but never benchmarks against it. The only weight-compression baseline (SVD-LLM) cannot be directly applied to vision transformers (the paper states this in line 47). LoRA is the most natural competitor for any parameter-efficient fine-tuning method and is widely used on ViT. Its absence weakens every comparative claim in Section 4.3.

- **TinyLlama experiment does not establish generality to LLMs.** The language model experiment (Section 4.3, Fig. 7) is limited to: (1) one dataset (BoolQ) with low absolute accuracy (~64-66%, well below typical fine-tuned BoolQ accuracy of 75-85%), (2) a single aggressive compression setting (ε=0.1), (3) only the last 5 layers fine-tuned with resources logged only at those layers (meaning the 953.86× figure is a partial accounting excluding frozen layers), and (4) no comparison against standard LLM fine-tuning baselines like LoRA. This does not convincingly demonstrate that WASI transfers to language modeling tasks.

### Minor

- **No error bars or statistical rigor.** No results include error bars, standard deviations, or repeated trial information. This matters for accuracy comparisons (a single run can differ by 1-2% on small datasets like CUB or Flowers) and especially for the Raspberry Pi latency measurements (Fig. 8), where CPU runtime is notoriously noisy and single-point measurements are insufficient.

- **No WSI-only ablation.** The paper includes ASI as a baseline (Fig. 5), so the marginal benefit of WSI can be partially inferred by comparing WASI vs. ASI. However, a standalone WSI-only baseline (weight compression without activation compression) would more cleanly disentangle whether weight compression adds meaningful value beyond what activation compression alone achieves.

- **Method overhead not analyzed.** WASI involves Gram-Schmidt orthogonalization (Algorithm 1) and iterative subspace updates. The paper does not analyze the computational overhead of these operations relative to the savings. The on-device speedup of only 1.4× vs. higher theoretical compression ratios suggests significant overhead that should be quantified and discussed.

- **Scope overclaiming.** The claim that "the underlying principles apply broadly to any neural network trained with backpropagation" (Conclusion, line 259) is unsubstantiated — only transformers (ViT, SwinT, TinyLlama) are tested. Convolutional networks have different architectural properties that may affect applicability.

### Trivial
None.

## Nice-to-Haves

- The WSI vs. SVD comparison (Fig. 3b) could be strengthened by also comparing against computing SVD once at initialization and fixing the subspace, which would more directly test whether the "iteration" component of WSI adds value beyond the initial decomposition.
- Clarify the memory accounting: specify whether the 62× figure counts only MLP linear layer memory or total model memory, and provide a breakdown of what is included (parameters, activations, optimizer states).

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **WSI vs SVD comparison is a strawman** — REMOVED. The paper compares WSI against recomputing truncated SVD at every training iteration, which is a valid upper-bound comparison to validate that subspace iteration preserves accuracy. This is a standard experimental design for approximation methods. The paper never claims SVD-every-iteration is a practical competitor; it uses it as a gold-standard reference to show WSI achieves comparable accuracy at lower cost.

2. **Notation issues with overline in Eq. 9-10** — REMOVED. The paper refers to Appendix A.1 for definitions, which was stripped by the parser. Minor notation clarification is a formatting artifact of the extracted text.

3. **Section 3.4 assumption about same optimal rank** — REMOVED. The paper explicitly acknowledges this as a simplification (line 165), and the actual experiments use independent ε thresholds for each component. This is standard practice for complexity analysis.

4. **Overclaim about "first method"** — REMOVED. While the word "jointly" would be more precise, this is a minor phrasing issue that does not threaten the core contribution.

5. **The 62× figure may come mostly from activation compression** — REMOVED. The paper reports separate weight and activation memory savings (30.12× weight, 953.86× activation for TinyLlama), and the WASI vs. ASI comparison in Fig. 5 allows readers to assess the marginal contribution of weight compression.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add LoRA as a direct experimental baseline across all vision transformer tasks.
2. Run TinyLlama experiments with full-model fine-tuning, report vanilla accuracy as a concrete number, compare against LoRA, and include at least one additional dataset.
3. Report standard deviations or error bars for key accuracy and latency measurements, particularly the Raspberry Pi results.
4. Add a breakdown table of what contributes to the reported memory savings (parameters, activations, optimizer states).
5. Analyze the computational overhead of subspace iteration (Gram-Schmidt orthogonalization, etc.) and discuss the gap between theoretical and realized speedup.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| nR0n4R1Ck2 (SubTrack-Grad) | 4.75 | R1 | Yes | Similar topic (gradient subspace tracking), had more fundamental weaknesses (theoretical gaps, missing memory validation) — WASI is slightly stronger due to cleaner practical contribution and hardware validation |
| 0tsJ7Nv5hk (OIALR - Orthogonality Low-Rank) | 4.25 | R1 | Yes | Very similar topic (SVD-based low-rank training), was seen as marginal with no baseline comparisons — WASI has clearer contribution and stronger evaluation |
| udtrtwkvk5 (GoLore/Subspace Optimization) | 5.25 | R1 | Yes | Similar topic (subspace optimization), had strong theory but limited experiments — WASI is comparable, with stronger experiments but weaker theory |
| LvNROciCne (AdaRankGrad) | 7.00 | R1 | Yes | Similar topic (adaptive gradient rank), had comprehensive experiments and theory — WASI is weaker due to evaluation gaps |
| 8Agcic0csh (Unlocking SVD-Space) | 4.40 | R2 | Yes | SVD-based local training, had major issues with incorrect theory and missing experiments — WASI is stronger |
| VpeAsLmcvg (SiVA/Singular Value Adaptation) | 3.75 | R2 | Yes | SVD-based PEFT, had unconvincing theory and unfair comparisons — WASI is substantially stronger |

**Weighted-item comparison:** WASI's strengths (+4.31 to +4.71) are comparable to or stronger than those of the 4-5 score range anchors (SubTrack-Grad's max +3.97, OIALR's max +4.87). Its major weaknesses (-5.56, -6.62) are significant but less severe than OIALR's (-8.95, -8.86) or SubTrack-Grad's (-7.81). Unlike AdaRankGrad (7.00), WASI lacks the comprehensive evaluation and theoretical depth to reach that tier. The missing LoRA baseline and weak TinyLlama experiment are the primary factors keeping it below the 6+ range.

**Round 1 bracket:** 4.5 – 5.5. **Round 2 narrowing:** The comparison against SubTrack-Grad (4.75) and GoLore (5.25) confirms this bracket. WASI's practical contribution (joint compression, hardware validation) is stronger than SubTrack-Grad's, but the evaluation gaps prevent it from reaching GoLore's 5.25 level despite GoLore's own experimental limitations.

**Final score:** 5.0 — The core idea is novel and the practical motivation is clear, but the evaluation has significant gaps (missing LoRA baseline, weak TinyLlama experiment, no error bars) that prevent the paper from fully establishing its contribution. These are fixable issues, and with a strengthened evaluation this would be a solid contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>