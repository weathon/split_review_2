Now I have comprehensive calibration data. Let me compile the final review.

**Calibration summary across all rounds:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| Du et al. 2024a (jlEjB8MVGa) - SAL | 6.50 | R1 | Yes | Most directly comparable paper; same setting (wild OOD, theory, 2-stage). Our paper has similar strengths but more numerous/more negative weaknesses. |
| GRIC (0owAtTCOlU) | 5.75 | R1 | Yes | Different approach (CLIP-based); our paper has weaker favorability on weaknesses. |
| NC-OOD (mUXdysoxEP) | 6.75 | R1 | Yes | Feature separation via NC; our weaknesses are more negative. |
| Semantic/Covariate (uWUovmBRUq) | 4.00 | R1 | Yes | More theoretical; weaker empirical component than our paper. |
| Pathologies (hlijRgXTDK) | 4.75 | R1 | Yes | Critical analysis paper; our empirical contribution is stronger. |
| GRDNORM (bcWwhF8cTZ) | 5.50 | R2 | Yes | Gradient-based OOD estimation; similar weakness severity to our paper. |

**Round-1 bracket:** 5.0–6.5
**Narrowing (Round 2):** Our paper's weakness favorability (-0.68 to 0.45) is slightly worse than the 5.50 anchor (GRDNORM: -4.35 to 4.35) but substantially worse than the 6.50 anchor (Du et al.: -4.90 to 5.56, with most >1). The key difference: our paper has multiple moderately negative weaknesses while the Du et al. anchor had one severely negative weakness and many mild ones. **Final score: 5.5.**

Now writing the review.

Here's my analysis of which criticisms to keep/remove:

**Keeping (as MAJOR):**
1. Missing Du et al. (2024a), CONJ, DRL comparisons - verified from paper (line 174 mentions them, but Tables 1&2 don't show them)
2. Dataset-level mixing claim unvalidated - verified from paper (line 258 makes the claim, but no experiment tests it)
3. Computational cost not addressed - verified (line 93 acknowledges cost but no analysis in main text)

**Demoting to MINOR:**
4. Theoretical bounds have large constants - This is a valid observation but many theory papers have loose bounds; the paper doesn't claim tightness
5. Predicted labels for OOD gradients not analyzed in main text - The paper defers to Appendix A.5; the main text gap is valid but minor since appendix exists
6. Favorable wild data setup - Valid point but common in this literature
7. Synthetic 2D experiment is too favorable - Valid but it's meant as an illustrative example, not a proof

**Removed per hard rules:**
- "Du et al. not yet released" - never claimed
- Missing appendix content - parser strips appendix
- Formatting/style issues - parser artifacts
- Strength #4 (broad baseline comparison) - conflicts with verified weakness about missing baselines

Let me finalize.## Summary

This paper introduces Medix, a framework for out-of-distribution (OOD) detection that uses the element-wise median (EWM) of gradients to filter OOD samples from unlabeled wild data. The method operates in two stages: (1) a greedy iterative algorithm that identifies candidate OOD samples by measuring how each wild sample's removal shifts the EWM gradient away from a clean InD reference, and (2) training a binary OOD detector on the filtered outliers plus labeled InD data. The paper provides theoretical bounds on both inlier and outlier misclassification rates and reports strong empirical results on CIFAR-10 and CIFAR-100 across multiple OOD test sets.

## Strengths

- **Novel and well-motivated method.** The paper introduces a genuinely non-trivial idea: using the element-wise median of gradients as a robust reference to separate InD from OOD samples in unlabeled wild data. The motivation experiment (Figure 1) showing a monotonic increase in L2 deviation as OOD samples are added provides a clean, actionable signal that directly informs the algorithm's stopping criterion. **[favorability=9.39]**

- **Strong empirical results on CIFAR-10.** Medix achieves an average FPR95 of 0.80% (vs. WOODS at 3.40% and OE at 6.16%) with tiny standard errors. On individual OOD datasets like LSUN-C and LSUN-RESIZE, it achieves near-perfect FPR95 of 0.01%. These results go beyond incremental improvement. **[favorability=10.45]**

- **Two-sided theoretical analysis.** The paper provides provable bounds on both inlier misclassification (InD flagged as OOD) and outlier misclassification (OOD kept as InD), which is more complete than most comparable papers. Identifying three driving effects — contamination, concentration, and separation — gives a useful conceptual framework for understanding when median-based filtering works. **[favorability=10.93]**

## Weaknesses

### Fatal
None.

### Major

- **Missing empirical comparison with the most directly comparable prior work (Du et al., 2024a).** The paper repeatedly cites Du et al. (2024a) as "the only work that provides such a foundation for the 'in-the-wild' setting" and explicitly follows its detector training protocol. Yet Du et al. (2024a) does not appear as a baseline in Tables 1 or 2, nor are its results reported anywhere. Since the filtering stage is the paper's main contribution, the reader cannot assess whether the median-based approach improves over Du et al. (2024a)'s thresholding method. The conclusion also claims Medix "outperformed state-of-the-art methods such as WOODS and DRL" — but DRL (Zhang et al., 2024) and CONJ (Peng et al., 2024), listed as baselines in Section 5.1, also do not appear in any results table. The paper claims "20 competitive baselines" (contributions and Section 5), but only 13 baselines actually appear in the result tables. **[favorability=-0.68]**

- **The claimed advantage of "dataset-level mixing" over "batch-level mixing" is not experimentally validated.** Section 6 (Related Work) claims that WOODS and Du et al. (2024a) "operate under the assumption of batch-level mixing, where each batch has a set ratio of InD and OOD samples" while Medix "addresses this by enabling dataset-level mixing without relying on batch-level structure." However, the experimental setup uses the same fixed mixing proportion π = 0.5 as WOODS. No experiment tests Medix under genuinely random (non-batched) mixing or compares Medix against baselines under such conditions. This claimed advantage is unsubstantiated by the evidence presented. **[favorability=-0.36]**

- **Algorithm 1's computational cost is not addressed in the main text.** The greedy leave-one-out algorithm requires, at each iteration, computing the element-wise median of gradient vectors for S \ {i} for each remaining sample i. For a wild set of ~25,000 samples (CIFAR-100 setup) and penultimate-layer gradients of at least thousands of dimensions, the algorithm as stated is O(T · |S|² · d). The paper defers all efficiency discussion to Appendix A.6 but claims "robustness and efficiency" in the main text without giving the reader any sense of runtime. The hyperparameter k ∈ {4k, 7k, 10k, 20k} removes up to 20,000 samples in a single iteration — calling this "leave-one-out" is misleading when k >> 1. **[favorability=-0.12]**

### Minor

- **The theoretical bounds carry large constants that limit practical informativeness at the operating point used.** Theorem 4.1's inlier misclassification bound includes a contamination term π/(2(1−π)). At π = 0.5 (the experimental setting), this term alone equals 0.5, meaning the bound allows up to ~50% of InD samples to be misclassified as outliers. Theorem 4.2's outlier bound has a symmetric issue with (1−π)/(2π) = 0.5. While the bounds are technically valid and the paper does not claim tightness, the abstract and introduction characterize the guarantees as showing Medix "achieves a low error rate" and errors "remain manageable," which overstates what the theory proves at the experimental operating point. **[favorability=0.45]**

- **The use of predicted labels for OOD sample gradients is not analyzed in the main text.** The gradient for a wild sample uses its predicted label ŷ from the InD classifier (Equation 4, Algorithm 1). For OOD samples, this predicted label is inherently unreliable — the InD classifier has no basis for classifying an OOD sample. The paper defers analysis of this mechanism to Appendix A.5 (stripped from the review copy), but the main text provides no justification for why gradients computed with unreliable predicted labels remain systematically separable. **[favorability=0.43]**

- **The wild data setup is favorable and may not generalize.** The InD portion of the wild mixture comes from the same CIFAR dataset as the training data (first 25k images for training, remaining for wild mixture). Real-world wild data typically has covariate shift relative to the labeled training set (different sources, collection conditions). The paper does not test this scenario. **[favorability=0.03]**

- **The synthetic 2D experiment (Figure 2) uses an extremely favorable setup.** The OOD mean is at [20, 2√3] while InD means are within [-2, 2] on the x-axis — a 10× separation. Citing this experiment's 12.5% error rate as evidence of "low error rate" without caveats about the favorable separation overstates the demonstration's value for the natural image setting. **[favorability=0.11]**

### Trivial
None.

## Nice-to-Haves
- An intuitive explanation or ablation in the main text for why computing gradients with predicted labels (rather than ground-truth labels) is effective for OOD separation.
- A brief wall-clock runtime or complexity statement in the main text so readers can assess practical viability.
- An experiment with covariate-shifted wild data (wild InD portion from a semantically similar but distinct distribution).

## Removed Points
These points were raised in the input review but removed after cross-checking against the paper:
- **"Comparison with KNN+ is unfair because Medix uses wild data"** — REMOVED: The paper presents both categories separately (Using P_in only vs Using P_in and P_out) and follows standard practice of comparing against all relevant methods. The categories are clearly separated in the tables.
- **"Du et al. (2024a) not yet released"** — REMOVED per hard rule: the paper cites it; it exists.
- **"Formatting/style/typos"** — REMOVED per hard rule: parser artifacts, not author errors.
- **Strength #4 from input ("Broad baseline comparison")** — REMOVED: this conflicts with the verified weakness that Du et al. (2024a), CONJ, and DRL are missing from the results tables.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Add Du et al. (2024a), DRL, and CONJ to the main results tables.** Without these numbers, the claim of "outperforming all baselines" is incomplete, and the most informative comparison (median-based vs. threshold-based filtering in the same setting) is absent.
2. **Validate the dataset-level mixing claim directly.** Design an experiment where batch-level mixing is violated (variable π across batches, or mixing structure unknown) and compare Medix against WOODS under that condition.
3. **Add complexity analysis to the main text.** Even a brief statement of O(T·|S|²·d) complexity and wall-clock time for the reported experiments would help readers judge scalability. Clarify the relationship between the "leave-one-out" framing and the aggressive k-sample-per-iteration removal.
4. **Tone down the characterization of the theoretical guarantees.** Acknowledge that at π=0.5 the contamination terms dominate the bound, and state clearly that the bounds are worst-case and not necessarily tight.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| jlEjB8MVGa.md (Du et al. 2024a - SAL) | 6.50 | R1 | Yes | Most directly comparable: same wild-OOD setting with theory. Our paper has similar methodological novelty but more numerous/more negative weakness favorability scores. |
| bcWwhF8cTZ.md (GRDNORM) | 5.50 | R2 | Yes | Gradient-based OOD method. Weakness severity distribution broadly comparable to our paper. |
| mUXdysoxEP.md (NC-OOD) | 6.75 | R1 | Yes | Strong strengths; our paper's weaknesses are more negative by comparison. |
| 0owAtTCOlU.md (GRIC) | 5.75 | R1 | Yes | CLIP-based OOD; our paper's weaknesses have lower favorability. |
| uWUovmBRUq.md (Semantic/Covariate) | 4.00 | R1 | Yes | More theoretical, weaker empirical contribution than our paper. |
| hlijkRgXTDK.md (Pathologies) | 4.75 | R1 | Yes | Critical analysis; our paper has stronger empirical contribution. |

**Round-1 bracket:** 5.0–6.5  
**Narrowing (Round 2):** The Du et al. anchor (6.50) has mostly positive weakness favorability (1.29–5.56) with one severe negative (-4.90). Our paper has 4 negative weaknesses (-0.68, -0.36, -0.12, 0.45) — a broader spread of moderate concerns. The GRDNORM anchor (5.50) has similar weakness distribution with a few severe negatives. Our paper sits between these: above GRDNORM due to stronger strengths (method novelty, two-sided theory) but below Du et al. due to the missing direct comparison and unvalidated claims.

The paper introduces a well-motivated, novel method with strong results and two-sided theory, but is undercut by three significant evaluation gaps: missing the most directly comparable baseline (Du et al., 2024a), an unvalidated claimed advantage over prior work, and unaddressed computational cost. These are fixable issues but substantially weaken the paper's central empirical claims in its current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>