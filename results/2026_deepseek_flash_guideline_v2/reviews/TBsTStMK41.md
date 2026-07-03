Now let me produce the final consolidated review.

## Summary

This paper studies the desk-rejection policies used by AI conferences that enforce per-author submission limits. It formalizes the problem of maximizing the number of papers forwarded to review (desk-accepted) under author-level submission caps as an integer program, proposes a two-stage algorithm using LP relaxation followed by a deterministic rounding scheme, and evaluates on 11 years of ICLR submission data. The method consistently matches or outperforms two baselines (ALLREJECT and FORWARDREJECT), reducing desk-rejections by up to 19.23% with runtimes under 54 seconds on modest hardware.

## Strengths

1. **First formal optimization formulation of submission-limit desk-rejection (Definition 4.1)**: The paper casts the desk-rejection decision as a maximum-desk-acceptance integer program that maximizes the number of papers advanced to review under per-author submission caps. While the formulation is intuitive, the paper is the first to provide an explicit mathematical formalization, enabling principled reasoning about the policy. The baselines (ALLREJECT, FORWARDREJECT) are also formalized with pseudocode and correctness proofs (Algorithms 1–2, Propositions 3.5–3.6), making the comparison reproducible.

2. **Consistent measurable improvement on 11 years of real ICLR data (Table 3)**: On ICLR 2018–2025 data, the proposed method never underperforms either baseline for any tested submission limit b ∈ {4,7,10,13,16,19,22,25}. Relative improvements reach 19.23% (ICLR 2024, b=22), and for the largest recent years (ICLR 2024 and 2025), improvements are positive across all tested b values. The comparison uses FORWARDREJECT (the stronger baseline reflecting actual conference practice) as the basis for improvement, which is appropriate.

3. **Practical runtime on realistic scale (Section 5.2)**: All results in Table 3 were computed within at most 53.64 seconds on modest hardware (2 vCPUs, 13GB RAM), demonstrating the approach is computationally feasible for large conferences handling ~10⁴ submissions.

## Weaknesses

### Fatal

None.

### Major

1. **LP relaxation uses a constraint that is stricter than the original IP (Definition 4.3, line 221)**: The integer program (Definition 4.1) has constraint `Ax ≤ b·1_n`, but the claimed LP relaxation (Definition 4.3) has `Ax ≤ b - 1_n` — the RHS vector has all entries equal to b-1 rather than b. A standard LP relaxation keeps the same constraints and only relaxes integrality. Here the RHS is tightened, which means: (a) the LP feasible region is a strict subset of the relaxed IP feasible region, so the LP optimum provides a *lower bound* on the IP optimum (not an upper bound as standard relaxation would); (b) the LP may be infeasible on instances where the IP has feasible solutions (e.g., an author with exactly b papers); (c) no theoretical guarantee (approximation ratio, optimality gap) is provided for the rounding algorithm. The paper neither discusses this choice nor offers any justification. If `b - 1_n` is a typo (should be `b·1_n`), it must be corrected. If intentional (e.g., as a budgeting mechanism to ensure post-rounding feasibility against the original b), the paper must explain the rationale and provide corresponding guarantees. **This undermines the paper's central technical claim of solving a relaxation of the IP.**

2. **No comparison against the optimal integer solution**: The instances are modest in scale (≤11,672 binary variables, ≤38,495 constraints, ~62K nonzeros in A). The paper does not report whether the IP can be solved directly by a standard solver (e.g., Gurobi, SCIP), nor does it bound the optimality gap of the LP-rounding solution (e.g., using the LP bound as a comparator, if the LP were correctly formulated). Without this information, readers cannot assess whether the LP-rounding approach provides meaningful value beyond what an off-the-shelf IP solver would deliver, or whether the observed improvements over greedy baselines simply reflect the gap to the true optimum. This weakness is compounded by the LP formulation issue above.

### Minor

1. **Mislabeled rounding scheme**: The abstract and introduction (line 45) state the method uses "randomized rounding" — a term that implies approximation guarantees in expectation (Raghavan & Thompson, 1987). However, Algorithm 3 is a completely deterministic greedy procedure (select the fractional variable with largest value, round to 1, force others to 0 as needed to satisfy constraints). The experiments section (line 374) confirms "The experiments are deterministic and contain no randomness." This inconsistency should be corrected; the method uses deterministic greedy rounding, not randomized rounding.

