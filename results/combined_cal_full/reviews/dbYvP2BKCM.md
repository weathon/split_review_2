Now I have all the information needed to write the consolidated final review.

---

## Summary

This paper proposes ZNet, a method for automatically learning instrumental variable (IV) representations from observed covariates by decomposing them into confounder (C) and instrument (Z) components. The key idea is to enforce three constraints—relevance, exclusion restriction, and unconfoundedness—via loss terms applied to learned representations Z = g(X) and C = f(X), enabling downstream IV estimation without requiring a pre-specified instrument. Experiments across semi-synthetic datasets with varying instrument availability show ZNet can recover known instruments and produce competitive ATE estimates.

## Strengths

- **Clearly motivated and well-scoped problem framing.** The paper identifies a genuine practical challenge—automating IV construction from observational data—and articulates this need well in Sections 1–3. The causal graph in Figure 2 usefully illustrates the desired decomposition of X into confounder and instrument representations.
- **Comprehensive experimental setup across data scenarios.** The evaluation covers four data classes (Disjoint Candidate, Mixed Candidate, Latent Categorical Instrument, No Candidate) in both linear and nonlinear variants, with three downstream estimators (TSLS, DeepIV, DFIV). This breadth is appropriate for a method that claims to work in "general observational settings."
- **Transparent architecture and loss design.** The ZNet architecture is clearly specified, and the loss terms (Equations 5–9) are explicitly tied to the three IV conditions. The code-to-constraint mapping is clear enough that an independent researcher could attempt to implement it.
- **Empirical demonstration of instrument recovery in candidate settings.** Figures 4–5 show that ZNet can recover ground-truth instruments in the Disjoint and Latent Categorical Instrument settings, with ablation experiments (Figure 5c) demonstrating the contribution of each constraint to successful recovery.

## Weaknesses

### Fatal

1. **Constraint 1 (Instrumental Unconfoundedness) is theoretically vacuous.** The loss \(L_{Z \not\leftrightarrow \epsilon_Y}^{PC}\) minimizes \(\text{Cov}(Z, Y - \hat{Y})\) where \(\hat{Y} = \Phi(X, T)\) estimates \(\mathbb{E}[Y|X,T]\). In the population, by the defining property of conditional expectations, \(\mathbb{E}[(Y - \mathbb{E}[Y|X,T]) \cdot h(X,T)] = 0\) for any measurable function \(h\). Since \(Z = g(X)\) is a function of \(X\) (hence of \((X,T)\)), \(\text{Cov}(Z, Y - \mathbb{E}[Y|X,T]) = 0\) holds for **any choice of \(g\)**, regardless of whether \(Z\) satisfies any IV condition whatsoever. Minimizing this covariance in finite samples is minimizing sampling noise, not learning about unconfoundedness. The paper's core mechanism for ensuring unconfoundedness provides no discriminative signal and does not distinguish valid instruments from invalid ones. This undermines the paper's central claim that "solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument" (Section 7).

2. **The proof of Lemma 1, on which the unconfoundedness enforcement strategy rests, contains a formal error.** Step 4 of the derivation (line 93) writes \(\mathbb{E}[Z \cdot e_Y] - \mathbb{E}[Z] \cdot \mathbb{E}[e_Y|X, T]\), where the left-hand term before this step should be \(\mathbb{E}[Z \cdot e_Y] - \mathbb{E}[Z \cdot \mathbb{E}[e_Y|X, T]]\). The expression \(\mathbb{E}[Z] \cdot \mathbb{E}[e_Y|X, T]\) is not equal to \(\mathbb{E}[Z \cdot \mathbb{E}[e_Y|X, T]]\) in general: the former is \(\mathbb{E}[Z]\) times a random variable, while the latter is a scalar. More broadly, as shown above, \(\text{Cov}(Z, e_Y - \mathbb{E}[e_Y|X,T]) = 0\) holds automatically for any \(Z = g(X)\) with \(\mathbb{E}[Z]=0\) (by the law of iterated expectations, since \(Z\) is \((X,T)\)-measurable). Thus Lemma 1's premise is always satisfied and its conclusion does not follow; the lemma provides no theoretical basis for enforcing unconfoundedness.

