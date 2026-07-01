Now I have thoroughly verified all the claims against the paper. Let me write the final consolidated review.

## Summary

This paper proposes DefNTaxS, a fully automated pipeline that uses an LLM to partition a dataset's classes into semantic subcategories (e.g., "birds of prey" vs. "water birds") and then augments CLIP zero-shot classification prompts with both class-level descriptors and this taxonomic context (e.g., "golden retriever, which has long fur, a type of dog"). The method requires no model retraining, costs $0.38 in total LLM inference, and is evaluated on 8 standard benchmarks. The core claim is that taxonomic semantic context is "essential" for robust zero-shot classification.

## Strengths

1. **Practical, fully automated pipeline.** The method requires no manual prompt tuning, no model retraining, and costs only $0.38 in LLM inference across all datasets (Section 4.2). This is a genuine practical advantage over approaches that require hand-crafted templates or fine-tuning.

2. **Broad and standard evaluation.** The paper evaluates across 8 benchmarks (ImageNet, CUB, Oxford Pets, DTD, Food101, Places365, EuroSAT, ImageNetV2) and compares against 7 baselines including D-CLIP, CuPL, WaffleCLIP, CHiLS, and CGPT-P (Table 1). DefNTaxS achieves the highest accuracy on 6 of 7 main benchmarks, with especially large gains on EuroSAT (+13.0% over CLIP).

3. **Clean ablation design.** The controlled ablations in Section 6.1.3 (W-TaxS removing taxonomic semantics, TaxCLIP removing descriptor semantics) are well-designed to isolate what contributes to gains. The paper honestly reports that random taxonomic labels are competitive on some datasets, which provides useful information about the mechanism.

## Weaknesses

### Fatal
None.

### Major

1. **Gap between "essential" claim for taxonomic semantics and ablation evidence.** The paper repeatedly asserts that taxonomic context is "essential" (Abstract, Section 1 contributions: "taxonomic context is not just helpful but *essential*", Section 5: "taxonomic context is not merely helpful but **essential**", Section 7: "fundamental requirement"). However, the W-TaxS ablation (Table 4) — which replaces taxonomic subcategory labels with *random characters* while retaining class descriptors — matches or exceeds DefNTaxS on ImageNet (63.24 vs. 62.96), Places (40.05 vs. 39.34), CUB (tied), and Food (within 0.20). On these four datasets, the "taxonomic semantic context" is providing no measurable benefit over random strings. The paper acknowledges this obliquely ("differentiation alone has an effect," Section 6.1.3) but does not reconcile this with the categorical framing in the abstract and introduction. If random taxonomies perform comparably to real ones on half the benchmarks, the claim that *semantic* taxonomic context is "essential" is not supported by the evidence. The contribution is better understood as *structured prompt differentiation* that happens to use LLM-generated labels, not as a demonstration that taxonomic semantics are necessary.

2. **Missing variance estimates for main results.** Table 1 reports a single accuracy number per method per dataset with no standard errors, confidence intervals, or significance tests. Several of DefNTaxS's improvements over D-CLIP are very small — ImageNet (+0.48), CUB (+0.79), Food101 (+1.05), Places365 (+0.16), ImageNetV2 (+0.66). The ablation experiments in Table 4 (5 iterations) show that DefNTaxS's own standard errors on these datasets range from ±0.09 (Food) to ±0.26 (IN, Places). On Places365, the ±0.26 standard error alone exceeds the +0.16 reported gain over D-CLIP. On ImageNet, the +0.48 gain is less than 2× the standard error (±0.26). Without variance estimates for the main table, readers cannot assess whether several of the claimed SOTA improvements are statistically reliable.

3. **Largest gain (EuroSAT) is unexplained by the claimed mechanism and may be confounded.** EuroSAT shows a +9.86% gain over D-CLIP — by far the largest improvement. Yet Section 3.3 states that for datasets with fewer than 20 classes (EuroSAT has 10), the method uses the dataset name as a single subcategory context (e.g., "EuroSAT dataset"). The taxonomic component is therefore simply appending "commonly found among EuroSAT dataset" to each class's D-CLIP descriptors — a context that is already implicitly known. The paper attributes this result to taxonomic disambiguation (Section 5: "where taxonomic context helps distinguish land use categories"), but the actual intervention is minimal. This suggests the EuroSAT gain may be driven by something other than the claimed mechanism — possibly differences in descriptor quality between the modified pipeline used for DefNTaxS and the original D-CLIP pipeline, or a specific interaction between the prompt format and EuroSAT's classes. The paper offers no analysis of this outlier result.

### Minor

