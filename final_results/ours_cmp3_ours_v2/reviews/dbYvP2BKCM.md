Now I'll write the final review.

## Summary

ZNet proposes a neural network that decomposes observed covariates X into a confounder representation C and an instrument representation Z, enabling IV-based causal effect estimation even when no pre-specified instrument exists. The method uses correlation-based and mutual-information-based loss constraints to enforce the three standard IV conditions (relevance, exclusion restriction, unconfoundedness) and is compatible with downstream IV estimators (TSLS, DeepIV, DFIV). Experiments across four data-generation classes in linear and nonlinear variants show that ZNet recovers ground-truth instruments when they exist and produces competitive ATE estimates.

## Strengths

1. **Well-motivated problem.** The difficulty of finding valid instruments in practice is genuine, and automating instrument construction from observed data would be a valuable contribution (Section 1, lines 16–23).

2. **Broad experimental coverage.** The evaluation spans 4 data-generation classes (Disjoint Candidate, Mixed Candidate, Latent Categorical Instrument, No Candidate), each with linear and nonlinear variants, using 3 downstream estimators and 3 competing IV-generation methods (AutoIV, VIV, GIV). This is the most comprehensive empirical setup in this sub-area.

3. **Ablation study confirms constraint contributions.** Figure 5c shows that removing each constraint degrades recovery of existing instruments, providing evidence that all three loss terms contribute to the learned representation.

## Weaknesses

### Major

1. **Lemma 1's proof is mathematically incorrect, undermining the theoretical justification for the unconfoundedness constraint.**

The proof (line 93) contains an invalid algebraic step. After expanding Cov(Z, e_Y − E[e_Y|X,T]), the derivation reaches:

E[Z·e_Y] − E[Z·E[e_Y|X,T]]

and then replaces E[Z·E[e_Y|X,T]] with E[Z]·E[e_Y|X,T] (which equals 0 since E[Z]=0). These two expressions are not generally equal: E[Z·E[e_Y|X,T]] is a scalar expectation, while E[Z]·E[e_Y|X,T] is a random variable depending on X,T. Since Z = g(X) is a deterministic function of X, it cannot be assumed independent of (X,T), so the substitution is unjustified. The claimed conclusion — that Cov(Z, e_Y − E[e_Y|X,T]) = 0 and Z ∼ N(0,σ²) together imply Cov(Z, e_Y) = 0 — does not follow from the algebra presented.

This matters because Constraint 1 (Instrumental Unconfoundedness, line 99) is presented as the paper's main advance over prior work that "assume[s] that unobserved confounders do not influence the observed data" (lines 386–390). The lemma is invoked to justify this constraint (lines 97, 133, 155). A corrected theoretical justification is needed, or the constraint should be reframed as a heuristic.

Even beyond the proof error, the constraint enforces Cov(Z, e_Y) = 0 — a single moment condition — which is substantially weaker than the independence (Z ⟂ U) that valid IV inference requires. The paper does not address this gap.

2. **Claimed relaxation of the U→X assumption is not empirically evaluated.**

The paper states: "Existing methods assume that unobserved confounders do not influence the observed data, while our method relaxes this assumption" (lines 386–390). However, in the data generation (Section 6.1), Y and T are constructed from functions of X plus additive errors from U, while X itself is drawn from IHDP covariates. The scenario where U directly influences X is never tested. Without empirical evaluation, this claim is unsupported.

### Minor

3. **The gap between correlation-based loss constraints and causal IV conditions is not honestly characterized.**

The paper claims "Solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument" (line 394). The loss constraints are correlation- and MI-based statistical conditions, which are necessary but not sufficient for the causal IV conditions. Satisfying Cov(C, Z) = 0 does not guarantee the exclusion restriction (no causal path from Z to Y except through T), and Cov(Z, residuals) = 0 does not guarantee Z ⟂ U. While the paper acknowledges "a lack of theoretical guarantees of identifiability in the general case" (line 394), this caveat addresses IV estimation in general rather than the specific gap between ZNet's correlation-based constraints and the causal IV assumptions.

4. **TrueIV shows anomalously large errors on Non-linear Latent without explanation.**

On the Non-linear Latent dataset (true ATE = 0.333), TrueIV with DFIV gives an ATE error of 4.762 and TrueIV with TSLS gives 1.381 (Table 1, line 359). These are far larger than ZNet's errors in the same setting (0.152 for TSLS, −0.063 for DFIV). While ZNet's own results are not invalidated by this, the anomaly suggests either a data-generation issue or a failure mode in the downstream estimators that should be discussed.

5. **No uncertainty quantification in the main ATE table.**

Table 1 reports mean ATE error across 50 bootstrap resamples but provides no confidence intervals or standard errors. The significance markers (*, **) are defined only relative to pairwise rank comparisons rather than proper statistical tests.

6. **"No Candidate (no U)" setting lacks interpretation.**