2. **Disconnect between theoretical runtime bound and practical implementation (Remark 4.4)**: Remark 4.4 cites the stochastic central path method with O*(m^2.37) complexity, but the actual implementation uses PuLP's default solver (which does not implement that algorithm). The practical runtime is whatever PuLP provides. The theoretical bound is not misleading per se, but the paper presents it as though it describes the practical algorithm, which it does not.

### Trivial

None.

## Nice-to-Haves

- **Evaluation on synthetic data with different author-paper graph structures** would strengthen claims of generality beyond ICLR's submission patterns (which the paper acknowledges as the only venue with public data).
- **A "random rejection" baseline** (randomly selecting which of an over-limit author's papers to reject) would test whether submission-ID ordering (FORWARDREJECT) introduces systematic suboptimality.
- **Runtime breakdown** showing time spent on LP solving vs. rounding.

## Removed Points

These points were raised by reviewers but are removed with justification:

- **"Hardness claim not substantiated"** (line 213): The paper references the multi-dimensional knapsack problem, which is standard for establishing NP-hardness of multi-constraint packing problems. This is sufficient for an applied paper not claiming a complexity-theoretic contribution.
- **"ALLREJECT describes no sensible venue's policy"**: The critic misread the paper. Algorithm 1 rejects exactly |P_i|-b papers per over-limit author (not "all papers"), and the paper correctly identifies FORWARDREJECT as the stronger, more realistic baseline.
- **"Code/data not released for verification"**: The paper states code and data will be released upon acceptance. The reviewing guidelines prohibit penalizing based on release timing — cited artifacts are assumed to exist.
- **"No variance reported"**: The paper explicitly states the algorithms are deterministic, so variance is inapplicable.
- **"Groundbreaking/pioneering language is overblown"**: A subjective style preference; many papers use such language without confusing readers about the nature of the contribution.
- **"Only ICLR data" as a fatal limitation**: The paper acknowledges this limitation, and ICLR is the only venue with publicly accessible submission records. This is a reasonable scope constraint for an initial study.
- **"Relative improvement calculation not stated explicitly"**: The numbers verify improvement is computed against the better baseline (FORWARDREJECT), which is standard and unambiguous.
- **Missing related works**: The reviewer cannot verify the existence of omitted references; this is excluded per reviewing guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviewer-identified LP constraint discrepancy (b-1_n vs b·1_n) is a real issue but is a correction to the paper's framing rather than an insight about the problem itself.

## Suggestions

1. **Fix the LP formulation issue**: Either correct Definition 4.3 to use `b·1_n` (standard relaxation) or explicitly justify the `b-1_n` RHS as a deliberate budgeting mechanism with accompanying theoretical guarantees (e.g., proof that solutions remain feasible after rounding, and characterization of the optimality loss incurred by tightening the constraint).

2. **Compare against the optimal IP solution**: Solve the IP with a standard solver for the same instances and report the gap. If LP-rounding matches the true optimum (or is within a small gap), this provides clean empirical validation. If the IP is easily solvable, acknowledge that the contribution is the *formulation* and *demonstration* that optimality improves over greedy baselines, rather than the LP-rounding algorithm itself.

3. **Correct the "randomized rounding" language throughout**: Replace with accurate terminology (e.g., "linear programming relaxation followed by deterministic rounding").

## Score and Decision

**Calibration**: The calibration search database was unavailable, so I was unable to retrieve anchor papers for score anchoring. I have used my expertise and the review guidelines to calibrate the score.

**Score rationale**: The paper addresses a real, timely problem with a clean formulation and solid empirical evidence on 11 years of real data. However, it has two significant technical weaknesses: the LP relaxation uses a constraint that is stricter than the original IP (b-1 instead of b — either a typo or an unexplained deviation from standard relaxation), and it does not compare against the optimal integer solution. These issues undermine confidence in the paper's core technical claims. The problems are fixable but require nontrivial revision.

**MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>**