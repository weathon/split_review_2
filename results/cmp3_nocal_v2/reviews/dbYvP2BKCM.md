Now I have verified all the key claims against the paper. Let me write the final review.

---

## Summary

This paper proposes ZNet, a deep learning method that learns instrument representations from observed covariates without requiring pre-specified candidate instruments. ZNet learns two functions f(X) and g(X) to decompose the observed variables into confounder C and instrument Z components, enforced via loss terms encoding relevance, exclusion restriction, and unconfoundedness. The paper evaluates ZNet across multiple semi-synthetic data generation scenarios and demonstrates that learned instrument representations can be used with downstream IV estimators (TSLS, DeepIV, DFIV) to estimate treatment effects.

## Strengths

1. **Well-motivated problem.** The paper correctly identifies a genuine practical challenge: in many observational studies, suitable instrumental variables may not be known a priori or may not exist as explicit variables in the data. The idea of learning instrument representations from observed covariates without requiring domain experts to pre-specify candidate IVs is practically relevant and timely.

2. **Comprehensive evaluation design (Section 6.1).** The paper constructs four distinct data generation scenarios — disjoint candidate, mixed candidate, latent categorical instrument, and no candidate — that systematically cover different relationships between the observed covariates and the latent IV structure. This allows for more informative diagnosis of where and why an IV-learning method might succeed or fail than a single benchmark would. Inclusion of both linear and non-linear response surfaces and the "no unobserved confounders" ablation is appropriate.

## Weaknesses

### Major

1. **Lemma 1 proof is mathematically incorrect, undermining the theoretical justification for the unconfoundedness constraint.** Lemma 1 (line 89) claims: *If Z ~ N(0, σ²) and Cov(Z, e_Y − E[e_Y|X,T]) = 0, then Cov(Z, e_Y) = 0.* The proof at line 93 contains an algebraic error. It writes:

   ```
   E[Z · (e_Y − E[e_Y|X,T])] = E[Z · e_Y] − E[Z] · E[e_Y|X,T]
   ```

   Because E[e_Y|X,T] is a random variable (a function of X and T), the term E[Z] · E[e_Y|X,T] is itself a random variable, whereas E[Z · e_Y] is a scalar — they cannot be subtracted in this way. The correct expansion is:

   ```
   E[Z·(e_Y − E[e_Y|X,T])] = E[Z·e_Y] − E[Z·E[e_Y|X,T]]
   ```

   Working through the covariance correctly: setting Cov(Z, e_Y − E[e_Y|X,T]) = 0 yields Cov(Z, e_Y) = Cov(Z, E[e_Y|X,T]), not Cov(Z, e_Y) = 0. Since Z = g(X), the term Cov(Z, E[e_Y|X,T]) = Cov(g(X), E[e_Y|X,T]) is not generally zero under the stated premises. The lemma's conclusion does not follow from its premises as given.

   **Why this matters.** The paper's central claim to handle cases where X *is* influenced by U (Section 3, line 87: "To allow for our method to produce an instrument even more generally when X may be influenced by U") depends on this lemma. The paper states (Discussion, lines 386–387): "Existing methods assume that unobserved confounders do not influence the observed data, while our method relaxes this assumption." Without a correct proof, Constraint 1 has no theoretical grounding, and this novelty claim is unsupported. The paper should either provide a correct argument or honestly characterize the unconfoundedness enforcement as a heuristic regularization.

2. **The main evaluation metric (mean signed ATE error) is potentially misleading, and no uncertainty estimates are reported (Table 1).** Table 1 reports "Mean error on ATE" across 50 bootstrap resamples. Because the values are signed (e.g., ZNet+TSLS on "Linear No Candidate" with U gives 0.025, while on "Linear No Candidate" without U gives 2.718), positive and negative errors can cancel across bootstraps, producing a small mean even when individual estimates are far from the truth. The paper does not report standard deviations, confidence intervals, or mean absolute/squared error. The significance annotation ("* indicates that the two best are significantly better than the third best"; "** indicates that the best is significantly better than the second best") is an unusual grouped comparison; the statistical test is not named, and the reader cannot assess whether ZNet's bolded entries represent meaningful improvements or noise.

