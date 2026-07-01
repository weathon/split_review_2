Now I'll write the final consolidated review.

## Summary

This paper proposes ZNet, a deep learning method that decomposes observed covariates X into a confounder representation C = f(X) and an instrument representation Z = g(X), enforcing the standard IV assumptions (relevance, exclusion restriction, unconfoundedness) through a multi-part loss function. The key claimed advance over prior IV-generation methods is that ZNet "relaxes" the assumption that unobserved confounders U do not influence the observed covariates X. Experiments across four data-generation settings (Disjoint, Mixed, Latent, No Candidate) with linear/non-linear structural equations show competitive ATE estimation, particularly in the challenging "No Candidate with Unobserved Confounding" setting.

## Strengths

1. **Comprehensive experimental design.** The evaluation covers four data-generation settings crossed with linear/non-linear structural equations, with and without unobserved confounding, and reports results across multiple downstream estimators (TSLS, DeepIV, DFIV) with bootstrapped significance indicators (Table 1). This is more thorough than most prior work in this area.

2. **Competitive empirical performance in the "No Candidate" setting.** In the most practically relevant setting — where no instrument exists among observed variables and unobserved confounding is present — ZNet delivers the best or second-best ATE error across multiple downstream estimators. For example, on Non-linear No Candidate (with U): ZNet achieves ATE errors of 0.260** (DeepIV) and 0.049** (DFIV), both best among all IV-generation methods (Table 1, lines 374–378).

3. **Architecture that encodes the SCM of IVs.** The idea of partitioning X into C and Z through separate networks f and g with structurally enforced constraints is well-motivated and provides transparency compared to black-box variational approaches. The three-stage training procedure and use of gradient surgery for conflicting loss terms are sensible engineering choices.

4. **Demonstrated instrument recovery.** When true instruments exist (Disjoint, Mixed, Latent settings), ZNet demonstrably recovers representations correlated with them, as shown in Figures 4, 5(a,b) and the ablation study in Figure 5(c).

## Weaknesses

### Major

1. **Lemma 1 is mathematically incorrect, undermining the paper's central differentiating claim.** Lemma 1 (line 89) and its proof (lines 91–93) contain a fundamental mathematical error. The proof writes:

   ```
   E[Z·(e_Y - E[e_Y|X,T])] = E[Z·e_Y] - E[Z]·E[e_Y|X,T]
   ```

   This step incorrectly replaces E[Z·E[e_Y|X,T]] with E[Z]·E[e_Y|X,T]. The expression E[Z]·E[e_Y|X,T] is a random variable (not a scalar expectation), making the algebra incoherent. The correct expansion would be E[Z·e_Y] - E[Z·E[e_Y|X,T]].

   More critically, even setting the proof error aside, when Z = g(X) (as it always is in ZNet), the lemma's premise Cov(Z, e_Y - E[e_Y|X,T]) = 0 is **identically satisfied** for any g(X), regardless of whether Cov(Z, e_Y) = 0. This is because:
   
   Cov(g(X), E[e_Y|X,T]) = E[g(X)·E[e_Y|X,T]] - E[g(X)]·E[e_Y] = E[g(X)·e_Y] - E[g(X)]·E[e_Y] = Cov(g(X), e_Y)
   
   Hence Cov(Z, e_Y - E[e_Y|X,T]) = Cov(g(X), e_Y) - Cov(g(X), e_Y) = 0 identically. The premise imposes no restriction, and the conclusion (Cov(Z, e_Y) = 0) does not follow from it.

   **Why it matters:** The paper's signature claim — that ZNet "relaxes" the assumption that U does not influence X (abstract, lines 386–390) — is justified entirely through Lemma 1. Lines 97–98 state: "Lemma 1 suggests how to construct a loss term which enforces unconfoundedness." Line 133: "To enforce unconfoundedness, we leverage Lemma 1." Since Lemma 1 provides no valid mechanism for enforcing unconfoundedness, this claim is unsupported. Without it, ZNet operates under the same assumptions as prior IV-generation methods.

2. **The unconfoundedness loss L_{Z↔ϵ_Y}^{PC} does not enforce what it claims.** As shown above, when Z = g(X), the population covariance Cov(Z, e_Y - E[e_Y|X,T]) is identically zero. The loss PC(Y-Ŷ, Z)² (Equation 6) therefore minimizes an empirical quantity that is zero in population regardless of whether Z is correlated with e_Y. The claim that "As L_{Z↔ϵ_Y}^{PC} approaches 0, satisfaction of Constraint 1 and thereby instrumental unconfoundedness is reached" (line 141) is not supported by the mathematics.

