## Summary

This paper formalizes desk-rejection under per-author submission limits (a policy increasingly used by AI conferences) as an integer program that maximizes the number of papers forwarded to review. The authors propose solving an LP relaxation followed by a greedy rounding heuristic, and evaluate it on 11 years of ICLR submission data (2013–2025), reporting up to 19.23% relative reduction in desk-rejections compared with the current ID-order-based policies. Execution time is under 54 seconds.

## Strengths

- **Clean, practical problem formulation.** Definition 4.1 (maximize desk-acceptance subject to author-level submission limits) is a natural and appropriate formalization of a real, growing problem in AI conference management. Translating an ad‑hoc policy into a well‑defined optimization task is the paper's strongest contribution.

- **Ecologically valid evaluation data.** The paper uses 11 years of real ICLR submission data obtained via the OpenReview API (2013–2025, covering 67–11,672 submissions per year). This is a non‑trivial data-collection effort and provides a realistic testbed.

- **Consistent empirical improvement.** Across all years and submission-limit values tested, the proposed method never desk-rejects more papers than either ALLREJECT or FORWARDREJECT (the policies currently deployed by conferences), and it frequently reduces rejections noticeably (e.g., 10–19% relative improvement for recent years at tighter limits).

- **Practical efficiency.** All results are computed within 53.64 seconds on modest hardware (2 vCPUs, 13GB RAM), demonstrating that even if the formulation were solved per conference cycle, it is feasible.

## Weaknesses

### Major

- **The "LP relaxation" in Definition 4.3 is not a relaxation.** The integer program (Definition 4.1) has the constraint \(Ax \leq b \cdot \mathbf{1}_n\). The linear program presented as its relaxation (Definition 4.3) has \(Ax \leq (b-1) \cdot \mathbf{1}_n\) — a *tighter* right-hand side. A relaxation must have a feasible region that is a superset of the original; here it is strictly smaller. The paper neither acknowledges this change nor explains why it exists. If \(b-1\) is an intentional buffer for the subsequent rounding, the paper must (a) justify it, (b) stop calling it a relaxation, and (c) compare empirically with the true LP relaxation (\(Ax \leq b \cdot \mathbf{1}_n\)) to quantify what is lost. As written, a reader cannot tell whether the correct RHS is \(b\) or \(b-1\), and the framing is technically incorrect.

### Minor

- **Inconsistency between promised and delivered method.** The introduction (line 45) promises an algorithm "based on linear programming relaxation and **randomized rounding**," but Algorithm 3 (MAXROUNDING) is entirely deterministic (confirmed by line 374: "The experiments are deterministic and contain no randomness"). This is a factual discrepancy that erodes trust in the paper's framing.

- **"Maximizing" language overstates what the algorithm guarantees.** The paper uses "maximizes" (title, abstract, conclusion) to describe its method's effect. Theorem 4.6 only establishes *feasibility*, not optimality — the algorithm has no approximation guarantee, and the paper provides no bound on how far its output is from the IP optimum. A reader familiar with the LP+rounding literature will recognize this as a heuristic; the current wording implies a level of theoretical support that is not delivered.

- **Baseline comparison is too narrow to fully evaluate the algorithm's value.** The only comparators (ALLREJECT and FORWARDREJECT) are the naïve ID-order policies currently used by conferences. Beating them is meaningful for practical impact, but it does not distinguish whether the specific LP+rounding approach is necessary. A simple greedy baseline (e.g., sort papers by number of co-authors and accept greedily) would cost minutes to implement and would substantially strengthen the claim that the LP machinery earns its complexity.

- **Under-specified algorithmic step.** Algorithm 3, line 14: "Find the set \(S_i \subseteq (S \cap T_i)\) such that \(\sum_{j \in S_i} \tilde{x}_j \geq (1 - x_l)\)." The paper does not specify *how* \(S_i\) is chosen (greedy smallest subset? largest fractional values first?). This ambiguity affects reproducibility.

- **Contradiction between "random initialization" and "deterministic."** Algorithm 4 line 2 says "Randomly initialize \(x_0\)," but line 374 says "The experiments are deterministic and contain no randomness." If the LP solver's output is independent of the initial point, the randomization is unnecessary; if it matters, then the reported single-run results may not be reproducible.

- **Hardness claim is promised but not stated in the main text.** The introduction (line 45) says "we establish the computational hardness of the problem," but no hardness theorem (e.g., "this problem is NP-hard") appears in the visible main text. If the proof is deferred to the (stripped) appendix, the main text should at minimum state the result explicitly.

- **Ordering of FORWARDREJECT not specified.** Algorithm 2 iterates \(j = 1 \dots m\), but the paper does not state what ordering of papers this corresponds to (submission ID? timestamp? random?). Since FORWARDREJECT is order-dependent, this matters for reproducibility.

### Trivial

- None beyond what is covered above.

## Nice-to-Haves

- **Run the true IP with a solver.** For problem sizes up to \(m \approx 11,672\) and a sparse constraint matrix, a standard IP solver (e.g., CBC or Gurobi) may solve the integer problem directly, or at least report an optimality gap. Providing this bound would clarify how close the LP+rounding heuristic is to optimal.

- **Compare with the true LP relaxation** (RHS = \(b\) instead of \(b-1\)) to quantify the cost of the unexplained tightening.

- **Acknowledge the transparency/adoptability trade-off.** The current ID-order policy is simple and auditable. An LP-based policy requires trust in a solver and is less transparent. A brief discussion of this practical barrier would strengthen the paper.

## Removed Points

These points were identified in the input review but are removed or demoted for the following reasons:

- The critic's concern that "small absolute improvements" (e.g., 5 papers saved out of 7404) undermines the contribution → **Removed.** The paper correctly reports *relative* improvement, which is a standard framing; the absolute numbers are visible in Table 3 and the reader can judge.

- The critic's claim that the paper lacks "any theoretical or empirical bound on how far the output is from optimal" is **demoted** from a "fatal" structural issue to a minor overclaim — the paper's language is ambiguous but never claims the algorithm is optimal; it attributes "maximizing" to the IP formulation's objective. The absence of an optimality bound is a weakness but not a fatal error.

- Criticisms about "no variance reported" and "order of baselines" being potentially unfair → The paper explicitly states experiments are deterministic. If the algorithm is indeed deterministic, variance reporting is inapplicable. The ordering concern is kept as a minor reproducibility point.

## Novel Insights

None beyond the paper's own contributions. The input review's substantive observations (the b-1 error, the framing mismatch) are concrete verifications of issues in the paper rather than novel cross-paper insights.

## Suggestions

1. **Fix the LP formulation.** Decide whether to use \(b\) or \(b-1\). If \(b-1\) is intentional, explain why, stop calling it a relaxation, and compare with \(b\) empirically. If \(b\) is correct, the LP relaxation is standard.
2. **Add a greedy baseline.** This is the single most informative additional comparison — it directly tests whether the LP+rounding complexity provides value over a simple alternative.
3. **Remove or substantiate the "maximize" language.** Replace with "increases" or "improves" unless an optimality bound is provided.
4. **Correct the "randomized rounding" claim** in the introduction to match the deterministic algorithm actually used.
5. **Specify the ordering** used by FORWARDREJECT and the selection criterion in Algorithm 3, line 14.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>