## Summary

This paper introduces a novel concept called *random set stability* to replace intractable mutual information (IT) terms in data-dependent worst-case generalization bounds. The authors derive expected worst-case bounds in terms of this stability parameter and a Rademacher complexity term, then apply the framework to obtain IT-term-free versions of existing fractal and topological bounds (Theorems 4.3, 4.4). The theoretical framework subsumes classical stability bounds (J=1) and fixed-hypothesis-set Rademacher bounds (J=n) as special cases. Empirical experiments on ViT and GraphSage provide a first-order numerical assessment of the bounds.

## Strengths

- **Well-motivated problem.** The paper correctly identifies that existing data-dependent worst-case generalization bounds (Simsekli et al., 2020; Birdal et al., 2021; Andreeva et al., 2024) all contain intractable mutual information terms that are poorly understood, potentially infinite, and practically impossible to compute. Replacing these with a stability parameter is a sensible and well-motivated theoretical goal (Section 1, lines 53–57).

- **Clean recovery of classical bounds as special cases.** Lemma 3.4 introduces a free parameter J. Setting J=1 recovers classical algorithmic stability bounds (Corollary 3.5), and setting J=n recovers the standard Rademacher complexity bound for fixed hypothesis sets (Corollary 3.6). This demonstrates internal coherence and shows the framework subsumes known results (Section 3.2, lines 171–185).

- **Explicit connection to prior stability literature.** Lemma 3.2 establishes that random set stability is implied by uniform argument stability (Definition 2.1), giving a direct recipe for verifying the assumption in practice via known SGD stability results (Section 3.1, lines 137–151).

- **First IT-term-free versions of topological bounds.** The paper provides mutual-information-free versions of intrinsic dimension bounds (Theorem 4.3) and topological bounds based on weighted lifetime sums and positive magnitude (Theorem 4.4). Prior work could only state these bounds with the IT term as an unevaluated black box. Making them computable in principle, even at the cost of a slower rate, is a genuine theoretical advance (Section 4.1, lines 207–235).

## Weaknesses

### Fatal

None. The theoretical contribution is sound and stands on its own.

### Major

- **The empirical evaluation does not test the claimed theoretical bounds.** The experiments replace the Rademacher complexity term in Lemma 3.4 with Massart's lemma bound, yielding `2√(2 log(T)/J) + 2Jβ_n` (lines 260–261). This simplified proxy does not involve the local Lipschitz constant L_{S,U} from Assumption 4.1, the topological complexity measures from Theorems 4.3/4.4, or the loss bound B — i.e., all the structural information that distinguishes the paper's bounds from a generic finite-set bound. The paper claims to "validate our theory" (abstract, line 9) and to be "the first to *fully* estimate a bound on the worst-case error" (line 280), but the topological bounds (Theorems 4.3, 4.4) — which are the paper's core claimed advance — are never computed. The experiments test a heavily weakened upper bound on Lemma 3.4, not the theorems that constitute the paper's novelty.

- **Optimistic estimation of β_n and a vacuous bound are conflated with meaningful guarantees.** The paper acknowledges that the estimation of β_n "necessarily leads to an optimistic estimation" (line 254). The claim that bounds "remain below 100% accuracy, hence, provide meaningful guarantees" (line 278) is contradicted by Table 1, where ViT with η=10⁻⁴, b=64 yields a bound of 104.43% (the worst-case generalization error can be at most 100%). Since the true β_n can only be larger than estimated, this vacuity would worsen under correct estimation.

- **The "interplay" analysis does not provide the claimed support for Theorem 4.4.** The paper asserts that "our experimental results strongly support Theorem 4.4" (line 297). However, Theorem 4.4 predicts a relationship between *log* E¹ and β_n^{-1/3} G_S(W_{S,U}), while the experiments report Pearson correlations between *raw* E¹ and G_S(W_{S,U}) — a fundamentally different and weaker relationship. The correlations degrade substantially with n for GraphSage (r=0.92 for n=100 falling to r=0.28 for n=10,000), and the paper's explanation ("reaching local minima is harder when n increases") is post-hoc and itself undermines the claimed strong support for the theory.

### Minor

