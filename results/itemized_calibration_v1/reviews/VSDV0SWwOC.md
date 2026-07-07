## Summary

LS-Merge proposes encoding LLM weights into a learned latent space via a Transformer VAE, performing merging operations (interpolation, soup, etc.) on the latent codes, then decoding back to weights. The key innovation is enabling cross-architecture merges (e.g., LLaMA → Gemma) that prior weight-space methods cannot handle, using optimal transport to align disparate latent distributions before interpolation. The paper also contributes a weight-distribution analysis documenting the heavy-tailed, non-Gaussian structure of LLM parameters, and demonstrates that non-linear encoding is necessary (VAE preserves functional performance while PCA collapses).

## Strengths

1. **The core idea is novel and well-motivated.** Encoding LLM weights into a learned latent space and performing merging there directly addresses a real limitation of prior methods: the assumption of architectural homogeneity. The paper correctly identifies that existing weight-space methods (Model Soup, Task Arithmetic, DARE, TIES, etc.) all require matched architectures, and shifting the merge to a fixed-dimensional latent space is a principled way to circumvent this constraint.

2. **The weight distribution analysis (Section 3.1, Table 1) is a concrete empirical contribution.** The finding that LLM weights exhibit markedly high excess kurtosis (up to ~15) with heavy tails, contradicting Gaussian assumptions used in prior weight-space learning work, is useful independently of the proposed method and provides a clear design rationale for the encoder architecture.

3. **The PCA vs. VAE comparison (Table 8) cleanly demonstrates that linear compression is insufficient.** The near-complete collapse of PCA-reconstructed models (MMLU ~25% even at r=1.6) versus the VAE's stable performance (~39-40% across r=1.6 to 4.0) provides strong evidence that pretrained weight manifolds are non-linear, validating the paper's architectural choices.

4. **The OT-based alignment for heterogeneous merging (Section 3.3, Algorithm 1) is technically sound.** Treating heterogeneous merging as a manifold registration problem and solving it with a closed-form Gaussian OT map is principled and computationally tractable, and the ablation (Table 5) shows it helps compared to no alignment.

## Weaknesses

### Fatal

None.

### Major

1. **Cross-architecture results are evaluated on too few benchmarks with too little analysis.** The paper's headline differentiating claim is enabling cross-family model merging. Yet the cross-family evaluation (Table 5) covers only three benchmarks (WinoGrande, ARC-C, HellaSwag), and the gains over the base model are modest (+0.92, +0.56, +1.03). Only one cross-family direction (LLaMA → Gemma) is tested; the reverse direction is not reported. For a contribution framed as enabling cross-architecture merging "for the first time" (conclusion), this evidence base is thin. The intra-family results (Figure 4) show gains but lack tabular detail.

2. **Computational cost is not reported, undermining the "scalable" claim.** The abstract identifies scalability as a first-order challenge ("LLMs contain billions of parameters, which makes latent encoding computationally demanding"), and the conclusion calls the method "scalable." Yet the paper provides no information about: the VAE parameter count, GPU-hours required for training, encoding/decoding latency for a 7B model, or the amount of training data (how many weight snapshots were used). The method requires access to intermediate training checkpoints, which is a significant practical limitation that is not discussed.

3. **Self-merging mechanism is underspecified and the claims are over-interpreted.** The paper describes self-merging as "sampling multiple latent codes from its posterior distribution, merging these codes into a single representation" (Section 4.1) but never specifies: how many samples are drawn, how they are aggregated (mean? median? weighted average?), or how this differs from standard posterior predictive averaging. Moreover, in Table 2, the gain on Gemma-3-4b-it is marginal (54.20 vs 54.10 VAE, +0.10), and the "≈4% average improvement" claim does not clarify whether this is relative or absolute improvement, nor how it is computed across baselines and model sizes.

4. **Inconsistent error reporting undermines evaluation rigor.** Table 2 reports standard deviations (some suspiciously small at 0.00), but Tables 3, 4, 5, 6, and 7 report no standard deviations at all. The 0.00 entries in Table 2 (e.g., `54.20 ± 0.00` on MMLU) are not credible as actual standard deviations and suggest possible rounding artifacts or a lack of multiple independent runs. Without error bars, it is unclear whether observed improvements (e.g., LS-Merge 55.07 vs AIM 54.18 on MMLU in Table 4) are statistically significant.

### Minor

1. **The OT Gaussian approximation is not validated.** The paper shows (Figure 9b, referenced at line 115) that heterogeneous models' latent distributions "lie on disjoint manifolds with different covariance structures." The closed-form Gaussian OT solution assumes latent distributions are Gaussian, but the paper does not evaluate whether this approximation is faithful to the true latent geometry, nor does it compare against empirical (non-parametric) OT or simpler alternatives like affine whitening.

2. **Discrepancy between Table 7 and Table 8 at r=2 is not reconciled.** Table 7 shows VAE generalization at r=2 degrades sharply (Gemma-3-1B-it MMLU drops from 40.76 to 32.22), while Table 8 shows the same VAE with same-architecture reconstruction maintains strong performance at r=2 (MMLU 39.80 vs 41.44 base). This discrepancy is explained by the different settings (cross-architecture generalization vs same-architecture reconstruction), but the paper should discuss why generalization fails at r=2 while reconstruction succeeds.

3. **Ablation (Table 6) does not specify whether "MLP only" and "Attention only" also use OT alignment.** The base scores match Table 5's cross-family setting, suggesting OT is used, but this is not stated. The interpretation that disrupting "learned co-adaptations" depends on knowing the counterfactual.

