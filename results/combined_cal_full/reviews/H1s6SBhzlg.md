Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper studies how to aggregate responses from multiple LLMs, going beyond majority voting by leveraging higher-order information. The authors propose two algorithms: Optimal Weight (OW), a Bayesian-optimal linear aggregator using first-order information (agent accuracies), and Inverse Surprising Popularity (ISP), a novel inversion of the "surprisingly popular" rule that uses only second-order information (answer correlations between agents). The paper provides theoretical analysis showing ISP dominates majority voting (MV) in expected advantage, which in turn dominates the standard surprisingly popular rule. Experiments on synthetic data, UltraFeedback, MMLU, and a real healthcare dataset (ARMMAN) consistently show ISP and OW-based methods outperforming MV.

## Strengths

- **Principled formalization of the LLM aggregation problem.** The paper grounds the problem in the information aggregation literature (Sec. 2), introducing a clean model with symmetric priors (via random shuffling) and conditional independence that yields tractable theoretical analysis. This framing is appropriate and enables the theoretical results.

- **Theoretical analysis with concrete guarantees.** Theorem 1 (Bayesian optimality of OW), Theorem 2 (ISP > MV > SP in expected advantage with closed-form gap expressions), and Theorem 3 (finite-sample bound) are all clearly stated and appear technically correct under their assumptions. The closed-form expressions in Eqs. 209–213 are especially informative, showing how the gaps scale with K and agent accuracies.

- **ISP is a genuinely novel aggregation rule.** Inverting the surprisingly popular rule (Eqs. 4–5) is a simple but non-obvious modification, well-motivated by the insight that LLM agents have less systematic bias than humans (so SP underperforms MV, the reverse of the human setting). The example in Table 1 cleanly demonstrates ISP achieving perfect accuracy where MV and SP both err.

- **Consistent empirical improvement across diverse settings.** The methods outperform MV on synthetic data (Table 2), on standard NLP benchmarks (UltraFeedback, MMLU), and on a real-world healthcare dataset (ARMMAN). The improvements range from 0.54% to 14.20% absolute, and MV never achieves the best performance across 16 model ensembles. The per-question comparisons (Table 4) and t-statistics confirm the gains are statistically reliable.

- **Practical unsupervised instantiation of the first-order method.** The OW-L and OW-I pipelines (Sec. 5.2) show how to estimate the accuracies needed for OW without any ground-truth labels, addressing the key practical obstacle to deploying the theoretically optimal aggregator.

## Weaknesses

### Fatal

None.

### Major

- **OW-L and OW-I produce identical results, which demands explanation.** On all three real datasets (Table 3), OW-L and OW-I achieve identical accuracy to two decimal places (73.66%, 90.37%, 85.78%). Moreover, the per-question comparison counts in Table 4 are *exactly* identical between the two methods (2545/1727, 1821/659, 264/195). Two distinct estimation procedures — one solving an ERM over N accuracy parameters to fit N²K² conditional probabilities, the other using ISP predictions as pseudo-labels — yielding exactly the same predictions on every question across three datasets is extremely unlikely by chance. The paper must clarify whether the methods actually produce identical predictions and, if so, explain why. Without clarification, a reader cannot rule out a dependency or bug in the experimental pipeline. This is the most significant issue because it affects trust in the experimental reporting, though it does not undermine the paper's core contribution (ISP independently outperforms MV even without OW-L/OW-I).

### Minor

- **The theory proves an ordering of expected *advantage*, not expected *accuracy*.** Theorem 2 establishes that E[Adv_ISP(s*)] ≥ E[Adv_MV(s*)], where the advantage is a specific scoring function. The paper argues (line 205) that because all methods select the label with maximum advantage, higher expected advantage for s* should translate to higher expected accuracy. While this is plausible and the experiments directly validate the accuracy result, the theoretical connection between the two is not formally proven. The abstract's claim that ISP "provably has an advantage over majority voting" is ambiguous between the technical (advantage function) and colloquial senses. This is a gap of evidence level rather than a fatal flaw — the experiments confirm the accuracy claim — but bridging it would strengthen the theoretical narrative.

