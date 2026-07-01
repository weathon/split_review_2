Now let me finalize with the complete review.

**Round 1 bracket**: Based on calibration anchors, I initially bracket this paper between 5.5 and 7.5. Papers at ~4.75 (αMax-B-CUBED) have weaker empirical validation; papers at ~6.0 (SSME, Guaranteed Error) have similar theory+application structure; papers at ~7.0-8.0 (M3C, STKR) have deeper theoretical contributions or more thorough evaluation. This paper sits in the upper-middle of that range — the core idea is more novel than the 6.0 papers, but the presentation gaps narrow the gap.

**Narrowing**: The paper has no fatal flaws, and its weaknesses are fixable. The closest comparable is the SSME paper (6.00, rejected due to related work omissions) and the Guaranteed Error paper (6.00, accepted despite limited empirical scope). The current paper has stronger novelty than both. I settle at **6.5**.

**Calibration Anchors** (all rounds):
1. P49gSPmrvN (1.00, R1) — Not comparable; trivial method paper.
2. 5lUdTogEL3 (1.00, R1) — Not comparable.
3. oyFCgkkLUK (4.75, R1) — Clustering evaluation metric; less empirical validation than current paper.
4. HvkXPQhQvv (6.00, R1/R2) — SSME, similar evaluation-without-labels framing, but the current paper has more novel theory.
5. ptCIlV24YZ (5.80, R1) — Image clustering; accepted but contributions seen as incremental. Current paper is more novel.
6. 6tqgL8VluV (6.00, R1) — Guaranteed Error for DB ops; similar theory+empirical structure. Current paper comparable.
7. AXC9KydyZq (7.00, R2) — M3C graph matching; stronger experiments. Current paper slightly weaker.
8. OeQE9zsztS (8.00, R1) — STKR; much deeper theory. Current paper not at this level.

Here is the final review:

## Summary

The paper proposes an unsupervised method for evaluating record linkage (specifically, detecting "cross-applicants" who submit multiple mortgage applications) by exploiting a structural constraint: an individual can originate at most one first-lien mortgage. This yields observable lower bounds on precision and relative recall that require no labeled data. The bounds are derived theoretically (Theorem 1, Corollaries 1-2), validated on simulated data, and demonstrated on 65.5 million HMDA mortgage records (2018-2023), achieving an estimated 92.3% precision on 314,344 detected clusters.

## Strengths

1. **The core theoretical idea is genuinely novel and well-motivated (Section 2.2).** The insight that a structural constraint — a person can originate at most one first-lien mortgage — yields an *observable* lower bound on precision is clever. The bound depends only on two observable quantities (the unconditional origination probability p and the rate of multi-origination clusters). This is a genuine advance over existing unsupervised record linkage evaluation, which typically relies on labeled data or heuristics with no formal guarantees.

2. **The simulation validates that the bound closely tracks true precision (Figures 3a vs. 4a, Section 3.1).** In the simulated data, where ground truth is known, the estimated precision bound (Figure 4a) closely matches the true precision (Figure 3a) across the full ε range. This is the strongest evidence that the method works as claimed.

3. **The method-agnostic framing is appropriate (Theorem 1, Corollaries 1-2).** The bounds apply to *any* algorithm that generates predicted labels, not just the specific clustering approach used here. They depend only on predicted labels and the origination outcome.

4. **The HMDA application is large-scale and practically relevant (Section 4).** The dataset covers 65.5 million mortgage applications with a clear real-world need for identifying cross-applicants (fairness measurement, lending standard monitoring, shopping behavior research).

## Weaknesses

### Major

1. **The abstract overclaims recall for the HMDA application, where recall is not directly estimated.** The abstract states: "Our preferred specification identifies cross-applicants with 92.3% precision with only minimal loss in relative recall." The 92.3% precision is estimated from HMDA data using the bound. However, "minimal loss in relative recall" is supported only by the simulation (92% recall at ε=0.06, line 216), where ground truth is available. The recall bound (Corollary 1) depends on P_tot — the true number of cross-applicants — which is unknown in the HMDA data. The paper cannot compute a numeric recall value for the real application. The abstract and conclusion should clearly separate what is demonstrated in simulation (the bound works and recall can be high) from what is estimated in the real data (only precision is bounded).

2. **The preferred specification parameters are not reported.** The paper considers 96 combinations of distance functions and ε values, selects one as the "knee" of the frontier (Figure 5), but does not report which distance function, ε value, or weight vector produced the chosen point. Line 238 states: "We consider a total of 96 combinations… and select the best combination based on an accuracy-sample size trade-off." Without reporting the specific parameters, another researcher cannot verify the optimality claim or apply the same selection procedure to other datasets. The paper should report the specific distance function, ε, and weight vector for the preferred specification.

