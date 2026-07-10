Now I have sufficient calibration data. Let me write the final consolidated review.

**Round 1 Bracket:** Based on my comparison of the draft's favorability ratings against the anchors, I place this paper in the **6.5–7.5** range. The strongest anchor is MINDE (6.50, sim 0.64–0.78), which shares the same paradigm (diffusion-based MI estimation) but addresses continuous data. INFO-SEDD's strengths are notably higher in favorability (avg ~13.47 vs MINDE's ~9.15), and its weaknesses are all mild (lowest at -1.77 vs MINDE's -1.60). The Efficient Perplexity Bound paper (6.75) and Discrete Diffusion Convergence paper (7.00) confirm that work at the ~7 level in this area is considered acceptable.

**Round 2 — Narrowing:** The MINDE anchor (6.50) had 3 reviewers at 6 and 1 at 8. INFO-SEDD's strengths are materially higher (novelty of extending to discrete data, dramatic synthetic gains), and its weaknesses are comparably mild. No speculative or fatal flaws exist. The paper is clearly above borderline-accept territory but below strong-accept because of addressable evaluation gaps (text reference, no runtime, qualitative-only motif analysis). This narrows to **7.0**.

Here is the final review.

## Summary

This paper introduces INFO-SEDD, a method for estimating mutual information (MI) and KL divergence for high-dimensional discrete data using Continuous Time Markov Chains (CTMCs) with absorbing states. The key insight is connecting CTMC score functions to information-theoretic quantities via Dynkin's formula, enabling a single joint diffusion model trained with the DWDSE loss to yield marginal scores via an absorbing-state trick. The method is evaluated on synthetic benchmarks (where it dramatically outperforms variational competitors), text summarization model selection, and genomics (consistency tests and TATA-box motif discovery).

## Strengths

- **Novel methodological contribution (Sections 2–3).** Using discrete diffusion models (CTMCs with absorbing states) to estimate KL divergence and MI for high-dimensional discrete data is genuinely novel. The connection between score functions of CTMCs and information-theoretic quantities via Dynkin's formula is non-trivial and clearly derived. The absorbing-state design (Equation 6) that allows a single joint model to also yield marginal scores is clever and practically significant. **[favorability=17.48]**

- **Strong synthetic benchmark results (Table 1, Section 4.1).** On the high-dimensional/high-MI synthetic benchmark, INFO-SEDD dramatically outperforms all 7 competitors. At MI=50, D=50, INFO-SEDD estimates 47.77±1.18 while the next-best method (MINDE) estimates 32.60±3.93. The gap is large and consistent across all 5 settings, with substantially lower variance than competitors. This is the paper's strongest evidence. **[favorability=12.51]**

- **Theoretical error bound (Equation 7, Section 3).** The bound decomposing error into estimation error (scaling with score approximation error) and truncation bias (decaying exponentially with T) provides a principled characterization of when the estimator works. The structural decomposition is informative, even though constants are not quantified. **[favorability=10.15]**

- **Meaningful real-world applications.** The text summarization model selection (Table 2) shows INFO-SEDD-C achieves Pearson r=0.74 with human consistency ratings vs. r=0.214 for KL-DIME, demonstrating genuine practical utility. The TATA-box motif discovery (Figure 5) identifies the known motif region without task-specific training, serving as a compelling proof-of-concept. **[favorability=13.74]**

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The text consistency test reference is not a valid ground truth for MI (Section 4.2).** The paper uses text entropy rates (256–303 nats) — the entropy of texts, not the mutual information between texts and summaries — as reference lines in Figure 1, then claims INFO-SEDD "closely matches the empirical derivation." Since I(text; summary) ≤ H(summary), and summaries are much shorter than full texts, the reference is an extreme upper bound, not a plausible MI estimate. The relative ordering of estimators in Figure 1 remains meaningful (competitors saturate while INFO-SEDD does not), but the specific "close match" claim is overstated. The classifier-based reference used in the genomics experiment (Section 4.3) is more principled and should have been the model for this experiment as well. **[favorability=1.97]**

- **No computational cost or runtime comparison.** The paper claims INFO-SEDD is "lightweight and scalable" but provides no runtime, FLOP counts, parameter counts, or wall-clock time comparison with competitors. Training a discrete diffusion backbone like MDLM-SMALL is substantially more expensive than the competitors' much smaller models. Without such data, the practical "scalability" claim is unsubstantiated, which matters for a paper whose selling point includes practical applicability. **[favorability=-1.00]**

