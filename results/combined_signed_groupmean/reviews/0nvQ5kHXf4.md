Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper presents WASI (Weight-Activation Subspace Iteration), a method that jointly compresses both weights and activations into low-rank subspaces during transformer fine-tuning. The core idea leverages the stability of parameter and activation subspaces during fine-tuning to use warm-started subspace iteration rather than recomputing full SVD at every step. The method is evaluated on ViT, SwinT, and TinyLlama models, with a real on-device latency experiment on Raspberry Pi 5.

## Strengths

- **The core insight—that both weight and activation subspaces remain stable during fine-tuning—is empirically supported.** Fig. 3a shows stable singular values of W6 across 40 epochs, and Fig. 4 shows activation energy concentrated in the first few singular values. This provides a plausible foundation for warm-started subspace iteration instead of recomputing full SVD at every step. **[impact=+8.83]**

- **The on-device latency measurement on Raspberry Pi 5 (Fig. 8) is a genuine strength.** WASI achieves ~1.4× wall-clock speedup on real hardware, grounding efficiency claims beyond FLOPs-only estimation. Many papers in this area omit this kind of real-hardware validation. **[impact=+10.00]**

- **The SwinT results across five datasets (Fig. 6) show consistent accuracy-efficiency trade-off improvements**, suggesting the method is not dataset-specific. At ε=0.9, WASI matches vanilla accuracy while cutting memory by up to 62× and FLOPs by 1.5×. **[impact=+3.77]**

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison against LoRA/QLoRA.** The paper discusses LoRA in Related Work and even claims it overlooks activation map costs, but never experimentally compares against it. LoRA is the dominant PEFT baseline; without this comparison, the paper's memory/FLOPs claims ("62× reduction") are relative only to vanilla full fine-tuning—a baseline no practitioner would choose for on-device deployment. The paper's rationale for exclusion ("three directly comparable baselines at the time of conducting experiments," line 177) is insufficient since LoRA predates all baselines used and is the most natural point of comparison for any method claiming memory-efficient fine-tuning. **[impact=-10.00]**

- **The TinyLlama experiment (Sec. 4.3) is not informative.** The setup uses ε=0.1 (extreme compression retaining ~10% explained variance), fine-tunes only the last 5 layers, and achieves ~64–66% accuracy on BoolQ (binary task, random=50%; standard fine-tuned accuracy for models of this size is 75–80%). The paper admits "limited resources" and uses "the same configuration as in our previous experiments" (line 227) for a language task. This suggests the vanilla fine-tuning configuration itself is not working well, making the comparison between WASI and vanilla uninterpretable. The resulting compression numbers (953× activation memory drop) are not meaningful on a broken baseline. **[impact=-10.00]**

- **No ablation studies to isolate the contribution of weight compression within WASI.** The paper contains zero ablation studies. WASI = WSI + ASI, but the individual contribution of WSI is never measured against ASI alone in a controlled comparison. Fig. 5 shows WASI and ASI achieving very similar accuracy-memory Pareto curves for ViT on CIFAR-10, raising the question of how much benefit actually comes from the weight compression component versus what ASI (activation compression only) already provides. Without this ablation, the paper cannot demonstrate that the combination is synergistic rather than additive. **[impact=-9.19]**

### Minor

- **The weight update mechanism (Eq 11) is underspecified in the main text.** Eq 11 states "L_i R_i = L_i R_i + η · ∂L/∂W_i" but does not explain how a gradient on the product L_i R_i translates into individual updates to L_i and R_i. It is unclear whether the factorization is re-computed after each step, whether the gradient is projected onto the low-rank manifold, or whether L_i and R_i are updated via chain-rule factorization. The paper defers to Appendix A.1, leaving a core reproducibility concern in the main exposition. **[impact=-8.62]**

- **The paper characterizes SVD-LLM as using "LoRA adapters"** (lines 221, 223: "WASI achieves up to 100× higher memory efficiency than SVD-LLM at similar accuracy, owing to its avoidance of LoRA adapters"). SVD-LLM (Wang et al., 2024) decomposes weight matrices via SVD and fine-tunes SVD factors directly—it does not use LoRA-style low-rank adapters. This mischaracterization undermines the claimed rationale for the comparison. **[impact=-10.00]**

- **No statistical variance reporting.** All experimental results are presented as single runs without error bars or confidence intervals. Given the stochasticity of training and the sensitivity of low-rank methods to initialization, variance should be reported. **[impact=-8.13]**

### Trivial
None.

## Nice-to-Haves