### Minor

3. **The ablation study does not test the most important use case.** Figure 5(c) ablates each constraint and measures instrument recovery (R² for predicting true instruments) — but only on the "Mixed Candidate" dataset where instruments actually exist. The more informative ablation would measure ATE error when each constraint is removed in the "No Candidate with U" setting, which is where ZNet's claimed advantage matters most. Without this, it is unclear which loss terms drive performance in the paper's key use case.

4. **No confidence intervals for ATE estimates.** Table 1 reports point estimates with significance stars ("two best are significantly better than third best") but no standard errors or confidence intervals. For a causal estimation paper, uncertainty quantification around each ATE estimate would help readers judge whether differences between methods are meaningful, especially given the moderate sample sizes (IHDP has 985 individuals).

5. **Hyperparameter tuning procedures across methods are not fully comparable.** The tuning procedure for ZNet uses Bayesian optimization to maximize F-statistic and minimize C-Z correlation (line 165), while downstream estimators are tuned to minimize NN ATE MSE. It is not reported whether the same tuning budget, search space, and procedure were used for all baselines. Since the tuning of baselines (AutoIV, GIV, VIV) could significantly affect performance, this is a gap in the experimental reporting.

### Trivial

6. The correlation between U and Z in Figure 6(c) is reported as 0.126 on the test set. No baseline comparison is provided (e.g., what would AutoIV's U-Z correlation be?), making it hard to interpret whether this value is small or large relative to alternatives.

## Nice-to-Haves

- An ablation showing ATE error in the "No Candidate with U" setting when the unconfoundedness loss is removed would directly test whether this constraint adds value empirically, even if the theory is flawed.
- Reporting CATE metrics (e.g., PEHE) in the main text rather than only in the appendix would strengthen the evaluation.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Lemma 1 is mathematically incorrect (structural flaw) — this invalidates the paper's core claims" (from harsh critic):** Kept as Major weakness 1, but downgraded from "fatal/structural" to "major" because the empirical contributions stand independently even if the theoretical claim is flawed.
- **"The method does not guarantee a valid instrument (methodological gap)" (from harsh critic):** This point about Z potentially inheriting correlation with U through X is a known limitation shared with all IV-generation methods. It is acknowledged in the paper (line 85) and does not uniquely harm ZNet. Removed as it is a generic limitation of the approach, not a specific weakness.
- **"Comparisons with TrueIV are interpretable only in Disjoint and Mixed settings" (from harsh critic):** The paper correctly marks TrueIV as unavailable ("–") when no true instrument exists. This is appropriate reporting, not a weakness.
- **"No analysis of variance or confidence intervals" (from harsh critic):** Downgraded to Minor — bootstrapped significance indicators are standard in ML causal inference papers.
- **"No evaluation of CATE estimation quality in main text" (from harsh critic):** The paper notes CATE results are in the appendix. Given space constraints, this is acceptable.
- **"The three-stage training introduces sequential dependencies" (from harsh critic):** This is standard practice in multi-stage training and not a weakness specific to this paper.
- **Strengths removed as generic/superficial:** "A practically important problem" — the importance of the problem is generic and not specific to this paper's contributions.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis identifies a genuine mathematical error in Lemma 1 that the paper's own review process should have caught, but this is a flaw in the paper rather than a novel insight generated by the reviews. The observation that Cov(Z, e_Y - E[e_Y|X,T]) = 0 identically when Z = g(X) reveals a structural gap in the paper's theoretical claims that is worth noting for the authors' revision.

## Suggestions

1. **Fix or remove Lemma 1.** Either provide a correct theoretical justification for why minimizing Cov(Z, Y-Ŷ) helps enforce unconfoundedness, or explicitly drop the claim about relaxing the assumption that U does not influence X. If the method works empirically without this justification, state this honestly rather than relying on an incorrect lemma.

2. **Run the ablation study on "No Candidate with U."** The most informative test of whether the unconfoundedness constraint adds value is to measure ATE error with and without L_{Z↔ϵ_Y}^{PC} in the setting where there are no candidate instruments and U influences X.

3. **Report standard errors or confidence intervals** for the ATE estimates in Table 1 to allow readers to assess the significance of differences between methods.

4. **Calibrate the paper's claims** to match what is actually supported. The empirical results are promising and speak for themselves — the paper does not need to overclaim theoretical guarantees to be a valuable contribution.

## Score and Decision

<score>3</score>
<decision>Reject</decision>