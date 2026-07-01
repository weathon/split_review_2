## Summary

This paper introduces a unified framework for approximate quantum loaders (AQLs) and derives information-theoretic lower and upper bounds on the approximation error (infidelity) in terms of a sum of single-qubit Rényi-2 entropies. Motivated by these bounds, the authors propose AQER, a scalable AQL method that constructs loading circuits by iteratively reducing this entanglement measure. Extensive experiments on classical (MNIST, CIFAR-10, SST-2) and quantum (random circuits, TFIM ground states) datasets with up to 50 qubits demonstrate that AQER consistently achieves lower infidelity with equal or fewer two-qubit gates compared to existing methods (MPS, HEC, AQCE), while also showing good trainability and scalability.

## Strengths

- **Unified theoretical framework.** The paper provides a common formulation for TN-based and circuit-based AQL methods, enabling an algorithm-independent analysis. The derived bounds linking infidelity to the entanglement measure \(S\) offer a principled justification for entanglement reduction as a design principle.
- **Novel and well-motivated method.** AQER directly leverages the theoretical insight by constructing circuits that progressively reduce \(S\). The three-step procedure (entanglement reduction, explicit single-qubit rotations, parameter refinement) is clean and practical. The explicit construction of single-qubit rotations without numerical optimization (Corollary 3.2) is a nice practical advantage.
- **Strong empirical results.** AQER outperforms all three baselines across five diverse datasets, often by a large margin (e.g., >60% infidelity reduction on S-RQC). The experiments include up to 50 qubits, demonstrate scalability, and show that the optimization does not suffer from barren plateaus. Downstream tasks (phase transition detection, image reconstruction, classification) further validate the practical utility.
- **Thorough evaluation.** The paper reports infidelity with standard deviations, studies the effect of gate count \(T\) and measurement shots, and provides ablation-style analysis (infidelity vs. \(S\), infidelity vs. \(T\)). The comparison with baselines uses matched or slightly larger gate counts, ensuring fairness.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical bounds are loose and the linear scaling claim is only asymptotic.** The lower bound scales as \(S/N\) (very weak for large \(N\)), and the upper bound involves a discontinuous \(\lceil S \rceil\) term. The claim that “infidelity scales linearly with \(S\)” is only shown in the small-\(S\) limit and is not a tight characterization. While the bounds still motivate the method, their practical tightness is unclear.
- **The entanglement measure \(S\) is not a standard total entanglement measure.** It is the sum of single-qubit Rényi-2 entropies, which can be large even for states with only local entanglement (e.g., GHZ state gives \(S=N\)). The paper does not discuss limitations of this measure or compare it with other entanglement monotones. The theoretical analysis would be stronger if it connected to more established measures like bipartite entanglement entropy.

### Minor
- **The upper bound construction requires access to the reduced density matrices of the target state.** For quantum data, this is feasible via local measurements, but the paper does not discuss the sample complexity or potential overhead in practice.
- **The comparison with baselines, while fair, does not include more recent tensor-network-based methods (e.g., tree tensor networks, MERA) that might be competitive for certain data types.** The selected baselines are reasonable but not exhaustive.
- **The paper claims “first study to establish theoretical limits for AQL from an information-theoretic perspective.”** This is a strong claim; while the bounds are novel, they rely on a specific entanglement measure and are not information-theoretic in the Shannon sense. The phrasing could be softened.

### Trivial
- The notation in Theorem 3.1 uses \(\lceil S \rceil\) without explanation of why the ceiling appears; the bound is not intuitive at first glance.
- Figure 3(a) uses a color bar for \(T\) that is hard to read in grayscale; the dashed lines for bounds are not clearly labeled in the caption.

## Nice-to-Haves

- A discussion of the sample complexity for estimating \(S\) on quantum hardware, and how many measurements are needed per iteration.
- A comparison with a simple baseline that uses random two-qubit gates instead of entanglement-guided selection, to isolate the benefit of the optimization in Step I.
- An analysis of the computational cost (classical simulation time) of AQER relative to baselines, especially for larger \(N\).

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the approximation error of any AQL is fundamentally bounded by the amount of entanglement that the loading circuit can “undo” in the target state. This reframes the problem of approximate state preparation as one of entanglement reduction, which is a clean and actionable principle. The observation that this principle also helps mitigate barren plateaus is a valuable practical connection.

## Suggestions

- Clarify the tightness of the bounds: provide a simple example where the lower bound is achieved or show that the gap between upper and lower bounds can be large.
- Discuss the choice of Rényi-2 entropy vs. von Neumann entropy: why is Rényi-2 more convenient, and are the bounds extendable to von Neumann entropy?
- Include a brief complexity analysis in the main text (e.g., time per iteration, total classical cost) to help practitioners assess scalability.

## Score and Decision

**Score:** 8  
**Decision:** Accept

The paper makes a solid contribution by providing a unified theoretical perspective on approximate quantum loaders, deriving meaningful (if not tight) bounds, and introducing a practical method that demonstrably outperforms existing approaches on a range of benchmarks. The experiments are thorough and support the claims. The work is likely to influence future research on efficient quantum state preparation.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>