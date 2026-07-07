Now let me produce the final consolidated review.

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), the first complete Riemannian treatment of the Proper Velocity (PV) model — an unconstrained representation of hyperbolic space from special relativity — for deep learning. The authors derive closed-form exponential/logarithmic maps, parallel transport, and geodesic distance for PV space (Theorems 4.3–4.4), then build a full neural network layer suite including MLR with a practical simplification for efficient computation (Theorem 5.2), FC, convolution, activation, and batch normalization. Experiments across numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate that PV's unconstrained nature provides substantial numerical advantages and competitive or superior accuracy.

## Strengths

- **First systematic Riemannian toolkit for the PV model in deep learning.** The paper derives closed-form Exp, Log, parallel transport, and geodesic distance for PV space (Theorems 4.3–4.4). No prior ML work has provided this complete toolkit for this model. The isometry-based derivation strategy (Theorem 4.2 — leveraging the known gyro-isomorphism to Poincaré to transfer operators) is mathematically clean and principled.

- **Complete and principled neural layer suite.** The paper provides MLR with a practically important simplification (Theorem 5.2, Eq. 19) that converts costly per-class gyroaddition into a matrix-multiplication-friendly inner-product form, plus FC, convolution, activation, and batch normalization layers (Section 5). This goes beyond many prior HNN works that only cover a subset of layers.

- **Numerical stability advantage is convincingly demonstrated.** Tables 1–3 show decisive evidence: PV maintains zero failure rate up to scalar multiplier r=1000 in FP32 (hyperboloid fails at r≈20), has orders-of-magnitude better round-trip Exp/Log error, and keeps gradient magnitudes in a safe band while Poincaré gradients vanish and hyperboloid produces NaNs. This advantage follows directly from the unconstrained nature of PV space and is the paper's strongest evidence.

- **Strong and consistent empirical gains on genomic sequence learning.** Table 10 shows PVCNN improving over HCNN-S by ~8–9 MCC points on SINEs and LINEs, with consistent gains across all five TEB tasks. This is the most compelling accuracy evidence in the paper.

## Weaknesses

### Major

- **The framing conflates parameterization advantage with geometric advantage.** Theorem 4.2 proves that PV and the Poincaré ball are Riemannian isometric — they are the same geometric space, just parameterized differently. Yet Section 6.3 states "these results suggest that PV geometry is more effective on strongly hyperbolic graphs." Because the two spaces are isometric, any accuracy improvement must stem from numerical/optimizational advantages during training (stable gradients, no constraint enforcement), not from a fundamentally richer or different geometry. The paper occasionally frames the contribution as a geometric breakthrough when it is, precisely, a *parameterization* breakthrough that yields better numerical behavior. This is a real but fixable framing issue: the contribution should be presented as "a more stable and convenient parameterization of hyperbolic space" rather than "a different/better geometry." The abstract and conclusion largely get this right (focusing on stability and unconstrained representation), but Section 6.3 overstates the claim.

- **Graph learning comparison fairness is not fully verifiable.** On Airport, PVNN achieves 97.96% vs. 92.10% for the strongest baseline (KNN), a striking 5.86% gap. The paper states all models share the same architecture (two FC layers + MLR) differing only in the hyperbolic model. However, the hyperparameter tuning protocol (how curvature K, learning rate, weight decay, and initialization were selected for each baseline) is not described. Without this information, readers cannot assess whether the gap reflects a genuine practical advantage, undertuned baselines, or different hyperparameter budgets. This is the one large-margin result where the effect is big enough to warrant scrutiny.

### Minor

- **Most accuracy improvements are modest and within standard deviation overlap.** On CIFAR-10 (95.30±0.18 vs. 95.12±0.20), CIFAR-100 (78.20±0.37 vs. 77.96±0.09), Disease (81.15±0.23 vs. 80.57±0.23), and PubMed (74.33±0.22 vs. 73.68±0.39), PV improvements over the best baseline are small relative to the reported standard deviations. No statistical significance tests are reported. The paper's accuracy evidence is strongest on genomic (Table 10) and Airport (Table 5), but on most other benchmarks the improvements are marginal.

- **Computational cost of PV layers is not discussed.** The PV MLR (Eq. 19) and FC (Eq. 22) involve special functions (sinh⁻¹, sinh, cosh, sqrt) per output dimension. The wall-clock overhead relative to Euclidean, Poincaré, and hyperboloid layers is not reported, making it hard for practitioners to assess the practical trade-off between numerical stability and computational cost.

- **The K→0 Euclidean limit (Theorems 5.2, 5.3) is stated but not empirically validated.** Showing that at very small |K| the PV layers behave indistinguishably from Euclidean layers would strengthen the correctness claims and give practitioners a clear rule for curvature initialization or scheduling.

