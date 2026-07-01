Here is the final consolidated review.

---

## Summary

This paper proposes HOMIL, a multi-instance learning framework for whole-slide image classification that extends ABMIL by computing both first-order moments (attention-weighted mean) and second-order moments (covariance) from patch features, combined with DBSCAN-based adaptive clustering. The clustering groups similar patches into variable-size clusters—large for abundant normal tissue, small for rare pathological regions—yielding computational savings while preserving diagnostic information. Experiments on CAMELYON16 and TCGA-NSCLC show consistent improvements over nine baselines across ACC, AUC, and F1, with competitive runtime.

## Strengths

1. **Well-motivated statistical framing (Sections 3.1–3.2).** The paper correctly identifies that ABMIL's attention-weighted mean is a first-order moment that discards variability information, and proposes second-order statistics as a principled extension. This conceptual framing is the paper's clearest intellectual contribution.

2. **Computational efficiency is credibly demonstrated and explained.** On CAMELYON16, HOMIL (310s) is faster than ABMIL (455s) despite computing more statistics, because clustering reduces ~3000 patches to ~540 clusters. The paper clearly attributes this to the reduction in effective instance count.

3. **Ablation study (Table 3) is informative.** The paper reports four variants isolating the contributions of the clustering module (CM) and second-order moment module (SOM), allowing readers to see the effect of each component.

4. **Consistent improvements across all metrics and both datasets.** HOMIL achieves top ACC, AUC, and F1 on both CAMELYON16 and TCGA-NSCLC, against nine baselines including recent methods (MambaMIL, HMIL, S4MIL).

## Weaknesses

### Major

1. **No statistical significance testing despite claiming "significantly" improved performance.** The abstract states HOMIL "significantly improves the state-of-the-art performance," but no significance tests are reported. On CAMELYON16, HOMIL's ACC (96.98±2.43) vs. MambaMIL (96.48±1.37) and AUC (99.23±0.62) vs. S4MIL (99.02±0.87) show overlapping standard errors under 5-fold cross-validation. Similarly on TCGA-NSCLC, HOMIL's ACC (93.24±2.47) vs. HMIL (92.89±1.45) has overlapping SE. Without a significance test, the "significantly" claim in the abstract is not supported by the evidence presented.

2. **The ablation reveals that the second-order module alone (without clustering) reduces AUC, which the paper does not discuss.** In Table 3, variant "w/o CM" (keeps second-order moments but removes clustering) achieves AUC 98.14±2.45 vs. ABMIL's 98.88±1.01—a *decrease* of 0.74 points. This means adding the second-order moment to per-patch processing reduces discriminative performance by AUC, even as ACC improves slightly. The paper attributes the AUC drop solely to removing CM (line 270), without acknowledging that what is being compared is ABMIL vs. ABMIL+SOM, and the SOM component on its own is associated with worse AUC. The second-order module only improves AUC when combined with clustering, raising the question of whether the benefit comes from second-order statistics themselves or from an interaction with clustering's smoothing effect. This weakens the paper's causal narrative that second-order moments are independently valuable for WSI classification.

3. **The covariance vectorization via 1D convolution with double max-pooling is ad-hoc and lacks justification (Section 4.3.3).** The paper compresses the d×d covariance matrix to a d-dimensional vector by: (a) convolving each row with T=4 kernels of width m=64, (b) max-pooling over the convolution output per kernel, (c) max-pooling again across kernels. The paper offers no justification for why 1D convolution on rows is appropriate for a covariance matrix, why m=64 and T=4 were chosen, or why two successive max-pooling operations are preferable to simpler alternatives (e.g., vectorizing the upper triangle, eigenvalue decomposition, or using the diagonal directly). Since the output is one scalar per original feature dimension—structurally the same shape as a variance vector—it is unclear whether the off-diagonal (inter-feature correlation) information that motivated the covariance computation is actually preserved or exploited. No comparison against simpler alternatives is provided.

### Minor

4. **The "attention-weighted covariance" label is inconsistent with the formula.** Sections 4.1 (line 108) and 4.3.3 (line 147) repeatedly claim to compute an "attention-weighted covariance matrix," but the formula at line 152 is:
   $$\mathbf{C} = \sum_{k=1}^K \tilde{\mathbf{g}}_k \tilde{\mathbf{g}}_k^\top$$
   This is an *unweighted* sum of outer products of centered cluster features. The centering uses the attention-weighted mean \(\mathbf{v}^{(1)}\), but each cluster contributes equally to the sum regardless of its attention weight. A genuinely attention-weighted covariance would weight each outer product by \(a_k\). This naming imprecision could confuse readers about the role of attention in the second-order computation.