- **Bounds are only in expectation, not high-probability.** The paper acknowledges this limitation (line 307: "we only provide expected bounds"). However, prior work (Dupuis et al., 2024; Andreeva et al., 2024) provides high-probability PAC-Bayesian bounds. An expected bound is a weaker guarantee — an algorithm could have large generalization error on a nontrivial fraction of datasets while still satisfying the expected bound. The paper does not discuss converting its expected bounds into high-probability guarantees or compare tightness against the (IT-term-containing) high-probability bounds of prior work.

- **The O(n^{-1/3}) rate is a significant regression from classical rates.** The paper acknowledges this as a "deliberate trade-off" (lines 231–235), but the practical cost is worth stating directly: for n=10,000, the rate-limiting factor is ~0.046 vs ~0.01 (for O(1/√n)) and ~0.0001 (for O(1/n) stability bounds). While the trade-off (removing terms that can be unbounded) is legitimate, the magnitude of the regression deserves more prominent discussion.

- **Uncertainty is not propagated to the bound.** Table 1 reports β_n with error bars (e.g., 4.72 ± 0.52), but the bound is reported as a single number without accounting for this uncertainty. This makes it impossible to assess the statistical reliability of the bound-vs-gap comparison.

### Trivial

- **Assumption 3.1 quantifies over "any data-dependent selection ω"** — this is a very strong quantification. The paper may only need the assumption to hold for the specific selection ω₀ that attains the supremum of the generalization gap (Definition 3.1). Clarifying whether the stronger quantification is required would improve precision.

## Nice-to-Haves

- **Test the specific structural predictions of the theory.** Instead of collapsing the bound to a Massart-based proxy, estimate each component (β_n, the topological complexity) and check whether their product correlates with the observed generalization gap across configurations of (n, η, b). This would genuinely validate the framework's structure.

- **Compare against prior IT-term-containing bounds.** Even a rough upper bound on the mutual information term from prior work would clarify what is gained and lost by switching to a stability-based framework.

- **Provide at least one setting where the bound is non-vacuous.** Currently bounds range from ~48% to ~104% (Table 1). A configuration where the bound demonstrably constrains the worst-case generalization error below a practically meaningful threshold would strengthen the paper.

## Removed Points

These points were flagged to be removed; treat them with caution.

- **Unfair comparison / missing related work:** Removed because the paper's stated scope is replacing IT terms; comparisons with works outside that scope are not required weaknesses.
- **Corollary 3.3 expression appears non-standard:** The reviewer acknowledged this may be a formatting artifact. Per instructions, formatting artifacts are parser issues and not author errors.
- **Section 1 framing about IT terms possibly being bounded in practice:** This is a reasonable suggestion but not a weakness of the paper as written.
- **"Missing estimation of L_{S,U}" and "Theorem 4.4 itself never computed":** These are restatements of the major weakness about the simplified proxy bound, already addressed.
- **No discussion of regime where β_n is not O(1/n):** The paper does include some discussion (lines 231–235), though it could be expanded. Not a core weakness.

## Novel Insights

None beyond the paper's own contributions. The reviewer accurately identifies a gap between the paper's claimed empirical validation and what the experiments actually test, but this is a critique of the presentation, not a novel synthesis.

## Suggestions

1. **Either run experiments that actually estimate the quantities in Theorems 4.3/4.4** (even approximately, e.g., by estimating L_{S,U} and the topological complexity measures), or **reframe the empirical section** as an initial investigation of the stability parameter β_n itself (which is new and interesting) rather than as validation of the topological bounds. The theory is strong enough to warrant acceptance even with a substantially reduced empirical section.

2. **Correct the claim about bounds staying below 100%** — Table 1 shows a counterexample (ViT, η=10⁻⁴, b=64: bound = 104.43%). Acknowledge that some bounds are vacuous and discuss why.

3. **Clarify why Assumption 3.1 quantifies over all data-dependent selections ω** rather than only ω₀, or state that the assumption can be weakened.

## Score and Decision

The theoretical contribution — random set stability and its application to produce IT-term-free topological bounds — is sound, well-structured, and represents a genuine advance over prior work that relied on intractable mutual information terms. The empirical evaluation, however, substantially overclaims what it demonstrates: it tests a heavily simplified proxy rather than the stated topological bounds, and some reported claims (e.g., "below 100%") are contradicted by the data. The theory itself is publishable, but the experimental framing needs significant revision.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>