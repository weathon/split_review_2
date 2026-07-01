Here is the final consolidated review:

---

## Summary

This paper introduces ShadowFM, a framework for generating classical shadows of quantum many-body states conditioned on Hamiltonian parameters, using geometric flow matching. Two methods are proposed: (1) Spherical Flow, operating on S² via Riemannian Flow Matching motivated by the Bloch sphere, and (2) Anisotropic Dirichlet Flow, which generalizes Dirichlet flow matching by introducing a target/anti-target push-pull mechanism on the probability simplex. Experiments on TFIM, Heisenberg (1D and 2D), and quantum dynamics show consistent improvements over non-geometric flow matching baselines.

## Strengths

1. **Principled geometric motivation (Section 3.1).** The connection between single-qubit shadows and S² via the Bloch map and Fubini-Study metric is clearly articulated. The toy experiment (Figure 2) showing spin errors (moving across the Bloch sphere) are more harmful than basis errors provides concrete intuition for why geometry matters. This is the strongest conceptual contribution.

2. **Anisotropic Dirichlet Flow is a genuine generalization (Section 3.2.2).** The derivation introduces a drift coefficient γ that simultaneously pushes toward a target vertex while pulling away from an anti-target vertex, and explicitly shows that γ=0 recovers standard Dirichlet flow. Equations (6)–(9) are non-trivial and the derivation is substantive.

3. **Consistent empirical improvement across diverse settings (Tables 1–6).** Across TFIM (L=10, L=30), Heisenberg (L=10, L=30), 2D Heisenberg (4×4), and quantum dynamics extrapolation, both proposed methods outperform all baselines (LinearFM, Diff-LM, StatisticalFM, RBFK, NTK) in nearly every configuration. For example, on TFIM L=10 at 100k shadows, Spherical and AD achieve RMSE of 0.041 and 0.021 versus StatisticalFM's 0.126.

4. **Training data scaling analysis (Section 4.4, Figure 5c).** The experiment varying training sample size shows that the proposed methods scale better with more data than baselines, providing useful insight into data efficiency.

## Weaknesses

### Fatal
None.

### Major

1. **Multi-qubit generation process is not specified.** This is the most significant gap in the paper's methodological description. The paper describes the Spherical Flow as operating on S² (K=3, line 135) and the AD Flow as operating on Δ⁵ (K=6, line 157) — both per-qubit outcome spaces. Yet the flown object x₁ is described as a full shadow vector "[5, 0, 2, 1, 3]" (Figure 1), and the dimension of the denoising classifier p̂_θ(x₁|x_t, c) is never stated. The paper never clarifies whether the model generates qubit outcomes independently (factorized across sites) or jointly, and if jointly, how the 6ⁿ outcome space is made tractable. For n=30 systems explicitly evaluated (Tables 2, 4), this question matters. The empirical results show good performance on correlation functions, but without this specification, the reader cannot assess whether the model is truly capturing inter-qubit correlations or whether correlations are mediated entirely through the Hamiltonian condition c. This is not a missing experiment — it is a missing architectural and methodological specification that is prerequisite to evaluating the contribution.

### Minor

2. **Contradiction between main text and figure caption for the phase transition experiment (Figure 5).** Line 251 states "While LinearFM and StatisticalFM fail to accurately capture the phase transition (abrupt change of derivative), DirichletFM and our spherical and AD flow succeed." Yet line 317 states "In (a) and (b), all methods follow the exact curve closely." These statements are at odds. Even if the intended distinction is derivative accuracy vs. value accuracy, the paper does not make this clear, and the contradiction undermines confidence in qualitative claims.

3. **AD flow's poor entropy performance on quantum dynamics is not discussed.** In Table 5, AD flow achieves entropy RMSE of 0.389 at 1k shadows versus Spherical's 0.195 — nearly double the error. This large gap persists across all shadow counts. The paper does not comment on why AD flow struggles on entropy for this task while Spherical does not, which would be informative given that both are proposed methods.

4. **Motivational claim about autoregressive limitations is not evaluated.** Lines 39–40 motivate the work partly by stating that existing methods "suffer from sequential bottlenecks of auto-regressiveness." Yet the experiments include no autoregressive baselines (e.g., Yao & You 2024). The conclusion acknowledges this gap (line 333), but the mismatch between motivation and evaluation remains. The paper's core contribution is the geometric approach, not surpassing autoregressive models, but the motivation should align with what is actually tested.

### Trivial

5. **Neural network architecture is not described in the main text.** The architecture of the denoising classifier p̂_θ and the velocity field network v_θ — number of parameters, layers, model type — is deferred entirely to Appendix D. While the appendix likely contains these details, a brief architectural summary in the main text would aid evaluation.

6. **Some comparisons between the two proposed methods have overlapping uncertainty intervals** (e.g., Table 3, Heisenberg L=10: Spherical 0.044±0.002 vs. AD 0.049±0.002 at 10k shadows) without any significance discussion. Given that the main claim is about geometric vs. non-geometric approaches, this is a secondary concern.

## Nice-to-Haves

- A runtime/compute cost comparison would help calibrate practical trade-offs, especially since AD flow involves pre-computed integrals (Eqs. 8–9).
- Consider moving the tetrahedral POVM results (Table 7, cited but in appendix) to the main text to strengthen the broader-applicability claim.

## Removed Points

These points from the input review were removed with justification:
- **"Missing Table 7 makes it impossible to assess broader-applicability claim"** — The table is cited in the paper and exists in the full submission (appendix); the parser stripped it. Per policy, cited content is assumed to exist.
- **"Architecture must be in main text for paper to be evaluable"** — The appendix contains these details; the criticism that they are absent from the main text is a presentation concern. Merged into Trivial (point 5 above).
- **"Slightly exaggerated novelty claim"** — Not a substantive weakness; all papers scope their contributions relative to prior work.
- **Compute cost as a standalone issue** — Moved to Nice-to-Haves.
- **Statistical significance criticism as a standalone issue** — Merged into Trivial (point 6).
- **Section-by-section notes that are evaluative but not concrete weaknesses** — Removed as noise (e.g., "Background is adequate but minimal", "Derivation deferred to appendix — would strengthen to sketch in main text").

## Novel Insights

Beyond the paper's own contributions, the key insight from the review process is that the per-qubit vs. joint generation question is not a minor detail — it determines how the paper's claims about capturing quantum correlations should be interpreted. If the model generates per-qubit outcomes independently conditioned on c, the correlation results measure how well the Hamiltonian parameter c encodes correlation structure — a finding that would itself be interesting but different from what the paper's framing implies. If the model generates jointly, the mechanism needs to be specified. This ambiguity is the single most impactful issue to resolve.

## Suggestions

1. **Clarify the multi-qubit generation process explicitly.** State whether p̂_θ predicts per-qubit outcomes (factorized across sites) or joint outcomes. If factorized, discuss whether and how inter-qubit correlations are captured. If joint, describe the architecture and the tractability mechanism for the 6ⁿ outcome space.
2. **Resolve the phase transition contradiction.** Align the main text and figure caption, or clarify the intended distinction between curve values and derivative accuracy.
3. **Add a brief discussion of AD flow's entropy gap in Table 5.** Comment on whether this reveals a limitation of the anisotropic approach for certain observables.
4. **Either add an autoregressive baseline or remove the anti-autoregressive framing** from the motivation so the paper stands on its geometric contribution alone.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>