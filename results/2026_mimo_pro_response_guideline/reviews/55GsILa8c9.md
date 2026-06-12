Now I have sufficient calibration data. Let me finalize the review.

## Summary
This paper introduces CausalNovo, a model-agnostic framework for de novo peptide sequencing that uses a Structural Causal Model to motivate disentangling causal (signal fragment ions) from non-causal (noise peaks) representations in mass spectra. The framework adds a Causality Extraction Module (CEM) trained with contrastive independence, cross-entropy sufficiency, and purification objectives. Experiments on three datasets with three baselines show consistent improvements of up to ~12% in amino acid, peptide, and PTM-level metrics, with strong robustness to noise perturbation.

## Strengths
- **Comprehensive empirical evaluation across diverse settings**: CausalNovo is applied to three architecturally different baselines (CasaNovo, AdaNovo, π-HelixNovo) across three benchmark datasets (Nine-species, Seven-species, HC-PT) with consistent improvements in every combination at amino acid, peptide, and PTM levels (Tables 1, 2). For example, on Seven-species amino acid precision: CasaNovo 0.357→0.477 (+12.0%), π-HelixNovo 0.465→0.536 (+7.1%).

- **Strong robustness evidence via vulnerability and NSR analysis**: The vulnerability analysis (Figures 1, 3; Table 6) demonstrates that baselines degrade substantially when noise peaks are perturbed, while CausalNovo mitigates this (relative improvements of 13.5–28.5% at strictest thresholds). NSR generalization (Figure 4) shows consistent precision gains across varying noise-signal ratios (average +10–12%). The pattern of larger gains on harder/noisier datasets provides indirect evidence that improvements come from the causal framework rather than extra capacity alone.

- **Mechanistic evidence via attention analysis**: Table 7 shows CausalNovo increases the fraction of predictions fully attending to causal peaks from 19.26% to 32.87%, and reduces those ignoring causal peaks from 12.73% to 10.76%, supporting the claim that the framework shifts model attention toward signal ions.

- **Model-agnostic design demonstrated with three different architectures**: The CEM operates on latent representations and plugs into any encoder-decoder model with <1% inference overhead, validated across CasaNovo, AdaNovo, and π-HelixNovo without modifying their architectures.

- **Well-motivating preliminary investigation**: Figure 1's systematic noise peak replacement experiment provides concrete, quantitative evidence that existing models rely on spurious correlations, directly motivating the causal framework.

- **Cross-species generalization**: Leave-one-out validation on Nine-species (Table 3) shows CausalNovo improves peptide precision by +2.6% on average across all eight species, and +6.7% on Seven-species (Appendix Table 8), demonstrating generalization beyond standard train/test splits.

## Weaknesses

### Fatal
None

### Major
- **Missing capacity-matched baseline**: The CEM adds 3 Transformer layers + MLP head on top of the 9-layer encoder (Section 4.2, line 221), representing ~33% additional Transformer capacity on the encoder side. No experiment compares against a baseline with equivalent extra capacity but without the causal framework (e.g., a 12-layer encoder CasaNovo). Without this, the reader cannot fully distinguish whether improvements come from the causal framework itself or from additional model capacity. Table 4's ablation varies objectives while keeping CEM parameters present in all rows, so it does not address this. The paper's own vulnerability/NSR analysis provides indirect evidence favoring the causal explanation (larger gains on noisier/harder settings), but a direct control experiment would substantially strengthen the central claim.

- **Loss function composition and key hyperparameters unspecified**: The paper defines four objectives — baseline L_CE (Eq. 1), contrastive loss (Eq. 5), L_CE(z_c) and L_CE(z_s) (Eq. 6) — but never specifies how they are combined into a total training loss, what weights are used for each component, or what fraction α of noise peaks are replaced during perturbation (Section 3.4.1). These are not incidental details: loss weights in multi-objective training can dramatically affect which components dominate, and α directly controls the strength of the causal intervention. This affects both reproducibility and the interpretation of ablation results.