3. **Missing: the empirical origination rate p̂ for the HMDA data and handling of missing values.** The bound's tightness depends on p². The paper reports p̂ = 0.7917 for the simulation (line 182) but does not report this quantity for the HMDA data. Since the bound is precision ≥ 1 − Pr[Mult]/p², knowing p̂ is essential for assessing the credibility of the 92.3% estimate. Additionally, the paper does not discuss how missing values in income, credit score (fico), or LTV are handled (line 236 lists these as clustering variables). Given 65.5M records, missing data is almost certain and could substantially affect clustering and bound computation.

### Minor

4. **The refinancing/multi-origination concern over the 2018–2023 window is not discussed.** The bound relies on Pr[Mult|¬False] = 0 (line 132): a true cluster cannot have multiple originations because "an individual can originate at most one loan." Over a six-year window, a person could originate a purchase mortgage and later refinance it (two first-lien originations for the same property). If both applications fell into the same cluster, Pr[Mult|¬False] > 0 and the bound would not be guaranteed. The paper partitions by loan purpose (line 230), which separates purchase from refinance applications, so this specific scenario is avoided. However, the paper does not discuss this concern explicitly, and it is unclear whether other scenarios (e.g., first-lien home equity products with the same loan-purpose code as purchase mortgages) could arise. An explicit discussion would strengthen the paper.

5. **The selection bias from dropping multi-origination clusters is not discussed.** The paper drops clusters with multiple originations (known false positives) to improve the bound (Equation 1, line 140-142). This is sensible for improving precision, but the paper does not discuss whether the dropped clusters differ systematically from kept ones. For downstream applications (e.g., measuring fairness across demographic groups), if dropped clusters are systematically different from kept ones, the composition of the final sample could be biased.

6. **No comparison to alternative unsupervised tuning baselines.** The simulation shows that the bound tracks true precision, but does not compare bound-based tuning to any alternative unsupervised strategy (e.g., silhouette score, gap statistic, or fixed ε). This limits the ability to assess how much practical benefit the bound provides over simpler heuristics.

### Trivial

- None.

## Nice-to-Haves

1. A sensitivity analysis showing how the precision bound changes if p is varied by ±5% or ±10% would substantially strengthen the empirical section.
2. Brief positioning against related work on unsupervised record linkage evaluation (e.g., Fellegi-Sunter model, EM-based methods, capture-recapture approaches) would strengthen the claim of being "first work to derive observable lower bounds" (line 15).
3. A simulation with heavier-tailed application counts and lower origination probabilities would test the bound's robustness under more challenging conditions.

## Removed Points

- **Issue 4 from harsh critic (cluster-level vs. pair-level precision):** The paper explicitly restricts to size-2 clusters (footnote 4: "we drop all clusters with more than two applications in both our simulation results and our application"), so cluster-level and pair-level precision coincide. The remaining concern about individuals with 3+ applications is acknowledged but minor.
- **"Unfair comparison" criticisms:** None raised; all comparisons in the paper are within-method (varying ε/distance), not against external methods.
- **Complete-linkage motivation (Section 2.1):** This is a presentation preference, not a flaw — the paper uses complete linkage because the cluster definition requires d(xⱼ, xⱼ') ≤ ε for *all* pairs within a cluster, which is correctly implemented by complete linkage.
- **Formatting nitpicks, missing related work references:** Parser artifacts and issues outside the paper's stated scope.
- **Reproducibility concerns about large artifacts:** HMDA data restrictions and the computational scale make full reproduction impractical but do not affect correctness.

## Novel Insights

The review process surfaces one genuinely novel observation: the paper's theory is strong enough that the authors could convert the "missing details" from weaknesses into positive evidence. For instance, reporting p̂ for HMDA and showing the bound under a range of p values would turn a transparency gap into a robustness demonstration. The refinancing concern, while ultimately addressed by the partition design, is worth surfacing because it reveals a subtlety about multi-year panels that the paper's framing (single-origination constraint) elides — and addressing it explicitly would strengthen rather than weaken the paper.

## Suggestions

1. **Revise the abstract and conclusion** to state that "recall is validated in simulation and the bound enables relative recall comparisons across specifications; a precise numeric recall for HMDA is not directly estimated" rather than implying recall has been measured in the real data.
2. **Report the specific distance function, ε, and weight vector** for the preferred specification, along with the empirical origination rate p̂ for the HMDA data.
3. **Add a paragraph discussing missing data handling** for the continuous clustering variables (income, credit score, LTV).
4. **Explicitly discuss the refinancing scenario** and explain why the partition-by-loan-purpose design prevents it from violating Pr[Mult|¬False] = 0.
5. **Add a sensitivity analysis** showing how the precision bound varies with p.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>