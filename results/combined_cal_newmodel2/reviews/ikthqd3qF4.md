Now I have sufficient calibration data. Let me write the final consolidated review.

**Score anchoring summary:**

| Anchor | Score | Round | Itemized? | Comparison |
|--------|-------|-------|-----------|------------|
| Fréchet bounds for PWS validation | 5.50 | R1 | Yes | Same goal (bounds without labels); our paper has cleaner theory, stronger simulation validation, and real HMDA application → above |
| Domain constraints improve risk prediction | 7.25 | R1 | Yes | Similar use of domain constraints for inference; our paper has comparable theory but suffers from overclaiming and under-discussed limitations → below |
| Learning from weak labelers as constraints | 6.50 | R1 | Yes | Both use constraints for bounds; our paper's approach is more domain-specific and better validated |
| Imprecise Label Learning | 6.00 | R1 | Yes | Both address label-free evaluation; mixed reviews suggest similar quality tier |
| Guaranteed Error for Learned DB Ops | 6.00 | R2 | No | Both provide theoretical guarantees; similar score tier |
| αMax-B-CUBED | 4.75 | R1 | Yes | Cluster evaluation metric paper with limited experiments → our paper is stronger |

**Round-1 bracket:** 5.5–7.0 (above Fréchet bounds at 5.50, below Domain Constraints at 7.25)

**Narrowing:** Comparing itemized favorability: our draft's strengths (9.96–12.77) rival the Domain Constraints anchor's strengths (5.66–12.17), but our two lowest-favorability weaknesses (0.11 for the size-2 restriction, 1.29 for the abstract overclaim) are more severe than any individual weakness in that anchor's profile. The Fréchet bounds anchor (5.50) had numerous weaknesses below 4.0 and fundamental concerns about its assumptions. Our paper sits between these: a stronger theoretical contribution than Fréchet bounds, but with more serious presentation issues than Domain Constraints. **Final score: 6.0 (borderline accept).**

---

## Summary

This paper introduces a novel method for evaluating unsupervised record linkage without labeled data. The key idea exploits a structural constraint (individuals can originate at most one first-lien mortgage) to derive an observable lower bound on precision: Pr[False] ≤ Pr[Mult]/p² (Theorem 1). The authors instantiate this using agglomerative clustering on 65.5M HMDA mortgage applications, reporting 92.3% estimated precision at their preferred specification. The theoretical framework is method-agnostic and applicable beyond mortgages to any setting where a per-individual cap on positive outcomes exists.

## Strengths

- **Novel theoretical core.** Theorem 1 (Pr[False] ≤ Pr[Mult]/p²) provides an observable lower bound on precision that requires no labeled data, only the structural constraint that an individual can originate at most one loan. This is a genuinely clever and clean contribution. [favorability=12.77]

- **Simulation validates bound tightness.** Figure 4a closely tracks Figure 3a: the inferred precision bound (93.7% at ε=0.06) nearly matches the ground-truth precision (~95%) under the simulation's generative assumptions, demonstrating the bound is not overly conservative. [favorability=10.99]

- **Practical significance of the HMDA application.** The HMDA dataset is widely used in economics and finance and critically lacks person-level identifiers. Identifying cross-applicants at 92.3% estimated precision without labels is genuinely useful for downstream research on mortgage market fairness, shopping behavior, and lending standards. [favorability=10.77]

- **Computational scalability.** Using nearest-neighbor chain agglomerative clustering (O(ℓ²)) via fastcluster makes the method feasible for 65.5M applications — a meaningful engineering contribution. [favorability=9.96]

## Weaknesses

### Fatal
None.

### Major

- **Abstract overclaims recall observability in the HMDA application.** The abstract states the method identifies cross-applicants "with only minimal loss in relative recall." However, the recall bound (Corollary 1) depends on P_tot (the unknown true number of cross-applicants) and is not numerically estimable in the real application. The 92% recall figure reported at line 216 comes from the simulation where ground truth is known. The abstract conflates an observable precision bound with an unobservable absolute recall, giving a misleading impression of what the method delivers in practice. [favorability=1.29]

- **Restriction to size-2 clusters is a substantive limitation buried in a footnote.** Footnote 4 (line 186) states all results are based on clusters of size exactly 2. This means individuals who submit 3+ applications are systematically excluded. The paper does not report how many size>2 clusters arise in the data, discuss the rationale for excluding them, or address the unit mismatch: an individual with 3 applications can generate up to 3 choose 2 = 3 clusters, so cluster-level metrics do not cleanly map to individual-level concepts. The generalizability of findings is conditional on a potentially non-random subpopulation. [favorability=0.11]

