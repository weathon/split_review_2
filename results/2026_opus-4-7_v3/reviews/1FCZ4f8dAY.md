Now let me read the remaining parts of the paper more carefully, especially the experiments section and discussion.Now I have a comprehensive understanding of the paper. Let me draft the review before calibration.Now let me proceed with Round 1 calibration — bracketing across score bands.This is very informative. I found what appears to be an earlier version of the same paper (`kyVzYpDxHg.md`, avg score 5.75). Let me read the full reviews for key anchors.Now let me read the Lie algebra canonicalization paper briefly for another accepted anchor comparison.I now have comprehensive calibration data. Let me finalize the review.

**Round 1 bracket:** Based on the anchors, this paper sits between **5.5 and 7.0**. Key comparisons:
- The earlier version of this same paper (kyVzYpDxHg, 5.75) was rejected with only one experiment. The current version has significantly expanded experiments and improved presentation.
- The accepted papers in the 6.5-7.0 range (LieLAC 6.5, Characterization Theorem 7.0) have comparable theoretical depth but cleaner experimental validation.
- Papers in the 4-5 range had more fundamental issues with scope, clarity, or contribution.

The paper sits in the borderline accept range, improved meaningfully from 5.75 but still below the solid 7.0 accepted papers due to the Sp(d) experiment gap, missing CG comparison, and unexplained Table 3 patterns.

Now let me write the final consolidated review.

---

## Summary
This paper develops a unified invariant-theory framework for constructing equivariant ML architectures on tensor-to-tensor maps under the diagonal action of classical Lie groups: O(d), O(s,d−s) (including Lorentz), and Sp(d). The core theoretical results (Theorems 1–2, Corollaries 1–3) characterize equivariant polynomials and entire functions via sums of tensor products with isotropic tensors, parameterized by scalar MLP coefficients that depend on invariant inner products. Three experiments — materials science stress-strain prediction, path signature estimation, and sparse vector recovery — demonstrate the approach, with strong results on the first two tasks and mixed results on the third.

## Strengths

- **Unified invariant-theory framework genuinely broader than prior CG-based methods.** Theorems 1–2 and Corollaries 1–3 provide a single framework covering O(d), O(s,d−s), and Sp(d), whereas CG-based methods (e3nn, escnn, Domina et al.) are limited to SO(d)/O(d) for d=2,3. The related work in Section 1 is thorough and honest about the trade-offs. Specifically, the paper acknowledges that "Clebsch–Gordan–based methods...are more memory efficient than our general formulation" (line 33) while correctly noting the generality advantage.

- **Corollary 2 is elegant and yields decisive experimental gains.** The reduction of O(d)-equivariant functions on symmetric 2-tensors to permutation-equivariant eigenvalue functions (Section 3) is a clean theoretical insight. Table 1 demonstrates order-of-magnitude improvements across all dataset sizes: e.g., 4.057e-6 vs. 2.020e-5 for n=5,000 and 7.748e-7 vs. 9.365e-6 for n=20,000. This experiment is particularly convincing because the ground truth (Equation 23) is analytically known.

- **Diverse experimental applications demonstrating generality.** Three genuinely different domains — materials science, time series via path signatures, and sparse vector recovery — are tested. The path signature experiment (Table 2) is notable for connecting equivariant tensor learning to an increasingly active time series representation area, with strong results for both O(d) (0.002 vs 0.007 next-best) and Lorentz (0.005 vs 0.186 next-best) settings.

- **Clear mathematical exposition with good accessibility scaffolding.** The progression from Definitions 1–9 through Theorem 1 to practical Corollary 1 is well-paced. The suggestion to focus on Corollary 1 for practitioners (line 109), along with Example 1 (Equations 12–14) and Figure 1, make the construction concrete and implementable.

## Weaknesses

### Fatal
None

### Major

1. **Symplectic group is in the title but absent from experiments.** The title "Tensor Learning with Orthogonal, Lorentz, and Symplectic Symmetries" and the abstract promise results for all three groups. Corollary 3 and Theorem 2 provide the Sp(d) generalization. Yet no experiment validates symplectic equivariance — not even a synthetic sanity check. The authors note that Sp(d) "is the underlying group in much of classical and quantum mechanics" (Section 1, line 17), making the absence of a Hamiltonian mechanics experiment a clear missed opportunity. This creates a notable gap between the paper's advertised scope and its delivered validation. While the theory may be correct, a third of the theoretical contribution remains practically unvalidated.

