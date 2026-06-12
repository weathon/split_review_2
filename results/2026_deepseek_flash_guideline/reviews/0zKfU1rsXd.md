## Summary

This paper proposes a unified framework for approximate quantum loaders (AQLs) and derives information-theoretic bounds (Theorem 3.1) linking the infidelity of quantum state preparation to the sum of single-qubit Rényi-2 entropies of the target state evolved through the inverse of the loading circuit. Building on the insight that lower entanglement yields lower infidelity, the paper develops AQER, a three-step algorithm that iteratively adds two-qubit gates to reduce entanglement (Step I), applies closed-form single-qubit rotations without numerical optimization (Step II), and refines parameters via standard optimization (Step III). Experiments on five datasets (MNIST, CIFAR-10, SST-2, S-RQC, GS-TFIM) with up to 50 qubits show AQER consistently achieves lower infidelity than MPS, HEC, and AQCE baselines, often using fewer two-qubit gates.

---

## Strengths

1. **First information-theoretic bounds on AQL approximation error (Theorem 3.1).** The bounds connect infidelity to $\mathcal{S}(U^\dagger|\psi_{\text{target}}\rangle)$ — the sum of single-qubit Rényi-2 entropies. This is the first result of its kind for AQL, providing a principled theoretical foundation that prior heuristic methods lacked. The bounds are empirically validated in Fig. 3(a), where all measured (infidelity, S) points across five datasets lie within the linearized bounds.

2. **Closed-form product-state approximation in Step II (Corollary 3.2).** After entanglement reduction, the single-qubit rotation parameters for approximating the low-entanglement state are derived analytically without numerical optimization. This is a concrete algorithmic advantage over fully variational methods and reduces the need for costly gradient-based training.

3. **Consistent empirical outperformance across five diverse datasets.** Table 1 shows AQER achieves the lowest infidelity on MNIST, CIFAR-10, SST-2, S-RQC, and GS-TFIM compared to MPS, HEC, and AQCE — often with fewer two-qubit gates. On S-RQC at G=80, AQER achieves infidelity 0.067 vs. second-best AQCE at 0.367 (an 82% relative reduction). The baselines use equal or larger G values, making the comparison conservative.

4. **Broad applicability: handles both classical data and unknown quantum states.** Unlike TN-based approaches that are limited to classical data with low-entanglement structure, AQER can process quantum data (random circuit states, TFIM ground states) via direct measurement-based optimization of the entanglement measure S. Experiments span up to 50 qubits.

5. **Downstream task validation on both quantum and classical tasks.** AQER-loaded TFIM ground states correctly capture the ferromagnetic-to-paramagnetic phase transition near g/J=1 (Fig. 4c), and SST-2 classification error approaches the exact-loading baseline as T increases (Fig. 5b), demonstrating practical utility beyond raw infidelity.

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Statistical significance is not established for the headline comparison results.** Many Table 1 entries have overlapping standard deviations between methods (e.g., CIFAR-10 smallest G: MPS 0.068(0.038), AQCE 0.068(0.036), AQER 0.043(0.023)). The standard errors are tighter with M=50 samples (~σ/√50), but the paper reports no confidence intervals or significance tests. The central claim that AQER "consistently surpasses" baselines would be strengthened by establishing whether observed differences are statistically significant, especially for the smaller-gap comparisons.

2. **Evidence for barren plateau mitigation is preliminary.** The claim that AQER "mitigates barren plateau issues" (Remark ii, Sec. 3.2; Sec. 4.3, line 183) rests on one optimization curve (Fig. 4a) for one dataset (GS-TFIM, N=50) across a few T values. While the curve is suggestive (initial infidelity ≈0.3, decreasing stably), barren plateau analysis typically requires characterizing gradient variance across the full parameter landscape. The single demonstration does not constitute systematic evidence.

3. **Step I optimization procedure is underspecified for full reproducibility.** The paper states that the qubit pair is selected by "selecting the qubit pair that minimizes S through adjusting αₜ" (lines 163-164), which implies an exhaustive search over O(N²) candidate pairs with nested continuous optimization (Nelder-Mead) for each. The paper should state explicitly whether the search is exhaustive, whether early termination is used, and report the number of S evaluations or cost-function calls per iteration.

4. **Computational cost of Step I is not characterized in the main text.** For T=100 iterations on N=50 qubits with O(N²) candidate pairs per iteration and Nelder-Mead optimization for each, the classical overhead could be substantial. The paper references Appendix G for time-complexity analysis but reports no wall-clock time, number of S evaluations, or classical cost scaling in the main text — an important omission for a method claiming "scalability" and "efficiency."

5. **Entanglement measure choice is not justified.** The paper uses the sum of single-qubit Rényi-2 entropies without discussing why this specific measure was chosen over alternatives (von Neumann entropy, Rényi-α for other α, entanglement of formation). Since Theorem 3.1's bounds depend on this choice, some justification would help contextualize the theoretical results.

