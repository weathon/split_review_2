The favorability scores are informative: all strengths are strongly positive (1.00), while the two Major weaknesses are heavily negative (0.07, 0.14) and the Minor ones are moderately negative (0.33–0.49). The core SVD contribution is strong and well-demonstrated, but the Sinkhorn mechanism claim needs sharper support, and one important baseline is missing from a key experiment. Neither issue is fatal. I'll assign a score of 7.

---

## Summary

This paper proposes RADAR, a neural framework for asymmetric vehicle routing problems (VRPs) that augments existing constructive neural solvers with two components: (1) an SVD-based initialization that encodes static asymmetry from the distance matrix into compact node embeddings, and (2) Sinkhorn normalization in the attention mechanism to model "dynamic asymmetry" during encoding. The paper evaluates RADAR on ATSP, ACVRP, 16 multi-task asymmetric VRP variants, and 3 real-world datasets, consistently outperforming prior neural baselines and generalizing to larger out-of-distribution instances.

## Strengths

- **The problem framing is precise and actionable.** The decomposition of asymmetry into *static* (the input distance matrix) and *dynamic* (how asymmetry should propagate through encoder layers) cleanly motivates the two proposed components and connects each design choice to a specific limitation of prior work.

- **The SVD-based initialization is well-grounded and convincingly demonstrated.** Definition 1 formalizes what it means for an embedding to encode static asymmetry, the SVD construction provably satisfies it (Eqs. 1–5), and the ablation (Table 6) shows SVD alone reduces the gap from 2.08% to 1.19% on ATSP100 — a clear, meaningful isolated gain over prior uninformed and kNN-based embeddings.

- **The evaluation is unusually broad and thorough.** It covers ATSP, ACVRP, 16 multi-task asymmetric VRP variants, and 3 real-world datasets, plus controlled studies on asymmetry levels, demand distributions, and coordinate effects. This breadth makes the empirical case substantially stronger than a single-benchmark evaluation.

- **The coordinate-ablation study (Table 4) is informative and honestly presented.** RADAR without coordinates outperforms RRNCO *with* coordinates (38.958 vs 39.385 on in-distribution ATSP), cleanly showing that the SVD-based embedding captures structural information that coordinate-based methods cannot recover when distances are asymmetric.

## Weaknesses

### Fatal
None.

### Major

- **The Sinkhorn normalization's claimed connection to "dynamic asymmetry" is not empirically validated.** The paper argues that row-wise softmax ignores node j's neighborhood and that Sinkhorn normalization addresses this by making attention doubly stochastic (Section 4.2, lines 93–107). However, no analysis is provided to show that Sinkhorn-normalized attention actually preserves or enhances directional asymmetry compared to softmax — e.g., a comparison of A_{i,j} vs A_{j,i} margins, or an analysis of whether Sinkhorn suppresses asymmetry rather than encoding it. The ablation (Table 6) shows Sinkhorn helps empirically, but the improvement on ATSP100 (0.47% additional gain beyond SVD) is modest compared to SVD's contribution (0.89%), and the mechanism linking doubly stochastic attention to directional awareness remains underspecified. The paper should either provide evidence for the claimed mechanism or reframe this contribution more modestly. This does not invalidate the empirical finding but weakens the claimed interpretation.

- **The multi-task evaluation (Table 2) omits RRNCO, the most relevant asymmetric neural baseline, without explanation.** RRNCO (Son et al., 2026) is cited throughout the paper as the key prior work on asymmetric neural VRP solvers, used as a baseline in the real-world experiments (Table 3) and asymmetry-level studies (Table 5), yet it is entirely absent from the 16-variant multi-task setting that is the paper's main evidence for cross-variant generalizability. The paper states it adapts RouteFinder with two changes (line 190) but does not explain why RRNCO could not be adapted similarly.

### Minor

