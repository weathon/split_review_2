Now let me write the final consolidated review.

## Summary

This paper reformulates approximate quantum loader (AQL) methods into a unified optimization framework and derives information-theoretic bounds relating infidelity to an entanglement measure. Motivated by these bounds, the authors propose AQER, a scalable algorithm that constructs loading circuits by greedily reducing single-qubit Renyi-2 entropies. Experiments across five datasets (classical images, text embeddings, random quantum circuits, ground states of the transverse-field Ising model) with up to 50 qubits show that AQER consistently achieves lower infidelity than existing baselines (MPS, HEC, AQCE) at equal or smaller gate counts, and avoids barren plateaus during optimization.

## Strengths

- **Unified framework for AQL methods (Sec. 3.1).** The paper reformulates TN-based and circuit-based AQL methods as instances of a single optimization problem (Eq. 1). This conceptual contribution surfaces structural commonalities across previously disparate approaches and provides a foundation for the theoretical analysis. Prior work treated these families of methods as largely separate paradigms.

- **Strong and consistent empirical results (Table 1, Figs. 3–5).** AQER achieves the lowest infidelity across essentially all 15 dataset×gate-count configurations, often by a wide margin. On S-RQC with G=40, AQER achieves infidelity 0.128 versus the next-best 0.363 (AQCE) — a factor-of-three reduction. Scalability results (Fig. 4b) show roughly constant infidelity when T scales linearly with N for N up to 50 qubits. Downstream task validation (quantum phase transition detection, SST-2 classification) confirms that the infidelity reductions translate into practically meaningful improvements.

- **Principled algorithm design.** The three-step procedure follows from the theoretical analysis. Step I (using the sum of single-qubit Renyi-2 entropies as a proxy for loading error during circuit construction) is genuinely novel among AQL methods. Step II's explicit construction of single-qubit gates (Corollary 3.2) avoids unnecessary optimization overhead.

- **Barren plateau mitigation (Fig. 4a).** AQER's Step I initialization places the optimization landscape in a region where gradients are informative: initial infidelities are far from 1 even at N=50, and optimization succeeds without plateaus. This is a practically important demonstration, as trainability is a well-known obstacle in variational quantum algorithms.

## Weaknesses

### Fatal

None.

### Major

None. The issues identified below are real but do not threaten the paper's core contributions — the empirical evaluation is strong enough to carry the paper, and the theoretical limitations can be addressed without changing the conclusions.

### Minor

1. **Limited informativeness of the upper bound in Theorem 3.1.** The upper bound f₂(S) evaluates to ≥ 1 for S ≥ 2, making it trivially satisfied (and thus uninformative) for any state with S ≥ 2. Since infidelity is bounded by definition in [0, 1], the bound provides no constraint outside the S < 2 regime. The paper's narrative emphasizes the bounds collectively, but this limitation is not explicitly discussed in the main text. The lower bound f₁(S) is always informative and the asymptotic (S → 0) linear scaling is correctly stated, so the result is not vacuous overall — but the limited range of the upper bound should be acknowledged directly in the main text rather than only implicitly via the linearized plot in Fig. 3(a).

2. **Lack of a priori predictive guarantees.** Theorem 3.1 bounds infidelity in terms of S(U†|ψ_target⟩), which depends on the circuit U being constructed. The theorem provides a design principle (small S ⇒ small infidelity) rather than a prevalence guarantee (for a given target state, how small can S be made with T gates?). AQER is honestly described as heuristic (Remark iii), and the paper cites the known impossibility of efficient worst-case preparation. The paper would be strengthened by explicitly stating this scope limitation: the theory justifies the optimization target but does not provide a priori bounds on achievable S for arbitrary target states.

3. **No ablation study isolating the contribution of individual steps.** The paper never runs AQER without Step I (i.e., using only random two-qubit gates + Steps II and III) to verify that the entanglement-reduction optimization is causally responsible for the performance gain. Similarly, no ablation removes Step II or Step III. Given the three-step design is a claimed advantage over existing methods, these ablations would directly validate the algorithm's architecture.

4. **SST-2 results operate in a qualitatively different regime.** SST-2 infidelities (0.4–0.9) are an order of magnitude worse than MNIST (0.03–0.33) or GS-TFIM (0.003–0.055). The paper describes the preprocessing but does not discuss why SST-2 is harder or whether the difficulty is inherent to text data or an artifact of the encoding choice (amplitude encoding 1024-dimensional Sentence-BERT embeddings into 10–11 qubits). Since the absolute numbers are all poor, the comparison between methods is less informative here, and a brief discussion would help readers interpret the results.

