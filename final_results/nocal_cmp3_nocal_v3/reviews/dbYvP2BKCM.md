## Summary

This paper proposes ZNet, a deep learning architecture that learns instrumental variable (IV) representations from observed covariates X by decomposing them into a confounder component C = f(X) and an instrument component Z = g(X). The method enforces three IV conditions — relevance, exclusion restriction, and unconfoundedness — through covariance-based loss terms and is compatible with standard downstream IV estimators (TSLS, DeepIV, DFIV). The paper evaluates on semi-synthetic data derived from the IHDP benchmark across multiple data-generating scenarios.

## Strengths

1. **Ambitious and well-motivated problem.** Automatically constructing IV representations from observed data without requiring domain expertise to identify instruments is a genuinely important and difficult problem. The paper's framing is clear and compelling (lines 9, 23, 67-68).

2. **Comprehensive experimental scope.** The evaluation spans four data classes (Disjoint Candidate, Mixed Candidate, Latent Categorical, No Candidate), two functional forms (linear/non-linear), and three downstream estimators (TSLS, DeepIV, DFIV), with both the presence and absence of unobserved confounding. This breadth is notable for an IV representation learning paper.

3. **Well-chosen baseline set.** The comparison includes TrueIV, TARNet, AutoIV, VIV, and GIV, covering the relevant competing paradigms (candidate-selection methods, variational methods, and clustering-based methods). The ablation study in Figure 5(c), showing degradation when individual constraints are removed, provides useful diagnostic evidence.

## Weaknesses

### Major

1. **The unconfoundedness constraint (Constraint 1) is theoretically vacuous — it targets a quantity that is identically zero for any Z = g(X) in population, regardless of whether Z is a valid instrument.**

   The paper proposes to enforce unconfoundedness by minimizing the covariance between the learned instrument Z = g(X) and the residuals Y − Ŷ from a model Φ that predicts Y from X and T (lines 97, 133-141). The argument proceeds via Lemma 1: if Cov(Z, e_Y − 𝔼[e_Y|X,T]) = 0 and Z ~ N(0,σ²), then Cov(Z, e_Y) = 0. The loss then minimizes PC(Y−Ŷ, Z)².

   However, for any Z that is a deterministic function of X — which Z = g(X) is by construction — we have:

   Cov(Z, e_Y − 𝔼[e_Y|X,T]) = 𝔼[Z·(e_Y − 𝔼[e_Y|X,T])]  
   = 𝔼[g(X)·𝔼[(e_Y − 𝔼[e_Y|X,T]) | X,T]] = 𝔼[g(X)·0] = 0

   The population target is zero for **any** Z = g(X), irrespective of whether Z is correlated with the unobserved confounders U or the error term e_Y. The loss term therefore imposes no meaningful constraint on Z. In finite samples with an imperfectly learned Φ, the sample covariance will not be exactly zero, but the population target toward which the loss drives is zero by construction.

   This means the paper's central claimed advantage — that ZNet "relaxes" the assumption that unobserved confounders do not influence the observed data (lines 86-87, 386-390, and the abstract's claim of applicability "regardless of whether the (untestable) assumption of unconfoundedness is satisfied") — has **no theoretical basis** in the proposed machinery. The method may still produce useful representations via the other constraints, but not through the mechanism claimed.

2. **Lemma 1's proof contains a mathematical error.**

   The proof in lines 91-95 writes:

   𝔼[Z·(e_Y − 𝔼[e_Y|X,T])] = 𝔼[Z·e_Y] − 𝔼[Z]·𝔼[e_Y|X,T]

   The term 𝔼[e_Y|X,T] is a random variable (a function of X and T), not a constant. The expression 𝔼[Z]·𝔼[e_Y|X,T] is itself a random variable and cannot appear inside an unconditional expectation operator as a separate term from the expectation. The correct expansion would be:

   𝔼[Z·(e_Y − 𝔼[e_Y|X,T])] = 𝔼[Z·e_Y] − 𝔼[Z·𝔼[e_Y|X,T]]

   The lemma's conclusion does not follow from the presented algebra. (As a separate matter, the paper later depends on Lemma 1 to motivate the normality requirement on Z, so this proof error cascades into the justification of the KL loss on Z at line 155.)

3. **Covariance constraints are strictly weaker than the conditional independence conditions required for IV validity; the gap is unaddressed.**

   The paper replaces three conditional independence conditions (lines 37-41) with marginal covariance constraints (lines 99-103):

   | Required IV condition | ZNet constraint |
   |---|---|
   | Z ⟂̸ T \| C (relevance) | Cov(T, Z) > 0 |
   | Z ⟂ Y \| C, T (exclusion restriction) | Cov(C, Y) > 0, Cov(C, Z) = 0 |
   | Z ⟂ e_Y \| C (unconfoundedness) | Cov(Z, e_Y) = 0 (vacuous — see above) |

   Covariance is a second-order marginal statistic; the IV conditions require conditional independence, which is strictly stronger. A variable can be uncorrelated with another yet depend on it conditional on a third variable. The paper mentions a mutual-information (MI) variant (line 131) that could in principle capture non-linear dependencies, but provides no separate evaluation of the MI variant versus the PC variant, so it is unclear whether the MI loss is ever used or whether it bridges the gap.

