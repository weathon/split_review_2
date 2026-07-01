Now I have all the evidence needed. Let me write the final consolidated review.

## Summary

This paper proposes DefNTaxS, a training-free framework that uses LLMs to cluster image class labels into semantically meaningful subcategories and appends this taxonomic context (e.g., "commonly found among dog breeds") to CLIP prompts for zero-shot classification. The method builds on D-CLIP's descriptor-based prompting by adding a relational layer that groups similar classes. Across seven benchmarks, DefNTaxS achieves average gains of +5.5% over vanilla CLIP and +2.44% over D-CLIP, with a total LLM API cost of $0.38.

## Strengths

- **Well-motivated core idea.** The paper identifies a genuine limitation: existing zero-shot methods treat class labels in isolation, missing the disambiguating value of knowing which semantic neighborhood a class belongs to. The "boxer as dog breed vs. fighter" example (Section 1) cleanly illustrates a real problem neither D-CLIP descriptors nor CHiLS hierarchies fully solve.

- **Practical and cheap.** DefNTaxS requires no model retraining, no manual prompt engineering, and cost $0.38 total LLM API fees (Section 4.1). It can be dropped into existing CLIP pipelines with minimal overhead.

- **Consistent improvement across diverse benchmarks.** In Table 1, DefNTaxS achieves the highest accuracy on 6 of 7 datasets, with gains across fine-grained classification (CUB, Pets), texture (DTD), scenes (Places), and satellite imagery (EuroSAT). The improvement is not concentrated in one domain.

- **Reasonably thorough ablation studies.** Sections 6.1.1–6.2 investigate reduced taxonomic refinement, removal of descriptors, addition of subcategory descriptors, random-character substitutions, and LLM vs. k-means clustering. This level of analysis is more extensive than many comparable papers provide.

## Weaknesses

### Fatal
None.

### Major

**1. Unresolved discrepancy between main results and multi-run ablation results.** Table 1 reports DefNTaxS as 63.48 on ImageNet and 40.00 on Places. Table 4 reports DefNTaxS across 5 runs as 62.96±0.26 on ImageNet and 39.34±0.26 on Places. The ImageNet value from Table 1 is ~2 standard errors above the Table 4 mean; the Places value is ~2.5 standard errors above. The paper neither acknowledges nor explains this discrepancy. Since Table 1 reports no variance estimates, the reader cannot assess whether DefNTaxS's margins over baselines (e.g., +0.48% over D-CLIP on ImageNet, +0.16% over D-CLIP on Places) are real or noise. *Verification: Table 1 (line 191) vs. Table 4 (line 256).*

**2. The headline EuroSAT result (+13.0% over CLIP, +9.86% over D-CLIP) is obtained under conditions where the paper's claimed mechanism is effectively disabled.** Per Section 3.3: "For datasets with fewer than 20 classes, we use the dataset name as the single subcategory context." EuroSAT has 10 classes. This means DefNTaxS produces prompts of the form "*class*, which has {descriptor}, commonly found among EuroSAT dataset" — a single subcategory covering all classes, with zero stratification or inter-class disambiguation via taxonomy. Yet Section 5 claims this improvement occurs because "taxonomic context helps distinguish land use categories." Since no taxonomic differentiation exists on this dataset, the paper's own explanation of why EuroSAT improves is inconsistent with the method's design. The result itself may be valid, but attributing it to taxonomic stratification is misleading. *Verification: Section 3.3 (line 99), Table 1 (lines 191-193), Section 5 (line 199).*

**3. Central claim of taxonomic context being "essential" and "inevitable" is at odds with the paper's own ablation evidence.** The title, abstract, and Section 5 frame taxonomic context as a necessity. However, Table 4 shows that W-TaxS (random characters replacing the subcategory label, retaining descriptors) *outperforms* DefNTaxS on ImageNet (63.24 vs. 62.96) and Places (40.05 vs. 39.34). Table 3 shows that removing descriptors entirely (keeping only taxonomic context) yields competitive results (Food: 81.35 vs. 81.26), and adding *more* taxonomic context ("tax. desc.") substantially hurts performance (IN: 63.48→59.80; Places: 40.00→35.67). These results suggest the method's success partly comes from having *any* structure that differentiates classes, not specifically from the semantic content of the taxonomy. Section 6.1.3 acknowledges "differentiation without semantic content" but the paper never reconciles this with the "essential/inevitable" framing. *Verification: Title (line 5), abstract (line 9), Section 5 (line 179), Table 4 (lines 256-258), Table 3 (lines 236-238).*

### Minor