- **The motif discovery experiment is purely qualitative (Section 4.3, Figure 5).** The MI profile peaks in the known TATA-box region, which is a nice demonstration. However, no quantitative comparison is provided against Umarov and Solovyev (2017) or any other motif discovery method, so readers cannot assess whether INFO-SEDD provides better localization, higher sensitivity, or any practical advantage. The claim about "robustness to correlated motifs" is stated without experimental evidence. **[favorability=-1.77]**

- **Certain mathematical steps in the derivation are glossed over.** Equation (2) asserts KL[p₀‖q₀] = E[log(p_T/q_T)(X_T)], which relies on KL divergence being invariant under the same CTMC generator — a non-trivial property that is neither justified nor cited. The transition from Equation (4) to Equation (5) substitutes learned scores for true ratios, but the connection between the DWDSE loss and score estimation is assumed familiar from Lou et al. (2024). While both steps are correct, a reader unfamiliar with the discrete diffusion literature would be lost. **[favorability=4.45]**

- **Classical discrete MI estimators are not benchmarked.** The paper cites classical estimators (Miller-Madow, NSB, plug-in with shrinkage) as failing at high dimensionality, but never actually benchmarks them. Including even one such estimator on the synthetic task would close the loop on the motivation that existing discrete estimators are inadequate. **[favorability=0.10]**

### Trivial
None.

## Nice-to-Haves
- Replace the text consistency reference with a principled classifier-based approximation, as done for the genomics experiment, which would make the comparison rigorous.
- Add a table reporting wall-clock training time, inference time per MI estimate, and approximate parameter counts for each method on the synthetic benchmark.
- Provide a quantitative baseline comparison for the motif discovery experiment (e.g., localization accuracy or AUC against Umarov and Solovyev (2017) or a simple PWM-based method).

## Removed Points
These points from the input review are removed with justification:

- **"The paper does not discuss the ceiling effect visible in Figures 2–3":** REMOVED because the paper explicitly states (Section 4.2) that "consistency saturates around the maximum score, whereas MI does not have the same ceiling effect." The reviewer's claim is factually wrong.
- **"Missing appendix content (synthetic data generation, entropy results, proofs):"** REMOVED per policy — the parser strips appendices from all papers; these sections exist in the original submission.
- **"DWDSE loss connection not explained":** REMOVED — the paper properly cites Lou et al. (2024) for this standard formulation.
- **"The paper should include a limitations section":** REMOVED — a nice-to-have, not a genuine weakness.
- **"The entropy estimation results are in the stripped appendix":** REMOVED per policy about stripped appendix.
- **Criticisms about format, typos, or notation:** REMOVED as parser artifacts or formatting nitpicks.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Replace the text consistency test's "empirical derivation" reference with a classifier-based approximation (mirroring the genomics experiment) to provide a valid ground-truth comparison.
- Add a computational cost table (training time, inference time, parameter counts) to substantiate the "lightweight and scalable" claim.
- Include at least one classical discrete estimator (e.g., Miller-Madow or NSB) on the synthetic benchmark to empirically verify the claim that such estimators fail at high dimensionality.
- For the motif discovery experiment, add a quantitative baseline — e.g., report localization accuracy comparing INFO-SEDD's MI peak against Umarov and Solovyev (2017) or a position-weight-matrix approach.

## Score and Decision

**Score calibration summary:** The strongest anchor is MINDE (0kWd8SJq8d, avg 6.50, Accept), a diffusion-based MI estimator for continuous data. INFO-SEDD's strengths have higher favorability (avg ~13.47 vs ~9.15) and comparable mild weaknesses. The Efficient Perplexity Bound paper (Mri9WIfxSm, avg 6.75, Accept) and Discrete Diffusion Convergence paper (pq1WUegkza, avg 7.00, Accept) are related but less directly comparable (theory/language modeling, not MI estimation). The f-DIME MI estimator (KC2MViQASx, avg 5.60) addresses a similar problem but with weaker empirical evidence. INFO-SEDD sits above MINDE and f-DIME due to its stronger novel contribution and dramatically better synthetic results, but the evaluation gaps (text reference, no runtime, qualitative-only motif analysis) prevent it from reaching strong-accept territory. Final score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>