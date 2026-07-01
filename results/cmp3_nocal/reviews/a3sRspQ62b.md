# Review: FourierFlow: Frequency-Aware Flow Matching for Generative Turbulence Modeling

## Summary

FourierFlow proposes a flow-matching framework for generative turbulence modeling that addresses two diagnosed failure modes: spectral bias and common-mode noise. The method combines three components — a Salient Flow Attention (SFA) branch, a Frequency-guided Fourier Mixing (FFM) branch with adaptive fusion, and MAE-based feature alignment during training — and is evaluated on compressible N-S and shear flow benchmarks. The paper demonstrates strong results on the M=0.1 compressible N-S regime and includes generalization tests that go beyond standard practice.

## Strengths

1. **Clear problem diagnosis with supporting evidence.** The paper identifies two specific failure modes (spectral bias and common-mode noise) and provides empirical evidence: Figure 1 shows that STDiT residuals are concentrated at high wavenumbers while FourierFlow produces a more balanced residual spectrum. This targeted diagnosis motivates the method's components rather than assembling unrelated techniques.

2. **Coherent architecture-to-problem mapping.** Each of the three main components addresses a specific diagnosed problem: the FFM branch targets spectral bias explicitly, the SFA branch targets common-mode noise, and the MAE alignment targets high-frequency feature learning implicitly. The ablation study is logically structured around this mapping.

3. **Strong empirical performance on the M=0.1 compressible N-S case.** FourierFlow achieves MSE 0.0277 vs the next best 0.0519 (Ours-Surrogate) — a ~47% improvement. The long-horizon rollout (Figure 8) shows more graceful degradation than surrogate-based rollout, which is practically significant for scientific simulation.

4. **Generalization experiments go beyond standard practice.** The OOD evaluation across different shear/bulk viscosities (Figure 7) and the long-horizon rollout (Figure 8) test dimensions that many PDE-learning papers omit, strengthening the paper's claims about practical applicability.

## Weaknesses

### Fatal
None.

### Major

1. **Ablation numbers are approximate chart readings that disagree with the main results.** In the ablation table (Figure 4), the full FourierFlow model is reported as MSE ~0.05, nRMSE ~0.18, Max_Err ~1.0 on compressible N-S. But in the main results (Table 1), on the same dataset (compressible N-S M=0.1), FourierFlow achieves MSE **0.0277**, nRMSE **0.1530**, Max_Err **0.9625**. The MSE differs by nearly a factor of 2 (0.05 vs 0.0277). The alignment coefficient sweep (Figure 5) reports MSE ~0.06 at γ=0.01, while the main result for the full model is 0.0277. The paper states for the alignment ablation that "All experiments are conducted on compressible N-S simulations using the same settings as in the main results" (line 245), yet the numbers differ substantially. The "~" prefix indicates these are approximate chart readings, which is itself not rigorous reporting for a conference paper. The discrepancy undermines confidence in the quantitative conclusions of the ablation study. **The authors must (a) report exact numerical values rather than chart readings, and (b) clarify whether the ablation uses the same experimental setup as the main results, and if not, specify the differences.**

### Minor

1. **The "~20% on average" claim masks large variation across scenarios.** Examining Table 1: M=0.1 MSE improvement is ~47%, M=1.0 is ~5%, Shear Flow is ~1.6%. The average (~18%) is pulled up almost entirely by the M=0.1 case. On the two harder regimes the margins are thin. Reporting a single aggregate percentage without per-scenario breakdown is misleading. The paper's own data show that the method's advantage is strong on M=0.1 and marginal elsewhere; acknowledging this gradient honestly would make the paper more credible.

2. **Common-mode noise loss terms defined but never used in training.** Section 2.2 defines $\mathcal{L}_{\text{cm}} = \lambda_{\text{cm}} \|\hat{e}_{\text{cm}}\|_2^2$ and a frequency-selective variant, stating they "penalize" common-mode noise. However, the actual training objective in Section 3.3 is $\mathcal{L}_{\text{Total}} = \mathcal{L}_{\text{CFM}} + \gamma \cdot \mathcal{L}_{\text{Align}}$ — neither $\mathcal{L}_{\text{cm}}$ nor $\mathcal{L}_{\text{cm}}^{\text{freq}}$ appears anywhere in the method, loss, or experimental setup. The SFA architecture addresses common-mode noise architecturally, which is fine, but the unused loss formalism in Section 2.2 creates a false expectation. The authors should either remove these loss definitions or incorporate them and report results.

