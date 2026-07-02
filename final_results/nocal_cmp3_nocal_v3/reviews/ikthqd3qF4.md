## Summary

This paper proposes a method for evaluating unsupervised anonymous record linkage without ground-truth labels. The key insight is to exploit a structural constraint—an individual can originate at most one first-lien mortgage—to derive observable lower bounds on precision and relative recall from the rate of multiple-origination clusters. The method is instantiated with hierarchical clustering on HMDA mortgage data (65.5M applications) to detect "cross-applicants" who submit multiple applications. The preferred specification achieves an estimated 92.3% precision.

## Strengths

- **The core theoretical insight is genuinely clever and well-articulated.** The observation that clusters with multiple originations are *necessarily* false positives (since an individual can originate at most one first-lien mortgage), and that the rate of such clusters therefore bounds the false positive rate from below, is both simple and non-obvious. The intuition is clearly laid out in Section 2.2 (pp. 121–124), and the formal statement in Theorem 1 is precise. This is a nice example of turning a domain-specific constraint into a performance guarantee in an unsupervised setting.

- **The simulation provides a convincing sanity check under controlled conditions.** The close correspondence between Figures 3a (actual precision, requires ground truth) and 4a (implied precision bound, uses only observable quantities) demonstrates that the bound works as intended when its assumptions hold by construction. This is the strongest evidence in the paper.

- **The domain-agnostic framing is appropriate.** The paper correctly identifies that the structural constraint (one positive outcome per individual) applies beyond mortgages—insurance claims, college admissions, job offers, etc. (p. 13). The framework's generality is a genuine strength, and the paper does not overstate it.

## Weaknesses

### Fatal

None.

### Major

1. **Assumption 1 (independence of origination decisions across borrowers) is stated without defense or sensitivity analysis.** The bound Pr[False] ≤ Pr[Mult]/p² (Theorem 1, p. 115) relies on Lemma 1, which requires Assumption 1: origination decisions are independent across different borrowers (p. 63–65). In real mortgage data, this is unlikely to hold—origination outcomes are correlated through common interest rates, local housing market conditions, lender-specific underwriting criteria, and macroeconomic shocks. The paper asserts the assumptions "do not appear very strong to us" (p. 138) but provides no empirical justification, no discussion of when the bound would remain valid under dependence, and no simulation that relaxes this assumption to test robustness. If the assumption fails such that Pr[Mult|False] < p² (e.g., under negative correlation in origination outcomes), the bound could overstate precision. This is the most significant unresolved issue in the paper.

2. **The restriction to size-2 clusters substantially limits generality and is under-analyzed.** The paper states in footnote 4 (p. 186) that all results are based on clusters of size 2. This means: (a) the simplification Pr[Mult|False] = p² only applies to size-2 clusters; the generality of Theorem 1 does not translate to a practical bound for larger clusters; (b) the method cannot detect applicants who submit three or more applications, or if it does, the theoretical guarantees no longer apply; (c) the paper does not report how many clusters of size >2 are discarded, making it impossible to assess the practical significance of this restriction. The paper presents the framework as general but the actual implementation is limited, and the consequences of this gap are not quantified.

### Minor

3. **The recall bound is relative, not absolute, which limits what can be claimed.** Corollary 1 (p. 152–154) states Recall(θ) ≥ α̂(θ) N⁺(θ) / P_tot, where P_tot (the true number of cross-applicants) is fundamentally unobservable. The paper transparently notes that the bound is proportional to an observable quantity (p. 156) and correctly frames the contribution as bounding "relative recall." However, a 92% recall figure is mentioned in the simulation section (p. 216, where ground truth is known), and the abstract's phrasing ("only minimal loss in relative recall") is qualitative. A reader could easily miss that the recall bound is not numerically computable in the real-data application.

