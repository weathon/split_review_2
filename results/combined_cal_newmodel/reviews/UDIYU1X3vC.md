## Summary

This paper proposes Proper Velocity Neural Networks (PVNNs), developing the complete Riemannian toolkit (exponential/log maps, parallel transport, geodesic distance) for the Proper Velocity model of hyperbolic space — an unconstrained representation that avoids the boundary and coordinate-value instabilities of the Poincaré ball and hyperboloid models. The authors construct core neural network layers (MLR, FC, convolution, activation, batch normalization) in PV space and validate across four tasks: numerical stability, image classification, graph node classification, and genomic sequence learning.

## Strengths

- **Novel and well-motivated contribution.** The PV model is genuinely underexplored in ML. The paper correctly identifies numerical instabilities in both the Poincaré ball (near-boundary gradient vanishing) and hyperboloid (gradient explosion/NaN under large values), and PV's unconstrained representation directly addresses these issues in a principled way. *(favorability: 11.85)*

- **Sound theoretical derivations (Secs. 4–5).** Establishing the isometry between PV and the Poincaré ball (Theorem 4.2), then leveraging it to derive closed-form Riemannian operators (Theorem 4.3), is a clean approach. The MLR simplification (Theorem 5.2, Eq. 19) converting gyroaddition into an inner-product formulation avoids O(b×C×n) intermediate tensors — a genuine practical contribution. *(favorability: 13.37)*

- **Clean numerical stability evidence (Sec. 6.1).** Tables 1–3 clearly demonstrate that PV avoids the gradient vanishing of the Poincaré ball and the gradient explosion/NaN issues of the hyperboloid. The round-trip error (Table 2) shows PV is ~1000× more accurate than the Poincaré ball in FP32 and ~10⁵× more accurate in FP64. This is the paper's cleanest result. *(favorability: 12.67)*

- **Compelling genomics results (Sec. 6.4, Table 10).** PVCNN outperforms both Euclidean CNN and HCNN-S across all five TEB tasks, often by substantial margins (e.g., +9 MCC points on SINEs). Gains are consistent across datasets and meaningful given 5-fold cross-validation. *(favorability: 11.73)*

- **Extensive ablations.** The paper provides thorough ablations (tangent vs. Riemannian layers in Table 6, batch statistics in Table 7, Exp₀ effects in Table 8, activation choices in Table 9) that help isolate which design choices drive the gains. *(favorability: 12.23)*

- **Practical simplification from unconstrained space.** PV's unconstrained nature allows direct Euclidean activations without exponential/log maps (Sec. 5.3), which is practically simpler than the Poincaré and hyperboloid models. *(favorability: 10.82)*

## Weaknesses

### Major

- **Downstream performance gains are uneven.** The claim of "competitive or superior performance" across all four tasks is only partially supported. Image classification (Table 4) gains over the best baselines are 0.18% (CIFAR-10) and 0.24% (CIFAR-100) — well within one standard deviation and not statistically compelling. Graph learning (Table 5) is mixed: a clear win on Airport (+5.86% over strongest baseline) but the variation among non-PV baselines on this dataset is itself very large (75.20–92.10), making it hard to attribute the gain specifically to PV's numerical properties. Gains on Disease (+0.58% over HNN++) and PubMed (+0.65% over HNN++) are modest. On Cora, PVNN is worse than LNN (51.42 vs. 53.34). Only the genomics experiment (Table 10) shows consistent, substantial gains across all five tasks. The paper's evidence for practical advantage is strong for numerical stability (by design) and genomics, but modest to weak for vision and graphs. *(favorability: aggregate ~1.5)*

### Minor

- **No statistical significance tests.** The paper reports means and standard deviations from 5-fold CV but never tests whether differences are statistically significant. Given the small margins in vision (0.18–0.24%) and some graph tasks (0.58% on Disease, 0.65% on PubMed), significance testing would substantially strengthen the conclusions. *(favorability: -0.75)*

- **No computational cost analysis.** The Riemannian operators derived in Theorem 4.3 are complex, involving gyrations and compositions of multiple maps. The paper does not analyze the computational cost or wall-clock time of these operators vs. Poincaré/hyperboloid counterparts under repeated application in a deep network (Table 7 provides runtime for GyroBN variants but not for the core operators). This is relevant for assessing practical overhead. *(favorability: 2.97)*

- **Curvature tuning not discussed for vision/graph experiments.** For numerical stability, K=-1 is fixed; for genomics, "a single curvature shared for all layers" is mentioned. But for graph learning and vision, the curvature selection protocol is not described in the main paper. Since curvature interacts differently with different coordinate systems, any systematic difference in tuning between PV and baselines could confound the comparison. (Details may exist in the appendix, which was stripped by the parser.) *(favorability: 3.85)*

