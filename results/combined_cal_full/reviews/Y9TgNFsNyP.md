## Summary

This paper introduces FF-Erase, the first machine unlearning method designed specifically for Forward-Forward (FF) neural networks. FF models use layer-wise greedy optimization of a "goodness" score rather than backpropagation, which breaks conventional gradient-ascent-based unlearning methods. FF-Erase addresses this by using a guidance model (generated via mini-retraining or fast distillation) to provide stable target goodness distributions, then performs unlearning by shifting the original model's layer-wise goodness vectors toward these targets via KL divergence. The paper also proposes G-MIA, a membership inference attack that leverages FF models' layer-wise goodness vectors for verifying unlearning. Experiments on VGG13/CIFAR-10 show FF-Erase achieves 1.9–3.1× speedup over retraining with comparable effectiveness.

## Strengths

- **Guidance-model approach is well-motivated and cleanly validated.** The core design — using a separate guidance model to provide target goodness distributions and unlearning via KL divergence rather than direct goodness minimization — directly addresses the instability challenge the paper identifies. The ablation study (Table 1) convincingly validates this: a randomly initialized guidance model (R.G.M) causes catastrophic accuracy drop to 51.18%, while proper guidance models (D-(0.5,0.5), R-(0.5,0.5)) maintain 78–81% accuracy. This is a clear causal demonstration that the guidance model is necessary.

- **G-MIA exploits an FF-specific signal that is genuinely novel.** Using layer-wise goodness vectors — which are a natural and cheap output of FF inference — for membership inference is a creative architectural insight. The paper demonstrates (Figure 3) that G-MIA consistently outperforms the standard black-box FL baseline across all tested architectures (TinyCNN, AlexNet, VGG13) and datasets, and sometimes matches or exceeds white-box methods on deeper architectures. This is a non-trivial finding about the informativeness of FF goodness vectors.

- **Problem formulation is original and timely.** The paper correctly identifies that FF models' layer-wise independent optimization, absence of a global loss function, and sensitivity to parameter tuning make standard BP-based unlearning methods structurally inapplicable. To the best of my knowledge, no prior work has addressed unlearning for FF models.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Inconsistent classification of G-MIA as black-box.** The paper's own taxonomy (Section 2, line 62) defines black-box MIAs as those that "only use the model's final prediction output." G-MIA uses goodness vectors from all layers, which are not the single final prediction. However, in FF models the goodness vectors from all layers *are* the model's natural output for inference (Section 3.1, line 88: "FF models output the goodness vectors from all layers g^1, g^2, ..., g^L for inference"), distinguishing them from raw hidden activations used by white-box methods (GAP, ST). The paper should make this distinction explicit rather than relying on the blue/red background coloring in Figure 3. This does not invalidate the contribution — G-MIA still exploits an FF-specific signal — but the framing needs correction.

- **Main unlearning evaluation rests on a single architecture-dataset pair in the main text.** The core unlearning results (Figure 4, Section 6.2) — including the efficiency (1.9–3.1× speedup) and effectiveness comparisons — are presented only for VGG13 on CIFAR-10. The paper notes additional results are in Appendix C (which the parser has stripped). The G-MIA evaluation (Figure 3) is broader (3 architectures, 4 datasets), but the unlearning validation itself needs at least one additional pair in the main body to support the strength of the claims made, particularly the claimed 1.9–3.1× speedup range.

- **G-MIA scores in the unlearning evaluation lack statistical confidence.** In Figure 4(c), the G-MIA scores across methods are very close: RE (0.5320), FF-Erase(D) (0.5245), FF-Erase(R) (0.5260), GA λ=10 (0.5520) — all within ~3% of each other. (Note: the lower G-MIA for FF-Erase(D) than RE is not "internally inconsistent" as one reviewer claimed — lower G-MIA means less information leakage, consistent with strong unlearning.) The paper reports no confidence intervals, standard deviations, or repeated-trial information. Given the small differences, the reliability of G-MIA as a distinguishing verification metric is not fully established.

### Trivial

- The early-stopping thresholds ε₁ and ε₂ in Algorithm 1 are mentioned but their practical setting (fixed across experiments vs. tuned per dataset) is not discussed.