### Trivial

None.

## Nice-to-Haves

- **OW-L optimization details.** The ERM objective in Eq. (7) optimizing N accuracy parameters to match N²K² conditional probabilities could benefit from a brief description of the solver, initialization, or convexity properties. Some details may be in Appendix F.2 (stripped in this format), but the main text would benefit from a short description, especially since OW-L achieves the best accuracy in 2/3 of the ensembles.

- **Random shuffling procedure description.** While the concept of shuffling labels per question is described (line 49, line 75), briefly operationalizing it for each dataset (e.g., "for UltraFeedback, we randomly swapped 'chosen' and 'rejected' with probability 0.5 per question") would improve reproducibility.

- **Advantage-to-accuracy bound.** A bound (even a loose one) connecting expected advantage differences to accuracy differences would formally close the minor gap between the theory and the empirical claims.

## Removed Points

These points from the input review were removed as they fail the filtering criteria:

- *Abstract vs body σ_K definition inconsistency* (σ_K(x) = x²/(K-1+x²) vs e^x/(K-1+e^x)) — This is a parser rendering artifact (superscript confusion), not an author error. The body version is consistent with Corollary 1.
- *Formula rendering on line 82* — Parser artifact affecting LaTeX rendering, not an error in the submission.
- *Random shuffling not sufficiently described* — The paper does describe the procedure at the conceptual level (line 49, line 75 with an example), and the nature of the operation (random label permutation per question) is standard enough for each dataset setting. The concern is a minor reproducibility nitpick.
- *Statistical test procedure not described* — The t-statistics and per-question counts (Table 4) imply a standard paired comparison; this is standard practice and the omission is minor.
- *Conditional independence assumption concern* — The paper explicitly acknowledges this assumption may not hold (line 63) and references Appendix C for extensions; this is appropriate handling.
- *K vs accuracy scaling discussion* — The paper already discusses this at line 215.

## Novel Insights

None beyond the paper's own contributions. The key conceptual insight — that the surprisingly popular rule underperforms MV in LLM settings because LLM agents have less systematic bias than humans, and that inverting the rule (ISP) corrects for this — is well articulated by the paper itself.

## Suggestions

1. **Explain why OW-L and OW-I produce identical results** — this is the single most important issue to address. State whether the predictions are identical per-question, and if so, explain the mechanism (e.g., does the ERM in OW-L converge to the ISP-based pseudo-label estimates?).
2. **Add a brief remark connecting advantage ordering to accuracy** — even a short discussion of when the advantage gap could fail to translate to an accuracy gap would suffice.
3. **Add brief solver details for OW-L** — a single sentence on the solver, initialization, and whether the optimization is convex.

## Score and Decision

I place this paper at **7.0 (Accept)**.

**Calibration grounding.** I compared my draft's weighted items against three anchors: Dl6nkKKvlX.md (6.25, LLM ensembles), grM2Yv49cI.md (6.00, model aggregation), and NO6Tv6QcDs.md (6.50, LLM-as-judge evaluation). My paper's strengths all carry high positive model weights (+3.53 to +5.18), exceeding those of the 6.25 and 6.50 anchors. More importantly, my paper's weaknesses are substantially milder: the strongest negative item (OW-L/OW-I identical results, weight -1.87) is much less severe than the -3 to -4.5 weighted weaknesses present in all three anchors. The round-1 bracket was [5.5, 7.5]. Within this bracket, the paper sits near the top because its theoretical contributions (Bayesian optimality of OW, closed-form advantage gaps) are clean and principled, its core empirical claim (ISP > MV) is consistent across all settings, and no weakness undermines the paper's main conclusions. The paper does not reach the 8.0 level of the strongest accept papers (which tend to have no significant methodological concerns), hence the 7.0.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>