Now let me carefully verify the Lemma 1 proof and the critic's claims about it.Now I have a thorough understanding of the paper. Let me verify the key mathematical claim about Lemma 1 by re-reading the proof carefully one more time.Now I have thoroughly verified all the reviewer's claims. Let me draft my review.Now let me proceed to calibration. Round 1 — Bracketing:Let me read the most topically relevant anchor papers to calibrate.Now I have enough calibration data to form my bracket and finalize the review.

**Round 1 Bracket Analysis:**

- **Strong reject band (< 1.5):** Papers here are fundamentally broken or not real research (e.g., Uj0h13lVrR, nSDOkm0SKo). ZNet is clearly better than these.
- **Reject band (1.5–3.5):** Papers like AvXrppAS2o (3.0), jFox1iMWUa (3.4), 4u0ruVk749 (3.0) — rejected for marginal contributions, limited baselines, or questionable methodology. ZNet has a more comprehensive experimental setup than these.
- **Borderline reject band (3.5–5.5):** Papers like F7XPZnIUHh (4.20) — rejected for errors in derivations, novelty concerns, and unstable optimization. This is the closest analog: decomposed representation learning with derivation errors. ZNet has a similar profile.
- **Borderline accept band (5.5–7.5):** Papers like qDhq1icpO8 (6.75) — accepted CIV paper with sound theory, real-world experiments, and competitive results. ZNet is weaker: flawed theory, no real-world data, less convincing results.
- **Accept band (7.5–8.5):** Strong causal inference papers with solid theory and evidence. ZNet doesn't reach this level.
- **Strong accept band (> 8.5):** No topically similar papers found here.

**Initial bracket: 3.5 – 5.0.** The paper's theoretical flaw is significant and central (undermines the main claimed advantage), placing it below borderline accept. But the architecture is intuitive, the experimental grid is comprehensive, and the method has some empirical value, placing it above a pure reject.

Now let me write the final review.

---

## Summary
The paper proposes ZNet, a multi-arm deep learning architecture that decomposes observed covariates X into instrument (Z = g(X)) and confounder (C = f(X)) representations for use in two-stage IV regression. The key claimed advance is that, through Lemma 1 and a residual-based loss, ZNet can construct valid instruments even when observed covariates X are influenced by unobserved confounders U — relaxing the standard assumption in the IV-generation literature. The method is evaluated on ten semi-synthetic dataset configurations with three downstream estimators and four IV-generation baselines.

## Strengths
- **Intuitive and transparent architecture.** The multi-arm design (Figure 3) encoding IV structural assumptions through targeted loss terms (Constraints 1–3) is architecturally clean and immediately interpretable. Each component's role maps directly to the causal graph. This is a genuine design advantage over the variational approaches of AutoIV, VIV, and DVAE.CIV.
- **Comprehensive experimental grid.** Table 1 covers ten dataset configurations (linear/nonlinear × disjoint/mixed/latent/no-candidate × with/without U) crossed with three downstream estimators and four baselines. This breadth exceeds most prior IV-generation papers and provides useful empirical signal.
- **Meaningful ablation.** Figure 5c demonstrates that removing each constraint family degrades instrument recovery (R² for predicting true instruments drops), substantiating the multi-loss design.
- **Latent instrument recovery.** Figure 4 shows near-perfect cluster recovery in the latent categorical instrument setting, demonstrating the method's capacity to extract latent structure beyond simple variable selection.

## Weaknesses

### Fatal

None

### Major

1. **Lemma 1 is mathematically vacuous for Z = g(X), undermining the paper's central theoretical claim.** The proof of Lemma 1 (Section 3, line 93) contains an algebraic error: the fourth line replaces E[Z · E[e_Y|X,T]] with E[Z] · E[e_Y|X,T], which requires Z and E[e_Y|X,T] to be independent. Since Z = g(X) and E[e_Y|X,T] is a function of (X,T), they are generally dependent, making this factorization invalid. More fundamentally, even if Lemma 1 were correct, its premise — Cov(Z, e_Y − E[e_Y|X,T]) = 0 — is *trivially satisfied for any Z = g(X)* by the tower property of conditional expectation: E[g(X)·(e_Y − E[e_Y|X,T])] = E[E[g(X)·(e_Y − E[e_Y|X,T])|X,T]] = E[g(X)·(E[e_Y|X,T] − E[e_Y|X,T])] = 0 for any g. Consequently, the loss L^{PC}_{Z↮ε_Y} (Eq. 6) is always near zero regardless of g, providing no gradient signal. The paper's central theoretical claim — that ZNet handles the setting where X is influenced by U (lines 87, 386–390) — has no theoretical support. Without this, ZNet's theoretical advantage over the simpler assumption X ⊥ U (under which any g(X) is trivially unconfounded) disappears.