- **Genomics comparison against a single baseline only.** Table 10 compares PVCNN against Euclidean CNN and one hyperboloid baseline (HCNN-S). While HCNN-S is the prior state of the art on this task, the absence of Poincaré-ball baselines leaves open whether the gains are specific to PV or obtainable with other hyperbolic representations. *(favorability: 0.94)*

### Trivial

- None.

## Nice-to-Haves

- **Connect the two narratives.** The paper has two separate stories — numerical stability (Sec. 6.1) and task performance (Secs. 6.2–6.4) — but never directly connects them. When does PV's numerical stability translate to better performance? The genomics setup (long sequences, deep convolutions) differs qualitatively from vision (shallow head after pretrained backbone). Explaining this pattern would be more valuable than adding more benchmarks.
- **Add curvature sensitivity analysis.** A simple experiment varying K for PV and one baseline (e.g., Poincaré) on a single task would show whether PV's advantage is robust to curvature choice or requires careful tuning.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The isometry fundamentally changes the nature of the contribution."** Removed because the paper explicitly proves and acknowledges this isometry (Theorem 4.2) and uses it constructively to derive operators. The same isometry holds between the Lorentz model and Poincaré ball, yet the Lorentz model is a standard and accepted hyperbolic representation. The paper correctly positions PV as an "unconstrained representation" of hyperbolic space, which is factually accurate. This is a framing observation, not a substantive weakness.
- **"The paper overstates the novelty of PV as a 'geometric alternative'."** The paper primarily calls PV a "representation" and "model"; only one instance of "alternative geometry" appears (line 15). The criticism overstates the issue.
- **"The 'without Exp₀' finding could be explored more."** This is a future-work suggestion, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add statistical significance tests (e.g., paired t-tests or confidence intervals) for the downstream comparisons, especially for vision and graph tasks where margins are small.
2. Include a computational cost comparison (training time, memory usage) between PV layers and Poincaré/hyperboloid layers.
3. Report the curvature tuning protocol for all experiments and add a sensitivity analysis showing how performance varies with K for PV vs. baselines.
4. Acknowledge the isometry with the Poincaré ball more centrally in the framing, clarifying that PV is a practically useful coordinate system for hyperbolic space rather than a distinct geometry.

## Calibration Report

Retrieved anchors (all rounds):

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `ekz1hN5QNh.md` (Fully Hyperbolic CNNs) | 6.00 | R1 | Yes | Most similar anchor: both develop hyperbolic NN layers and test on vision. The HCNN paper's key weakness was marginal vison gains with results within uncertainty — the same issue this paper has. However, this paper is stronger due to additional numerical stability experiments (Tables 1–3) and a clear genomics win (Table 10). |
| `bwOndfohRK.md` (Symmetric Spaces NN) | 6.00 | R1 | Yes | General theoretical framework for NNs on symmetric spaces. Less directly comparable but similar in contribution type. |
| `30aSE3FB3L.md` (Matrix Manifold NNs++) | 5.67 | R1 | Yes | Similar in developing new neural layers on non-Euclidean manifolds. Had mixed reviews (3, 8, 6). |
| `zbKcFZ6Dbp.md` (Shadow Cones) | 6.33 | R2 | Yes | Hyperbolic representation learning paper. Different focus (partial order embeddings) but comparable quality. |
| `zboCXnuNv7.md` (Semialgebraic NNs) | 6.50 | R2 | No | Different topic (novel architecture for semialgebraic functions). Less comparable. |

**Round-1 bracket:** Between 5.5 and 7.5, with the closest anchor being "Fully Hyperbolic CNNs" at 6.0.

**Narrowing (Round 2):** Comparing itemized favorability ratings, the PV paper's strengths (11.85–13.37) are comparable to the HCNN anchor's strengths (10.58–11.87). The PV paper's most negative weakness items (−0.75) are less severe than the HCNN anchor's (−3.75 for missing citations, −1.29 for results within uncertainty). The PV paper has stronger evidence overall (numerical stability + genomics + 4 task domains vs. 1), placing it above the 6.0 HCNN anchor. The 6.33–6.50 anchors (Shadow Cones, Semialgebraic NNs) are from different subareas but suggest a reasonable upper bound. A final score of **6.5** reflects that the paper has a solid theoretical contribution, clear numerical stability wins, and one compelling downstream result (genomics), but is held back by uneven downstream performance, absent significance testing, and missing computational cost analysis.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>