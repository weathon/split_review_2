Now I have all the information needed. Let me write the final consolidated review.

## Summary

The paper proposes ZNet, a deep learning architecture that decomposes observed covariates X into confounder (C) and instrument (Z) representations without requiring a priori candidate instruments. By encoding three IV constraints (relevance, exclusion restriction, unconfoundedness) into a multi-part loss function, ZNet produces representations that can be plugged into standard IV estimators (TSLS, DeepIV, DFIV). The paper evaluates on semi-synthetic IHDP data across four instrument-availability scenarios.

## Strengths

1. **Systematic evaluation across four instrument-availability classes (Disjoint, Mixed, Latent, No Candidate).** The paper defines realistic scenarios that span the spectrum from easy (a clean instrument exists) to hard (no individual variable satisfies the IV conditions). This design covers settings where prior methods like sisVIVE, Ivy, and TEDVAE would fail because they require pre-specified candidate variables.

2. **Ablation study (Figure 5c) cleanly isolates the contribution of each constraint.** Removing Constraint 1 (Unconfoundedness) drops instrument-recovery R² from 0.84 to 0.19–0.30; removing Constraint 2 (Exclusion Restriction) drops it to 0.36–0.39; removing Constraint 3 (Relevance) drops it to 0.31–0.33; removing all constraints drops it to 0.02–0.05. This confirms non-redundancy of the loss terms.

3. **Compatibility with three downstream IV estimators (TSLS, DeepIV, DFIV).** The learned {C, Z} representations work as drop-in replacements for the instrument in both linear and neural-network-based second-stage regressions, supporting the claim of a general-purpose plug-in module.

4. **Competitive ATE estimation results.** ZNet achieves best or second-best ATE error in 14 out of 24 estimator-method cells in Table 1 across 8 data scenarios, often approaching the performance of the ground-truth instrument (TrueIV).

## Weaknesses

### Fatal
None.

### Major

1. **Lemma 1's proof is mathematically invalid, which undermines the paper's central claim of relaxing the standard assumption that U does not influence X.** The proof (lines 91–94) attempts to show that Cov(Z, e_Y − 𝔼[e_Y|X,T]) = 0 and Z ~ 𝒩(0, σ²) implies Cov(Z, e_Y) = 0. The critical step replaces 𝔼[Z·𝔼[e_Y|X,T]] with 𝔼[Z]·𝔼[e_Y|X,T]. This is algebraically incorrect: 𝔼[e_Y|X,T] is a random variable (function of X,T), while 𝔼[Z]·𝔼[e_Y|X,T] is also a random variable, but 𝔼[Z·𝔼[e_Y|X,T]] is a scalar — the equation mixes objects of different types. The correct expansion is Cov(Z, e_Y − 𝔼[e_Y|X,T]) = Cov(Z, e_Y) − Cov(Z, 𝔼[e_Y|X,T]). Setting this to zero gives Cov(Z, e_Y) = Cov(Z, 𝔼[e_Y|X,T]), which is not generally zero. The paper explicitly states (line 87) that Lemma 1 is what enables the method to work "when X may be influenced by U" — i.e., the paper's stated advance over prior work hinges on this lemma. Without a correct proof, the claim to have "relaxed" the U→X assumption is unsubstantiated.

2. **Gap between correlation-based loss constraints and the actual IV conditions they are supposed to enforce.** Constraint 2 (Exclusion Restriction) is encoded as Cov(C,Y) > 0 and Cov(Z,C) = 0, but the exclusion restriction requires Z ⟂ Y | C, T — a conditional independence condition far stronger than zero covariance between Z and C. Z could influence Y through a nonlinear pathway invisible to Pearson correlation, and the MI variant (line 131) is presented only as a tunable alternative, not as a theoretically grounded solution. Constraint 3 (Relevance) is encoded as Cov(T,Z) > 0, but relevance requires Z ⟂̸ T | C, not marginal correlation. The paper does not establish that satisfying these correlation constraints is sufficient for the IV conditions under stated assumptions.

3. **Overclaim in the "No Candidate" setting.** The paper states (line 194) that ZNet "generates an instrument representation that is correlated with T, independent of the confounder representation C, independent of the error in predicting Y, and unconfounded by U" even in settings where, by construction (line 178), no subset of X satisfies the IV conditions. The empirical checks in Figure 6 provide suggestive evidence (F-statistics, correlation magnitudes), but the paper provides no theoretical justification that a valid instrument can be constructed from purely confounded observed data. The claim on line 394 that "Solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument" overstates what the loss functions guarantee — they enforce correlational proxies, not the IV conditions themselves.

