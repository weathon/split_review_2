## Summary

This paper proposes a conformal prediction method for constructing lower prediction bounds (LPBs) for counterfactual survival times under different treatments in general right-censored data. The key innovation is a reweighting scheme that transforms the counterfactual coverage problem into a weighted conformal inference problem, enabling exact marginal coverage guarantees (rather than PAC-type guarantees) under the strong ignorability assumption. The method is doubly robust against model misspecification, and its validity and informativeness are demonstrated on synthetic data and a real lung cancer clinical dataset.

## Strengths

- **Exact marginal coverage for a challenging setting**: The paper is the first to achieve exact marginal coverage guarantees for counterfactual LPBs under general right censoring, moving beyond the PAC-type guarantees of prior work (Gui et al., 2024; Davidov et al., 2025). This is a meaningful practical improvement for high-stakes clinical decision-making.
- **Sound theoretical framework**: The authors provide a clear derivation connecting the counterfactual coverage probability to a weighted conformal prediction problem, and prove distribution-free finite-sample bounds (Theorem 4.1) as well as asymptotic double robustness (Theorem 4.2). The theoretical claims are appropriate for the setting.
- **Strong empirical validation**: Experiments on six synthetic settings and a real lung cancer dataset show that the method consistently achieves near-nominal coverage while producing less conservative LPBs than baselines. The outlier experiments (Figure 3) convincingly demonstrate the robustness of the exact guarantee compared to PAC-type methods.
- **Practical relevance**: The real-data analysis on distinct radiochemotherapy regimens reveals sensible treatment effect patterns consistent with medical literature, demonstrating that the method can produce interpretable and clinically meaningful LPBs.

## Weaknesses

### Major

1. **Derivation opacity in the key coverage transformation (Eq. 1)**: The chain of equalities and inequalities that maps the target coverage probability to a reweighted expectation over observed data is not fully explained in the main text. Step (iii) is referenced to Lemma A.1 in the appendix, which is not available in the submitted version. This makes it difficult for the reader to verify the correctness of the core reduction that enables weighted conformal calibration. While the result likely holds, the presentation should be self-contained or at least outline the key idea.

2. **Limited efficiency discussion**: The calibration set uses only uncensored observations (e_i=1) from the treated group. This can discard a large fraction of the data under high censoring rates. The paper does not analyze how the effective calibration sample size affects the width of the LPB or the stability of the coverage guarantee. The empirical settings shown (e.g., Setting 6) have moderate censoring, but the method's performance under extreme censoring (e.g., >80%) or with very small calibration sets is not investigated.

### Minor

3. **Overclaimed "exact" guarantee**: Theorem 4.1 shows that the miscoverage rate is bounded by α + (1/2)E|ω̂ − ω|. This is not "exact" in the finite-sample sense unless the density ratio is known exactly. The bound depends on the quality of the estimated weights, which introduces an approximation error. The paper acknowledges this, but the title and abstract could be more precise.

4. **Baseline comparison limited to PAC-type methods**: The main comparisons are against "Focus" and "Fused" from Davidov et al. (2025), which only provide PAC guarantees. There is no comparison with methods that might provide exact coverage in simpler settings (e.g., Candès et al. 2023 for Type-I censoring) or with non-conformal LPB approaches. The paper would benefit from a broader empirical context.

### Trivial

5. **Typographical inconsistency in Figure 1 color description**: The text refers to "Uncal (grey)" and Figure 1 caption lists "Uncab (light pink)". This appears to be a naming mismatch (Uncal vs Uncab), and the color description is inconsistent between the Figure 1 caption and the text (grey vs light pink). Clarify the method name.

## Nice-to-Haves

- Provide a toy example or intuitive explanation of the reweighting idea (the Radon-Nikodym derivative connection) to make the method more accessible.
- Include a sensitivity analysis showing how the coverage gap (α + error term) behaves as a function of the calibration set size and the censoring rate.
- Report the effective calibration sample size (number of uncensored treated units) for each experimental setting.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Move the key Lemma A.1 (or its statement) into the main text or at least sketch its meaning, so that the derivation in Eq. 1 becomes self-contained.
- Add an experiment that systematically varies the censoring rate (e.g., from 20% to 90%) to demonstrate the method's robustness and to understand when the weight estimation error dominates.
- Consider comparing against a simpler baseline that simply uses the standard conformal quantile regression on the uncensored observations without reweighting (the "Naive" method already included) to clearly isolate the benefit of the reweighting.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>