2. **Systematic pattern of Ours (Diag) outperforming Ours in Table 3 is unexplained.** In the sparse vector experiment, the diagonal-only variant (using only norms, discarding cross-products) outperforms the full model in 6 of 12 settings — specifically all Diagonal and Identity covariance rows for Accept/Reject, Bernoulli-Gaussian, and Corrected Bernoulli-Gaussian sampling. The gaps can be dramatic: under BG/Diagonal, Diag achieves 0.914 vs. Ours at 0.463; under BG/Identity, 0.908 vs. 0.342. This systematic pattern — that the additional equivariant cross-product features can severely hurt performance — is never discussed in the paper. This undermines confidence in understanding the method's practical behavior and raises questions about when the full parameterization should be preferred over the simpler diagonal variant.

### Minor

1. **No comparison with CG-based equivariant baselines.** Despite extensively discussing e3nn, escnn, and Domina et al. in the related work and asserting "the computational and approximation power should be equivalent" (Section 1, line 33), no head-to-head comparison is attempted. This makes the equivalence claim untested. Weakened because the paper's main value proposition is generality across groups where CG methods don't apply (Lorentz, Sp(d)), and the CG methods are restricted to d=2,3 — but a comparison on the O(d) tasks (stress-strain or path signature) would have been informative.