In datasets without unobserved confounding, IV methods are unnecessary. The paper presents ZNet's "comparable" performance to TARNet in this setting as a positive, but it is unclear what the learned Z captures when there is no unobserved confounding, and this setting does not demonstrate the method's value for the problem it targets.

### Trivial

7. The claim of "learning SCMs" (lines 69, 117, 394) is overstated. ZNet learns representations f(X) and g(X) that satisfy statistical constraints, not structural equations or a causal graph.

## Nice-to-Haves

- A sensitivity analysis of the 7 weighting hyperparameters (α₁–α₇), or at least reporting the selected values from Bayesian optimization.
- Runtime comparisons with baselines (AutoIV, VIV, GIV) to contextualize ZNet's three-stage training procedure.
- A formal or simulated analysis of when the loss constraints can be satisfied but the learned Z is not a valid instrument (e.g., when all observed variables affect both T and Y).

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- *"The Emergency Department example weakens the case."* — This is an opinion about pedagogical framing, not a substantive weakness.
- *"TSLS assumes independence of U and X, so results are not informative."* — TSLS is one of three downstream estimators; DeepIV does not require this assumption. The paper does not claim ZNet fixes TSLS's assumptions.
- *"ZNet does not consistently outperform baselines."* — ZNet is bolded (best) or italicized (second-best) in 15 of 24 table entries, which supports the "on average highest performing" claim.
- *Significance marker formatting nitpicks.* — These are parser artifacts, not author errors.
- *"Missing appendix content."* — The parser strips appendices; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix or remove Lemma 1.** If it cannot be repaired, present the unconfoundedness constraint as a heuristic regularization term rather than a theoretically justified condition.

2. **Test the U→X scenario.** Generate at least one dataset where U directly influences observed covariates X to support the claim of relaxing this assumption.

3. **Diagnose the TrueIV failure on Non-linear Latent** (Table 1, line 359) — either explain it as a known limitation of DFIV/TSLS in this setting or investigate the data-generation pipeline.

4. **Add confidence intervals or standard errors** to Table 1.

5. **Clarify the statistical/causal gap** explicitly: state that the loss constraints encode necessary, not sufficient, conditions for the IV assumptions.

## Score and Decision

### Calibration Anchors

All retrieved calibration papers for the query "instrumental variable learning from observed data neural network representation":

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Analyzing Complex Interdependencies in Financial Markets | nSDOkm0SKo.md | 1.00 | Bracket | Unrelated topic (financial news impact); score not usable as anchor |
| KL Divergence Optimization for Stochastic GFlowNets | Uj0h13lVrR.md | 1.00 | Bracket | Unrelated topic |
| Potential Outcomes Under Hidden Confounders | 5AJ8R4z5g0.md | 3.25 | Bracket | Related (unobserved confounders, CATE); weaker experiments, stronger theory |
| Causal Neural Networks for Continuous Treatment Effect Estimation | jFox1iMWUa.md | 3.40 | Bracket | Related (treatment effect estimation); less comprehensive experiments |
| The best of both worlds: Improved outcome prediction using causal structure learning | AvXrppAS2o.md | 3.00 | Bracket | Related (causal structure learning); different approach |
| **Adversarial Learning of Decomposed Representations (ADR)** | **F7XPZnIUHh.md** | **4.20** | **Bracket** | **Most comparable: decomposes covariates into I/C/A, has proof errors and heuristic loss → rejected** |
| Regularized DeepIV with Model Selection | 0gqCIaBRQ9.md | 5.25 | Bracket | IV theory paper; different contribution type |
| Feature Matching Intervention | 8GhwePP7vA.md | 4.25 | Bracket | Related (causal representation learning); different setup |
| Conditional IV Regression with Representation Learning | qDhq1icpO8.md | 6.75 | Narrow | Similar topic but stronger theoretical foundation → accepted |
| Catch the Shadow: Automatic Shadow Variables Generation | Oc4ji1iCjQ.md | 6.75 | Narrow | Similar approach (learning representations for causal assumptions); stronger theory, rejected despite high score |
| CFDiVAE | wFf9m4v7oC.md | 5.75 | Narrow | Front-door adjustment with VAE; different causal framework |
| Nuisance-Robust Weighting Network | TC9r8gsaoh.md | 6.00 | Narrow | Treatment effect estimation; different approach |

**Round 1 bracket:** 3.5 – 5.0

The most directly comparable anchor is the ADR paper (F7XPZnIUHh.md, avg 4.20, rejected), which also decomposed covariates into causal components, had a proof error in the theoretical derivations, and used heuristic loss functions. The ZNet paper has broader experiments than ADR and addresses an arguably more important problem (learning IVs vs. generally decomposing covariates). However, it shares the same structural weakness (an incorrect proof undermining the theoretical justification) and adds additional overclaiming issues. Papers with stronger theoretical grounding (qDhq1icpO8 at 6.75) were accepted.

**Final score:** 4.0 (borderline reject)

**Decision:** Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>