## Nice-to-Haves

- The paper compares FF-Erase against only two baselines (RE and GA). While this is defensible for a first-of-its-kind method (the paper's scope is that BP-based methods fundamentally don't transfer), demonstrating the failure of one more adapted method would strengthen the "problem identification" contribution.
- Experimenting with different forgetting ratios (currently fixed at 20%) would improve understanding of the method's robustness.
- A diagnostic showing per-layer goodness distributions during failed GA unlearning attempts would strengthen the motivation about layer divergence.

## Removed Points

These points were flagged for removal; treat them with caution:

1. **"G-MIA is not a black-box attack, invalidating its contribution"** (critic's fatal claim): Demoted to Minor. The paper (Section 3.1) states that goodness vectors from all layers are the FF model's natural inference output, distinguishing them from raw hidden activations. The inconsistency in the paper's own taxonomy is real, but it does not invalidate the contribution.
2. **"Baseline comparison too narrow"**: Removed as scope creep. The paper's core contribution is a first-of-its-kind method for a new architecture; it is reasonable to demonstrate why the simplest representative baseline (GA) fails rather than adapting every prior BP-based method.
3. **"FF-Erase(D) lower G-MIA than RE is internally inconsistent"**: Factually incorrect. Lower G-MIA = less information leakage = better unlearning. There is no contradiction. The valid sub-concern (lack of CIs) is retained above.
4. **Comparison against FL is "unfair"**: Addressed by point 1 above. G-MIA uses goodness vectors which are the FF model's natural output, not internal activations.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the G-MIA access model.** Explicitly state that goodness vectors are the FF model's natural inference output (not internal activations), and explain why this justifies the "black-box" label in the FF context. Distinguish clearly from white-box methods that access raw hidden activations.
2. **Add confidence intervals or standard deviations** for G-MIA scores in Figure 4(c) and Table 1, ideally from multiple random seeds.
3. **Include at least one more architecture-dataset pair** (e.g., AlexNet on CIFAR-100 or TinyCNN on Fashion-MNIST) for the unlearning evaluation in the main text.
4. **Discuss the choice of ε₁, ε₂** — whether they are fixed across all experiments or tuned per dataset.
5. **Consider analyzing per-layer goodness distributions** during GA unlearning to empirically demonstrate the divergence mechanism described in Section 1.

## Score and Decision

**Calibration anchors used:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| PPU | Xagys9QD3T.md | 3.00 | R1 | Yes | Has severe formatting/privacy negatives (-7.68, -6.78); this paper has none. |
| SPE-Unlearn | drrXhD2r8V.md | 5.00 | R1 | Yes | Has -8.50 evaluation concern; this paper's negatives are far milder. |
| TARF | OHOmpkGiYK.md | 5.75 | R1, R2 | Yes | Has -7.42 effectiveness concern; this paper lacks comparable severity. |
| SFD | gjwhDHeAsz.md | 6.50 | R1 | Yes | Very strong positives but also -6.66/-6.09 negatives; this paper's negatives are milder. |
| Deep Unlearning | pUOesbrlw4.md | 5.25 | R2 | No | Training-free class unlearning; comparable novelty level but this paper has stronger ablation. |
| Label-Agnostic Forgetting | SIZWiya7FE.md | 6.00 | R2 | No | Supervision-free unlearning; similar evaluation breadth. |
| NegMerge | bKQJzuBSRJ.md | 6.00 | R2 | No | Weight negation for unlearning; similar score band. |

**Scoring rationale:** Round 1 bracket was 5.75–6.5. The paper sits at **6.0**. This is below SFD (6.5) because SFD has stronger theoretical foundations (+4.21) and broader evaluation, but above TARF (5.75) because TARF had a -7.42 effectiveness concern and this paper lacks comparable severity. The weighted-item comparison shows this paper's strongest positive (+5.29 for G-MIA signal) and strongest negative (-1.41 for narrow CI) both support a mid-6 score — the positives are genuinely strong but the weaknesses (narrow main-text unlearning evaluation, G-MIA framing inconsistency, no CIs) prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>