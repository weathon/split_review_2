## Summary

The paper proposes ZNet, a deep learning method that decomposes observed covariates $X$ into confounder $C = f(X)$ and instrument $Z = g(X)$ representations through a multi-objective loss function designed to enforce the three IV assumptions (relevance, exclusion restriction, unconfoundedness). The learned $(C, Z)$ can then be plugged into standard downstream IV estimators (TSLS, DeepIV, DFIV). The evaluation covers eight semi-synthetic data configurations with thorough instrument-recovery visualizations.

## Strengths

1. **Comprehensive evaluation design.** The paper constructs eight semi-synthetic configurations crossing (linear/non-linear) × (disjoint/mixed/latent/no-candidate instrument settings), with and without unobserved confounding. This is genuinely broader than most prior IV-generation papers and is a real contribution to the evaluation infrastructure for this area.

2. **Demonstrated recovery of known instruments.** Figure 5c shows that when ground-truth instruments exist (Linear Mixed Candidate), ZNet's learned Z predicts them with moderate $R^2$ (~0.3–0.5), and ablating individual constraints degrades this recovery. The confusion matrix in Figure 4 showing near-perfect recovery of a 5-cluster latent categorical instrument is also convincing.

3. **Modular architecture.** ZNet outputs $(C, Z)$ can be plugged into multiple downstream IV estimators (TSLS, DeepIV, DFIV). This is architecturally clean and practically useful.

## Weaknesses

### Major

1. **The unconfoundedness constraint (Constraint 1 via Lemma 1) is theoretically vacuous when $Z = g(X)$.**  
   The paper introduces Lemma 1 and a loss term $L_{Z \not\leftrightarrow \epsilon_Y}^{PC}$ that minimizes $\text{Cov}(Y - \hat{Y}, Z)^2$, intended to enforce $\text{Cov}(Z, e_Y) = 0$. However, since $Z = g(X)$ is a deterministic function of $X$, $Z$ is $\sigma(X)$-measurable. For any such $Z$,  
   $$\mathbb{E}[Z \cdot e_Y] = \mathbb{E}[\mathbb{E}[Z \cdot e_Y \mid X, T]] = \mathbb{E}[Z \cdot \mathbb{E}[e_Y \mid X, T]],$$  
   which implies $\text{Cov}(Z, e_Y - \mathbb{E}[e_Y|X,T]) = 0$ identically — the condition in Lemma 1 is automatically true for any $Z = g(X)$ regardless of whether $Z$ is actually independent of $e_Y$. The loss term therefore does not constrain the learned representation in any meaningful way toward unconfoundedness. Consequently, the paper's central differentiating claim — *"Existing methods assume that unobserved confounders do not influence the observed data, while our method relaxes this assumption"* (Discussion, lines 386–390) — is not theoretically supported. Figure 6c confirms this empirically: the average absolute $U$-$Z$ correlation in the No Candidate setting is ~0.1–0.13, not zero.

### Minor

2. **Table 1 reports only mean bias without variance information.**  
   Mean error on ATE across 50 bootstrap resamples is reported, but no standard errors, confidence intervals, or RMSE are given. Bias alone can be misleading (cancelling positive and negative errors), and the star annotations ($*$, $**$) for significance are explained only briefly with no specific statistical test described. Without variance information, the reader cannot assess whether ZNet's apparent advantages over baselines in many cells are statistically meaningful.

3. **The $(C, Z)$ decomposition is not identifiable under the proposed moment conditions.**  
   Constraints 2 and 3 ($\text{Cov}(C,Y)>0$, $\text{Cov}(C,Z)=0$, $\text{Cov}(T,Z)>0$) are moment conditions that infinitely many pairs $(f,g)$ can satisfy (e.g., any rotation preserving decorrelation). Different valid decompositions may yield different downstream causal estimates. The paper acknowledges this general limitation of IV estimation in the Discussion but does not address its specific implications for the proposed method.

4. **The tuning procedure may disadvantage baselines.**  
   All IV generation methods (ZNet, AutoIV, GIV, VIV) are tuned with Bayesian optimization on a multi-objective criterion designed for ZNet (maximize relevance F-statistic, minimize $C$-$Z$ correlation). This criterion may not align with the inductive biases of variational methods (AutoIV, VIV, GIV), which were developed with different objectives. A fairer comparison would use each method's recommended tuning procedure or include a version tuned on downstream ATE error directly.