- **Gap baselines shift between problem types in a way that changes the interpretation of headline numbers.** On ATSP (Table 1), gaps are computed against LKH-100 (~1 min search). On ACVRP, gaps are computed against LKH-10000 (~2.79 hours). The RADAR gap of 0.72% on ATSP100 vs a cheap traditional solver is genuinely impressive; the gap of 1.64% on ACVRP100 vs a solver that runs nearly three hours is a different kind of claim. The table visually suggests comparable performance across problem types, but the yardsticks are very different.

- **HGS infeasible solutions are reported with negative gaps** (e.g., -8.83% on ACVRP200, line 177). Despite the footnote disclaimer (line 184), presenting these numbers alongside feasible results could mislead readers into inferring that HGS strongly outperforms everything, which the paper itself acknowledges is not meaningful.

- **No standard deviations or confidence intervals are reported for any results.** For neural methods with stochastic decoding, variance matters — especially since RADAR's gaps are often small (<2%), a difference of 0.3% between methods may not be statistically significant.

- **Section 5.6 (Different Demand Distribution) defers all results to Appendix C.3** without providing any summary conclusion in the main text. A one-sentence finding would make this section informative on its own.

- **SVD truncation to k=10 captures ~85% of the distance matrix information** (line 91), but the paper does not analyze what information is lost or whether the truncated singular vectors preserve the practically important directional structure or discard it along with noise.

- **Definition 1 and its SVD construction (Eqs. 1–5) are somewhat self-verifying:** the definition is crafted so that the SVD construction provably satisfies it by setting W1 and W2 to extract left and right halves of the concatenated embedding. This is a clean design justification but should not carry weight as a theoretical contribution — it is a verification that the construction meets its own specification.

### Trivial
None.

## Nice-to-Haves
- The z-score normalization choice in Algorithm 1 (line 114) is not discussed or justified.
- Encoder depth (5 layers, line 45) is stated without sensitivity analysis.
- Sinkhorn iteration count sensitivity is deferred to the appendix.

## Removed Points
These points from the harsh critic review were removed (or demoted) — treat with caution:
- *Claim that Sinkhorn "symmetrizes" the attention matrix* — Removed as factually incorrect. Doubly stochastic constraints (equal row and column sums) do not imply symmetry for n>2 matrices.
- *Claim that the paper overstates the prevalence of symmetric-only solvers* — Removed. The paper correctly notes that most neural VRP solvers assume symmetric Euclidean instances; the few asymmetric-handling methods (MatNet, ICAM, ReLD, UniCO, RRNCO) are the exceptions and are cited.
- *Related-work section style nitpick* — Removed as generic.
- *Algorithm 2 column-then-row normalization order* — Removed; alternating normalization order is a standard variant and does not affect convergence.
- *Base architecture underspecified* — Removed; architectural details are standard for the MatNet family and deferred to the appendix (stripped by the parser).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add an analysis comparing the asymmetry (A_{i,j} vs A_{j,i}) of Sinkhorn-normalized attention against softmax attention to validate the "dynamic asymmetry" claim, or reframe the Sinkhorn contribution more modestly as a general-purpose attention improvement for routing.
2. Include RRNCO in the multi-task evaluation (Table 2) or provide a clear explanation of why it cannot be adapted.
3. Report standard deviations or confidence intervals for the main results.
4. Use a consistent gap baseline or explicitly discuss the different yardsticks in the caption of Table 1.
5. Add a one-sentence summary finding to Section 5.6 so the main text is self-contained.

## Score and Decision

The core contribution — SVD-based initialization for asymmetric VRPs — is clean, well-motivated, theoretically grounded, and convincingly demonstrated across a broad evaluation. The Sinkhorn normalization component shows empirical gains but the claimed "dynamic asymmetry" mechanism is underspecified. Two issues (the missing RRNCO baseline in the multi-task setting and the claim-vs-evidence gap for Sinkhorn) need addressing. Neither is fatal; the method is sound and the evaluation is thorough.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>