4. **ATE evaluation is presented without variance estimates, and the results are mixed.**

   Table 1 reports mean ATE errors across 50 bootstrap resamples but provides **no standard errors, confidence intervals, or any other measure of variability** for these estimates. Without variance information, it is impossible to assess whether observed differences between methods are meaningful relative to sampling variability, especially on a dataset of 985 samples.

   The results themselves are mixed: ZNet is sometimes the best method (e.g., Non-linear No Candidate, ZNet+DFIV: 0.049), sometimes substantially worse (e.g., Linear No Candidate (no U), ZNet+TSLS: 2.718), and often comparable to competitors. The significance notation (comparing the top two methods against each other, not against ground truth) is non-standard and uninformative about absolute accuracy — a method can be marked best (**) while having an ATE error of 0.437 (ZNet+TSLS on Linear Mixed).

### Minor

5. **The MI variant of the loss is mentioned but never separately evaluated or compared to the PC variant.** Since the paper explicitly flags linearity as a limitation of covariance-based constraints (line 131), evaluating whether the MI version improves performance — and reporting when each variant is selected by hyperparameter tuning — is important for the reader to assess the method's effectiveness beyond linear settings. As it stands, it is unclear whether the MI variant provides any benefit.

6. **The paper contains strong overclaims.** The discussion states: "Solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument since IV constraints are explicitly embedded in the loss function" (lines 393-394). Given that one of the three constraints is vacuous (Weakness 1) and the others are necessary but not sufficient for IV validity (Weakness 3), this statement is not supported. Similarly, the abstract claims the method works "regardless of whether the (untestable) assumption of unconfoundedness is satisfied" — but the mechanism purported to enable this is defective.

## Nice-to-Haves

- **Connect diagnostic metrics to downstream performance.** The paper reports F-statistics, C-Z correlations, and correlations with U as independent diagnostics (Section 6.2) but does not establish whether these metrics predict ATE/CATE accuracy. Showing this relationship would substantially strengthen the evaluation.
- **Report confidence intervals for ATE estimates.** The bootstrap procedure (50 resamples) naturally provides variance information; reporting it would allow readers to assess the reliability of observed differences.
- **Clarify the perfect confusion matrix in Figure 4.** A 5×5 confusion matrix with all 1.0 on the diagonal is unusual for real-data-derived covariates. If this is the average over multiple runs, the variance matters; if it is a single well-performing run, that should be stated. Some discussion of robustness would be helpful.
- **Acknowledge the gap between covariance and conditional independence** explicitly as a limitation, rather than presenting the constraints as equivalent to the IV conditions.

## Removed Points

- **"Hyperparameter tuning inflates performance"** — The tuning optimizes diagnostic metrics (F-statistic, C-Z correlation), not the final ATE evaluation, and similar tuning was applied to baselines. While not ideal, this is standard practice and the concern is not strong enough to retain as a separate weakness.
- **"Missing confidence intervals / standard errors"** — Already covered as part of Weakness 4 (merged).
- **"Disconnected evaluation metrics"** — Moved to Nice-to-Haves.
- **"Distinction between ZNet and variational methods is overstated"** — The reviewer's point conflates a claim in the related work section with the paper's own limitations. The claim about variational methods "lacking theory" (line 113) is a statement about those works, not about ZNet's guarantees; it does not directly bear on ZNet's validity.
- **"Section 2 defines IV conditions conditional on C, but constraints drop the conditioning"** — The constraints (lines 99-103) are stated as marginal conditions, and the paper's goal is to learn Z such that conditioning on C is unnecessary (line 43). This mismatch is acknowledged in the footnoted text. The criticism is too minor to retain.
- **Pure formatting/style nitpicks and grammar issues** — Removed per instructions (parser artifacts).

## Novel Insights

None beyond the paper's own contributions. The reviews raise a significant theoretical concern (the vacuity of the unconfoundedness constraint) that the paper itself does not address or acknowledge. The other criticisms (covariance vs. conditional independence, missing variance estimates) are standard evaluation concerns that do not introduce fundamentally new observations about the method.

## Suggestions

1. **Drop or substantially revise the claim about handling settings where X is influenced by U.** The current mechanism (Constraint 1 via Lemma 1) does not provide a meaningful constraint. The paper should be honest about what the method actually enforces and where it operates within the standard assumptions.

2. **Fix the proof of Lemma 1 or remove it.** If the lemma is to be retained, provide a correct proof or replace it with a proper mathematical argument that establishes the intended relationship.

3. **Provide confidence intervals / standard errors for all ATE estimates in Table 1.** The bootstrap procedure already generates this information; reporting it is essential for the reader to assess reliability.

4. **Evaluate the MI variant separately** and clarify when it is selected over the PC variant during hyperparameter tuning. This directly addresses the concern about whether the method works beyond linear settings.

5. **Acknowledge the theoretical gap** between marginal covariance constraints and conditional independence as an explicit limitation, and discuss what kinds of violations would cause the covariance-based conditions to be insufficient.

## Score and Decision

The paper tackles an important problem and provides a broad empirical evaluation. However, the central theoretical mechanism for handling unobserved confounders' influence on X — which is the paper's claimed advance over prior methods — is mathematically vacuous: the unconfoundedness constraint targets a quantity that is identically zero in population for any possible learned Z. The proof it depends on contains a mathematical error. The remaining two constraints (relevance, exclusion restriction) are covariance-based and strictly weaker than the conditional independence conditions they replace, with no argument that the gap is bridged. The empirical results are mixed and reported without variance estimates.

The paper cannot be accepted in its current form because its core claimed contribution (learning valid IV representations that handle settings where X is influenced by U) is unsupported. A substantially revised version that removes the invalid theoretical claims, addresses the proof error, and provides a frank assessment of what the method actually guarantees would be a different paper requiring re-review.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>