4. **Uncontrolled confound in descriptor generation pipeline.** Section 4.1 states that descriptors were generated using "a modified version of D-CLIP's generation pipeline... due to the deprecation of OpenAI's GPT-3 API," and Section 4.3 states that baselines were "recreated using the setup described in 4.1." This implies D-CLIP baselines also used the modified pipeline with GPT-4o-mini rather than the original GPT-3 pipeline. However, the nature of the modification is not described, and it is unclear whether the WaffleCLIP+Conc. baseline (which explicitly references "a high-level semantic concept generated by GPT-3," Section 4.3) was regenerated with GPT-4o-mini or kept with the original GPT-3 outputs. Without specifying exactly how descriptors were generated for each baseline, there is a residual confound between taxonomic context and descriptor quality.

5. **Motivating examples do not match the evaluation setting.** The introduction motivates the problem with cross-domain polysemes ("boxer" as dog vs. sport, "crane" as bird vs. equipment, "mouse" as animal vs. peripheral). However, none of the evaluated benchmarks contain such cross-domain ambiguity — ImageNet's 1000 classes are all within everyday objects, and the fine-grained datasets (CUB, Pets) involve within-domain distinctions. The kind of ambiguity DefNTaxS actually addresses is fine-grained differentiation (e.g., distinguishing dog breeds from each other), which is a different (and less dramatic) problem than disambiguating genuinely polysemous labels. This mismatch inflates the perceived importance of the contribution.

6. **Table 1 mean column inconsistency.** The Mean column for DefNTaxS (61.17) excludes ImageNetV2 (7-dataset average), while the Δ CLIP and Δ D-CLIP rows include ImageNetV2 in their means. This makes the reported improvements not directly comparable to the absolute accuracy means. The table should clarify what the Mean covers.

### Trivial
- Some visual formatting artifacts from PDF extraction (parser issues, not author errors).

## Nice-to-Haves

- **Concrete examples of LLM-generated subcategories** per dataset would help readers assess whether the groupings are reasonable and how they vary across domains.
- **Sensitivity analysis** for the ~20-class-per-subcategory threshold (Section 3.3) would strengthen the paper since this parameter is central to the method.
- **Ablation on LLM choice** (e.g., a weaker model) would test robustness of the pipeline.
- **The k-means comparison** (Section 6.2) is a reasonable controlled experiment but would be more informative if the k-means condition also generated its own subcategory labels (rather than using LLM labels for both), to fully isolate the effect of LLM-based clustering.

## Removed Points

These points were flagged but removed after verification:

- **"k-means ablation is unconvincing"** — The comparison actually controls for label quality (LLM generates labels in both conditions), making it a fair test of clustering method. The criticism misunderstands the experimental design.
- **"Sensitivity to LLM not tested"** — This is a nice-to-have, not a weakness of what is presented.
- **"Missing appendix / missing proofs"** — These were stripped by the PDF parser; they exist in the original submission.
- **"Reproducibility concerns about hyperparameters/implementation details"** — Standard for this type of empirical paper; not a substantive weakness.
- **"W-TaxS is ~fatal~/structural"** — While the W-TaxS result weakens the central claim, it does not invalidate the method or its practical value. Tagged as Major, not Fatal, because the method still demonstrably helps (especially on Pets, DTD, ESAT) and the paper does acknowledge the differentiation effect.

## Novel Insights

The key insight from cross-referencing the reviewers' perspectives is that the paper's strongest evidence actually supports *structured differentiation* (class-specific prompt structures that differentiate classes from each other) rather than *semantic taxonomic context* specifically. This reframes the contribution from a "context is essential" claim to a more nuanced finding: LLMs are a convenient tool for generating structured partitions of the class space, and the structure itself (even with random subcategory labels) accounts for much of the benefit. The paper's own W-TaxS ablation and the prior WaffleCLIP result converge on this interpretation.

## Suggestions

1. **Reframe the central claim** to match what the evidence supports: that structured prompt differentiation via LLM-generated class partitions improves zero-shot CLIP classification, with semantic taxonomic context providing moderate additional benefit on some (but not all) datasets. Remove or soften the "essential"/"fundamental" language.

2. **Report variance for all main results** (Table 1), at minimum using standard errors computed across multiple descriptor-generation seeds, so readers can assess whether sub-1% gains are meaningful.

3. **Analyze the EuroSAT result specifically** — report whether descriptors differ between the DefNTaxS pipeline and the D-CLIP baseline, and test whether adding a generic dataset-name suffix to D-CLIP prompts replicates the gain independently of other pipeline differences.

4. **Run an additional controlled experiment** comparing D-CLIP with and without a dataset-name suffix appended to its prompts, to isolate the effect of the "context" component on EuroSAT.

## Score and Decision

This paper presents a simple, practical method with broad evaluation and honest ablations. However, the paper's central claim (that taxonomic semantic context is "essential") is contradicted by its own ablation evidence, the largest empirical result (EuroSAT) is unexplained by the claimed mechanism, and the main results lack variance estimates needed to assess several small-margin improvements. These are correctable in revision but significant in the current form.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>