### Trivial

- The quantity ρ in the upper bound of Theorem 3.1 is not formally introduced in the main text.
- The paper does not discuss failure modes or limitations (e.g., dataset types where AQER might perform poorly, or regimes where Step I's cost outweighs the benefits).
- The claim in the introduction that the bounds are "independent of specific AQL strategies" (line 22) is slightly imprecise — the bounds depend on the specific circuit U via S(U^†|ψ_target⟩), though they do hold for any AQL strategy that produces such a circuit. The main text (line 88) clarifies this correctly.

---

## Nice-to-Haves

- Present comparisons at exactly matched gate-count values in a supplementary table to complement the current presentation (the current asymmetry, where baselines use larger G, is conservative but a direct row-by-row comparison would aid readability).
- Extend barren plateau analysis with gradient variance characterization across multiple datasets and circuit sizes.
- Report wall-clock time for the complete AQER pipeline on representative (N, T) configurations to substantiate the "scalable and efficient" claim.

---

## Removed Points

- **Criticism that "the theoretical bounds are fundamentally different from what the paper's rhetoric claims":** The paper's main text (line 88) clearly states that S depends on both the target state and the circuit U, and characterizes the bounds as conditional. The abstract/intro framing is slightly imprecise but not misleading in context; this has been downgraded to a trivial note.
- **Criticism about experimental comparison transparency (misaligned G values):** The asymmetry favors baselines (they use larger or equal G), so this is not unfair to the authors. The comparison is, if anything, conservative.
- **Criticism that "unified framework adds less structure than claimed":** The framework usefully organizes existing methods under a common formulation. The claim that it "enables algorithm-independent analysis" is reasonable since Theorem 3.1 applies to any method fitting the framework.
- **Criticism about missing baseline comparisons:** The paper covers representative methods from each category (MPS for TN-based, HEC and AQCE for circuit-based).
- **Criticism about missing appendix content (Appendix E.2 details, proof in Appendix B.2):** Per filtering rules, content removed by the parser is not the authors' omission.
- **Criticism about the ceiling function in f₂(S) being "unusual":** Without seeing the proof, this is not evaluable as a weakness.
- **Criticism about "linear scaling" being only asymptotic:** The paper explicitly states "When S → 0" for the expansions; this is standard practice.

---

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any observation about the paper that the paper itself does not already state or imply.

---

## Suggestions

1. **Add statistical significance analysis** for the main Table 1 comparisons (e.g., bootstrap confidence intervals on the mean, or paired tests across the M=50 samples) to substantiate the claim that AQER "consistently surpasses" baselines.

2. **Strengthen the barren plateau claim** by providing gradient variance characterization across the parameter landscape for multiple datasets and circuit sizes, or at minimum add a caveat that the current evidence is preliminary.

3. **Explicitly specify the search procedure** for qubit pairs in Step I (exhaustive over O(N²) pairs? early termination?) and report wall-clock time or number of S evaluations for representative (N, T) configurations to support the "scalable" claim.

4. **Add a brief justification** for using the sum of single-qubit Rényi-2 entropies as the entanglement measure, and acknowledge the dependence of the bounds on this choice.

5. **Reframe the theoretical bounds slightly** in the abstract and introduction to match the precise statement in Theorem 3.1 (a consistency condition on candidate circuits, parameterized by S(U^†|ψ_target⟩), rather than a fundamental limit on the target state alone).

---

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| ER-AAE (un9Gzm0BZb) | 4.75 | R1, R2 | Directly same topic (entropy-reduction approximate encoding). Current paper is stronger: has theory, handles quantum data, larger-scale experiments. |
| Provably Noise-Resilient (hqxzi4d3Ws) | 3.00 | R1 | Much weaker; unrelated subfield. |
| Symmetry-preserving circuits (SL7djdVpde) | 6.75 | R2 | Strong theory + experiments, good upper bound for quality comparison. |
| CRLQAS (rINBD8jPoP) | 5.60 | R2 | Accepted with scores 5–6. Comparable in quality; current paper has stronger theory. |
| Quantum Circuit Compression (bB0OKNpznp) | 6.00 | R2 | Accepted mid-range anchor. Comparable in quality. |

**Round-1 bracket:** 4.5–6.5.  
**Round-2 narrowing:** 5.5–6.5.  
**Final:** 6.0.

The paper's strengths — first theoretical bounds for AQL, well-motivated algorithm, consistent empirical outperformance across 5 diverse datasets and up to 50 qubits, downstream validation — outweigh its addressable minor weaknesses (statistical significance, barren plateau evidence, cost characterization). The core contributions are genuine and the method is clearly scoped, well-motivated, and supported by the evidence presented.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>