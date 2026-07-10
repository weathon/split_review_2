Now I have sufficient calibration data. Let me compose the final review.

**Round 1 bracket**: Based on the most comparable anchors (graph pruning paper at 3.86, LeanFlex-GKP at 5.0, Fast Framework at 5.0, PvR at 3.75), ACSP sits between 3.86 and 5.0 — stronger than the graph pruning paper in scope and novelty, but weaker than LeanFlex/Fast Framework in evidential rigor. Initial bracket: **[3.5, 5.0]**.

**Final score placement**: ACSP's strongest item (complementary selection, impact +9.99) and automated pruning (+9.82) are genuinely novel contributions that surpass the graph pruning paper's contributions. However, the three decisive weaknesses (no ablations -10.00, no variance -10.00, FLOP/wall-clock gap -9.89) are at least as severe as those in the 3.86 anchor. The LeanFlex anchor (5.0) had missing ablation (-10.00) but did not have additional variance + FLOP/wall-clock issues. This places ACSP below 5.0 but above 3.86.

---

## Summary

This paper introduces Automatic Complementary Separation Pruning (ACSP), a structured pruning method for CNNs that selects components with complementary separation capabilities via clustering in a graph space built from JM distances between class-pair activations. ACSP also automates the pruning extent per layer using knee-finding on the Mean Simplified Silhouette curve, removing manual pruning-ratio tuning. Experiments span 5 architectures (VGG-16/19, ResNet-50/56, DenseNet-40, MobileNet-V2) and 3 datasets (CIFAR-10/100, ImageNet-1K).

## Strengths

- **Complementary-selection idea is principled and addresses a genuine limitation of magnitude-based pruning.** Using JM distance between class-pair activations to construct a graph space, then k-Medoids clustering to enforce diversity among kept components, directly tackles the problem that top-k selection by importance can pick near-duplicate components. The illustrative example in §3.3.2 (components T_{i,j}, T_{i,k}, T_{i,l}) makes the motivation concrete and clear.

- **Automated pruning extent via knee-finding is a practical contribution.** Replacing manual pruning-ratio sweeps with a data-driven Kneedle approach on the MSS curve (§3.4.1) addresses a real pain point in deploying pruning in practice. The claim that this runs in O(N_i²) with wall-clock cost below 0.1s per layer (N_i ≤ 256) is specific and testable.

## Weaknesses

### Major

- **No controlled ablation experiments to validate the paper's central claims.** ACSP has at least four major design choices (complementary selection via k-Medoids + MSS, MSS index vs. standard Silhouette, Kneedle for automatic pruning extent vs. fixed ratio, JM distance vs. alternatives), and none are isolated by ablation. The paper states "we evaluated several metrics, including the JM, Hellinger, and Wasserstein distances" (§3.3.1) but never presents these results — no table, no figure, no quantitative comparison. Without ablations, the reader cannot determine whether ACSP's results come from complementary selection, knee-finding, post-pruning fine-tuning, or simply from evaluating on training-set activations. This is the most serious weakness in the paper: the claimed mechanism has not been shown to cause the observed results.

- **No measure of variance or statistical significance.** Accuracy results are reported as single numbers with no standard deviation, confidence intervals, or mention of how many seeds/runs were averaged. The inference times in Table 2 are "means over 100 runs" but of random inputs, not different pruned models. Given that reported accuracy differences between ACSP and competing methods are often fractions of a percent (e.g., +0.13% vs. +0.24% for DepGraph on ResNet-56), single-run reporting is insufficient to support claims of superiority.

- **FLOP-based speedup claims significantly outstrip measured wall-clock speedups, and the contribution is framed around the former.** The abstract and contributions list prominently claim "2.25× speed-up on ResNet-50" and "1.5–2.5× reduction in computation (FLOPs)." However, Table 2 shows wall-clock improvements are much more modest: single-image latency improvements range from 2.62% to 8.07%, and the best batch inference improvement is 20.39%. The paper acknowledges this gap ("hardware utilization is not perfectly linear with FLOP count") but continues to foreground FLOP reductions as the headline result. For single-image latency (the more practically relevant metric for many deployment scenarios), the measured gains are marginal. The paper should clearly distinguish between FLOP reduction (which is what ACSP provides) and actual wall-clock speedup (which depends on hardware characteristics).

### Minor

- **Weight-based tie-breaking after clustering is underspecified.** After clustering, the method selects the highest-weight component from each cluster — for convolutional layers the L1 norm of the filter, for fully-connected layers the absolute weight magnitude. The paper provides no justification for L1 norm as the appropriate filter-importance metric, and no analysis of whether this weight adjustment actually preserves diversity or reverts to magnitude-based selection. The concern is that if the highest-weight components in different clusters happen to be functionally similar, the diversity benefit of clustering is lost.

- **The class-pair scaling limitation is acknowledged but not quantified.** The paper notes that the method "scales with classes C and may bottleneck for large C." For ImageNet-1K (1000 classes), the separation matrix has dimension N_i × (p×p×C(1000,2)) ≈ N_i × (p×p×499,500). The paper should report actual wall-clock time for constructing this matrix for a representative ImageNet layer and discuss practical scaling.

- **The comparison table (Table 1) mixes methods with different base accuracies, making Δ accuracy an imperfect metric.** For example on CIFAR-10 VGG-16, ACSP starts from 93.55% while HRank starts from 93.96% and AOFP from 93.38%. The differences are small (<0.5%) and this practice is common in the pruning literature, but it reduces the reliability of quantitative comparisons.

