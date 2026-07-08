## Summary

This paper introduces Distributed Neural Architectures (DNAs), a new architecture class where tokens/patchs can traverse any sequence of modules in any order, with routing decisions learned end-to-end. DNAs generalize MoE, MoD, parameter sharing, and early exit into a single learnable routing system. The paper demonstrates DNAs in both vision (ImageNet classification at ViT-Small scale) and language (autoregressive LM on FineWeb-Edu at GPT-2 Medium scale), with the central contribution being the feasibility analysis and interpretability study of emergent computation patterns rather than achieving state-of-the-art performance.

## Strengths

- **Conceptually novel architecture class (Sec. 2.1).** The DNA framework formally generalizes MoE, MoD, parameter sharing, and early exit into a single learnable routing system where tokens can traverse any module sequence. This is a clean formalization that makes the routing topology itself learnable rather than fixed — a genuinely new contribution to the conditional computation literature. **[weight=9.11]**

- **Cross-domain validation.** DNAs are demonstrated in both vision (ImageNet classification, Sec. 3) and language (autoregressive LM on FineWeb-Edu, Sec. 4). This dual-domain evidence is substantially stronger than a single-domain demonstration would be and provides evidence that the approach generalizes beyond one modality. **[weight=9.48]**

- **Interpretability analysis yields genuinely novel insights.** The finding that paths specialize — boundary vs. background patches in vision (Fig. 1e), sentence-ending tokens, verb variants, and adjectives in language (Fig. 1f, Sec. 4.2) — is the most striking result. The deep-dream reconstruction analysis (Fig. 4), where early routing decisions recover textures, intermediate ones recover lighting, and later ones recover large-scale features, provides real insight into how the model organizes computation hierarchically. This is the paper's strongest contribution. **[weight=10.35]**

- **Intellectually honest framing.** The paper explicitly states (footnote 3, Sec. 5) that it is not focused on beating SOTA, acknowledges the language models are too small for the data (Sec. 4), and documents cases where findings differ between domains (e.g., parameter sharing correlation in Sec. 4.3). This candor is valuable and sets clear expectations. **[weight=5.89]**

## Weaknesses

### Fatal
None.

### Major

- **No comparison against MoE or MoD baselines** despite the paper framing DNAs as "a natural generalization" of these methods (abstract, Sec. 1) and stating MoE as its "main inspiration" (Sec. 1). The only baselines are dense ViT and GPT-2. The entire motivation for DNAs' additional complexity — learnable routing, dynamic module selection, non-feedforward topology — is that it should provide some advantage over existing conditional computing methods. Without this comparison, the reader cannot assess whether the extra complexity is warranted. This is a decisive evidential gap given the paper's own framing. **[weight=-2.09]**

- **Compute efficiency claims are supported only by a proxy metric** (module counts) rather than actual FLOP or wall-clock measurements. No FLOP, throughput, or latency numbers are reported. The "effective compute nodes" metric conflates attention (quadratic in sequence length) and MLP (linear) operations. Additionally, the 30% skip language model shows substantial degradation on several downstream tasks (e.g., LAMBADA drops from 34.0% to 23.8%, ARC-E from 58.9% to 52.5% in Table 3), which undermines the claim that compute savings come with "minor effects on performance." **[weight=0.72]**

### Minor

- **No multiple seeds, error bars, or confidence intervals** are reported anywhere. Given that the performance differences are small (0.7–1.0% in vision accuracy, 0.03–0.07 in language loss), the reader cannot determine whether the observed gaps are meaningful or just optimization noise. **[weight=3.06]**

- **No ablation of key architectural design choices.** The backbone layers (N_b, used values 0,1,2), the number of modules (N_m), the top-k value, and the identity bias update parameters (r, u) are all free hyperparameters with no systematic study. The paper states that optimization "converges much better" with backbone layers (Sec. 2.2) but provides no controlled experiment demonstrating this. For a paper introducing a new architecture class, ablations would help establish which design choices are critical. **[weight=5.84]**

- **The random baseline observation is not quantitatively resolved.** The paper notes that a randomly initialized DNA model also shows power-law path distributions and can cluster images (Sec. 3.2, Fig. 1c caption), acknowledging this as "surprising." This raises a legitimate concern about how much of the claimed "emergent specialization" is genuinely learned vs. an artifact of the routing mechanism's combinatorial structure. The paper discusses qualitative differences but provides no quantitative metric (e.g., mutual information between paths and semantic classes, or path-path agreement across images) to distinguish trained from random patterns. **[weight=2.48]**

### Trivial
None.

## Nice-to-Haves

- **MoE and MoD baselines** at matched parameter/compute budgets. This is the single most important addition given the paper's framing.
- **Actual FLOP or throughput measurements** to ground the compute efficiency claims.
- **Quantitative comparison** of trained vs. random models on path-specialization metrics.
- **Multiple seeds** with error bars for all reported numbers.
- **Ablation of the backbone layers** (N_b) and other key hyperparameters.

## Removed Points

These points from the input review were removed with justification:

- **"Competitive claim not supported"** — Removed. The paper explicitly disclaims SOTA focus (footnote 3: "our work is *not* focused on beating SOTA models"). 79.1% vs 79.8% on ImageNet (0.7% gap) and top-2 DNA (433M) outperforming GPT-2 (406M) on most language benchmarks is reasonably described as "competitive with dense baselines." The framing is appropriate for a feasibility paper.
- **"Scale too small to support generality"** — Removed. This is a generic criticism applicable to most papers at this scale. The paper acknowledges this limitation for language. ViT-Small scale is standard for analysis-oriented work.
- **"No analysis of training cost"** — Removed. The paper focuses on *inference* efficiency, which is its stated scope. Criticizing the absence of training cost analysis is scope creep.
- **"Table 3 comparison not par-for-params"** — Removed. The paper already includes a "30% shallower" GPT-2 baseline (line 180). The top-2 DNA's comparison against GPT-2 is fair given the paper's feasibility framing.
- Pure formatting, style, and typo complaints — Removed as parser artifacts per instructions.
- Any mention of missing appendix content or unreproducible results from missing appendices — Removed per instructions (appendix stripped by parser).

## Novel Insights

The harsh reviewer's observation that the random DNA baseline shows power-law distributions and path clustering goes beyond what the paper itself engages with. The paper treats this as a curiosity, but the reviewer correctly identifies that this demands quantitative comparison — if a random model already exhibits power-law path distributions and can cluster images, the burden shifts to the authors to quantify *how much more* structure the trained model learns. This is a genuinely insightful critical framing: it suggests that some of the "emergent specialization" might be an inherent property of the routing mechanism's combinatorial structure rather than learned computation, and the paper's qualitative dismissal ("uses a very different similarity measure") is insufficient to resolve this.

## Suggestions

1. **Add MoE and MoD baselines** at matched parameter/compute budgets. This is the single highest-leverage improvement. If DNAs are competitive with MoE/MoD, that is a strong positive result. If they are worse, that is also informative. Either way, the paper's intellectual framing demands this comparison.
2. **Report actual FLOP or throughput numbers** to ground the compute efficiency claims.
3. **Run at least 3 seeds** and report means with error bars/standard deviations.
4. **Quantitatively compare trained vs. random DNA models** on path-specialization metrics (e.g., mutual information between path assignments and semantic classes).
5. **Ablate key design choices** (N_b, N_m, top-k, identity bias parameters) to establish which are critical.

## Score and Decision

### Calibration Report

**Round 1 — Bracketing Search (all bands).** Retrieved anchors across score bands:

| Band | Anchor Path | Avg Score | Topic Match |
|------|------------|-----------|-------------|
| <1.5 | Various low-quality/domain-mismatched papers | 0.5–1.0 | Low |
| 1.5–3.5 | XVHXVdoV11, OovfCS4FYT, fnO5h1CFyh, ZHTYtXijEn | 2.33–3.40 | Moderate (conditional computation) |
| 3.5–5.5 | **ar9tcnD4e9** (Neural Modules), tI3eqOV6Yt (Adaptivity & Modularity) | **4.75, 5.00** | **High** |
| 5.5–7.5 | **1qq1QJKM5q** (COMET, MoE), **T26f9z2rEe** (DynMoE), **QHzzAU7Qf9** (SMEAR) | **5.67, 7.00, 6.00** | **High** |
| 7.5–8.5 | Neuroscience/biology-focused papers | 8.00 | Low |
| >8.5 | None found | — | — |

**Itemized anchors used:** ar9tcnD4e9 (Neural Modules, 4.75), z1mLNhWFyY (Gradient Routing, 5.25), 1qq1QJKM5q (COMET, 5.67), T26f9z2rEe (DynMoE, 7.00), QHzzAU7Qf9 (SMEAR, 6.00), HiTg16qhxp (DNRT, 5.50), RQz7szbVDs (Specialisation Theory, 6.00).

**Weighted-item comparison.** The DNA paper's strongest positive items — interpretability analysis (10.35) and cross-domain validation (9.48) — sit at or above the strongest positive items of the COMET paper (11.27, 9.17) and SMEAR (10.87, 9.27, 9.47). However, the DNA paper's single genuinely negative weight (-2.09 for missing MoE/MoD baseline) is a larger drag than any single weakness in SMEAR (all positive) or COMET (all positive). Gradient Routing (5.25) also has negative-weighted weaknesses (-3.18, -1.89) setting a lower floor. The DNRT paper (5.50) has similar weight distribution with one negative (-1.24) and mostly positive weaknesses.

**Bracket: 5.0–6.0.** The paper sits above Gradient Routing (5.25, has more severe negative-weighted weaknesses) and close to COMET (5.67, similar method paper but with MoE baselines) and DNRT (5.50, similar innovation + evaluation tradeoffs). It sits below SMEAR (6.00, more complete evaluation). The missing MoE/MoD comparison prevents it from reaching the 6.0+ band, but the genuine conceptual novelty and strong interpretability analysis keep it above the 4.5–5.0 range.

**Final score: 5.5.** This reflects a paper with a genuine conceptual contribution and notable interpretability findings, held back by the absence of comparisons against the methods it claims to generalize and incomplete compute efficiency validation.

### Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>