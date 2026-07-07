I now have all the information I need. Let me write the final consolidated review.

---

## Summary

This paper proposes two algorithms—Optimal Weight (OW) and Inverse Surprising Popularity (ISP)—for aggregating outputs from multiple LLMs. OW is a Bayes-optimal linear weighting scheme that uses first-order information (accuracies), while ISP is a modification of the Surprising Popularity rule that leverages second-order information (answer correlations between LLMs). The paper provides theoretical guarantees under conditional independence, closed-form expressions for advantage gaps, and empirical validation on simulated data, UltraFeedback, MMLU, and a healthcare dataset (ARMMAN).

## Strengths

1. **Clean, principled OW derivation.** Section 3 derives the Bayes-optimal aggregation weights under conditional independence as ω_i ∝ log((K−1)x_i/(1−x_i)), connecting to an interpretable inverse-logistic weighting scheme. The proof that this simple linear aggregator maximizes expected accuracy among all possible aggregators is a solid theoretical contribution that formalizes what majority voting approximates.

2. **Well-motivated ISP design.** The paper gives a clear explanation for *why* SP underperforms MV in LLM settings (Section 4.2): the systematic overconfidence bias that SP exploits in human crowds is less pronounced in LLMs. The ISP counterfactual—swapping the conditioning to amplify this weaker signal (Equations 3–4)—is grounded and clearly communicated. The closed-form expression for E[Adv_ISP(s*) − Adv_MV(s*)] in Theorem 2 is a non-trivial theoretical result.