### Minor
- **Gap between SCM framing and implementation**: The paper presents a formal SCM (Figure 2A, Eq. 2) suggesting principled causal inference, but the implementation is more accurately described as causality-motivated invariance learning with data augmentation. Specifically: (1) C ⊥ S in Eq. 2 is an assumption of the SCM, not something enforced by the method; (2) the do(S) intervention is approximated by replacing noise peaks with noise from other training examples — this is data augmentation, not Pearl's do-operator; (3) the sufficiency objective (maximizing I(z_c; Y) via cross-entropy) is equivalent to the baseline's own training loss. The contribution is genuine — the design choices motivated by causal thinking improve robustness — but the paper would benefit from more honest positioning as "causality-motivated invariance learning" rather than implying faithful SCM implementation.

- **Purification mechanism poorly explained**: The paper argues (Section 3.3, line 97) that maximizing I(z_s; Y) "can indirectly lead to the purification of z_c." The actual mechanism — requiring both z_c and z_s to predict Y prevents z_c from becoming a catch-all, while the contrastive objective differentiates stable (causal) vs. unstable (spurious) information — is reasonable from the disentanglement literature but the current explanation reads as contradictory. The paper should clarify this with explicit reference to representation disentanglement principles.

### Trivial
None

## Nice-to-Haves
- A noise-augmentation-only baseline (same augmentation strategy but without CEM or contrastive/purification objectives) would isolate the contribution of the causal mask vs. the augmentation strategy.
- Breaking down the 2.3× training time increase into its sources (extra forward pass for intervened spectrum vs. CEM computation) would help readers assess practicality.
- Discussion of why PointNovo's Seven-species results are anomalously poor (0.196 precision vs. ~0.3–0.5 for other methods on that dataset, line 125).

## Removed Points
These points are flagged to be removed, treat them with caution:
- Typos, formatting issues, or parser artifacts — these are not paper problems.
- The harsh critic's point about Figure 1 y-axis label being confusing — the paper does define RI correctly in Section 4.4, and this is a minor presentation nitpick.
- The harsh critic's point about the sufficiency objective "adding no new inductive bias" — while it's true that the cross-entropy on z_c is the same type of loss as the baseline's, the key difference is that it's applied specifically to the causal component z_c, not to the full representation z. This is a meaningful difference even if the loss form is the same.

## Novel Insights
The vulnerability analysis methodology — systematically perturbing noise peaks to quantify model reliance on spurious correlations — is a valuable evaluation contribution in its own right, and could serve as a standard diagnostic tool for de novo sequencing models. The pattern of larger improvements on harder/noisier datasets provides an important empirical signal that the causal framework addresses the right problem, and the attention analysis (Table 7) provides interpretable mechanistic evidence supporting the causal mechanism.

## Suggestions
- Add a capacity-matched ablation: retrain CasaNovo with 12 encoder layers (matching total CEM capacity) without CEM or new objectives. This single experiment would either confirm that the gains come from the causal framework or reveal that extra capacity explains most of the improvement.
- Add a paragraph specifying the total loss function with explicit weight values (L = L_CE + λ₁·L_contrastive + λ₂·L_CE(z_c) + λ₃·L_CE(z_s)) and report α.
- Clarify the purification mechanism by referencing the representation disentanglement literature and explaining why requiring both z_c and z_s to predict Y, combined with the contrastive objective, drives stable causal information into z_c.

## Calibration Reporting

