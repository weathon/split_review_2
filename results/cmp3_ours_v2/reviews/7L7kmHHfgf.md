Now I have all the information I need. Let me finalize the review.

**Round 1 bracket:** Based on calibration, the plausible score range for this paper is between 5.5 and 7.0. It is stronger than rejected papers scoring 3–5 (e.g., PTAD at 4.25, Prototype-based OT OOD at 4.60) and comparable to accepted papers like One-for-All Few-Shot AD (6.40) and AnomalyCLIP (6.17), but has a clear gap in variance reporting that keeps it below the 8+ tier.

**Final score: 6.0** — a solid borderline-accept. The core contribution is well-motivated and empirically supported, but the lack of variance reporting in a few-shot setting is a non-trivial gap that the authors should address.

Here is the final review:

## Summary
PIRN proposes a prototype-driven reconstruction framework for few-shot multimodal anomaly detection, introducing three components: Balanced Prototype Assignment (BPA) via optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) for test-time adaptation of prototypes, and Multimodal Normality Communication (MNC) for cross-modal prototype exchange. Evaluated on MVTec-3D-AD, Eyecandies, and Real-IAD across 5/10/50/all-shot settings, PIRN consistently outperforms baselines with meaningful margins while being substantially more efficient.

## Strengths

1. **Well-motivated, failure-aware design (Section 1).** The paper identifies specific failure modes of existing MAD methods under few-shot training — cross-modal alignment overfitting narrow correspondences and memory-bank methods missing unseen normal variations — and designs each component (BPA, APR, MNC) to address a stated failure mode rather than applying generic techniques.

2. **Consistent and meaningful experimental gains (Tables 1, 4).** On MVTec-3D-AD and Eyecandies, PIRN outperforms all baselines across all metrics and all shot settings. Gains are substantive: +3.7–4.0 AUROC_I in 10-shot, +2.2–2.4 in 50-shot. Full-shot results are competitive, showing no trade-off between few-shot and full-data regimes.

3. **Substantial computational efficiency advantage (Table 4).** PIRN achieves 0.922 AUROC_I (tied with FIND's 0.921) while requiring 85% fewer FLOPs and 4.35× lower latency — a genuine practical advantage that goes beyond accuracy comparisons.

4. **Informative, hypothesis-validating ablations (Tables 5, 6, 7).** Ablations on prototype count K, decoder depth L, and token aggregation method produce interpretable results (e.g., K=50/100 degrades because the bottleneck becomes too loose; L=8 overfits; balanced OT outperforms top-k averaging) that validate the core design intuition.

## Weaknesses

### Fatal
None.

### Major

1. **No reporting of variance or statistical significance across any experiment.** In few-shot settings with only 5–50 training samples per class, results can vary significantly depending on which samples are drawn. The paper reports only point estimates — no standard deviations, confidence intervals, or multiple-seed averages. Given that the claimed improvements are 2–4 AUROC points and few-shot training can exhibit run-to-run variance of 1–3 points, the reader cannot assess whether the reported gains are statistically significant. This is especially pressing for the 5-shot setting where sampling variability is largest. The paper should report results averaged over at least 3–5 random seeds or few-shot draws with standard deviations.

### Minor

1. **APR's key assumption is unverified empirically.** APR's defense against anomaly corruption — that anomalous patches produce diffuse OT assignments and therefore contribute weakly to prototype updates (Section 3.3) — is plausible but untested. For subtle anomalies near the normal manifold, the assignment may not be diffuse, and anomalous information could leak into prototypes via the GRU update. The paper provides no empirical analysis (e.g., measuring cosine distance between training prototypes and their APR-updated versions on normal vs. anomalous test samples) to validate this central mechanism.

2. **Missing implementation details relevant to reproducibility.** Several hyperparameters are not reported: (a) the entropic regularization parameter (ε) for the Sinkhorn algorithm, which governs assignment sharpness and is critical for OT-based methods; (b) GRU architecture details (hidden dimensions, input/output sizes); (c) the number of GAT attention heads and the K value for KNN-based graph construction in MNC Stage 1. These do not invalidate the method but make exact reproduction unnecessarily difficult.

3. **Epoch count asymmetry unexplained.** The paper uses 60 epochs for few-shot training versus 8 epochs for all-shot training (Section 4, Implementation Details). While it is reasonable that few-shot tasks need more iterations, the rationale and whether baselines received comparable training budgets are not discussed.

### Trivial
None.

## Nice-to-Haves
- Measure prototype drift empirically (training vs. test-time prototype vectors on normal vs. anomalous inputs) to directly validate APR's diffuse-assumption defense.
- Restructure the Real-IAD D3 comparison (Table 8) to more clearly separate unimodal baselines from multimodal ones, though the current presentation already transparently notes D³M's tri-modal advantage.

## Removed Points
These points are flagged to be removed; treat them with caution.

1. **Table 2 component ablation formatting.** The harsh critic noted that all rows show identical checkmarks and the 4th row (0.967) exceeds the full model (0.922). This is a PDF extraction artifact — the checkmark alignment was lost in text rendering. The accompanying text clearly describes the ablation: "The baseline model (first row) excludes all proposed modules. The full PIRN model achieves superior performance. Removing each component from the full model results in a consistent performance drop." Per the hard rules, formatting artifacts from PDF parsing are removed.

2. **Real-IAD D3 comparison fairness.** The harsh critic argued that including unimodal baselines inflates the comparison set. The paper transparently labels each baseline's input modalities in Table 8, explicitly acknowledges D³M's tri-modal advantage ("D³M (AUROC_J 0.890) uses a unique tri-modal data representation... PIRN relies solely on two standard modalities"), and reports all results honestly. This is not a weakness.

3. **Loss function specification.** The paper specifies the training loss as minimizing "the cosine distance between the encoder's patch embeddings and the corresponding reconstructed embeddings across all spatial locations for both modalities" and references the soft mining loss (Luo et al., 2025). This is sufficiently specific for a conference paper.

4. **Missing limitations section.** Noted but this is a presentation preference, not a substantive weakness. Many conference papers do not include a dedicated limitations section in the main text.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Report results with standard deviations over at least 3 random seeds / few-shot sample draws for the 5-shot and 10-shot settings on at least one dataset (preferably MVTec-3D-AD). This single addition would substantially strengthen the paper's empirical claims.
2. Provide the missing hyperparameter values (Sinkhorn ε, GRU hidden dimension, GAT head count, KNN-K) in the final version.
3. Add a brief experiment measuring APR prototype drift to validate the diffuse-assumption defense against anomaly corruption.
4. Briefly explain the epoch count asymmetry (60 vs. 8) and confirm baselines received comparable training budgets.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>