### Major

3. **The decomposition \(X \to (C, Z)\) is fundamentally underdetermined from observational data.** The three constraints are purely associational (\(\text{Cov}(Z,T) > 0\), \(\text{Cov}(C,Y) > 0\), \(\text{Cov}(C,Z) = 0\), \(\text{Cov}(Z,Y-\hat{Y})=0\)). These conditions are necessary but not sufficient for the *causal* IV conditions, which involve unobserved confounders \(U\) and counterfactual quantities. They do not guarantee that \(Z\) is independent of \(U\) or that \(Z\) has no direct effect on \(Y\). The paper acknowledges this implicitly (Section 7: "IV estimation in general is limited by a lack of theoretical guarantees of identifiability") but the issue is more acute than acknowledged: the method provides no argument that the learned representation corresponds to any meaningful causal quantity, even approximately.

4. **The "No Candidate" setting lacks a convincing explanation.** When no variable in \(X\) satisfies the exclusion restriction by construction (the most challenging and ambitious setting), any function \(g(X)\) will inherit direct paths from \(X\) to \(Y\). The paper does not explain why learning \(Z = g(X)\) should produce a valid instrument rather than a confounded predictor of \(T\). This is the paper's most distinctive claim and it receives the least defense, despite being critical to the generality claim.

5. **Experimental results do not demonstrate clear or consistent superiority.** ZNet is best (bolded) in roughly 11 out of 30 dataset/estimator combinations, and in several settings its error is substantially worse than baselines (e.g., Linear No Candidate (no \(U\)) ZNet TSLS = 2.718 vs. VIV TSLS = 0.279; Linear Disjoint ZNet DFIV = \(-0.303\) vs. TrueIV DFIV = 0.132). No standard deviations or confidence intervals are reported despite using 50 bootstrap resamples. The significance notation (*, **) is explained in the table caption, but the specific statistical test used to determine significance is not described, and many cells lack annotations entirely.

### Minor

6. **The MI-based loss variant is mentioned but never empirically compared to the PC variant** (Section 5.1). Given the paper's awareness that linear correlation may be insufficient for nonlinear settings, comparing these two variants is important for understanding when each is appropriate.

7. **No analysis of the learned \(C\) representation is provided.** If \(C = f(X)\) is meant to capture confounding, the paper does not evaluate whether \(C\) correlates with known confounders in the IHDP data or whether adjusting for \(C\) alone reduces bias.

8. **Hyperparameter sensitivity (loss weights \(\alpha_1\)–\(\alpha_7\)) is not analyzed.** Given the three-stage training procedure with gradient surgery and Bayesian tuning, the sensitivity of results to these choices is unclear. An ablation or sensitivity analysis would strengthen confidence in the method.

### Trivial

None.

## Nice-to-Haves

- Report standard deviations or confidence intervals for ATE estimates in Table 1.
- Compare the PC and MI loss variants empirically to characterize when nonlinear dependence matters.
- Include a simple fully-synthetic experiment with a known ground-truth IV structure to validate that the learned \(Z\) recovers the correct causal quantity, not just an associational proxy.
- Analyze the learned \(C\) representation (e.g., correlation with known confounders).

## Removed Points

**"The only non-IV baseline is TARNet"** — Removed per scope rules. The paper focuses on IV methods; TARNet and Difference in Means are reasonable baselines, and requesting sensitivity analysis or bounds is outside the paper's stated scope.

**"Lemma 1 failure makes the entire paper unsalvageable"** — Merged into the fatal weakness above. The deeper issue is not the lemma's proof error per se but that Constraint 1 is vacuous regardless; treating the proof error as the sole problem would understate the structural issue.

**"Missing appendix content"** — Removed per formatting rules. The appendix is stripped by the parser and exists in the original submission.

**"Covariate set definitions in data generation need more detail"** — Removed. The data generation is described in Section 6.1 with clear definitions of the four data classes. Additional details would be in the appendix (stripped by parser).