### Minor

- **Notational inconsistency in Equation (1).** The text introduces Equation (1) as "a new lower bound on the precision of our algorithm" (line 140), but the left-hand side writes Pr[False] — the false-positive rate defined at line 109. The right-hand side (1 − Pr[Mult]/p²)/(1 − Pr[Mult]) is indeed a lower bound on precision (as confirmed by its use as α̂(θ) in the corollaries), so the LHS notation is incorrect. This will confuse readers. [favorability=5.65]

- **Assumption 1 (independence of origination decisions across borrowers) is strong and insufficiently defended.** The paper dismisses it with "which do not appear very strong to us" (line 138) without discussing that interest rate cycles, regional housing markets, and macroeconomic shocks create correlation. The bound remains conservative under positive correlation (as the paper's Lemma 1 suggests), so violations do not invalidate results. But the lack of any sensitivity analysis or discussion of plausible violation magnitudes leaves the defense incomplete. [favorability=5.74]

- **The HMDA application does not report the origination rate p̂.** The bound depends critically on p² in the denominator — if origination rates are very low, the bound becomes trivially close to 1. The simulation reports p̂=0.7917, but p̂ is absent for the HMDA data, making it impossible to assess how informative the bound is in the real application. [favorability=4.13]

- **The paper does not report how many clusters were dropped due to containing multiple originations** at the preferred specification. This is the key empirical quantity determining the gap between the raw and improved precision bounds. [favorability=6.18]

- **The definition of "individual" as "borrower-property pair" (line 39)** means the method only captures same-property shopping, not general mortgage shopping across different properties. This limitation is stated once in Section 2 but not revisited in the conclusion, where language becomes more expansive ("cross-applicants" generally). [favorability=4.18]

### Trivial
None.

## Nice-to-Haves
- A comparison with a simple baseline (e.g., exact matching on discretized continuous variables) would help contextualize the 92.3% precision claim, though the paper's primary contribution is the bounding framework, not achieving SOTA.
- A sensitivity analysis of how the bound changes under plausible violations of Assumption 1 (e.g., introducing cross-borrower correlation at various levels) would strengthen the paper.

## Removed Points
These points from the input review were excluded after verification:
- "No comparison with alternative record-linkage approaches": The paper's contribution is the bounding framework; absence of a baseline comparison is not a flaw given the novel theoretical focus.
- "No error bars/confidence intervals": Standard practice for large-scale applications; standard errors at this scale would be negligible.
- "Confidential data not reproducible": The paper clearly acknowledges using confidential HMDA data; this is a standard data-access limitation, not a paper flaw.
- "Complete linkage choice not explained": The paper's focus is the bounding framework, not clustering algorithm optimality; this is a reasonable methodological choice.
- "Dropping withdrawn applications could exclude cross-applicants": A reasoned data-cleaning choice; the paper need not trace every exclusion criterion's effect on every subpopulation.
- "Novelty claim against Fellegi-Sunter should be more carefully scoped": The critic speculates about prior work without showing a specific error in the paper's novelty claim.
- "Simulation sensitivity to application rate": The 1.25 expected applications per individual is a realistic parameterization; requesting additional sensitivity analysis here is a nice-to-have, not a weakness.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Fix the abstract.** Distinguish clearly between the precision bound (observable) and recall (only rank-orderable via its bound, not absolutely estimable). Remove or qualify the "minimal loss in relative recall" claim for HMDA.
2. **Move the size-2 restriction out of the footnote into the main text.** Report the prevalence of size>2 clusters in the data, discuss why they are excluded, and address the cluster-to-individual unit mismatch.
3. **Correct Equation (1)'s left-hand side** to indicate it bounds precision (or 1 − Pr[False after dropping]), not Pr[False].
4. **Report p̂ and the number of dropped multi-origination clusters** for the HMDA application.
5. **Discuss Assumption 1 more carefully**: acknowledge that violations (e.g., correlated originations) would make the bound more conservative, and briefly explain why this does not threaten the method's validity.
6. **Revisit the "individual" definition in the conclusion** to avoid over-generalizing from same-property to all cross-applicant detection.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>