### Minor

1. **The "NN ATE" used as a tuning target (line 165) is not defined in the main text.** The hyperparameter tuning for causal inference methods minimizes MSE against a "nearest-neighbors (NN) ATE," but it is unclear what this estimator is and whether it is a reasonable surrogate for the true ATE during tuning. If the NN ATE is itself biased, the tuning process could select parameters that minimize error against a biased target rather than recovering the true effect.

2. **The KDE-based MI approximation (line 131) lacks specification details.** Bandwidth selection, kernel choice, and computational scaling with dimensionality are not discussed. Since Z can be 10-dimensional, KDE-based MI estimation is known to scale poorly, and the paper does not address whether this affects training stability or quality.

3. **The significance notation in Table 1 is unconventional and does not address the quantity of interest.** One star indicates the two best methods are significantly better than the third; two stars indicate the best is better than the second. These markers do not test whether any method's ATE estimate is significantly different from the *true* ATE, which is the central question for causal inference. Confidence intervals around each ATE estimate would be more informative, especially given the high variance visible across methods and settings.

4. **The "ZNet Val" column in Figure 5c shows 0.84 for every ablation row**, making the table layout ambiguous — it is unclear whether these are repeated validation values from the full model or values from different conditions.

### Trivial
None.

## Nice-to-Haves

- Clarify how the dimensionality of Z and C is chosen and how sensitive results are to this choice.
- Provide a discussion of regularization, given the model parameter count relative to the IHDP sample size (985 units, 25 covariates, 10 Z dimensions, learned C representation).
- Specify the hypothesis test used for the significance stars in Table 1.

## Removed Points

- "Criticism that ZNet does not 'learn the SCM'": The paper explicitly states it learns structural equations via neural networks (line 69); this framing is standard and appropriate.
- "Suspicious perfect diagonal in confusion matrix": After K-Means with cluster relabeling on well-separated latent classes, a perfect diagonal is entirely plausible and not suspicious.
- "Missing related work": I cannot confirm the existence or absence of related work without external sources, per the guidelines.
- "Formatting/notation nitpicks about L_{Z→Y}^{PC} vs L_{Z↔ε_Y}^{PC}": Could be a parser artifact.
- "Criticism about missing appendix content": The parser strips appendix content; these exist in the original submission.
- "Missing hyperparameters/disclosure of implementation details": The paper provides architecture details and a tuning procedure; routine implementation details are not required for reproducibility at this stage.

## Novel Insights

The interplay between the harsh critic's discovery of the Lemma 1 proof error and the strength finder's emphasis on the ablation study reveals an interesting tension: the method's empirical success (verified by ablation) is not backed by the theoretical justification the paper claims for itself. The constraints that demonstrably help in the experiments might be working for reasons other than those stated — for example, Cov(Z, Y−Ŷ) = 0 might be a useful regularization objective even if Lemma 1's derivation is incorrect. This suggests the paper could be strengthened by reframing the constraints as empirically motivated regularizers rather than theoretically grounded guarantees, which would be a more honest and still valuable contribution.

## Suggestions

1. **Fix or remove Lemma 1.** If a corrected proof exists with additional assumptions, provide it. Otherwise, honestly reframe Constraint 1 as a heuristic regularizer (supported by ablation evidence) rather than a theoretically grounded guarantee. The paper's central claim about relaxing the U→X assumption cannot stand without a valid theoretical argument.

2. **Tighten the connection between loss constraints and IV conditions.** Acknowledge explicitly that the Pearson-correlation-based constraints are proxies, not guarantees, for the conditional independence conditions required by IV theory. If the MI variant can guarantee independence under some conditions, state those conditions.

3. **Replace the unconventional significance markers with confidence intervals** for each ATE estimate, or at minimum test each estimate against the true ATE.

4. **Define the NN ATE estimator** used during hyperparameter tuning and discuss whether this could introduce bias.

5. **Provide details on the KDE-based MI approximation** (bandwidth selection, kernel, computational scaling).

## Score and Decision

I will assign score 4 (borderline reject) and decision Reject.

**Reasoning:** The paper addresses an important problem and presents a well-designed evaluation framework. However, the mathematical error in Lemma 1's proof — the very result that is supposed to justify the paper's claimed advance over prior work (relaxing the U→X assumption) — is a verifiable mistake that undermines the core theoretical contribution. The gap between the correlation-based constraints and the IV conditions they are meant to encode further weakens the paper's claims. The empirical results are competitive but not dominant, and the evaluation has several presentation issues. A substantially revised version with a corrected theoretical argument (or honestly reframed claims) could be a meaningful contribution to the field.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>