2. **Scalability analysis absent despite acknowledged factorial complexity.** The complexity is O(k'! n^{k'} (Q d n² + d^{k'})), which is factorial in output tensor order k'. The paper honestly acknowledges this is "only practical for small values of k'" (line 135), and all experiments use small d (3 or 5) and low k' (≤4). However, no wall-clock comparison, memory analysis, or scalability plot is provided to help practitioners understand the method's practical envelope.

3. **Introduction's "almost all cases" claim is somewhat overstated.** Line 19 states "our equivariant learned models outperform prior static methods and non-equivariant learned models in almost all cases," but Table 3 shows SoS outperforming all learned models in 5 of 12 rows (the entire Bernoulli-Gaussian block plus Accept/Reject Identity and Corrected BG Identity). The Table 3 caption provides nuanced discussion of this, so the paper partially addresses the issue, but the introduction's framing doesn't match the actual results.

4. **Discussion section is extremely terse.** Section 6 consists of four sentences with no limitations analysis, no failure-case discussion, and no substantive future-work directions. Given the mixed Table 3 results and the acknowledged scalability constraints, an explicit limitations section would increase credibility. The unexplained Ours vs. Ours (Diag) pattern in particular deserves discussion.

### Trivial
None

## Nice-to-Haves
- At least one synthetic Sp(d) experiment (e.g., learning a symplectic map on phase space) to align experiments with the title and validate the Sp(d) theory branch
- A head-to-head comparison with e3nn on a shared O(d) task
- Ablation studies on number of summation terms, MLP depth/width, and weight-sharing scheme for the q functions
- A brief scalability analysis (wall-clock or memory vs. k' and d)
- Analysis of when the full model vs. diagonal variant should be preferred, based on the Table 3 patterns

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Missing standard deviations in Table 2.** The table caption explicitly states "standard deviation given as ±0.xxx when it is at least 1e-3," so omitted stds represent very small variance (<0.001). The performance gaps are large enough that statistical significance is not in doubt. Removed: addressed by the paper.

- **Gap between polynomial theory and MLP practice.** Remark 1 (line 137) addresses this via Stone-Weierstrass, noting that polynomial approximation on compact sets is sufficient. While the reviewer correctly notes this doesn't guarantee an MLP finds a good approximation, this gap is standard across essentially all equivariant ML papers that use universal approximation arguments. Removed: not specific to this paper.

- **TFENN baseline numbers taken from reference rather than reproduced.** Table 1 notes "TFENN errors are the results reported in Garanger et al. (2024)." This is standard practice when comparing to published results. Removed: not a real weakness.

- **Section 4 brevity and proof details in appendix.** The section concisely presents the generalizations to other groups; full proofs belong in the appendix. Removed per rules: appendix-deferred content.

- **Path signature metric not normalizing by scale at each tensor order.** The metric is clearly defined in Table 2 caption. While per-order normalization could provide additional insight, the current metric is a reasonable and standard choice. Removed: speculative concern without evidence of actual problem.

## Novel Insights
The paper's central insight — that classical invariant theory provides a practical, implementable parameterization for equivariant tensor ML across multiple Lie groups without requiring Clebsch-Gordan decompositions — is genuinely novel in the ML context. Corollary 2's reduction to permutation-equivariant eigenvalue functions is particularly elegant and practically powerful, as evidenced by the order-of-magnitude stress-strain improvements. The connection between path signatures (an increasingly popular time series tool) and equivariant tensor learning is a natural but previously unexploited bridge that opens interesting directions.

## Suggestions
- Add at least one Sp(d) experiment to validate the theoretical claim and align experiments with the title — even a simple synthetic Hamiltonian system would suffice
- Analyze the systematic pattern of Ours (Diag) outperforming Ours in Table 3 and provide guidance on when cross-product features help vs. hurt
- Expand Section 6 to include explicit limitations (especially scalability constraints and the Sp(d) gap), failure-case analysis, and concrete future directions
- Soften the "almost all cases" claim in the introduction to more accurately reflect the mixed Table 3 results, or scope it to exclude the sparse vector experiment where SoS has stronger theoretical guarantees

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Earlier version of this paper | kyVzYpDxHg | 5.75 | R1 | Same core theory but only sparse vector experiment; current version significantly expanded |
| GRepsNet | tzpXhoNel1 | 4.25 | R1 | Similar goal (general equivariant networks) but weaker theory and presentation issues |
| Unified Universality Theorem | NxLWeK4P3q | 5.00 | R1 | Purely theoretical equivariant universality; less practical demonstration |
| Multi-permutation equivariance | 4v4nmYWzBa | 5.25 | R1 | Narrower scope (permutations only), less experimental breadth |
| Learning symmetries via loss | 0aaaM31hLB | 5.25 | R1 | Empirical approach to equivariance; different methodology, weaker theoretical contribution |
| LieLAC | 7PLpiVdnUC | 6.50 | R1 | Accepted; comparable scope covering arbitrary Lie groups, stronger experimental validation |
| Characterization Theorem | 79FVDdfoSR | 7.00 | R1 | Accepted; strong theory paper with clear practical implications, cleaner scope |
| Lie Group Decompositions | p34fRKp8qA | 6.83 | R1 | Accepted; similar ambition covering multiple Lie groups with practical demonstrations |
| Affine Invariance CNNs | NukRlEUICA | 3.00 | R1 | Rejected; narrower scope, less convincing results |
| PowerNet | OopiU1q328 | 2.00 | R1 | Rejected; quasi-equivariance approach, fundamental methodological concerns |
| NN symmetry parameter spaces | oMfZUSbVwf | 3.00 | R1 | Different focus (parameter space), less broad |
| Financial market NN | nSDOkm0SKo | 1.00 | R1 | Strong reject; fundamentally weak paper, not comparable |

**Round 1 bracket: 5.5–7.0**

The paper is clearly above the earlier version (5.75) that had only one experiment and limited practical relevance — both major criticisms that are now addressed. The three experiments, improved presentation, and Figure 1 represent meaningful improvements. However, it falls below the accepted 6.5–7.0 papers (LieLAC, Characterization Theorem, Lie Group Decompositions) due to: (1) the Sp(d) experiment gap creating a mismatch between title claims and validation, (2) the unexplained mixed Table 3 results, and (3) the missing CG comparison despite explicitly claiming equivalence.

**Final score: 6.0.** The paper makes a genuine theoretical contribution with mostly strong experimental validation. The invariant-theory framework is broader than CG-based alternatives, the stress-strain and path signature experiments are convincing, and the exposition is clear. The major weaknesses — the Sp(d) gap between title and experiments, and the unexplained Ours vs. Ours (Diag) performance inversions — are significant but addressable concerns that keep the paper at the borderline rather than a clear accept. The contribution is real enough to merit acceptance, but only at the margin.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>