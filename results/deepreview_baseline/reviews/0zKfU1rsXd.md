## Summary

This paper introduces a unified theoretical framework for approximate quantum loaders (AQLs) and derives information-theoretic bounds showing that the infidelity of approximate state preparation scales linearly with the total single-qubit entanglement entropy of the target state after applying the inverse loading circuit. Motivated by this insight, the authors propose AQER, a scalable AQL method that constructs loading circuits by systematically reducing entanglement through iterative addition of two-qubit gates, followed by explicit single-qubit rotations and parameter refinement. Extensive experiments on classical datasets (MNIST, CIFAR-10, SST-2) and quantum datasets (random quantum circuits, TFIM ground states) with up to 50 qubits demonstrate that AQER consistently outperforms existing methods (MPS, HEC, AQCE) in both accuracy and gate efficiency.

## Strengths

- **Novel theoretical contribution**: The paper provides the first information-theoretic bounds connecting AQL approximation error to an entanglement measure, establishing a fundamental relationship that is algorithm-independent. Theorem 3.1 is a genuine theoretical contribution that provides both lower and upper bounds on infidelity in terms of the entanglement measure S.

- **Principled algorithm design**: AQER is directly motivated by the theoretical analysis, using entanglement reduction as a guiding principle for circuit construction. This is a clean and well-motivated approach that bridges theory and practice.

- **Comprehensive experimental evaluation**: The paper benchmarks AQER against three representative baselines across five diverse datasets (classical and quantum), with up to 50 qubits. The experiments cover accuracy, efficiency, trainability, scalability, and downstream task performance, providing strong empirical support.

- **Consistent outperformance**: AQER achieves the lowest infidelity across all datasets and gate budgets, often with substantial margins (e.g., 60%+ reduction on S-RQC compared to the second-best method). The results are statistically sound with standard deviations reported.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical bound practical significance**: While Theorem 3.1 is interesting, the bounds involve the entanglement measure S of the state after applying the inverse circuit U†, which depends on the circuit being constructed. This creates a circular dependency—the bound depends on the very circuit one is trying to find. The practical utility of the bound for guiding algorithm design is therefore limited, as one cannot evaluate the bound without already having a good circuit.

- **Computational cost of Step I**: The entanglement reduction step requires solving an optimization problem at each iteration to select both the qubit pair and gate parameters. For N qubits, there are O(N²) possible qubit pairs, and each evaluation requires computing the entanglement measure S, which involves partial traces and entropy calculations. The paper does not provide a clear analysis of the total computational cost of this search procedure, which could be prohibitive for large N.

- **Comparison fairness**: The baselines (MPS, HEC, AQCE) are compared with "equal or slightly larger G" due to "feasibility constraints." However, the paper does not clearly explain why the baselines cannot achieve the exact same gate counts as AQER. This raises questions about whether the comparison is truly fair, especially since AQER's advantage is partially attributed to using fewer gates.

- **Missing ablation studies**: The paper does not isolate the contribution of each of the three steps in AQER. How much does Step I (entanglement reduction) contribute versus Step II (product state approximation) versus Step III (parameter refinement)? Without ablation, it is difficult to assess whether the entanglement reduction principle is the key driver of performance or if simpler alternatives would suffice.

### Minor

- **Scalability analysis limited to TFIM**: The scalability experiments (Fig. 4b) are only performed on GS-TFIM, which has a specific structure (1D, low entanglement). It is unclear whether the favorable scaling (T = 4N - 40) generalizes to other types of quantum states or classical data.

- **Theoretical bound tightness**: The gap between the lower bound f₁(S) and upper bound f₂(S) is significant (roughly a factor of N), making the bounds relatively loose for practical prediction of achievable infidelity.

### Trivial
None.

## Nice-to-Haves

- An ablation study isolating the contribution of each of the three AQER steps would strengthen the paper.
- Analysis of the computational complexity of the qubit-pair search in Step I, and potential strategies to reduce it (e.g., greedy heuristics, random sampling).
- Experiments on more diverse quantum datasets beyond TFIM to test generalizability of the scaling behavior.

## Novel Insights

The key insight—that the approximation error of quantum state loading is fundamentally governed by the entanglement entropy of the target state after applying the inverse loading circuit—is genuinely novel and provides a principled foundation for designing approximate quantum loaders. The paper demonstrates that this insight can be operationalized into a practical algorithm (AQER) that outperforms existing heuristic methods. The connection between entanglement reduction and mitigation of barren plateaus is also an interesting observation that could have broader implications for variational quantum algorithm design.

## Suggestions

- Provide an ablation study comparing AQER with variants that skip Step I (random gate placement instead of entanglement-guided) and/or Step II to quantify the contribution of each component.
- Include a complexity analysis of the qubit-pair selection in Step I and discuss strategies for scaling to larger systems (e.g., 100+ qubits).
- Clarify why the baseline methods cannot achieve the exact same gate counts as AQER, and consider adding experiments where all methods use identical gate counts for a more direct comparison.

## Score and Decision

The paper makes a solid theoretical contribution by establishing information-theoretic bounds for approximate quantum loaders, and proposes a well-motivated algorithm that demonstrates strong empirical performance. The main weaknesses are the circular dependency in the theoretical bound's practical utility and the lack of ablation studies. However, the overall contribution—combining novel theory with a practical algorithm that consistently outperforms baselines—is significant and valuable to the quantum computing community.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>