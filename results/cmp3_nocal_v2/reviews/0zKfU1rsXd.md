## Summary

This paper proposes a unified framework for approximate quantum loaders (AQL), derives information-theoretic bounds connecting AQL infidelity to an entanglement measure (sum of single-qubit Rényi-2 entropies), and introduces AQER, a method that constructs loading circuits by greedily reducing this entanglement measure. Experiments on classical (MNIST, CIFAR-10, SST-2) and quantum (random circuits, TFIM ground states up to 50 qubits) datasets compare AQER against MPS, hardware-efficient circuits, and AQCE.

## Strengths

- **Unified theoretical framework (Section 3.1, Eq. 1).** The paper provides a clean reformulation of diverse AQL methods (TN-based, variational and non-variational circuit-based) as instances of a single optimization problem, creating a foundation for algorithm-independent analysis that was lacking in prior literature.

- **Information-theoretic bounds (Theorem 3.1).** The connection between AQL infidelity and the Rényi-2 entanglement entropy of the evolved state U†|ψ_target⟩ is novel. The bounds establish that low entanglement is sufficient for low infidelity, providing a principled design goal beyond the purely heuristic motivations typical in AQL.

- **Broad experimental scope.** Evaluation covers synthetic quantum circuits, a physical many-body system (TFIM), classical images (MNIST, CIFAR-10), and language embeddings (SST-2), with scalability up to 50 qubits on TFIM. This is substantially more comprehensive than typical AQL papers.

- **Downstream task validation (Figures 4c, 5a–5b).** The paper goes beyond infidelity as a proxy metric by validating that AQER-loaded states preserve physically relevant observables (magnetization for phase transition detection) and classification accuracy, demonstrating that low infidelity translates to useful downstream behavior.

## Weaknesses

### Fatal

None.

### Major

1. **Main comparative claim rests on unmatched gate budgets (Table 1, Section 4.3).** The central claim — that AQER "consistently outperforms existing methods in both accuracy and gate efficiency" — is supported by Table 1, where AQER uses G ∈ {20, 40, 80} while baselines use different G values (36/54/90 for MNIST, 30/60/90 for CIFAR-10, etc.). The paper acknowledges this is "due to feasibility constraints" and notes the baselines use "slightly larger G," but the comparison confounds method quality with gate budget. For example, AQER at G=20 vs. AQCE at G=36 on MNIST (0.195 vs. 0.206) shows AQER winning at a lower gate count — which directionally supports gate efficiency — but without a matched-G comparison the reader cannot cleanly separate the method's effect from the specific gate counts chosen. The 50% gate-count claim for S-RQC is also imprecise depending on which baseline tier is referenced. The consistent qualitative trend across all datasets is encouraging, but the evidence format does not meet the rigor the paper's strongest claims demand.

2. **No ablation study isolating the three components of AQER (Section 3.2).** AQER has three steps: (I) iterative entanglement reduction via two-qubit gates, (II) closed-form single-qubit correction, and (III) variational fine-tuning. The paper presents no experiment that isolates their individual contributions. This matters because Step III is a standard variational optimization; without a control where Steps I–II are replaced by random circuit construction with the same gate count, it is impossible to attribute the observed performance to the entanglement-guided design principle versus generic variational optimization from a favorable initialization. The paper's core thesis — that entanglement reduction is the right design principle — remains experimentally untested as a causal mechanism.

3. **Barren plateau mitigation claim is not supported by the presented evidence (Section 4.3, Figure 4a).** The paper shows optimization curves on GS-TFIM at N=50 that decrease from infidelity ~0.3 to ~0.1 and claims this "demonstrates that the entanglement-reduction mechanism in AQER successfully mitigates barren plateau effects" (line 183). The standard in the field (McClean et al. 2018, Cerezo et al. 2021) is to report gradient variance statistics or success-rate comparisons across many random initializations. A single set of optimization curves on one structured dataset family does not establish mitigation of barren plateaus — cost landscapes with global flatness can still yield successful runs from specific starting points. This overclaims what the evidence can support.

### Minor