2. **Weak instrument on held-out data in the no-candidate setting.** Figure 6a reports test F = 1.83 (p = 0.08), well below the Staiger-Stock threshold of 10 for instrument strength and not significant at conventional levels. This is the paper's most novel claimed setting — constructing instruments when none exist in the data — yet the learned instrument fails the standard relevance diagnostic on held-out data. The train F = 15.34 vs. test F = 1.83 gap also suggests overfitting of the instrument representation.

3. **Covariance constraints are insufficient proxies for the required IV conditions.** The IV unconfoundedness condition requires Z ⊥ e_Y | C (conditional independence), but ZNet operationalizes this via Pearson correlation (Eq. 6). Zero unconditional Pearson correlation is neither necessary nor sufficient for conditional independence. The MI option (Section 5.1) addresses nonlinear marginal dependence but not conditional independence — no conditional MI loss is described. Similarly, the exclusion restriction is a structural/causal condition (Z has no causal path to Y except through T), which cannot be established by statistical decorrelation alone.

4. **Discussion overclaims relative to theoretical support.** Section 7 (line 394) states: "Solutions to the ZNet loss minimization problem will always give a representation that serves as an instrument since IV constraints are explicitly embedded in the loss function." Given that Constraint 1 is vacuous (Major weakness 1) and the remaining constraints approximate but do not guarantee the actual IV conditions (Major weakness 3), this claim is not supported.

### Minor

5. **No real-world experiments.** All evaluation uses semi-synthetic data built from IHDP covariates (n = 985, d = 25). For a method claiming practical "plug-in" applicability (Abstract, Section 7), even one real-world experiment (e.g., returns-to-schooling, Mendelian randomization) where ground-truth instruments exist for comparison would substantially strengthen the empirical case.

6. **Downstream estimator tuning uses nearest-neighbors ATE as target.** Section 5.3 tunes downstream IV estimators to minimize MSE against a NN matching ATE estimate. While this is applied equally to all methods (making internal comparisons fair), the paper does not discuss how practitioners would perform model selection in real applications where even NN matching may be biased under unobserved confounding.

7. **No standard errors on ATE estimates.** Table 1 reports mean ATE error across 50 bootstraps with significance markers but no standard errors or confidence intervals, making it difficult to assess the magnitude of differences between methods.

### Trivial

None

## Nice-to-Haves
- At least one real-world dataset experiment to support the "plug-in module" claim.
- A conditional MI loss term for the unconfoundedness constraint, which would more directly target Z ⊥ e_Y | C.
- Discussion of CATE results (Appendix Tables 3, 4) in the main text, since CATE estimation is arguably more informative than ATE.
- Analysis of the train-test generalization gap for learned instrument quality beyond the no-candidate setting.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Two-layer depth insufficient for nonlinear settings"**: The choice of two-layer networks is a standard architecture decision and the paper evaluates on both linear and nonlinear settings. This is a design choice, not a flaw.
- **"TrueIV outperforms learned IVs in several settings"**: This is expected — the point of IV generation methods is to help when TrueIV is unavailable, not to beat oracle access to the true instrument. Outperformance of TrueIV would be surprising, not expected.
- **"Overfitting risk with small n = 985"**: While plausible, this concern is not specifically demonstrated in the paper and is speculative.
- **"Table 1 results noisy — ZNet best/second-best in roughly half of entries"**: While accurate, the paper doesn't claim dominance everywhere; it claims competitive performance on average, which is supported (Appendix Tables 9, 10 report average rankings).

## Novel Insights
The core architectural idea of encoding IV structure directly into a neural network via targeted loss terms — rather than through variational inference — is genuinely novel and potentially valuable. The decomposition of the learning problem into separate arms for instrument recovery (g), confounder recovery (f), treatment prediction (π), and outcome modeling (Φ) provides a clean separation of concerns that is more interpretable than VAE-based alternatives. If the theoretical foundation for unconfoundedness were corrected — either by developing a valid constraint or by honestly scoping the method to X ⊥ U — this approach could be a meaningful contribution to the IV-generation literature.