5. **Step I optimization cost is acknowledged but not concretely reported.** The paper references Appendix G for complexity analysis and notes the procedure is efficient because it uses only local measurements (Remark i). However, no wall-clock time, number of function evaluations per iteration, or total circuit calls are reported in the main text. Since AQER is proposed as a practical method, and each Nelder–Mead optimization at each iteration involves evaluating S over candidate qubit pairs, a concrete cost estimate would strengthen the scalability claims.

### Trivial

- The term ρ in Theorem 3.1 ("given access to ρ") is undefined.
- Fig. 3(a) shows linearized versions of the bounds rather than the full nonlinear functions; displaying both would be more informative.
- The linear scaling T = 4N − 40 in Fig. 4(b) is presented post-hoc as an empirical observation; the paper should clarify it is not derived from theory.

## Nice-to-Haves

- Include an ablation study isolating contributions of Steps I, II, and III.
- Show performance curves as continuous functions of G for all methods, enabling apples-to-apples comparison at any gate budget.
- Add a direct trainability comparison against randomly initialized circuits of the same structure to confirm that the entanglement-reduction initialization is causally responsible for the good training dynamics.
- Report concrete wall-clock time or total circuit evaluation counts for Step I.

## Removed Points

The following points from the input review are removed for the reasons stated:

- **"The connection between Theorem 3.1 and AQER has a circular flavor":** This mischaracterizes the theory→algorithm relationship. The theorem establishes that small S implies small infidelity — a genuine mathematical result. The algorithm optimizes S as a proxy for infidelity. This is standard theory-driven algorithm design, not a tautology. The theorem provides principled justification for the optimization target; it was not designed to provide a priori bounds (which is a different kind of theoretical claim beyond the paper's stated scope).

- **"Massive dimensionality reduction for SST-2 (1024 → 2¹⁰)":** This is factually incorrect. 2¹⁰ = 1024, so the 1024-dimensional embeddings map directly to 10 qubits with no dimensionality reduction. The high infidelity is not explained by a dimensionality mismatch.

- **"No statistical significance tests":** The paper provides means and standard deviations, which is the standard practice in the quantum computing and ML literature. Formal hypothesis tests are not expected.

- **"No comparison of gate types (R_ZZ vs CZ)":** Counting two-qubit gates homogeneously is standard practice in this literature. R_ZZ and CZ have similar implementation overhead on most platforms, and the paper acknowledges G as a proxy for resource consumption.

- **"Missing related works":** Cannot be verified without external sources. The paper's related work section (Sec. 2.1) covers TN-based and circuit-based methods appropriately.

- **Formatting/typo criticisms:** These are parser artifacts from the PDF extraction, not issues in the original submission.

## Novel Insights

The reviews raise a genuine tension around how to interpret Theorem 3.1. The critic correctly notes that the upper bound is uninformative for S ≥ 2, but simultaneously misunderstands what the theorem is trying to do: the bound is not meant to be a tight universal constraint for all S, but rather to establish the linear-scaling regime around S → 0 and thereby identify S as the right optimization target. The interesting insight is that this kind of "design principle, not prevalence guarantee" limitation is structurally common in theoretical computer science (e.g., generalization bounds in learning theory specify what to regularize, not the achievable error a priori), and the paper would benefit from being explicit about this framing. The empirical verification that S and infidelity track each other across diverse datasets (Fig. 3a) is the right kind of evidence for this type of theory — it validates the bound's qualitative predictions rather than its quantitative tightness.

## Suggestions

- Add a brief statement in Sec. 3.1 acknowledging the range of S for which the upper bound is informative (S < 2) and clarifying that the theorem's main value is establishing S as the right optimization target.
- Add an ablation study to Sec. 4 verifying the contribution of each step.
- Add a discussion paragraph for SST-2 results explaining the qualitatively different infidelity regime.
- Report concrete cost estimates (wall-clock time or function evaluations) for Step I.

## Score and Decision

This paper makes a genuine contribution to the AQL literature. The unified framework is a useful conceptual advance. The AQER algorithm is well-designed, principled, and substantially outperforms existing methods across diverse benchmarks. The scalability demonstration to 50 qubits with evidence of trainability is practically significant. The theoretical analysis has limitations (the upper bound is informative only for S < 2, and the theory provides a design principle rather than a priori guarantees), but these are not fatal — the empirical contribution is strong enough to carry the contributions. The paper should be accepted, with the above minor issues addressed in the final version.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>