- **The layer-by-layer iterative procedure cost is not reported.** Algorithm 1 prunes and fine-tunes per layer — for ResNet-50 this is ~48 rounds. Each fine-tuning round is 2 epochs on 25% of the data. The total pruning wall-clock time (including all fine-tuning rounds) should be reported and compared against methods that prune in one shot.

### Trivial

- **Table 1 contains an apparent copy-paste error.** The ACSP row for MobileNet-V2 on CIFAR-10 reads "ACSP (Gao et al., 2023)" — ACSP is the method introduced in *this* paper, not by Gao et al. (2023). This suggests a table was copied from a prior paper and not properly updated.

## Nice-to-Haves

- Add ablations on CIFAR-10 with at least two architectures: (a) full ACSP, (b) random selection at same pruning budget, (c) top-k weight-magnitude selection, (d) MSS replaced by standard Silhouette, (e) fixed pruning ratio instead of Kneedle.
- Report accuracy as mean±std over ≥3 random seeds.
- Qualify "speed-up" throughout as FLOP reduction or report conditions under which FLOP savings translate to wall-clock speedup.
- Report total pruning wall-clock time.
- Quantify class-pair computational overhead on ImageNet.
- Correct the "ACSP (Gao et al., 2023)" citation error.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add the controlled ablation study described above — this is essential to validate the paper's core claims.
2. Report all accuracy results with standard deviations over multiple seeds.
3. Separate FLOP-reduction claims from wall-clock speedup claims throughout the paper.
4. Report total pruning time (including all fine-tuning rounds).
5. Quantify the practical computational cost of the class-pair separation matrix for ImageNet-scale problems.

## Removed Points

- *"Potential circularity" criticism about using labels to construct the separation matrix*: This is by design for supervised pruning — the method is explicitly scoped to supervised learning (§1). Not a flaw.
- *"Inference time measured with random inputs"*: Standard microbenchmarking practice for latency measurement. Not a real weakness.
- *"Fine-tuning details are sparse"*: The paper provides learning rate, epochs, and subset fraction for both CIFAR and ImageNet settings (§4.1). This is adequate for reproducibility.
- *"Strength: The paper addresses an important problem"* (generic, removed per filtering rules).
- *"Strength: The paper makes novel contributions"* (generic, removed per filtering rules).

## Score and Decision

All anchors retrieved (all rounds):

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|--------------------------|
| AvLFLLqG0b (Graph Random Walk Pruning) | 3.86 | R1 | Yes | Most similar: graph-based CNN pruning. Similar evidential gaps (no ablation). ACSP has broader experiments and stronger conceptual novelty → ACSP is stronger. |
| KksPo0zXId (Fast Post-training Pruning) | 5.00 | R1 | Yes | Structured pruning without retraining. Clearer practical contribution, fewer evidential gaps → slightly stronger than ACSP. |
| g4VGwNqzpB (HENP Dynamic Pruning) | 3.00 | R1 | Yes | Very limited experiments (one dataset). ACSP is substantially stronger. |
| 88rjm6AXoC (Optimal Brain Apoptosis) | 6.25 | R1 | Yes | Strong theoretical grounding, accepted. ACSP lacks comparable theoretical depth and rigorous evaluation. |
| YhNXGWVH1N (LeanFlex-GKP) | 5.00 | R2 | Yes | Grouped kernel pruning. Missing ablation (-10.00) similar to ACSP, but fewer additional evidential gaps. |
| rO62BY3dYc (Pruning via Ranking) | 3.75 | R2 | Yes | Weaker novelty, limited experiments. ACSP is clearly stronger. |
| vvD0VFw0LG (PruningBench) | 4.75 | R1 | No | Benchmark paper, different category. Not directly comparable. |
| c5boBrSTKj (AMSC) | 5.67 | R1 | No | Multi-dimensional compression with theory. Different methodology. |
| 4bSQ3lsfEV (Feature Complexity) | 5.75 | R1 | No | Not about pruning methodology. |
| kOBkxFRKTA (Dynamic Sparse Training) | 6.20 | R1 | No | Sparse training, not pruning. |
| S83ldgJZLh (SPADE) | 4.75 | R2 | No | Specialized pruning for model-based DL. |
| And others < 3.5 | 1.0-2.5 | R1 | No | Not comparable (survey papers, unrelated topics). |

**Round 1 bracket (explicit)**: [3.5, 5.0] — below LeanFlex (5.0) due to additional evidential gaps (no variance, FLOP/wall-clock gap), above Graph Pruning (3.86) due to stronger experimental scope and more principled methodology.

**Narrowing to final score**: Compared to the Graph Pruning anchor (3.86), ACSP shares the "no ablation" weakness (both ~-10 impact) but ACSP has two additional decisive weaknesses (no variance at -10.00, FLOP/wall-clock gap at -9.89) that the anchor does not. Counterbalancing these, ACSP's strengths have higher impact (+9.99, +9.82) than the anchor's best strengths (+7.27, +5.99). The overall balance keeps ACSP slightly above 3.86 but well below 5.0, since the LeanFlex anchor (5.0) had only one of these three decisive weaknesses (missing ablation). The decisive weaknesses push the effective score down to **4.0**.

The paper proposes a well-motivated pruning framework with a genuinely novel idea (complementary selection via graph clustering) and a practical automation contribution (knee-finding for pruning extent). However, the experimental evaluation lacks the controlled ablation studies needed to verify that these mechanisms drive the observed results, reports no measure of variance despite tiny accuracy differences, and frames the contribution around FLOP reduction while wall-clock speedups are substantially more modest. These are not minor gaps — they challenge whether the paper's central claims have been validated. The paper is in the borderline reject range: interesting ideas, but the evidence is insufficient for acceptance at ICLR in the current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>