**All retrieved anchors across both rounds:**

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| GFlowNets KL Divergence | Uj0h13lVrR | 1.00 | 1 | Much weaker paper, rejected |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | 1 | Much weaker, rejected |
| Invariance Starvation | GF6UrrTWp1 | 2.60 | 1 | Weaker paper on spurious correlations |
| Neural Networks Causal Explanations | PoB6QGAM38 | 3.00 | 1 | Weaker causal method |
| Causal Structure Learning | AvXrppAS2o | 3.00 | 1 | Weaker, rejected |
| D3PM Causal Discovery | TRHyAnInUC | 3.25 | 1 | Weaker, rejected |
| Benchmarking AMPs | U5gNAmN3h1 | 3.50 | 1 | Weaker bioinformatics paper |
| CrossNovo (NAT distillation) | I2ZYngkRW6 | 4.25 | 1 | Same domain, rejected; weaker analysis |
| SurfFlow Peptide Design | MeCPwqrm19 | 4.60 | 1 | Related domain, weaker |
| Diversity Peptide Design | VY96NfQRIo | 4.75 | 1 | Related domain, weaker |
| Causal Rep Learning Identifiability | q07DDpu8Xb | 5.25 | 1 | More theoretical, rejected |
| Causal Framework Image Quality | ctvVXwUlnw | 5.25 | 1 | Weaker causal application |
| Feasible Recourse | SKfBx2rv2c | 5.00 | 1 | Weaker, rejected |
| OOD Self-Supervised Learning | 22ywev7zMt | 5.67 | 1 | Related concept, rejected |
| Fine-Tuning Causal Rep | tlH4vDii0E | 5.60 | 1 | Similar motivation, rejected |
| Nonlinear Rep Learning | 7oT1X8xjIk | 5.80 | 1 | More theoretical, rejected |
| Spawrious Benchmark | W0zgCR6FIE | 5.75 | 1 | Spurious correlations benchmark |
| Synergy Disentangled Rep | G1r2rBkUdu | 6.00 | 1 | Related disentanglement work |
| Causal Information Bottleneck | qac43AwuL9 | 6.00 | 1 | More theoretical causal work |
| Post-Nonlinear Causal | yQUbpAHbIZ | 6.00 | 1 | Causal discovery method |
| MADGEN Mass-Spec | 78tc3EiUrN | 6.00 | 1 | Related mass-spec domain |
| Yet Another ICU Benchmark | ox2ATRM90I | 6.20 | 1 | ML framework for bio |
| PepHAR Peptide Design | jqmptcSNVG | 6.20 | 1 | Related peptide domain |
| RNA Geometric Context | 9htTvHkUhh | 6.33 | 1 | Bioinformatics, geometric |
| ReNovo (de novo sequencing) | uQnvYP7yX9 | 6.50 | 1 | **Most directly comparable**: same domain, similar quality |
| Robust Causal/Anticausal | Q0s6kgrUMr | 6.67 | 1 | Causal discovery, accepted |
| AU-GOOD OOD Biochem | qFZnAC4GHR | 6.67 | 1 | OOD generalization biochem |
| Interaction Asymmetry | cCl10IU836 | 7.00 | 2 | Stronger theoretical contribution |
| Fast Uncovering Protein Diversity | 1iuaxjssVp | 7.25 | 1 | Stronger protein work |
| Two-layer Transformers | 97rOQDPmk2 | 7.33 | 1 | More theoretical transformer work |
| Intervention Extrapolation | 3cuJwmPxXj | 8.00 | 1 | Much stronger theoretical contribution |
| Comparing Noisy Neural Dynamics | cNmu0hZ4CL | 8.00 | 1 | Stronger, different domain |
| Cross-Entropy Invert DGP | hrqNOxpItr | 8.00 | 1 | Stronger theoretical |
| Root Cause Analysis Anomalies | k38Th3x4d9 | 8.00 | 1 | Stronger applied causal |
| Optimal Transport Comparisons | cNmu0hZ4CL | 8.00 | 1 | Strong theoretical work |
| Feature Matching Intervention | 8GhwePP7vA | 4.25 | 2 | Causal rep learning, rejected |
| Identifiability Nonlinear Rep | 7oT1X8xjIk | 5.80 | 2 | Theoretical, rejected |

**Round 1 bracket: 6.0 – 7.5**

**Reasoning:** CausalNovo is clearly stronger than CrossNovo (4.25, same domain, rejected for weak analysis and limited novelty) and comparable to or slightly stronger than ReNovo (6.50, same domain, accepted). It has more comprehensive analysis (vulnerability, NSR, cross-species, attention) and a more principled framework than ReNovo, but also has the loss-weights gap and missing capacity-matched baseline. It is weaker than the more theoretical causal papers at 7-8 (Interaction Asymmetry, Intervention Extrapolation) which have stronger formal contributions. The paper sits comfortably in the 6-7 range for applied papers with strong empirical evaluation.

**Final score: 6.5** — This places it as comparable to ReNovo (6.50) with slightly different trade-offs. The comprehensive evaluation and model-agnostic design are strong, but the missing capacity-matched baseline and unspecified loss weights prevent it from reaching 7+. The paper would likely move to 7+ with the suggested additions.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>