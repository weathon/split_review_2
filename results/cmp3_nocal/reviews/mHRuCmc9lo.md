## Summary

This paper studies how a conservative decision maker should act when given predictions that satisfy a partial ("ℋ-calibration") guarantee, rather than the intractable full calibration. The authors characterize the minimax-optimal decision rule via a duality argument (Theorem 3.1) that interpolates between fully conservative play and aggressive best-response, with the level of conservatism governed by the richness of ℋ. Their central theoretical result (Theorems 4.1–4.2) shows a sharp transition: once ℋ contains the decision-calibration class (|𝒜| indicator functions of decision regions), the optimal robust policy collapses to simple plug-in best response, and any further strengthening of calibration does not change this. For ℋ that falls short of decision calibration, the optimal policy remains efficiently computable.

---

## Strengths

- **A clean, non-trivial theoretical result (Theorems 4.1/4.2).** The "sharp transition" finding — that decision calibration (with only |𝒜| test functions) is sufficient to make plug-in best response minimax-optimal, and that any stricter calibration does not improve the guarantee — is genuinely surprising and goes cleanly beyond existing swap-regret guarantees (Noarov et al., 2023). Theorem 4.1 shows optimality over *all* policies mapping predictions to actions, which is a qualitatively stronger statement than the action-remapping comparison class.

- **The duality-based characterization (Theorem 3.1, Section 3)** provides a principled and tractable computational framework for deriving robust policies under any finite-dimensional ℋ, with a clear two-step procedure (solve for dual multipliers, then pointwise minimization). The interpolation perspective (Figure 1) correctly contextualizes the result between the two classical extremes.

- **The paper is well-scoped and honest about its limitations.** The linear-utility assumption (Assumption 2.1) is stated explicitly and its limitations are acknowledged in Section 6. The paper correctly delineates the two regimes (can vs. cannot influence training) and does not claim to solve the problem of achieving ℋ-calibration itself, deferring to existing work.

---

## Weaknesses

### Fatal
None.

### Major

- **The adversarial distribution construction in the experiments is underspecified.** Section 5 states that two adversarial distributions are constructed — "a worst case tailored to the plug-in policy, and a worst case induced by the robust dual, tailored to the robust policy" (lines 269–271) — but provides no algorithmic description of *how* these distributions are built, what optimization problem is solved to find them, or what constraints they satisfy. Since the entire experimental comparison hinges on these adversarial constructions, the absence of any concrete description makes it impossible for a reader to assess whether the comparison is meaningful or whether the construction could be biased. This is an evidential issue regardless of whether the paper is primarily theoretical.

### Minor

- **The experiments do not directly test the paper's headline theoretical result.** The experimental evaluation (Section 5) tests the self-orthogonality case (Proposition 4.4: ℋ = {h(v)=v}), which falls well short of decision calibration. The paper explicitly scopes the experiments this way (Section 1.1, contribution 4), so this is not a misrepresentation. However, the paper's most striking conceptual claim — that decision calibration suffices for plug-in best-response optimality — receives no direct empirical validation. A synthetic experiment where a forecaster is explicitly decision-calibrated (via post-processing) for a multiclass decision problem would directly substantiate Theorem 4.1.

- **No uncertainty quantification in experimental results.** Table 1 reports only point estimates of mean utility. The differences between plug-in and robust policies are small (0.01–0.02 on an absolute scale), and without standard errors, confidence intervals, or multiple train/test splits, it is unclear whether these differences are statistically significant or reflect meaningful practical improvements.

- **The practical significance of the decision-calibration result is narrower than the framing may suggest.** Decision calibration is inherently tied to a specific decision problem (action set 𝒜, utility u): a forecaster that is decision-calibrated for one decision maker may not be for another. The paper acknowledges this via Corollary 4.3 (union of test classes across multiple problems), but the test class then grows linearly in the number of problems and their actions. This does not invalidate the theory but means the "trustworthiness" guarantee is problem-specific rather than agnostic, which constrains its practical reach more than the "simple path to decision-theoretic trustworthiness" framing (line 147) may imply.

### Trivial

- None.

---

## Nice-to-Haves

- **Explicitly stating the general dual objective for Theorem 3.1 in the main text** would make the tractability claim concrete rather than deferred to the appendix. (A concrete dual is shown for the 1D self-orthogonality case in lines 238–241, which is helpful.)

---

## Removed Points

These points appeared in the input review but are removed per the filtering guidelines:

1. **"No discussion of finite-sample effects in the main text"** — The paper explicitly states (line 85) that approximate ℋ-calibration is discussed in Appendix B. Since the appendix is stripped by the parser, this criticism cannot be verified against the original submission and is removed per the hard rule on appendix-missing criticisms.

2. **"Self-orthogonality result is straightforward and not deep"** — This is a subjective judgment call, not a verifiable weakness. The paper presents it as an illustrative secondary contribution, and it serves its purpose.

3. **"Discontinuity of decision-calibration test functions raises sample complexity questions"** — The paper explicitly scopes out the problem of achieving ℋ-calibration (lines 103–104), deferring to existing work (Noarov et al., 2023; Zhao et al., 2021). The criticism asks the paper to address something it has explicitly declared outside its scope. The problem-specificity concern is kept above as a minor weakness; the achievability/sample-complexity concern is removed.

---

## Novel Insights

None beyond the paper's own contributions. The input review's framing largely echoes the paper's own narrative rather than adding a genuinely novel analytical lens.

---

## Suggestions

1. **Describe the adversarial construction concretely.** Provide the optimization problem (even a brief description: e.g., "the worst-case distribution for the plug-in policy is found by solving a linear program that minimizes the plug-in's expected utility subject to the ℋ-calibration moment constraints and fixing the marginal distribution of f(X) to the empirical distribution") so readers can assess the experimental comparison.

2. **Add variance or uncertainty estimates** (standard errors, confidence intervals, or results across multiple train/calibration/test splits) to Table 1. The observed differences are small enough that single-run point estimates are not informative.

3. **Add a synthetic experiment for the decision-calibration result.** A controlled setting where a forecaster is explicitly made decision-calibrated for a multiclass problem, and plug-in and robust policies are verified to coincide, would directly validate Theorem 4.1 and strengthen the paper's empirical contribution considerably.

4. **Refine the framing of decision calibration's practical scope.** The paper currently emphasizes that plug-in best-response is recovered under decision calibration, but a reader could miss that this guarantee is problem-specific. A brief clarifying sentence early in Section 4.1 would help.

---

## Score and Decision

This is a solid theory paper with a clean, non-trivial result that advances the theoretical understanding of when calibrated predictions can be trusted in decision making. The core theoretical contributions (Theorems 3.1, 4.1, 4.2) are sound, well-proven, and correctly contextualized against prior work. The experimental section has significant presentation gaps (underspecified adversarial construction, no variance estimates, disconnection from the main theoretical result), but for a primarily theoretical paper these weaknesses are addressable and do not undermine the central claims. The paper should be accepted on the strength of its theory.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>