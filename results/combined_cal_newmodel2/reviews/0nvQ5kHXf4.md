Now let me finalize my analysis and write the consolidated review.

**Round 1 bracket**: 4.5–6.5 (above OIALR at 4.25 and SVD-space at 4.40; below AdaRankGrad at 7.00 and ASVD at 6.25).

**Narrowing**: Comparing itemized favorability ratings, the paper's most damaging items (−1.18 for missing LoRA baseline, −0.07 for no variance reporting) are less severe than the −3.83 to −5.64 range seen in the 4.25–4.75 anchors (OIALR, EVA), but the evidential gaps are more numerous than in the 6.25 anchor (ASVD). This places the paper solidly in the 5.0–6.0 range.

**Final score**: 5.5 — borderline accept. The core method is sound and well-motivated, but the evidential presentation has significant gaps that require major revision.

---

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a method that jointly compresses both weights and activations into low-rank subspaces during fine-tuning of transformer models. Building on the observation that weight subspaces remain stable during fine-tuning (analogous to prior work on activation subspace stability), WASI replaces expensive per-iteration SVD with efficient subspace iteration for weights, and combines this with activation subspace compression. The method is evaluated on ViT, SwinT, and TinyLlama across multiple datasets, with on-device deployment on a Raspberry Pi 5.

## Strengths

- **Sound core insight with empirical backing.** The observation that weight subspaces remain stable during fine-tuning (Sec. 3.3, verified in Fig. 3a for layer W6 of ViT) is well-motivated. The paper shows that if the subspace is stable, recomputing the SVD every iteration is wasteful and subspace iteration is the natural replacement. This is empirically validated by comparing WSI to per-iteration SVD (Fig. 3b), which confirms subspace iteration matches SVD quality at lower cost.

- **Unified treatment of weights and activations.** Prior work (ASI, AMC) compressed activations only, leaving weights full-rank during training. WASI compresses both, which is a genuine extension. The gradient computation is re-derived for the joint low-rank space (Eqs. 8–11), and the paper provides this derivation clearly.

- **Breadth of evaluation across model families.** The paper tests on ViT, SwinT, and TinyLlama—spanning vision transformers and a decoder-only LLM—which is more coverage than many on-device learning papers achieve. Real hardware deployment on a Raspberry Pi 5 demonstrates practical feasibility.

## Weaknesses

### Major

- **No statistical significance or variance reporting across all experiments.** Every result is presented as a single value—no multiple seeds, standard deviations, or confidence intervals. This undermines comparative claims when accuracy differences are small: on TinyLlama (Fig. 7) the y-axis spans roughly 64–66% (a 2-point range), on SwinT/CUB WASI is claimed to "surpass vanilla," and the Raspberry Pi 5 timing results (Fig. 8) report single bars with no variance. Without error bars, the reader cannot assess whether claimed advantages are real or within noise.

- **The headline 62× memory reduction claim is ambiguous regarding scope.** The abstract states "reducing memory usage by up to 62×" without qualification. The experimental setup (Sec. 4.1, line 177) clarifies this applies only to "linear layers within multi-perceptron blocks" for fair comparison with prior methods. The fraction of total model memory these MLP linear layers represent is not reported, so readers cannot translate the 62× savings into overall training memory. The abstract will be read by most as total training memory.

- **The TinyLlama experiment (Sec. 4.3) raises significant methodological concerns.** (a) ε=0.1 is an explained-variance threshold of 10%—extremely aggressive compression—yet WASI reportedly matches or exceeds vanilla accuracy with no analysis of why. (b) Resource consumption is "logged only at the layers that are fine-tuned" (the last 5 layers), so the dramatic savings (953.86× activation memory, 30.12× weight memory) apply to a small fraction of the total model, not the full model. (c) Accuracy differences span only ~64–66% on BoolQ (Fig. 7), a narrow band where seed effects could dominate. (d) No comparison against LoRA or other parameter-efficient fine-tuning baselines is provided, which are the natural competitors for LLM fine-tuning (LoRA is discussed at length in Related Work but never used as a baseline).

### Minor

- **No ablation study separating the contributions of WSI (weight compression) from ASI (activation compression).** Since ASI is the direct predecessor, the paper's main claimed addition over prior work is weight compression (WSI). An ablation would cleanly quantify how much each component contributes to the overall savings and accuracy.