4. **No comparison against any baseline method.** The paper claims its bounds "enable both hyper-parameter tuning and cross-model comparisons" (p. 15) but does not compare its clustering approach to any alternative method for detecting cross-applicants—not even simple heuristic baselines. Without baselines, it is difficult to assess whether the reported 92.3% precision represents a meaningful advance or merely a calibrated lower bound for one specific algorithm.

5. **The partitioning step may systematically exclude certain cross-applicants.** The data is first partitioned on categorical variables including census tract, race, sex, and age (pp. 230–231). An applicant who applies for mortgages on two different properties in different census tracts, or whose reported income or credit score varies across applications, will be placed in different partitions or different clusters within a partition and can never be matched. The paper acknowledges this in footnote 5 but provides no quantification of how many cross-applicants might be missed or what selection bias this introduces.

### Trivial

- None of the formatting or small-presentation issues warrant inclusion.

## Nice-to-Haves

- **Relax or test the independence assumption.** A bound that holds under weaker dependence assumptions (e.g., bounded correlation), or a simulation showing how the bound degrades as correlation increases, would substantially strengthen the paper.
- **Validate a subset of real-data clusters manually or against external data.** Even a small-scale check (e.g., manual inspection of 100–200 clusters, or comparison against a credit bureau dataset with person-level identifiers) would greatly increase confidence that the 92.3% precision figure is meaningful.
- **Report the specific tuning parameters (distance function, weights, ε) for the preferred specification** to improve reproducibility.
- **Quantify the effect of restricting to size-2 clusters** by reporting how many larger clusters are discarded and discussing how the bound would change if they were included.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"The framing of 'unsupervised learning' is misleading"** — The method is unsupervised (no labeled training data required). Using observed origination outcomes (which are part of the data, not external labels) does not make it supervised. This is a strawman criticism.
- **"The step from Theorem 1 to Equation 1 is not fully justified"** — The paper explains this step clearly (p. 140–142): dropping known false positives (clusters with multiple originations) improves precision, and Equation 1 is the resulting bound. The derivation is straightforward.
- **"Distance function and weights not fully specified"** — Refers to Appendix B, which is stripped by the parser; the main text provides the distance function (weighted ℓ₂-norm, p. 69–71) and lists the five continuous variables used (p. 236). This is adequate for a conference paper.
- **"Specific tuning parameters for the preferred specification not reported"** — Partially about stripped appendix content; partially a reproducibility detail. Acknowledge as a nice-to-have.
- **"Reference to Elzayn et al. (2025) working paper"** — Not a weakness of the paper under review; the rule prohibits questioning the status of cited references.
- **"No code release mentioned"** — A reproducibility suggestion, not a scientific weakness.
- **"Real-data results not validated against ground truth"** — The paper's entire premise is that ground truth is unavailable in this setting. The simulation validates the method where ground truth exists. Asking for ground-truth validation in the real application contradicts the problem statement.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the core tension between the paper's clever theoretical contribution and the limited empirical validation, but do not add a novel analytical lens beyond what the paper itself provides.

## Suggestions

1. Add a simulation that relaxes Assumption 1 (e.g., introduce correlated origination outcomes) and show how the bound behaves—this would be the single most impactful addition.
2. Provide a small-scale manual validation or external-data validation of real-data clusters to increase confidence in the HMDA results.
3. Report the fraction of clusters of size >2 that are discarded, and discuss how the method could extend to larger clusters.
4. Add at least one simple baseline (e.g., exact matching on a subset of fields) to calibrate the 92.3% precision claim.
5. Clarify in the abstract and introduction that the recall bound is relative (scaled by unknown P_tot) and that the 92% recall figure applies to the simulation only.

## Score and Decision

The paper contains a genuinely novel theoretical insight and a compelling simulation. However, the two major weaknesses—the untested independence assumption and the underexplored size-2 restriction—prevent the empirical claims from being fully established. The paper would benefit from a substantive revision before acceptance. I lean toward rejection at this stage, with encouragement to address the major issues in a revision.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>