3. **Key baselines cited in related work are omitted from the experiments.** The related work (Section 4, line 113) discusses DVAE.CIV (Cheng et al., 2023) and GDIV (Chou et al., 2024) as contemporary methods in the same line of work, but they are not included as baselines in any experiment. The paper claims "the most comprehensive evaluation of IV generation for causal inference" (Discussion, line 392); omitting these methods weakens that claim and limits the reader's ability to assess ZNet against the state of the art.

### Minor

4. **Ablation measures instrument recovery, not treatment effect accuracy (Figure 5c).** The ablation study shows R² values for predicting candidate instruments from the learned Z under different loss-term removals. The paper's central claim is about improving causal effect estimation, but the ablation only tests whether the loss terms influence which latent features ZNet extracts. Without showing ATE/CATE degradation under each ablation, the necessity of each constraint for the paper's stated purpose remains untested.

5. **IV conditions are operationalized as marginal rather than conditional constraints, without acknowledgement.** Constraints 2 and 3 (lines 101–103) use marginal covariance conditions (Cov(C,Y) > 0, Cov(C,Z) = 0, Cov(Z,T) > 0) as proxies for exclusion restriction and relevance. Proper IV conditions require conditional statements (Z ⟂̸ T | C for relevance; Z ⟂ e_Y | C for unconfoundedness). While marginal proxies are a common practical concession, the gap should be acknowledged as a limitation rather than presented as a direct encoding of the IV assumptions.

6. **Confusion matrix for latent instrument recovery appears perfectly diagonal without variability metrics (Figure 4).** The paper reports a 5×5 normalized confusion matrix with all diagonal entries at 1.00 and off-diagonals at 0.00 for the linear categorical instrument dataset. While this may be plausible for well-separated clusters, no variability across random seeds or K-means restarts is reported, making it difficult to assess whether this result is representative or an artifact of the specific data generation process.

### Trivial

None.

## Nice-to-Haves

- Report absolute or squared ATE error alongside signed error, with standard deviations or confidence intervals from the 50 bootstrap resamples.
- Add pairwise significance tests (or effect sizes with error bars) rather than the grouped significance convention.
- Include DVAE.CIV and GDIV as baselines, or justify their omission.
- Extend the ablation study to measure downstream ATE accuracy under each loss-term removal.
- Acknowledge the gap between the marginal covariance conditions used in the loss functions and the proper conditional IV conditions.
- Report variability metrics (e.g., across random seeds) for the latent instrument recovery experiment.

## Removed Points

- **Criticism about the Lemma 1 error being "fatal" (categorized as fatal in the input).** The proof error is genuine and significant, but it does not invalidate the empirical results or the entire paper. The method may still work in practice even if the theoretical justification is incorrect; the paper could be reframed to treat Constraint 1 as a heuristic. Downgraded from Fatal to Major.
- **Criticism that the confusion matrix is "suspiciously perfect" (speculative tone).** The underlying point about missing variability metrics is valid and retained as Minor weakness #6. The speculation about the experiment being "not representative" or "trivial" is removed as it goes beyond what the paper shows.
- **Criticism about hyperparameter tuning using a proxy (F-statistic) rather than downstream ATE (Section-by-Section Notes).** This is a common and reasonable practice in multi-objective tuning; the downstream estimator would be expensive to optimize directly. Removed.
- **The "Strengthening the Paper on Its Own Terms" paragraph.** The concrete suggestions within it (fix the lemma, report absolute error, add CIs) are incorporated into Nice-to-Haves and the existing weakness framing. The narrative paragraph is not retained as a separate weakness.

## Novel Insights

None beyond the paper's own contributions. The main novel finding from the cross-review is the identification of the algebraic error in Lemma 1's proof, which was not noted by the authors and undermines a central theoretical claim, suggesting the paper's strongest contribution may be empirical rather than theoretical.

## Suggestions

1. Carefully re-examine Lemma 1. If it can be correctly proved under additional assumptions, state those assumptions explicitly and provide a correct proof. If not, remove or reframe the unconfoundedness constraint as a heuristic regularization and remove the claim about handling U→X cases without additional assumptions.
2. Report absolute or squared ATE error with standard deviations or confidence intervals from the 50 bootstrap resamples in Table 1.
3. Add DVAE.CIV and GDIV as experimental baselines, or clearly justify their omission.
4. Extend the ablation study to measure downstream ATE accuracy when each constraint is removed.
5. Acknowledge that the loss functions operationalize marginal rather than conditional IV conditions, and discuss how this gap might affect validity.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>