- **The SVD-LLM comparison is under-specified in the main text.** The paper notes SVD-LLM "cannot be directly applied to all vision transformer-based models" (Sec. 2), yet applies it as a ViT baseline. The phrase "for fairness, the same compression ratios are applied to SVD-LLM" (Sec. 4.3) is ambiguous—it could mean the same rank or the same ε threshold, which are different. How SVD-LLM was adapted for ViT image classification is not explained in the main paper.

## Nice-to-Haves

- Add an analysis of subspace drift as a function of learning rate to test the stability assumption's limits.
- Report concrete total memory numbers for at least one configuration (e.g., "at ε=0.8 on ViT/CIFAR-10, total training memory was X MB for WASI vs. Y MB for vanilla").
- For the TinyLlama experiment, include results at more standard ε values (0.8, 0.9) and provide an analysis of why ε=0.1 preserves accuracy.

## Removed Points

These points from the input review were filtered out as not substantive, factually wrong, or not applicable to this paper:

- Criticism of "the first method" claim as overstated — The phrasing refers to jointly compressing weights AND activations during training, which is a defensible characterization of the novel combination presented.
- Concern about complexity analysis assuming same rank for weights and activations — The paper explicitly says "for simplicity" and the analysis is presented as illustrative (Sec. 3.4).
- Concern about subspace drift with larger learning rates — The paper's scope is fine-tuning with small learning rates, and empirical validation is provided for one representative layer.
- Concern about WSI vs SVD FLOPs claim based on interpolation — Presenting accuracy-vs-FLOPs tradeoffs via discrete ε markers is standard practice for such comparisons.
- Generic speculation about unfair comparisons — When present, asymmetry favors baselines, not the author's method.

## Novel Insights

None beyond the paper's own contributions. The reviews largely agree with the paper's framing and identify evidential gaps rather than conceptual misunderstandings.

## Suggestions

1. Add multi-seed runs (at least 3–5) with standard deviations for all accuracy, memory, and timing results.
2. Clarify the scope of the 62× claim explicitly in the abstract (e.g., "on MLP linear layers, reducing memory by up to 62×"), and report the fraction of total model memory these layers represent.
3. For the TinyLlama experiment: (a) report total model memory/FLOPs including frozen layers, (b) include LoRA as a baseline, (c) test at more standard ε values (0.8, 0.9) for comparison, (d) provide analysis of why ε=0.1 preserves accuracy.
4. Add an ablation study isolating the contribution of WSI vs. ASI.
5. Clarify how SVD-LLM was adapted for ViT experiments in the main text.

## Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| On-Device TL Mixed Precision | eqKHuxIpp5.md | 2.50 | 1 | Yes | Much weaker: limited scope, poor writing, no baseline comparisons |
| OIALR (Orthogonality Low-Rank) | 0tsJ7Nv5hk.md | 4.25 | 1 | Yes | Similar topic but weaker: marginal contribution concerns, no baseline comparisons |
| SVD-Space Alignment | 8Agcic0csh.md | 4.40 | 1 | Yes | Same "no variance" weakness (−0.07) but also has fatal methodological errors (false Lipschitz claims); our paper is stronger |
| SubTrack-Grad | nR0n4R1Ck2.md | 4.75 | 1 | Yes | Similar evidential gaps but our paper has broader evaluation and no fundamental errors |
| EVA (Explained Variance Adaptation) | DM6Q45HWSk.md | 4.75 | 2 | Yes | Stronger experiments but "limited novelty" (−5.64) much worse than our weakest items; our contribution is clearer |
| MoE-SVD | ho7ZUS1z8A.md | 5.00 | 2 | No | |
| Decomposed Learning | 7Cx05z4pUc.md | 5.00 | 2 | No | |
| Adapprox | RtzxJLPxGk.md | 6.40 | 1 | No | |
| ASVD (Activation-aware SVD) | HyPofygOCT.md | 6.25 | 2 | Yes | Stronger empirical presentation but "minor over SVD-LLM" (−3.25); our novelty is clearer but experiments less rigorous |
| AdaRankGrad | LvNROciCne.md | 7.00 | 1 | Yes | Significantly stronger: theoretical proofs, comprehensive experiments; our paper does not reach this level |
| LDAdam | Zkp1GuHerF.md | 7.00 | 1 | No | |
| Small-scale proxies for training instabilities | d8w0pmvXbZ.md | 8.00 | 1 | No | |

The round-1 bracket was 4.5–6.5. Round 2 narrowed to 5.0–6.0 by comparing itemized favorability against ASVD (6.25) and EVA (4.75). The paper's worst items (−1.18, −0.07) are less damaging than EVA's worst (−5.64, −3.01) but more numerous than ASVD's. Final score: **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>