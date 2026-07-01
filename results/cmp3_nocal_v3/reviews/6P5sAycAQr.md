Now let me produce the final review.

## Summary

DefNTaxS proposes a training-free framework that uses LLMs to group image classes into taxonomic subcategories and integrate this grouping information into CLIP prompts for zero-shot classification. The method costs \$0.38 in API calls, requires no model retraining or manual prompt engineering, and reports consistent accuracy improvements across seven benchmarks (+5.5% average gain over vanilla CLIP, +2.44% over D-CLIP).

## Strengths

1. **Clear problem framing.** The paper correctly identifies that class label ambiguity (e.g., "boxer" as dog breed vs. combat sport) is a genuine limitation of zero-shot CLIP classification, and articulates why existing methods (D-CLIP's isolated descriptors, CHiLS's rigid hierarchies) do not fully address this (Section 1, lines 23–27).

2. **Practical engineering achievement.** The method costs \$0.38 in LLM API calls to generate all prompts across all benchmarks, requires no training data, no model modification, and no manual prompt engineering, making it immediately deployable for practitioners.

3. **Consistent positive results across diverse benchmarks.** DefNTaxS improves over vanilla CLIP on all benchmarks (Table 1), with the largest gains on EuroSAT (+13.0%) and Oxford Pets (+8.2%). It achieves the best accuracy on 5 of 7 core benchmarks.

4. **Well-designed ablations investigate the mechanism.** Section 6 probes the contribution of different components: comparing against k-means clustering (Table 5), testing reduced taxonomic refinement (Table 2), and—most informatively—replacing semantic content with random characters to isolate differentiation from semantics (Table 4). The ablation includes standard errors across 5 iterations.

## Weaknesses

### Fatal
None.

### Major

1. **The paper's strong semantic claims are undermined by its own ablation evidence.** The paper asserts that "taxonomic context is not just helpful but *essential* for robust zero-shot classification" (lines 31, 179) and that it is "a fundamental requirement" (line 293). However, Table 4 shows that WaffleTaxS—which replaces taxonomic subcategory labels with *random characters* while keeping class descriptors—performs comparably to DefNTaxS on ImageNet (63.24 vs. 62.96, within error bars), CUB (53.65 vs. 53.59), and Places (40.05 vs. 39.34, where W-TaxS is higher). This demonstrates that the *differentiation structure* (any unique per-class string), not the *semantic content* of the taxonomic labels, may be driving a substantial portion of the improvement. The paper acknowledges this obliquely in Section 6.1.3 ("the ability to differentiate between classes is crucial for performance, even without interpretable semantic content") but does not reconcile this with the strong framing in the abstract, introduction, and conclusion. The central claim needs to be reframed from "taxonomic semantics are essential" to "structured prompt differentiation improves accuracy, and taxonomic grouping provides a principled way to generate such structure."

2. **No statistical uncertainty on main results (Table 1).** Table 1 reports single numbers without standard errors or confidence intervals for the primary results supporting the paper's headline claims. Given that the method involves multiple stochastic LLM calls whose outputs can vary, the reader cannot assess whether gains of +0.16 on Places (40.00 vs. 39.84 for D-CLIP), +0.48 on ImageNet, or +0.66 on ImageNetV2 are statistically meaningful. The ablation (Table 4) *does* provide mean and standard error across 5 iterations, making the omission in the main experimental results conspicuous.

3. **EuroSAT's large gain comes from a qualitatively different mechanism.** EuroSAT has only 10 classes—below the 20-class threshold in Section 3.3—so per the paper's own protocol, "we use the dataset name as the single subcategory context (e.g., 'EuroSAT dataset')" (line 99). The "taxonomic context" here is a domain label, not a discovered taxonomic grouping. This mechanism (a strong domain prior telling CLIP "this is satellite imagery") differs from the lateral semantic grouping applied to larger datasets. EuroSAT's +9.86% gain over D-CLIP accounts for roughly 40% of the total improvement across all datasets. If EuroSAT is excluded, the average gain over D-CLIP drops from +2.44% to approximately +1.61%.

