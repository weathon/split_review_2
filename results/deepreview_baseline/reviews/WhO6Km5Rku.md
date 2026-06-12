## Summary
The paper proposes QubitCache, a KV-cache compression framework that shifts from token-selection to preserving attention patterns via quantum-inspired amplitude encoding. Critical tokens are stored classically (15%) while the attention patterns of the remaining tokens are encoded into 9-qubit quantum states, producing probabilistic attention weights through measurement. The authors claim 7× memory reduction while retaining 92-97% performance, with 15-25% higher F1 on multi-hop reasoning tasks compared to existing methods.

## Strengths
- The insight that relational information (attention patterns) may be more important than token-level storage is a reasonable motivation that departs from purely eviction-based compression.
- The hybrid architecture (classical storage for critical tokens plus probabilistic reconstruction for non-critical tokens) integrates naturally with autoregressive generation and provides a concrete mechanism for soft attention.
- The empirical evaluation covers five models (4B-8B and 70B variants) across multiple benchmarks with a relevant set of baselines, demonstrating that the proposed method can achieve competitive or superior performance under its chosen compression ratio.

## Weaknesses
### Fatal
The central claim of “logarithmic compression beyond classical information-theoretic limits” is not substantiated. The paper states that the quantum state requires \(O(\log N)\) storage, but the classical simulation used in all experiments must store the full amplitude vector (size \(2^{\log N}=N\)) to compute measurement probabilities. Therefore QubitCache does not achieve any quantum-advantage in memory; its savings come solely from discarding the KV pairs of non-critical tokens and storing only an attention probability distribution per segment. This mischaracterization undermines the paper’s core novelty and the rationale for introducing quantum concepts.

### Major
- The comparison with baselines (H2O, ScissorHand, StreamingLLM, GEAR) is performed at different compression ratios (QubitCache at 7× vs. baselines at 2×–6.7×). The paper does not provide controlled experiments under equal memory budgets, making it impossible to attribute performance differences to the method rather than the higher compression rate. The claimed 15-25% improvement on multi-hop reasoning is not consistently observed across all model×task combinations in Table 1.
- The necessity of quantum encoding is not demonstrated. The probabilistic weights \(p_j(\psi)\) are just normalized attention scores derived from the amplitude encoding; the same effect could be achieved by storing those scores classically. The ablation study shows only a 3.9% gain from quantum encoding over a no-quantum variant, which is marginal and does not justify the added complexity. A direct classical baseline that stores attention probabilities would be needed to validate the quantum-inspired approach.
- The theoretical claim of preserving rank-\(r\) attention structure with bounded reconstruction error is stated in the abstract and Section 3 but neither stated formally nor proved in the provided main text. This leaves a central promise of the paper unverified.

### Minor
- The method requires precomputed aggregated attention scores (Eq. 3) for token classification and quantum state construction. How these scores are obtained during efficient auto-regressive generation (without recomputing the full attention matrix at each step) is not clearly addressed beyond a brief re-evaluation procedure, whose cost could be significant.
- The definition of \(\lambda = \sqrt{|\mathcal{I}_p|/N}\) is ad-hoc and its sensitivity is not explored.
- Several key design decisions (segment size 512, 9 qubits, 0.15 retention ratio) are justified only through limited ablation; more thorough sensitivity analysis is needed.

## Nice-to-Haves
- A fair comparison where all methods are evaluated at the same memory budget (or a memory-performance curve) would substantially strengthen the empirical contribution.
- Including a classical soft-attention baseline that stores attention probabilities directly (without quantum simulation) would clarify whether the quantum formalism adds value.

## Novel Insights
None beyond the paper’s own contributions. The idea that attention patterns matter more than individual tokens has been explored in prior work on attention pruning and sparse transformers. The specific hybrid encoding scheme is a design choice but its quantum-inspired component is not shown to be essential or beneficial over classical alternatives.

## Suggestions
- Clearly separate the memory contribution: the reduction comes from indexing attention distributions rather than full KV pairs, not from any quantum advantage. Revise the abstract and claims accordingly.
- Add controlled experiments at equal compression ratios (e.g., 7× for all methods) to support the claimed superiority.
- Either prove the bounded reconstruction error theorem in the main paper or remove the claim.
- Replace the quantum simulation with a classical probability-storage baseline to demonstrate whether the quantum machinery is actually necessary.

## Score and Decision
MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>