### Trivial

5. **The proof of Lemma 1 contains a mathematical error.**  
   The step from $\mathbb{E}[Z \cdot (e_Y - \mathbb{E}[e_Y|X,T])]$ to $\mathbb{E}[Z \cdot e_Y] - \mathbb{E}[Z] \cdot \mathbb{E}[e_Y|X,T]$ is incorrect ($\mathbb{E}[e_Y|X,T]$ is a random variable, not a constant). The correct intermediate is $\mathbb{E}[Z \cdot e_Y] - \mathbb{E}[Z \cdot \mathbb{E}[e_Y|X,T]]$.

## Nice-to-Haves

- Report RMSE or MAE with bootstrap confidence intervals alongside mean bias in Table 1.
- Add a "random $Z$" sanity-check baseline for downstream IV estimation to verify that ZNet's $Z$ adds value beyond random noise.
- Include hyperparameter sensitivity analysis for the 7+ loss coefficients and architecture choices.
- Run at least one continuous-treatment experiment to substantiate the claim that ZNet "could easily be adapted for continuous settings."

## Removed Points

- *Criticism about the emergency department example requiring a large leap.* This is a pedagogical motivating example; the paper makes no claim that it validates the method.
- *Criticism about TARNet comparison being apples-to-oranges.* The paper explicitly states TARNet is "used in the absence of an IV" and it is standard practice to include a no-IV baseline even when it is expected to fail under confounding.
- *Criticism about missing description for assigning IHDP covariates to causal roles.* This detail may plausibly appear in the appendix (which was stripped by the parser).
- *Criticism about "moderate R²" (~0.3-0.5) being overstated.* The paper's language ("highly correlated") is somewhat strong, but this is a minor presentational issue that does not affect the core claims.
- *Several generic presentation and formatting nitpicks.* These are parser artifacts or matters of style that do not affect the paper's substance.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis reveals that the unconfoundedness constraint — the mechanism by which the paper claims to relax the $U \not\rightarrow X$ assumption — is theoretically vacuous, which is a genuinely novel observation not discussed in the paper itself. No other synthetic insights emerge from combining the reviews.

## Suggestions

The single highest-leverage revision would be to **drop or honestly scope the claim about relaxing the $U \rightarrow X$ assumption.** Option (a): explicitly state that the method assumes $U \not\rightarrow X$ (matching prior work), removing the theoretical pretense of the unconfoundedness constraint, and reposition ZNet as a method focused on recovering instrument and confounder representations under standard IV assumptions. Option (b): develop a genuinely non-vacuous identification strategy for unconfoundedness when $U \rightarrow X$, though this is a fundamentally hard problem. Under option (a), the instrument recovery results (Figures 4, 5) and the comprehensive evaluation would still stand as meaningful contributions.

Additionally, report standard errors or confidence intervals for ATE estimates in Table 1 to allow statistical comparison.

## Score and Decision

**Calibration:** I compared the paper against several anchors from the review corpus. **qDhq1icpO8** (avg 6.75, "Conditional Instrumental Variable Regression with Representation Learning for Causal Inference") is a paper on a closely related topic that was accepted; it has theoretical soundness proofs that the current paper lacks, and its scores (5,8,6,8) reflect a clearly stronger theoretical foundation. **F7XPZnIUHh** (avg 4.20, "Adversarial Learning of Decomposed Representations for Treatment Effect Estimation") is a rejected paper on representation decomposition for causal inference that also suffered from identifiable theoretical errors; the current paper has a more comprehensive evaluation and more novel architecture, placing it above that paper. **Oc4ji1iCjQ** (avg 6.75, "Catch the Shadow: Automatic Shadow Variables Generation") is a related paper on automatic variable generation for causal inference that was rejected despite its 6.75 average (scores: 6,8,8,5); it had a cleaner theoretical contribution than the current paper.

**Round 1 bracket:** After inspecting these anchors, the plausible score range for this paper is between 3.5 and 5.5. The paper has genuine empirical contributions (instrument recovery, comprehensive evaluation) but a significant theoretical flaw that makes it weaker than accepted papers on similar topics.

**Final score:** 4.5. This reflects a paper with meaningful empirical contributions that is held back by a structural theoretical issue — the unconfoundedness constraint does not work as claimed — which undermines its central differentiating proposition. The instrument recovery results and evaluation design are strengths, but the paper overclaims relative to what its method actually guarantees.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>