### Minor

4. **Inconsistent bold formatting in Table 1.** DefNTaxS values are bolded on Food (81.48) and Places (40.00), but CHiLS achieves higher scores on both (83.53 and 40.45, also bolded). This is confusing and could mislead a casual reader about which method is best on each benchmark.

5. **Imprecise result description.** Line 197 claims "highest accuracy across six of seven benchmarks," but DefNTaxS wins on 5 of 7 core benchmarks (IN, CUB, Pets, DTD, ESAT), losing on Food and Places. The same sentence claims DefNTaxS "usually outperform[s] the third place by a reasonable margin"—on Places DefNTaxS is itself 3rd with a 0.09 margin over 4th, which does not fit the description.

6. **No per-class or confusion-matrix analysis.** Given that the method's motivation is disambiguating specific ambiguous classes, the paper would benefit from showing where DefNTaxS helps most (and possibly hurts). The modest aggregate gains make it difficult to tell whether improvements concentrate on the ambiguous cases the method targets.

7. **Prompt length / context window interaction not tested.** Section 6.1.2 invokes CLIP's ~20-token effective context window (Zhang et al., 2024) to explain degraded performance when taxonomic subcategory descriptors are added. But DefNTaxS prompts use 20–30 tokens, meaning the taxonomic context appended at the end may already fall outside this effective window in the standard configuration. The paper raises this possibility but does not test it.

### Trivial
None.

## Nice-to-Haves

- A controlled experiment testing whether taxonomic labels systematically outperform random strings specifically on known ambiguous class pairs, which would help salvage the semantic claim.
- A cleaner k-means comparison (Table 5) where the LLM also labels the k-means clusters, isolating the LLM's contribution to clustering vs. labeling.
- Investigation of how prompt length and token position interact with CLIP's effective context window (e.g., by truncating prompts or moving taxonomic context earlier).

## Removed Points

The following points from the input review were removed after verification:

- **"DefNTaxS is fourth on Places"** — Removed because DefNTaxS (40.00) is actually 3rd on Places behind CHiLS (40.45) and W-CLIP+conc (40.22), not 4th. The reviewer miscounted. However, the underlying concern about imprecise language is retained in Minor #5.

- **"On Food, DefNTaxS is third"** — Removed because DefNTaxS (81.48) is actually 2nd on Food behind CHiLS (83.53), ahead of W-CLIP+conc (81.25). The reviewer miscounted.

- **"Section 1's third point about understanding what a class is *not* is never directly operationalized"** — Removed because the paper's method does address this through taxonomic context that helps differentiate classes; this is scope creep for a specific design choice.

- **"No theoretical basis for 20-class threshold"** — Removed as scope creep. Many heuristic thresholds in empirical ML papers lack deep theory, and the paper cites empirical analysis in the appendix.

- **"The k-means comparison conflates two variables"** — Removed because the comparison is still informative as-is; having the LLM also label k-means clusters would be a nice-to-have additional experiment, not a flaw of the existing one.

## Novel Insights

None beyond the paper's own contributions. The key tension (differentiation vs. semantics as the driver of improvement) is surfaced by the paper's own WaffleTaxS ablation and also noted in prior work (WaffleCLIP). The reviews do not contribute additional novel insights beyond this.

## Suggestions

1. Reframe the central claim to honestly reflect what the ablation evidence shows: structured prompt differentiation improves accuracy, and taxonomic grouping provides a principled, automated way to generate such structure. Drop the "essential"/"fundamental" language from the abstract, introduction, and conclusion.
2. Report standard errors for all main results (Table 1) across multiple runs, and indicate which differences are statistically significant.
3. Fix the bold formatting in Table 1 so that only the best-performing method per column is bolded.
4. Add a per-class analysis or confusion matrices for at least one benchmark (e.g., EuroSAT or ImageNet) to show where the method's improvements are concentrated.
5. Correct the "six of seven benchmarks" claim to reflect the actual count (5 of 7).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>