## Suggestions
- **Fix or replace Lemma 1.** Either develop a valid unconfoundedness constraint that is not trivially satisfied for Z = g(X), or honestly restrict the method's scope to the X ⊥ U setting and position the contribution as architectural rather than theoretical. The latter is more credible and still valuable.
- **Add a conditional independence-based loss.** Consider operationalizing Cov(Z, e_Y | C) = 0 directly, e.g., via conditional MI estimation or kernel-based conditional independence tests.
- **Report standard errors** on all ATE estimates in Table 1.
- **Investigate the train-test F-statistic gap** in the no-candidate setting (F = 15.34 train vs. 1.83 test). If the learned instrument doesn't generalize, this is a critical limitation that should be discussed.
- **Include at least one real-world experiment** to support practical applicability claims.

## Score and Decision

### Anchor Papers (All Rounds)

| Paper | Path | Avg Score | Round | Comparison to ZNet |
|-------|------|-----------|-------|-------------------|
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | 1 | Far worse — fundamentally broken; ZNet has genuine research contributions |
| Financial Markets NN | nSDOkm0SKo | 1.00 | 1 | Far worse — not a real research contribution; ZNet is substantive |
| IC-Light | u1cQYxRI1H | 10.00 | 1 | Outlier in score range, not topically relevant |
| Lifelong ReID | 5lUdTogEL3 | 1.00 | 1 | Far worse; ZNet is much better |
| Causal Structure Learning | AvXrppAS2o | 3.00 | 1 | Weaker than ZNet: marginal improvements, limited baselines; ZNet has more comprehensive evaluation |
| Causal Neural Networks | jFox1iMWUa | 3.40 | 1 | Weaker: writing quality and novelty concerns; ZNet has clearer architecture |
| DFITE | 4u0ruVk749 | 3.00 | 1 | Similar level of theoretical concerns; ZNet has a more principled approach |
| D³PM Causal Discovery | TRHyAnInUC | 3.25 | 1 | Different topic; ZNet is better organized |
| **ADR Treatment Effect** | **F7XPZnIUHh** | **4.20** | **1** | **Closest analog: decomposed representation learning with derivation errors. ZNet has a comparable theoretical flaw but more comprehensive experiments.** |
| Latent Structural Causal Models | 0sO2euxhUQ | 4.00 | 1 | Similar: ambitious scope, theoretical gaps. ZNet has more practical focus |
| Causality is Invariance | qsAckNdySL | 4.25 | 1 | Different approach; similar severity of issues |
| Feature Matching Intervention | 8GhwePP7vA | 4.25 | 1 | Similar: causal representation learning, some theoretical gaps |
| **CIV Regression (CBRL.CIV)** | **qDhq1icpO8** | **6.75** | **1** | **Most topically similar. That paper has sound theory, real-world experiments, and competitive results. ZNet is significantly weaker due to flawed theory and no real-world data.** |
| Nuisance-Robust Weighting | TC9r8gsaoh | 6.00 | 1 | Better: sound theory, practical approach. ZNet is weaker. |
| Neural Causal Graph | nmvmPIi185 | 6.25 | 1 | Better: clearer contributions. ZNet doesn't reach this level. |
| Variational Treatment Effects | S46Knicu56 | 7.33 | 1 | Substantially better: sound variational framework with measurement error |
| Intervention Extrapolation | 3cuJwmPxXj | 8.00 | 1 | Far better: strong identifiability results |
| Selection + Intervention | xByvdb3DCm | 8.00 | 1 | Far better: novel theoretical contributions |

**Round 1 bracket:** 3.5 – 5.0

**Narrowing rationale:** The closest analog is F7XPZnIUHh (4.20) — a rejected paper with similar issues (errors in derivations for decomposed representations, adversarial instability). ZNet has a comparable theoretical flaw (Lemma 1 vacuousness) but a more comprehensive experimental evaluation. However, ZNet's flaw is arguably more central — it undermines the paper's stated key advance over prior work, whereas F7XPZnIUHh's errors were more peripheral. The gap between ZNet and the accepted CIV paper (6.75) is large: sound theory, real-world data, and cleaner results separate them. ZNet sits in the borderline reject range.

**Final score: 4.0** — The paper has a genuinely interesting architectural idea and a comprehensive experimental grid, but the central theoretical claim (handling X influenced by U via Lemma 1) is demonstrably unsupported due to a mathematical vacuousness in the unconfoundedness constraint. The most novel empirical setting (no-candidate instruments) shows weak instruments on test data. These issues prevent acceptance but the paper has sufficient merit to warrant revision rather than outright rejection.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>