### Trivial

None.

## Nice-to-Haves

- Comparison against fine-tuning the target model directly, to calibrate whether the modest cross-architecture gains are practically meaningful.
- Analysis of when/why OT-aligned latents degrade performance (Table 5 shows "OT only" is worse than base, suggesting the OT map itself may distort functionally important structure).
- Discussion of how many weight snapshots are needed to train the VAE, since this affects practical accessibility.
- Report KL divergence or reconstruction fidelity metrics (the β-VAE objective is described but its empirical values are never reported).

## Removed Points

*These points were raised in input reviews but are removed for the following reasons:*

- **"Self-merging is not merging in any standard sense"** — semantic argument; the paper clearly defines the operation. The underspecification concern is retained above.
- **"Comparison with Task Arithmetic/AIM mixes settings"** — the paper explains using lm-eval for fair comparison with those baselines; using different benchmarks is a natural consequence of using different evaluation frameworks.
- **"Algorithm 1 vs algorithm 2 numbering error"** — trivial formatting artifact from paper reorganization.
- **"Kurtosis averaging discrepancy"** (Table 1: per-layer vs avg kurtosis) — the avg row aggregates across all layers, not just the representative ones shown; this is a presentation choice, not a data error.
- **"Abstract/Introduction framing is misleading"** — subjective framing criticism without concrete evidential basis.
- Various formatting/style nitpicks and missing related work concerns.

## Novel Insights

The harsh critic's observation about the r=2 discrepancy between Table 7 and Table 8 is a genuinely useful diagnostic: it suggests the learned latent manifold is architecture-specific, which is an important practical limitation the paper could acknowledge more directly. The critic's point that the OT-only baseline (Table 5) degrades performance below the base model is also worth emphasizing — it shows that OT alignment alone, without interpolation with target latents, actively harms performance, which illuminates a limitation of the method under high source-weight mixing.

## Suggestions

1. Report GPU-hours, VAE parameter count, and encoding/decoding latency to substantiate the "scalable" claim.
2. Expand cross-architecture evaluation to include MMLU and GSM8k, and test the reverse direction (Gemma → LLaMA).
3. Specify the self-merging procedure: number of posterior samples, aggregation method, and whether the "≈4%" is relative or absolute.
4. Add error bars (or at minimum report number of independent runs) to all tables; explain the 0.00 std entries in Table 2.
5. Validate the Gaussian OT approximation by comparing against an empirical OT solver on a subset of layers, or at minimum report whether latent distributions are approximately Gaussian.
6. Discuss the discrepancy between reconstruction fidelity (Table 8) and cross-architecture generalization (Table 7) at moderate compression ratios.

## Score and Decision

**Calibration methodology.** I retrieved 18 anchor papers from the deepreview_13k corpus across six score bands. The most directly comparable are model-merging papers in the 3.0–6.0 range:

| Anchor path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `lNtio1tdbL.md` (ATM) | 3.00 | R1 | Yes | Criticized for misrepresenting method as merging and flawed baselines; LS-Merge has sounder methodology |
| `IqGVIU4rvM.md` (VQ-VAE+Diffusion) | 2.50 | R1 | No | Different topic (image tokenizers) |
| `plflYGf23L.md` (CABS) | 4.75 | R2 | Yes | Similar weakness profile: small improvements, missing confidence intervals, limited model coverage — but LS-Merge has stronger novelty |
| `Bq3fEAGXUL.md` (Realistic Eval) | 5.33 | R1 | Yes | Evaluation paper without novel method; LS-Merge has genuine methodological novelty |
| `fvUVe2gJh0.md` (What Matters) | 5.33 | R2 | Yes | Systematic evaluation, rejected due to exclusive focus on PaLM and incomplete theoretical exploration |
| `2pvMZKGYDR.md` (WIDEN) | 5.67 | R2 | Partially | Accepted-style scores (6,6,5) but rejected; similar profile of genuine novelty + limited generalization evidence |
| `D7KJmfEDQP.md` (Gradient Matching) | 6.00 | R1 | Yes | Accepted (6,6,6,6); clear theory, consistent improvements, but "experimental section pretty thin" |
| `j6fsbpAllN.md` (LoRA LEGO) | 6.00 | R1 | Yes | Accepted; creative concept with solid theory and extensive experiments |

**Initial bracket.** After filtering the input review and reading the paper, I identified plausible score range as 4.5–6.0.

**Weighted-item comparison vs closest anchors.** Like `plflYGf23L.md` (4.75) and `2pvMZKGYDR.md` (5.67), LS-Merge has genuine novelty undermined by evidential gaps. However, LS-Merge's shared heavy-weight positive items (novel core idea, principled architectural choice justified by data analysis) are stronger than CABS's. Its shared heavy-weight negative items (thin cross-architecture evaluation, no error bars, uncosted computational claims) are comparable to WIDEN's limited generalization evidence. Unlike the 6.00 anchors (D7KJmfEDQP, j6fsbpAllN), LS-Merge lacks the experimental thoroughness or theoretical depth that would support a borderline-accept score.

**Final score.** I place LS-Merge at **5.0**. The paper introduces a genuinely novel latent-space merging paradigm with clear motivation and several solid empirical analyses (weight distributions, PCA vs VAE). However, its core differentiating claim — enabling cross-architecture model merging — rests on insufficient evidence (3 benchmarks, modest gains, one direction), and the "scalable" framing is unsupported by any cost reporting. These are evidential gaps rather than structural flaws, and a substantially expanded version could be competitive, but in its current form the evidence does not fully support the claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>