4. **The theoretical bounds are very loose (Theorem 3.1).** The linearized lower bound scales as (ln 2 / 2N) S while the upper bound scales as (ln 2 / 2) S — a factor of N gap (50× for N=50). The paper's phrasing that infidelity "scales linearly with S" is technically accurate (both bounds are linear), but the gap means the bounds primarily establish sufficiency (low S ⇒ low infidelity) rather than providing tight characterization. The framing in the abstract and introduction could more clearly acknowledge this looseness.

5. **Missing error characterization on scalability results (Figure 4b).** Figure 4(b) shows infidelity vs. N and T for GS-TFIM with no visible variance or error bars. The paper reports M=5 per configuration; without error bars or shaded regions the claimed scaling relationship (T = 4N − 40) may be within noise. For N=50, standard deviations comparable to those in Table 1 are not reported.

6. **Under-specification of resource cost for quantum data inputs (Remark, Section 3.2).** The paper claims AQER supports "unknown quantum states" and states that evaluating S is efficient because it "involves only local measurements" (line 116). For an unknown quantum state provided by an external source, evaluating S for candidate circuits requires many copies of the state with per-iteration costs that are not discussed in the main text. The paper references Appendix G for complexity analysis, but the main text should at least sketch the sample complexity.

7. **Limited quantum data diversity in scalability experiments.** Scalability to 50 qubits is demonstrated only on GS-TFIM, which has special structure (gapped ground states of a 1D Hamiltonian). The S-RQC experiments (more generic entangled states) are limited to N=10. Whether the scalability results transfer to more general quantum states is unclear.

### Trivial

None.

## Nice-to-Haves

- Run reference methods at matched G values {20, 40, 80} (AQER's values) so the central comparative claim rests on cleaner evidence. If feasibility truly prevents this, interpolate or extrapolate baseline performance.
- Conduct a stepwise ablation: (a) full AQER vs. (b) only Steps II+III with random circuits replacing Step I vs. (c) only Step III with fully random initialization.
- Compute gradient variances in Step III both with and without entanglement-reduction pre-training to support the barren plateau claim with field-standard evidence.
- Report paired significance tests or bootstrap confidence intervals for the differences in Table 1, since several comparisons have overlapping error bars.
- Provide error bars or shaded regions in Figure 4(b).

## Removed Points

These points were flagged for removal; treat them with caution:

- **"The claim that circuit-based methods 'suffer from barren plateaus' is broader than what is known"** — Removed. This is a standard, widely accepted claim in the VQA literature. The reviewer's concern about specific AQL methods is too narrow.
- **"The optimization procedure is only sketched (qubit pair selection)"** — Removed. The paper provides a sufficient algorithmic description for a heuristic method with appendix references.
- **"M=50 for classical datasets is small"** — Removed. Generic sample-size nitpick; the reported standard deviations are reasonable.
- **"SST-2 results are very poor"** — Removed. An observation about results, not a paper weakness; the paper presents these honestly.
- **"The Renyi-2 entropy is not a faithful entanglement measure for mixed states"** — Removed. The paper explicitly states Theorem 3.1 is for pure states and defers generalization to Appendix C.
- **"Abstract should qualify 'scales linearly' as an upper bound"** — Removed. The statement is technically correct: both lower and upper bounds show linear scaling.

## Novel Insights

The reviews surface a consistent pattern: the paper's theoretical contributions (unified framework, information-theoretic bounds) are genuinely novel and well-received, but the experimental evidence for the method's core advantage (entanglement-guided construction) is weaker than the paper asserts. The absence of ablation and matched-G comparisons means the paper presents correlational rather than causal evidence for its design principle. This gap between theoretical contribution and experimental validation — specifically, that the theory motivates the design but the experiments do not isolate whether the design accounts for the observed performance — is the single most actionable insight. The consistent qualitative trend across all datasets (AQER wins in 14/15 benchmark entries despite using fewer gates) suggests the conclusion is likely correct, but the evidence format needs tightening.

## Suggestions

1. Add matched-G experiments to Table 1 so the comparative claim is unambiguous.
2. Add a stepwise ablation (random vs. entanglement-guided construction) to directly test whether entanglement reduction is the causal mechanism behind AQER's performance.
3. Provide gradient variance statistics across multiple seeds to support the barren plateau mitigation claim, or soften the claim to match the evidence.
4. Add error bars to Figure 4(b) and clarify the statistical basis for the T = 4N − 40 scaling observation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>