**4. Method dependency on D-CLIP is underplayed.** DefNTaxS = D-CLIP descriptors + taxonomic context, with an average gain of +2.44% over D-CLIP. The paper repeatedly frames this as "new SOTA beating baselines," but the relationship is essentially an ablation of one component added to D-CLIP. The framing as an independent method rather than an augmentation inflates the apparent novelty. The paper would be better served by transparently characterizing itself as "adding taxonomic context to D-CLIP."

**5. Table 3's "tax. desc." row is ambiguous.** The row label and caption suggest subcategory descriptors are *added* to class descriptors, but the text (lines 245-249) says "We explore the impact due to both the inclusion of subcategory descriptors and removal of class descriptors," implying both variations were tested. Only one row is shown. It is unclear whether the reported numbers are with class descriptors retained or removed. *Verification: Table 3 caption (lines 240-241), text (lines 248-249).*

**6. ImageNetV2 mentioned in Table 1 but not listed in the datasets section.** Section 4.2 lists 7 datasets but the INV2 column appears in Table 1 without a corresponding description of how it was configured or evaluated. The main text mentions it only in passing (line 201). *Verification: Section 4.2 (lines 154-155), Table 1 (line 181).*

**7. Edge-case handling in class-to-subcategory assignment is not quantified.** Section 3.2 describes a loop mechanism for resolving classes that could belong to multiple subcategories, but provides no statistics on how often this occurs, how many iterations are needed, or how often the LLM makes conflicting assignments. *Verification: Section 3.2 (lines 83-84).*

**8. Hyperbolic framing in the conclusion.** Claiming DefNTaxS "represents a paradigm shift toward context-aware zero-shot learning" (Section 7) is excessive for a 2–5% accuracy improvement from appending LLM-generated context to existing descriptors. *Verification: Section 7 (line 297).*

### Trivial
None.

## Nice-to-Haves

- **Sensitivity to LLM choice.** All experiments use GPT-4o-mini. Showing whether weaker/cheaper models produce taxonomies of comparable quality would strengthen claims about practical deployability.
- **Failure case analysis.** The paper does not discuss datasets or class sets where the LLM produces bad taxonomies that hurt performance (the Places and reduced-refinement results in Table 2 suggest such cases exist).
- **Case study of generated taxonomies.** Showing actual taxonomies produced for a few datasets with examples of correct and incorrect assignments would help readers assess the quality of the LLM's taxonomic reasoning.

## Removed Points

- *Concern about CGPT-P/CHiLS baselines using different LLMs.* The paper states "We used GPT-4o-mini for all experiments" (Section 4.1) and that all baselines were recreated with the same setup (Section 4.3). The concern is addressed.
- *Concern about D-CLIP descriptor regeneration affecting comparability.* The paper explicitly notes descriptors were regenerated with GPT-4o-mini due to GPT-3 API deprecation and that all baselines were recreated identically. The in-paper comparison is fair.
- *Criticism about the ≈20-class heuristic being deferred to the appendix.* This is a standard practice; the appendix is available in the original submission.
- *Criticism about polysemous word examples not corresponding to actual dataset ambiguity.* The examples are motivating illustrations of a general principle; the paper's real target is semantically similar classes, which is clear from context.

## Novel Insights

The most insightful observation emerging from cross-referencing the paper's claims with its own ablations is that the benefit of taxonomic context may be substantially driven by *differentiation* (any structure that makes class prompts more distinct) rather than by genuine *semantic understanding* of the taxonomy. The W-TaxS result — where random character sequences replacing the subcategory name sometimes match or outperform the real taxonomy — directly supports this, yet the paper continues to frame taxonomic semantics as the active ingredient. This tension between what the method does and what the paper claims it does is the deepest unresolved issue.

## Suggestions

1. **Resolve the Table 1 vs. Table 4 discrepancy.** Report all main results with variance across multiple runs, or explain why Table 1 uses a different seed/configuration than Table 4.
2. **Contextualize the EuroSAT result.** Either provide a mechanistic explanation for why appending "EuroSAT dataset" to prompts yields +10% over D-CLIP, or stop using this result to claim that taxonomic stratification drives improvement, since the method does not actually stratify on this dataset.
3. **Reconcile the framing with the ablations.** Replace "essential/inevitable" with a more precise claim — e.g., "adding structured differentiation between classes, whether semantic or not, tends to improve CLIP zero-shot performance; semantic taxonomies additionally help on certain datasets."
4. **Add a case study.** Show the actual taxonomies produced for 2–3 datasets so readers can judge the quality of LLM clustering.
5. **Clarify Table 3.** Make explicit whether the "tax. desc." row adds subcategory descriptors to or replaces class descriptors.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>