### Trivial

None.

## Nice-to-Haves

- Report training dynamics (loss curves, gradient norms during real training) to directly illustrate the optimization advantage that the synthetic Table 3 hints at.
- Run statistical significance tests (e.g., paired t-test or bootstrap) on the main accuracy comparisons to better quantify whether differences are meaningful.
- Investigate the Airport gap further: e.g., apply PVNN's hyperparameter search to the best Poincaré baseline and report whether the gap narrows.
- Empirically validate the K→0 limit behavior.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The 'without Exp₀' variant is under-discussed"** — The paper actually addresses this extensively (Tables 4, 8; text lines 301–302, 359–361). Removed for being factually incorrect about the paper.
- **"Missing appendix / incomplete sections"** — These are parser artifacts; the original submission contains the appendix. Removed per hard rules.
- **"Missing related works"** — Per protocol, this cannot be raised by the meta-reviewer as external sources to confirm missing citations are not available.
- **Formatting, typo, and grammar nitpicks** — These are parser artifacts. Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The reviews surface one genuinely insightful point that the paper itself does not adequately address: because PV and Poincaré are Riemannian isometric (proven in Theorem 4.2), the accuracy improvements on real tasks cannot be attributed to geometric superiority. They must be attributed to numerical/optimizational advantages during training. This distinction is important for correctly interpreting the paper's contribution but is not discussed by the authors.

## Suggestions

1. Reframe the contribution: explicitly acknowledge the isometry and present PV as a *more numerically stable and convenient parameterization* of hyperbolic space, not a different geometry. Change the Section 6.3 claim from "PV geometry is more effective" to "the PV parameterization enables more effective training outcomes."
2. Document the hyperparameter selection protocol for all baselines in the graph learning experiments (curvature K, learning rate, weight decay, initialization scheme, and search budget per model).
3. Add a brief computational cost analysis (wall-clock time per batch) comparing PV layers against Euclidean, Poincaré, and hyperboloid counterparts.
4. Report training dynamics (loss curves per epoch, gradient norms) for one representative task to connect the synthetic stability results (Tables 1–3) to real training behavior.

## Score and Decision

**Score:** 6.0  
**Decision:** Accept

### Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| ekz1hN5QNh.md ("Fully Hyperbolic CNNs") | 6.00 | R1 (bracketing), R2 (narrowing) | Yes | Most structurally similar: both provide a complete hyperbolic layer suite and face "modest improvements" criticism. Our paper has stronger numerical evidence and fewer novelty disputes, but has an additional framing issue. Overall comparable quality. |
| jzneu6AO2x.md ("RHPN - Hyperbolic Prototypical Nets") | 4.25 | R1 (bracketing) | Yes | Rejected primarily for limited novelty (linear combination of existing ideas). Our paper's derivation of the Riemannian toolkit for PV is genuinely novel, placing it clearly above this anchor. |
| WOopKWDWtS.md ("Robust Hyperbolic Deep Learning") | 4.40 | R1 (bracketing) | Yes | Suffered from unclear presentation and marginal improvements with high complexity. Our paper is better organized and its numerical stability evidence is stronger. |
| zbKcFZ6Dbp.md ("Shadow Cones") | 6.33 | R2 (narrowing) | No | About hyperbolic entailment cones; different contribution type (representation learning framework rather than neural network toolkit). Comparable tier of acceptance. |
| bwOndfohRK.md ("NN on Symmetric Spaces") | 6.00 | R2 (narrowing) | No | About neural networks on symmetric spaces with derived distance-to-hyperplane formulations. Similar structure of deriving neural layers for non-Euclidean geometry. Comparable quality. |

### Score Justification

The round-1 bracket was **4.0–7.0** based on the similarity to accepted hyperbolic-layer papers (6.00) and rejected ones with novelty disputes (4.25). Round 2 narrowed this to **5.5–6.5** by comparing weighted items against the closest anchor (ekz1hN5QNh, avg 6.00). That anchor had a very heavy "results within uncertainty" weakness (−8.65 from the scoring model) and novelty disputes; our corresponding weakness is lighter (−4.42) and we have no novelty disputes. However, our paper has two additional weaknesses the anchor lacked: the framing/isometry issue and the graph-learning fairness concern. The weighted-item comparison shows our positive strengths (+4.25, +3.99, +4.33, +5.19) are competitive with the anchor's positive strengths, while our negative items are less severe. The final score of **6.0** reflects a solid borderline-accept paper: a genuinely novel theoretical contribution with clear numerical advantages, somewhat marred by overclaiming in the framing and incomplete reporting of hyperparameter tuning protocol for the graph experiments.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>