3. **Appropriate experimental scope.** Evaluation spans simulated data (varying K to validate Theorem 2's asymptotic predictions), two standard LLM benchmarks, and a real-world healthcare dataset (ARMMAN). This breadth strengthens the claim that the methods work beyond toy settings.

## Weaknesses

### Major

1. **OW-L and OW-I produce identical results across all three datasets, undermining confidence in the experimental pipeline.** In Tables 3 and 4, OW-L (ERM-based accuracy estimation from second-order probabilities) and OW-I (ISP-based pseudo-label accuracy estimation) report *exactly* the same accuracy (73.66%, 90.37%, 85.78%) and *exactly* the same per-question counts (2545/1727, 1821/659, 264/195) on all three datasets. These are two methodologically distinct estimation pipelines (line 265 vs. line 271). Identical results on every question across three independent datasets strains credibility. This could reflect (a) a data-processing bug, (b) one method not being computed independently, or (c) an undocumented equivalence under these conditions. As reported, the reader cannot tell whether OW-L and OW-I are genuinely being compared. This is a structural concern that must be resolved before the empirical claims about OW-L and OW-I can be trusted.

2. **No comparison against relevant LLM aggregation baselines.** The empirical evaluation compares only against MV, SP, and Single Best. SP is shown to be worse than MV, so the only competitive baseline is MV. The paper's own related work cites confidence-weighted aggregation (Chen et al., 2023a; Fu et al., 2025) and model selection approaches (Jiang et al., 2023), yet none are implemented. Given that absolute gains over MV are modest (0.54%–1.45% on real datasets, on subsets where models already disagree on only 31–52% of questions), comparison against stronger baselines from the LLM ensemble literature is needed to establish practical added value.

### Minor

3. **Theorem 2 proves an ordering of expected *advantage*, not accuracy.** The paper states that ISP "outperforms" MV and that this is "rigorously proved in Theorem 2" (lines 144, 207). Theorem 2 proves E[Adv_ISP(s*)] ≥ E[Adv_MV(s*)] ≥ E[Adv_SP(s*)], where Adv is the score used inside an argmax. A larger expected advantage for the correct label does not directly imply a higher probability that the argmax selects the correct label—the mapping from advantage to accuracy involves the full joint distribution of advantages across all labels. The simulations empirically confirm the accuracy ordering (Table 2), which mitigates this concern, but the theoretical claim is slightly mismatched with what is proven. The paper should clarify the relationship between advantage ordering and accuracy ordering.

4. **Conditional independence and no-position-bias assumptions are acknowledged but not tested for robustness.** The theoretical framework (Assumption 1) relies on agents being conditionally independent given the truth and on LLMs being order-invariant. Both are known to be partially violated in practice (correlated errors from overlapping training data, documented position bias). The paper acknowledges this (line 63) and defers to Appendix C, but the core experimental results are presented without diagnostic evaluation of how badly these assumptions are violated or how sensitive the methods are to violations. This limits the strength of conclusions for real LLM deployments.

5. **No variance or confidence intervals on accuracy numbers.** The simulated results (Table 2) report point estimates only. For real datasets, bootstrap confidence intervals would help assess the stability of the reported improvements over MV, especially given the modest gains. The t-statistics (line 303) are reported without degrees of freedom or p-values.

### Trivial

6. **t-statistics reported without degrees of freedom or p-values** (line 303), making the hypothesis test incomplete.

## Nice-to-Haves

- Clarify whether the ERM objective in Equation (7) is convex and whether the optimization is properly identified (i.e., whether different x vectors can produce the same second-order probabilities).
- The Single Best disclaimer ("not a fair baseline," line 287) is unnecessary and potentially confusing; Single Best is a natural sanity check for any aggregation method.
- Example 1 uses agents with accuracy exactly 1.0; a more realistic example with typical LLM accuracy values would be more informative.

## Removed Points

- **Abstract σ_K definition discrepancy (line 25 vs. line 73):** The abstract shows σ_K(x) = x²/(K-1+x²) while Section 3 shows σ_K(x) = eˣ/(K-1+eˣ). REMOVED as a likely parser artifact from superscript rendering; the Section 3 version is the correct one consistent with the Bayesian derivation.
- **Line 82 formatting issue** in algorithm pseudocode. REMOVED as a parser artifact.
- **Corollary 1 "overstating" BT model validation:** The harsh critic claimed this overstated the result, but the paper says "provides a theoretical justification for the validity of the BT model" (line 92), which is a reasonable statement given the connection shown. REMOVED as it misreads the paper's claim.
- **Missing related works:** REMOVED per policy (cannot verify external works).
- **Missing appendix/proof content:** REMOVED as these are stripped by the parser from all submissions.

## Novel Insights

The observation that SP's reliance on systematic overconfidence bias (effective for humans) backfires for LLMs, combined with the principled design of ISP as a counterfactual that inverts the conditioning to amplify a weaker signal, is a genuinely novel insight. Additionally, the derivation showing that Bayes-optimal aggregation under the random-shuffling model reduces to inverse-logistic weighting cleanly bridges classical information aggregation theory (Austen-Smith & Banks; Prelec et al.) and modern LLM ensemble methods, providing a theoretical foundation for why certain weighting schemes are optimal and when majority voting is sufficient (Corollary 2).

## Suggestions

1. **Resolve the OW-L/OW-I identity** — this is the single most important fix. If the two procedures genuinely produce identical predictions on every question, explain the theoretical or empirical conditions under which this occurs. If they do not, correct the reporting. Without this resolution, the empirical section cannot be taken at face value.
2. **Add at least one strong baseline** from the LLM ensemble literature—for instance, confidence-weighted voting using LLM token probabilities/logits (Chen et al., 2023a; Fu et al., 2025).
3. **Clarify the relationship between advantage and accuracy** in Theorem 2—either prove that advantage ordering implies accuracy ordering under the model, or explicitly state Theorem 2 as a result about advantage with accuracy validated empirically.
4. **Add bootstrap confidence intervals** to real-dataset results and complete the hypothesis test reporting.

## Score and Decision

The initial bracket (Round 1) placed this paper in the 5.0–6.0 range based on calibration against comparable papers: **SpecFuse** (avg 5.33, rejected) which has a similar empirical gap (missing baselines) but a weaker theoretical contribution; **Rethinking MoA** (avg 3.75, rejected) which had soundness concerns absent here; **Balancing Act** (avg 6.25, accepted) which had more comprehensive empirical analysis but less theory; and **ReConcile** (avg 6.00, rejected) which had uncontrolled confounds. Itemized comparison shows this paper shares the "missing baselines" weakness of SpecFuse (weight -4) and the "modest gains, limited baselines" pattern, but carries stronger theoretical grounding (+3 weight items absent in those anchors). The OW-L/OW-I identity issue is a major concern not present in any anchor, which prevents this paper from reaching the clear-accept range. Conversely, the theoretical contributions (Bayes-optimality proof, closed-form advantage expressions) are genuinely solid—stronger than the theory in any of the middle-range anchors. Weighting these factors, the score settles at **5.0**: the theoretical core is sound and the ISP idea is well-motivated, but the OW-L/OW-I identity and missing baselines prevent the empirical case from being convincing as submitted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>