3. **No statistical significance or variance reporting.** Table 1 reports single scalar values with no standard deviations, confidence intervals, or mention of the number of random seeds. Generative models on stochastic PDE data exhibit run-to-run variability. Without error bars, the reader cannot assess whether FourierFlow's margins on M=1.0 (~5%) and Shear Flow (~1.6%) are statistically significant or within noise. This is a standard expectation for ML conference papers.

4. **Data split inconsistency.** Line 208 states "We use 90% of the data for training," while line 212 states "each dataset is randomly split into 80% training, 10% validation, and 10% test sets." These conflict and need correction.

### Trivial

- Figure 7 labels three different lines identically as "Surrogate-MSE," making them visually indistinguishable. This appears to be a labeling error.

## Nice-to-Haves

- **Ablate SFA against vanilla differential attention (Ye et al., 2025) specifically.** The current ablation replaces SFA with standard self-attention (w. SA) or removes it entirely (w/o SFA), but never tests "SFA replaced by vanilla DiffAttn." This makes it impossible to attribute the improvement to the paper's specific SFA modifications (local-neighborhood normalization) versus differential attention in general.
- **Compare against generative baselines in OOD and long-horizon rollout experiments.** The generalization experiments (Figures 7 and 8) only compare FourierFlow against surrogate models. Including at least one strong generative baseline (e.g., STDiT) would clarify whether the temporal stability advantage comes from the generative paradigm broadly or FourierFlow specifically.
- **Clarify whether the hyperparameter $\eta$ in Equation 8 is learned or fixed.** The text says it is "initialized as 1" and "controls how the weight scales with the frequency magnitude," but does not specify whether it is updated during training. If learned, its final value would be informative.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"Theorem 4.1 is elementary and overclaims novelty."** The theorem is a straightforward algebraic consequence of the SNR definition and power-law assumption. However, the paper frames it as motivation for the method (Section 4 "To understand the fundamental limitations..."), not as a novel theoretical contribution. Formalizing known phenomena to motivate method design is standard practice. The critic's framing as a "critical issue" is overstated. (Downgraded from what would be a minor concern; removed because the critic's severity label was disproportionate to the actual content.)
- **"The introduction does not cite prior work on spectral bias in diffusion models."** This is a missing-citation concern that cannot be verified without external sources. (Removed per policy.)
- **"SFA ablation should compare against vanilla DiffAttn."** Moved to Nice-to-Haves above.
- **"The paper does not discuss the computational burden of MAE."** This is a reasonable observation but not a weakness — it is standard to use pretrained feature extractors without a full complexity analysis.
- **"Theorem 4.1... the paper should contextualize this as a known phenomenon and cite relevant work."** As noted above, not verifiable and the theorem is presented as motivation, not as a claimed contribution.

## Novel Insights

The most interesting insight from the reviews is the observation that the paper's three components form a logically tight chain from problem diagnosis to architectural solution — each component explicitly targets a failure mode identified in the preliminary analysis. This design philosophy is worth preserving. However, the same rigor does not extend to the evaluation: the ablation study's reliance on approximate chart-read values weakens the very evidence structure the authors set up. The paper would be significantly stronger if the quantitative evidence matched the quality of the problem decomposition.

## Suggestions

1. Report exact numerical values for all ablation experiments (replace the "~" chart readings with precise numbers).
2. Reconcile the ablation numbers with the main results, or explicitly state any differences in experimental conditions.
3. Remove the $\mathcal{L}_{\text{cm}}$ and $\mathcal{L}_{\text{cm}}^{\text{freq}}$ loss definitions from Section 2.2, or incorporate them into the training objective and report results.
4. Add standard deviations over multiple seeds to Table 1.
5. Replace the "~20% on average" claim with per-scenario reporting of margins.
6. Fix the data split inconsistency (90% vs 80% training).
7. Fix the labeling in Figure 7.

## Score and Decision

The paper makes a genuine contribution: it identifies real problems in generative turbulence modeling, designs components with a principled one-to-one mapping to those problems, and achieves strong results, particularly on the M=0.1 compressible N-S benchmark. The generalization experiments are a meaningful strength.

However, the ablation study — which is the primary evidence for the claim that each component contributes meaningfully — reports approximate chart readings that differ substantially from the main results. This is not a fatal flaw (the main results are independently strong), but it prevents full confidence in the component-level analysis. Combined with the lack of variance estimates and the other presentation issues, the paper falls short of the evidential standard for strong acceptance.

The contributions are real and the direction is promising. The issues are fixable with careful revision.

**Score:** 6

**Decision:** Borderline Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>