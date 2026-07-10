Now let me compile the final review.

## Summary

This paper proposes ZNet, a deep learning method that decomposes observed covariates X into a confounder representation C = f(X) and an instrument representation Z = g(X) through a multi-part loss enforcing correlational proxies for the standard IV conditions (relevance, exclusion restriction, unconfoundedness). The learned (C, Z) are then used with downstream IV estimators (TSLS, DeepIV, DFIV) for causal effect estimation. The paper evaluates across four data classes, two functional forms, and three estimators — a more thorough evaluation than most prior work.

## Strengths

- **Well-motivated problem.** The paper correctly identifies that finding valid instruments is a bottleneck in IV-based causal inference (lines 13–23), and the framing is clear and grounded in real challenges from medicine, economics, and epidemiology.

- **Comprehensive evaluation design.** The paper evaluates across four data generation classes (Disjoint, Mixed, Latent, No Candidate), two functional forms (linear, nonlinear), and three downstream estimators (TSLS, DeepIV, DFIV). This breadth of evaluation is more thorough than most work in this area.

- **Ablation study (Figure 5c).** The ablation of loss constraints on the Mixed Candidate dataset provides concrete evidence that each of the three constraints contributes to instrument recovery. This is a clean diagnostic experiment that helps isolate ZNet's mechanism.

## Weaknesses

### Fatal

- **Lemma 1 contains a mathematical error that invalidates the theoretical justification for the unconfoundedness constraint (Constraint 1).** The proof (lines 91–95) incorrectly expands E[Z·(e_Y − E[e_Y|X,T])] as E[Z·e_Y] − E[Z]·E[e_Y|X,T]. The correct expansion is E[Z·e_Y] − E[Z·E[e_Y|X,T]], and these are not equivalent — the paper's step treats the random variable E[e_Y|X,T] as a constant when factoring the expectation. Moreover, because Z = g(X) is (X,T)-measurable, E[Z·E[e_Y|X,T]] = E[Z·e_Y] holds always by the law of total expectation, making Cov(Z, e_Y − E[e_Y|X,T]) = 0 an unconditional identity rather than a constraint. The premise is vacuous and the conclusion Cov(Z, e_Y) = 0 does not follow. Since the unconfoundedness loss L_{Z↔ε_Y} (lines 133–141) and the paper's claim to "relax the assumption that observed variables are not influenced by U" (line 390) are motivated by Lemma 1, this is a structural flaw that undermines a central theoretical contribution.

### Major

- **The paper overclaims empirical superiority.** The abstract states ZNet produces "superior" instrument representations and the discussion claims ZNet is "on average the highest performing among IV generation methods." However, Table 1 shows a mixed picture: ZNet has the most bold entries among learned methods, but TrueIV (the ground-truth instrument) frequently dominates when available, and other learned methods (AutoIV, VIV, GIV) each win in multiple settings. ZNet's ATE errors are also large in absolute terms in some settings (e.g., Linear No Candidate (no U) with TSLS: error of 2.718 vs. true ATE 1.882). The results support "competitive" rather than "superior" or "highest performing," and the framing should be calibrated accordingly.

- **Covariance-based constraints are insufficient proxies for causal IV conditions.** The paper uses Pearson correlation to enforce all three IV conditions (lines 99–103). Relevance requires conditional dependence Z ⟂̸ T | C, but Cov(Z, T) > 0 only enforces marginal correlation. Exclusion restriction requires Z has no direct effect on Y, but Cov(C, Y) > 0 and Cov(C, Z) = 0 do not imply Z ⟂ Y | C, T. Unconfoundedness requires Z ⟂ e_Y | C, but Cov(Z, e_Y) = 0 is necessary but not sufficient for independence. The paper mentions mutual information as an alternative (line 131) but the description is vague ("approximated using kernel density estimation") and the experiments do not distinguish when MI was used vs. PC, making it impossible to assess whether this addresses the gap.

- **The decomposition X → (C, Z) is not identifiable from the correlational constraints alone.** The paper's constraints are conditions on moments of observed variables, while valid IV conditions are conditions on the underlying causal graph. Many decompositions of X into two uncorrelated components could satisfy these constraints without corresponding to the true causal model. The paper acknowledges this in principle (line 394: "IV estimation in general is limited by a lack of theoretical guarantees of identifiability in the general case") but does not state what specific assumptions (sparsity, functional form, etc.) would make the ZNet decomposition meaningful.

### Minor

- **The "No Candidate" setting (Figure 6) shows weak relevance on held-out data** (test F-statistic p = 0.08, line 292), indicating the learned Z has limited relevance to T on unseen data despite strong training-set performance. This raises concerns about generalization of the learned instrument.

- **The hyperparameter tuning procedure is complex** (Bayesian optimization over loss weights, PC vs. MI choice, gradient surgery, lines 162–166) but the selected configurations are not reported. This makes reproducibility difficult.

- **The paper claims (line 394) that "Solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument."** This is too strong given the gap between the correlational constraints enforced and the full causal IV conditions.

### Trivial

None.

## Nice-to-Haves

- Report selected hyperparameter configurations from the Bayesian optimization.
- Discuss why the test-set relevance degrades in the No Candidate setting and how this might be addressed.
- Evaluate on continuous treatments as suggested in the paper (line 172).
- Include CATE evaluation in the main text rather than only the appendix.

## Removed Points

These points from the harsh critic review were removed after verification:

- **Lemma 1 proof error analysis (partial):** The critic correctly identified the error in the proof step but did not identify the deeper issue that the premise is vacuous (an unconditional identity). Retained and strengthened in the Fatal section.

- **SCM ambiguity about error functions:** The paper clearly states the additive confounding assumption following Hartford et al. (2017) and adds ε_Y, ε_T noise terms in Section 6.1. Not a genuine ambiguity.

- **Lines 85–86 conflation of independence requirements:** The paper's framing is standard and consistent with the cited works. Not a substantive error.

- **IHDP data being artificial:** Semi-synthetic benchmarks are standard practice; the paper does not claim fully realistic instrument structure.

- **Non-binary treatments not evaluated:** The paper acknowledges this (line 172) and notes the method could be adapted. Scope-limitation, not a weakness.

- **Φ network overfitting concern:** A generic concern applicable to any neural approach; not paper-specific.

- **Missing CATE results in main text / missing standard deviations:** The paper reports significance markers (*, **) from 50 bootstrap resamples and states CATE is in appendix. This is standard practice.

- **Section-by-section formatting nitpicks and generic framing concerns.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix or remove Lemma 1.** If the unconfoundedness constraint can be justified by a different argument, provide it. Otherwise, remove the lemma and the associated claim about relaxing the X⟂U assumption.
2. **Reframe the empirical claims** to accurately reflect competitive (rather than superior) performance.
3. **Discuss explicitly the gap** between correlational constraints and causal IV conditions, and clarify when the decomposition is meaningful (e.g., under what specific assumptions).
4. **Report selected hyperparameter configurations** for reproducibility.
5. **Discuss the test-set relevance degradation** in the No Candidate setting and how the method handles it.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>