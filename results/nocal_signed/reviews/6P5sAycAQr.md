## Summary

DefNTaxS proposes a fully automated, training-free framework that uses LLMs to discover taxonomic subcategories among classes and augments CLIP zero-shot prompts with this hierarchical context. The method is conceptually clean — a four-step pipeline generates subcategory groupings, assigns classes, refines granularity, and constructs context-rich prompts combining class descriptors with taxonomic context. It demonstrates consistent accuracy gains over vanilla CLIP across all evaluated datasets at negligible cost ($0.38 total).

## Strengths

- **Fully automated taxonomy discovery.** The method requires no manual prompt engineering or dataset-specific hand-tuning — an LLM handles subcategory generation, class assignment, refinement, and context phrasing. This is a genuine practical advantage over approaches that rely on hand-crafted templates (E-CLIP) or manual disambiguation.
- **Very low computational overhead.** Total LLM cost of $0.38 (GPT-4o-mini) across all datasets is negligible, making deployment realistic.
- **Consistent improvement direction.** While the magnitude varies, DefNTaxS improves over vanilla CLIP on every dataset in Table 1. This directional consistency is a genuine signal that the method adds value.
- **Well-structured method description.** The four-step pipeline (Taxonomic Discovery → Contextual Assignment → Granularity Optimization → Prompt Enhancement) is clearly presented and logically sound.

## Weaknesses

### Major

- **Factual error in reporting results.** The paper claims DefNTaxS achieves "the highest accuracy across six of seven benchmarks" (line 197). Examining Table 1's seven main benchmarks (IN, CUB, Pets, DTD, Food, Places, ESAT), DefNTaxS wins on **5** (IN, CUB, Pets, DTD, ESAT) and loses on **2** (Food: CHiLS 83.53 vs DefNTaxS 81.48; Places: CHiLS 40.45 vs DefNTaxS 40.00). This is a straightforward error in the paper's own Table 1.

- **Overclaimed SOTA status.** The abstract claims "consistent improvement over other recent SOTA" (line 9) and "establishing new state-of-the-art results" (line 31), but CHiLS outperforms DefNTaxS on Food and Places. These claims are overstated by the paper's own evidence.

- **EuroSAT's largest gain is unexplained by the claimed mechanism.** Per Section 3.3 (line 99), for datasets with fewer than 20 classes (EuroSAT has 10), "we use the dataset name as the single subcategory context." This means every class gets the same non-discriminating subcategory phrase — literally zero differentiating information from the taxonomic context. Yet EuroSAT shows the paper's largest improvement: +9.86 over D-CLIP and +12.96 over vanilla CLIP. The paper offers no explanation for how the method achieves its headline result on the exact dataset where the core added component cannot be contributing discriminative information.

### Minor

- **Central claim weakened by ablation evidence.** The paper argues taxonomic context is "essential" (line 179), but Table 3 shows that adding *more* taxonomic information (tax. desc.: subcategory-level descriptors) *reduces* accuracy on every dataset (e.g., IN: 63.48→59.80, DTD: 45.89→41.26, ESAT: 57.22→51.22). The paper's speculation about CLIP's effective context window (~20 tokens) is untested. Combined with the "no desc." ablation also degrading performance on most datasets, this suggests the benefit may come more from the class-level descriptors (inherited from D-CLIP) than from taxonomic context, or that the interaction is not well understood.

- **Ablation results question the source of improvement.** Table 4 shows that WaffleTaxS (random characters replacing subcategory labels) beats DefNTaxS on IN (63.24 vs 62.96) and Places (40.05 vs 39.34), suggesting subcategory semantics are not driving the improvement on these datasets. While the paper discusses this fairly, it undermines the strong claim that taxonomic *semantics* are essential.

- **No variance or confidence intervals on main results (Table 1).** While Table 4 demonstrates the method can be run with multiple iterations, the headline results lack uncertainty estimates. Many gains over D-CLIP are small (<1 point on 4 of 8 datasets), making it difficult to assess whether these are meaningful improvements or noise.

- **Close competition with CGPT-P not discussed.** CGPT-P (Ren et al., 2024) is the most directly comparable prior work — it also uses LLMs to build hierarchical taxonomies. The gap between DefNTaxS and CGPT-P is very small on IN (+0.16), CUB (+0.28), and DTD (+0.08). The paper does not discuss this close competition or clearly differentiate its approach.

### Trivial

- **The k-means vs. LLM clustering comparison** (Table 5) shows an average gain of only +0.92 from LLM clustering. On DTD the gain is +0.02 (essentially zero). While not a weakness per se, this reinforces that the LLM's role in generating subcategory labels is not the primary source of improvement.

- **Connecting phrases ambiguity.** Section 3.4 says "the LLM creates a connecting phrase," but the examples ("commonly found among," "a type of," "used for transportation as") read like a small fixed set. Clarifying whether these are LLM-generated per dataset or a fixed set would help reproducibility.

## Nice-to-Haves

- A clean ablation that adds only the subcategory context phrase to D-CLIP (holding the descriptor pipeline identical) would directly isolate the contribution of taxonomic context vs. other changes (modified descriptor pipeline, connecting phrase format).
- Reporting variance on the main results would strengthen confidence, especially for the small-gain datasets.
- The connecting phrase generation mechanism — clarify in the text.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **EuroSAT baselines (E-CLIP 33.44, W-CLIP 31.49) are unreliable:** The reviewer argued these numbers are "clearly broken" and imply implementation errors. This cannot be verified from the paper as written — the paper states baselines were faithfully recreated using provided code. Baseline anomalies are not proof of error. Removed because a fatal flaw must be unambiguous from the page.
- **Non-overlapping partitioning constraint is a limitation:** The paper clearly states this as a design choice. Not a weakness.
- **Refinement threshold evidence in stripped appendix:** Removed per rule about missing appendix content.
- **Section 6.1.1 setup unclear:** Minor presentation point, not substantive.
- **Characterization of CHiLS as unfair:** Subjective opinion about related work framing.
- **Style/formatting nitpicks, missing related works:** Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the "six of seven" claim to "five of seven" and recalibrate all SOTA claims throughout the paper.
2. Provide an explicit explanation for the EuroSAT gain — ablate whether it comes from the modified descriptor pipeline, connecting phrases, or other factors, since the taxonomic context is non-discriminative on this dataset.
3. Report variance or confidence intervals for the main Table 1 results.
4. Include a direct ablation that adds only subcategory context to D-CLIP's descriptors, holding everything else fixed.
5. Discuss the close competition with CGPT-P and clarify the distinguishing aspects of DefNTaxS.

## Score and Decision

The paper proposes a clean, well-motivated, fully automated pipeline that consistently improves over vanilla CLIP at negligible cost. The core idea — using LLMs to discover taxonomic groupings and integrating them into prompts — is sensible and practically useful.

However, the paper contains a factual error in its own result reporting (5/7 vs claimed 6/7), overstates its SOTA standing (CHiLS wins on 2/7 benchmarks), and fails to explain its largest result (EuroSAT), where the claimed mechanism provides no differentiating information. The ablation evidence also raises unresolved questions about whether taxonomic context or class-level descriptors drive the improvements.

These issues are fixable (correcting claims, adding analysis) but are substantive enough that the paper should not be accepted in its current form. A revised version with corrected claims, variance estimates, and an explanation of the EuroSAT result would be significantly stronger.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>