5. **Abstract/method mismatch on what the covariance is computed over.** The abstract (line 9) states "we compute the covariance matrix of the *patch representation vectors* across the entire slide," but the method (Sections 4.1, 4.3.3) clearly computes it over *cluster* features \(\mathbf{g}_k\), which are mean-pooled representations of patches within each DBSCAN cluster. Within-cluster patch variability is discarded before covariance computation. The method sections are internally self-consistent (line 25 says "Both moments are computed based on cluster representations"), but the abstract gives an imprecise description.

6. **Figure 1 caption and method text describe inconsistent architectures.** The Figure 1 caption (lines 85–87) describes "instance features h\_i processed by a Conv1D layer to produce first-order features v^(1) (n × d)" and "a second Conv1D layer to produce second-order features v^(2) (n × d)." However, the method text (Sections 4.3.2–4.3.3) derives v^(1) as a d-dimensional attention-weighted sum of cluster features, and v^(2) as a d-dimensional vector from covariance matrix row-convolution—neither involves Conv1D layers acting on instance features, and both are d-dimensional, not n×d. This discrepancy makes the architecture difficult to interpret correctly.

### Trivial

None.

## Nice-to-Haves

- Add a statistical significance test (e.g., corrected paired t-test across CV folds) and moderate the "significantly improves" language accordingly.
- Ablate the covariance vectorization against simpler alternatives (diagonal-only variance vector, flattened upper triangle, learned projection) to validate that off-diagonal information drives performance.
- Discuss why the second-order module alone (w/o CM) reduces AUC, and whether the full model's gains reflect a synergy effect rather than independent contribution of second-order statistics.
- Align the Figure 1 caption with the method text, or clarify the role of Conv1D layers if they exist in the architecture.

## Removed Points

These points were raised in the initial review but are removed with justification:

- **"The paper does not comment on the learning curves dropping after epoch 30–40."** — The paper explicitly discusses this at line 285. The claim is factually incorrect and removed.
- **"DBSCAN hyperparameters lack justification and sensitivity analysis."** — The paper states a sensitivity analysis exists in the Appendix (line 287). Per policy, content stripped from the submission by the parser cannot be penalized.
- **"Efficiency comparison is confounded because HOMIL's time includes clustering."** — The paper transparently states this at line 240. This is a deliberate disclosure, not a hidden confound.
- **"The special case claim ignores fusion attention parameters."** — Pedantic reading; the claim (ABMIL as a degenerate case) is clear and reasonable.
- **"DBSCAN failure modes not discussed."** — Scope creep; not every methods paper must catalog failure modes of every subcomponent.
- **"The covariance vectorization is structurally identical to a variance vector."** — The output shape is the same (d-dimensional) but the computation uses the full covariance matrix, not just the diagonal. The lack of justification stands; the categorical identity claim does not.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the covariance formula at line 152 to either include attention weights \(a_k\) or rename it from "attention-weighted covariance" to "covariance centered at the attention-weighted mean."
2. Add a statistical significance test for Tables 1–2, and temper the "significantly improves" language in the abstract.
3. Discuss the ablation result showing that the second-order module alone (w/o CM) reduces AUC, and clarify whether the full model's gains reflect an interaction rather than an independent contribution of second-order statistics.
4. Align the Figure 1 caption with the method text.
5. Correct the abstract to say "cluster features" rather than "patch representation vectors."
6. Compare the proposed covariance vectorization against simpler alternatives (diagonal-only, flattened upper-triangle) to validate its design.

## Score and Decision

The paper identifies a genuine limitation of attention-based MIL and proposes a well-motivated framework to address it. The consistent empirical improvements and computational efficiency are real contributions. However, the absence of statistical significance testing, the ablation pattern that undermines the independent value of the core second-order contribution, the unjustified covariance vectorization design, and several presentation inconsistencies collectively reduce confidence. The paper would need substantial revision—particularly around experimental rigor and methodological justification—to be convincing for acceptance.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>