- **Optimizer state memory accounting.** The paper measures "memory" as weights + activations, but on-device training memory is also dominated by optimizer states (e.g., Adam's two moments). Since WASI reduces weight memory, it also reduces optimizer state memory—this should be explicitly measured and reported.
- **FLOPs counting methodology.** It is unclear whether reported FLOPs include the overhead of subspace iteration (SVD recomputation, orthogonalization, compression/decompression operations). A clear accounting would strengthen credibility.
- **Comparison against freezing weights (subspace not updated)** as a baseline for WSI, rather than only against full SVD recomputation at every iteration.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The paper addresses a genuine and important problem"** (strength): Generic/superficial; removed per filtering rules.
- **"35% higher accuracy claim is misleading"**: The FLOPs-constrained comparison is a standard Pareto analysis—not misleading. Removed.
- **"Abstract 2× FLOPs vs body 1.5× discrepancy"**: The abstract says "up to 2×" which is consistent with body results. Removed.
- **"WSI vs SVD comparison stacks the deck"**: Comparing WSI against full SVD recomputation at every step is a standard and informative baseline for measuring subspace iteration benefits. Removed.
- **"Complexity analysis assumes same rank for weights/activations"**: The paper explicitly states "for simplicity" (line 165) which is acceptable for an illustrative analysis. Removed.
- **"Missing sensitivity analysis for ε"**: The paper does sweep ε across {0.4, 0.5, 0.6, 0.7, 0.8, 0.9} in multiple figures, which constitutes sensitivity analysis. Removed.
- **"Notation simplification hides complexity"**: The paper acknowledges and defers the 3D tensor extension to Appendix A.1, a reasonable treatment. Removed.
- **"Optimizer state memory not accounted for"**: Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface evaluation gaps but do not add new technical insights about the method itself.

## Suggestions

1. **Add a direct comparison against LoRA (and ideally QLoRA)** on at least the ViT/CIFAR-10 and SwinT/Pets setups. This is the single most impactful improvement—it directly addresses whether WASI's joint compression approach offers practical advantages over the dominant PEFT baseline.

2. **Redesign the TinyLlama experiment.** Use a proper ε (0.8–0.9), fine-tune more layers with hyperparameters appropriate for language fine-tuning, and verify that the vanilla baseline achieves expected accuracy levels (75–80% on BoolQ).

3. **Add the core ablation:** WASI vs. ASI-only vs. WSI-only on a small-scale setup (e.g., ViT/CIFAR-10). This directly measures whether the weight compression component contributes beyond what activation compression alone achieves.

4. **Clarify Eq 11** by specifying how gradients flow through the joint low-rank factorization—whether L_i and R_i receive separate gradient updates via the chain rule, or whether the factors are recomputed after each step.

5. **Report results with error bars** over multiple random seeds.

## Score and Decision

**Calibration anchors:**

| Path | Score | Round | Itemized | Comparison |
|------|-------|-------|----------|------------|
| eqKHuxIpp5 (On-Device TL) | 2.50 | 1 | Yes | Much weaker paper; our paper has stronger methodology and more experiments |
| FVgizbs3o2 (TensorGPT) | 3.75 | 2 | Yes | Limited novelty; our paper has more novel methodology but similar evaluation gaps |
| FK6T0U4Mg1 (SubZero) | 4.25 | 1 | Yes | Similar missing-baseline issue; our paper has better practical validation (on-device) |
| 8Agcic0csh (Unlocking SVD-Space) | 4.40 | 1 | No | SVD-based training; similar technical quality |
| nR0n4R1Ck2 (SubTrack-Grad) | 4.75 | 1 | Yes | More limited experimental scope than our paper |
| udtrtwkvk5 (Subspace Opt LLMs) | 5.25 | 1 | Yes | Stronger theoretical contributions, weaker empirical grounding |
| oXh0939Zzq (LoSA) | 5.20 | 2 | No | Better evaluation quality, accepted |

**Bracket reasoning:** Round 1 placed the paper between 4 and 5 (above TensorGPT at 3.75 due to stronger core idea and on-device validation; below the 5.2–5.25 range due to decisive evaluation gaps). Round 2 confirmed this: the paper's strongest weaknesses (missing LoRA at -10.00, TinyLlama at -10.00, missing ablations at -9.19) are more impactful than SubZero's analogous missing-baseline issue (-9.33 for GaLore), because LoRA is a more universally expected baseline than GaLore for PEFT papers. At the same time, the paper's strongest strengths (subspace stability evidence at +8.83, on-device latency at +10.00) exceed those of SubZero and Unlocking SVD-Space. The net impact places the paper slightly below SubTrack-Grad (4.75) and Subspace Opt for LLMs (5.25), whose missing weaknesses were less decisive.

The paper has a sound core idea and genuine empirical strengths (especially the Raspberry Pi latency measurement), but the evaluation has three major gaps that prevent establishing the contribution: no comparison against LoRA, an uninformative TinyLlama experiment, and zero ablation studies. These gaps are fixable in principle but require substantial additional experimentation. The current submission does not meet the bar for acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>