## Novel Insights

The most penetrating insight from the review process is that Cov\((Z, Y - \mathbb{E}[Y|X,T]) = 0\) is automatically satisfied for any \(Z = g(X)\) in the population, making the unconfoundedness enforcement mechanism theoretically vacuous. This is not a standard "lack of identifiability" concern but a concrete demonstration that the loss provides no signal for distinguishing valid instruments from invalid ones. A second key insight is that the associational constraints used in the paper (covariance-based) are insufficient proxies for the causal IV conditions, and the paper provides no formal argument bridging this gap. The empirical results (Figures 4–5) showing successful instrument recovery in candidate settings suggest the architecture may still be useful, but the reasons for this success cannot be attributed to the unconfoundedness constraint as claimed.

## Suggestions

1. **Replace the vacuous unconfoundedness loss** with a loss that provides meaningful signal. One direction: instead of Cov\((Z, Y-\hat{Y})\), consider a conditional independence test or a loss that directly penalizes dependence between \(Z\) and the error term after conditioning on \(C\) and \(T\). Another direction: provide explicit assumptions about the data-generating process under which the loss is not automatically zero.
2. **Add identification analysis** specifying what structural assumptions on the data-generating process are sufficient for the decomposition \(X \to (C, Z)\) to recover causally meaningful quantities.
3. **Report standard deviations** for all ATE estimates in Table 1, and describe the significance test procedure.
4. **Provide explicit assumptions** for the No Candidate setting that justify why learning \(Z = g(X)\) can produce a valid instrument when no observed variable satisfies the exclusion restriction.
5. **Compare PC and MI loss variants** empirically to characterize settings where nonlinear dependence matters.

## Score and Decision

**Calibration.** I compared the paper's weighted items against four anchors from the human review corpus. The most topically relevant anchors are:

- **F7XPZnIUHh.md** (avg 4.20, "Adversarial Learning of Decomposed Representations for Treatment Effect Estimation"): Shares the topic of decomposing covariates into IV/confounder types. Its most negative items are about novelty (-9.02) and theoretical errors (-7.02). The current paper's fatal flaw (Constraint 1 is vacuous, weight -7.51) is more fundamental than those issues, justifying a lower score.
- **AvXrppAS2o.md** (avg 3.00, "Improved outcome prediction using causal structure learning"): Weaknesses include marginal improvements and no theoretical guarantees. The current paper has a similar severity of issues (fatal theoretical flaw) but also some empirical strengths (instrument recovery). Comparable overall.
- **5AJ8R4z5g0.md** (avg 3.25, "Potential Outcomes Estimation Under Hidden Confounders"): Weaknesses about strong assumptions (-7.50) and missing theoretical justification (-7.18). Comparable severity.
- **qDhq1icpO8.md** (avg 6.75, "Conditional Instrumental Variable Regression"): A stronger paper with theoretically grounded methodology and extensive experiments. The current paper's fatal flaw places it well below this anchor.

The initial bracket (Round 1) was [2.0, 4.0]. After comparing the heavy-weight items—the current paper's -7.51 fatal weakness (vacuous constraint) versus anchors' similar-magnitude weaknesses at ~3.0–3.25—I narrow the score to **3.0**.

**Score: 3 / Reject**

The paper addresses an important problem and presents a transparent architecture with a comprehensive evaluation. However, Constraint 1 (Instrumental Unconfoundedness) is theoretically vacuous: Cov\((Z, Y-\mathbb{E}[Y|X,T]) = 0\) holds for any \(Z = g(X)\) in the population, providing no signal about whether \(Z\) is actually unconfounded. This undermines the paper's central claim that the loss function enforces the IV conditions. The proof of Lemma 1 contains a formal error. Additionally, the decomposition is underdetermined, the No Candidate setting lacks convincing justification, and experimental results show mixed performance without error bars. These are structural issues that prevent acceptance; the paper would require a fundamentally different unconfoundedness enforcement strategy to be viable.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>