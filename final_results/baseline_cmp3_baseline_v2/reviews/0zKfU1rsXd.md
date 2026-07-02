## Summary

This paper addresses the problem of efficiently loading classical or quantum data into quantum circuits using approximate quantum loaders (AQLs). The authors first unify existing AQL methods into a common optimization framework and derive information-theoretic bounds showing that the infidelity scales linearly with a sum of single-qubit Renyi-2 entropies after applying the inverse loading circuit. Motivated by this, they propose AQER, a three-step method that iteratively reduces this entanglement measure, applies analytically derived single-qubit rotations, and refines parameters via optimization. Extensive experiments on classical (MNIST, CIFAR-10, SST-2) and quantum (random circuits, TFIM ground states) datasets with up to 50 qubits demonstrate that AQER consistently achieves lower infidelity with equal or fewer two-qubit gates compared to existing methods (MPS, HEC, AQCE).

## Strengths

- **First information-theoretic bounds for AQL.** Theorem 3.1 provides algorithm-independent lower and upper bounds on the achievable infidelity in terms of an entanglement measure, offering a principled understanding of the fundamental limits of approximate state preparation.
- **Novel and well-motivated method.** AQER directly leverages the theoretical insight that reducing entanglement lowers the approximation error. The three-step design (entanglement reduction, explicit product-state approximation, parameter refinement) is clean and each step has a clear purpose.
- **Strong empirical performance.** Across five diverse datasets and multiple gate budgets, AQER consistently outperforms three representative baselines (MPS, HEC, AQCE), often by a large margin (e.g., >60% infidelity reduction on S-RQC). The method also scales to 50 qubits and shows no signs of barren plateaus in the optimization.
- **Downstream validation.** The paper goes beyond infidelity metrics by demonstrating that AQER-loaded states preserve physical observables (magnetization in TFIM) and yield competitive classification accuracy on SST-2, confirming practical utility.

## Weaknesses

### Fatal
None.

### Major
- **The theoretical bounds rely on a non-standard entanglement measure.** The measure \(S = \sum_i S_{\{i\}}\) (sum of single-qubit Renyi-2 entropies) is not a conventional multipartite entanglement measure. The bounds involve \(S/N\) and become trivial when \(S\) approaches \(N\). The upper bound contains a \(\lceil S \rceil\) term that makes it discontinuous and potentially loose. While the linear scaling for small \(S\) is insightful, the practical tightness and operational meaning of the bounds are unclear.
- **Fairness of baseline comparisons is not fully transparent.** The paper states that baselines use "equal or slightly larger \(G\) due to feasibility constraints," but does not explain how the gate counts for each baseline were chosen. For MPS, the bond dimension directly controls \(G\); for HEC, the ansatz depth is fixed; for AQCE, the number of iterations determines \(G\). Without a clear protocol for matching gate budgets, the comparison may inadvertently favor AQER. The paper should report results for multiple \(G\) values for each baseline and discuss how the reported \(G\) values were selected.
- **Scalability is only demonstrated on low-entanglement states.** The GS-TFIM dataset (1D ground states) has area-law entanglement, which is favorable for entanglement-reduction methods. The S-RQC dataset uses only 40 gates, producing states with moderate entanglement. The paper does not test on highly entangled states (e.g., random Haar states or volume-law states), where the required number of two-qubit gates may grow exponentially. The claim of scalability is therefore limited to structured, low-entanglement data.

### Minor
- **The entanglement reduction step (Step I) requires optimizing over qubit pairs.** For each iteration, the method must search over \(O(N^2)\) pairs and optimize continuous parameters for each candidate. The paper does not discuss the computational cost of this step or how it scales with \(N\). For large \(N\), this could become a bottleneck, especially on quantum hardware where each candidate evaluation requires many measurements.
- **The upper bound in Theorem 3.1 is not directly used in the method.** AQER is motivated by the lower bound (infidelity decreases with \(S\)), but the upper bound construction (which requires access to the state) is not employed. The paper could clarify whether the upper bound provides any algorithmic guidance beyond the general principle.

### Trivial
None.

## Nice-to-Haves
- Provide a runtime analysis of Step I (number of pair evaluations, measurement cost) for the largest experiments.
- Test AQER on a dataset with volume-law entanglement (e.g., random Haar states) to understand its limitations.
- Include a comparison with a variational method that uses the same gate count but without entanglement reduction, to isolate the benefit of the proposed initialization.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the approximation error of any AQL is fundamentally tied to the entanglement of the target state after applying the inverse loading circuit. This reframes the problem of circuit design as one of entanglement reduction, providing a concrete optimization target (sum of single-qubit Renyi-2 entropies) that is both theoretically grounded and practically measurable. The observation that this entanglement measure can be efficiently reduced by greedily adding two-qubit gates, and that the resulting low-entanglement state can be approximated by analytically determined single-qubit rotations, is a clever synthesis of information theory and circuit synthesis.

## Suggestions
- Clarify how the gate counts for baseline methods were chosen and report results for multiple gate budgets to ensure a fair comparison.
- Discuss the computational complexity of the qubit-pair search in Step I and consider heuristics (e.g., random sampling, gradient-based selection) for larger systems.
- Add a discussion on the limitations of the method for highly entangled states and the expected scaling of required gates.

## Score and Decision

Score: 7

Decision: Accept

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>