Now I have all the information I need. Let me finalize the review.

## Summary

DefNTaxS proposes a fully automated, training-free framework for zero-shot CLIP classification that uses LLMs to discover meaningful subcategories among classes and integrate them as taxonomic context into enriched prompts (e.g., "boxer, which has a muscular build, commonly found among dog breeds"). The method is clean, costs only \$0.38 in API fees, and achieves consistent accuracy gains on 5 of 7 standard benchmarks over vanilla CLIP (average +5.5%) and over D-CLIP (average +2.44%).

## Strengths

- **Well-motivated framing.** The paper clearly articulates a genuine limitation of existing zero-shot CLIP pipelines: class-name ambiguity ("boxer" as dog vs. sport, "crane" as bird vs. equipment) that isolated descriptors do not resolve. The three failure modes (contextual blindness, incomplete disambiguation, semantic isolation) are well-defined and persuasive.

- **Practical and economical.** DefNTaxS requires no retraining, manual prompt engineering, or additional data. The total API cost across all experiments is \$0.38, making it immediately deployable. This is a genuine practical advantage over methods requiring model updates or per-dataset hand-tuning.

- **Consistent accuracy improvements.** DefNTaxS achieves the highest accuracy on 5 of 7 standard benchmarks (ImageNet, CUB, Oxford Pets, DTD, EuroSAT) and on ImageNetV2, with positive deltas over all baselines on those datasets. The +13.0% gain on EuroSAT and +4.25% on Oxford Pets over D-CLIP are particularly notable.

## Weaknesses

### Major

- **Central causal claim is overstated relative to the evidence.** The paper asserts that "taxonomic context is not just helpful but *essential* for robust zero-shot classification" (Abstract, Section 5 opening, Conclusion). However, the WaffleTaxS ablation (Table 4) replaces the taxonomic subcategory with random characters and achieves comparable or better performance on several datasets: ImageNet (63.24 vs. 62.96, random wins), CUB (essentially tied), and Places (40.05 vs. 39.34, random wins). DefNTaxS does outperform WaffleTaxS on 4/7 datasets, but the mixed results show that differentiation from longer/more structured prompts—not taxonomic *semantics* specifically—is a significant driver. The paper acknowledges that "differentiation alone has an effect" but continues to frame taxonomic semantics as the key contribution. This creates a coherence gap between the central narrative and the ablation evidence. The claim of "essential" is not supported in the strong sense asserted.

### Minor

- **Factual error in reported benchmark wins.** The paper states that "Table 1 shows DefNTaxS achieving the highest accuracy across six of seven benchmarks" (line 197). In reality, DefNTaxS achieves the highest accuracy on **5 of 7** benchmarks: CHiLS wins on Food101 (83.53 vs. 81.48) and Places365 (40.45 vs. 40.00). This is a straightforward factual inaccuracy.

- **Inconsistency between Table 1 and Table 4 accuracy numbers.** DefNTaxS accuracy values differ systematically between the two tables (e.g., ImageNet: 63.48 vs. 62.96; EuroSAT: 57.22 vs. 55.99; Places: 40.00 vs. 39.34). Table 1 reports point estimates without mentioning iteration count or standard error, while Table 4 reports 5-iteration means with standard error. This discrepancy is not explained, and the reader cannot determine which numbers are canonical.

- **Modest improvements over the most relevant baseline (D-CLIP).** The paper emphasizes the +5.5% average gain over vanilla CLIP, but the more informative comparison is against D-CLIP. Excluding EuroSAT (which shows an anomalously large +9.86%), the average gain over D-CLIP is approximately +1.3%. Several individual gains are within 1 percentage point (ImageNet: +0.48, CUB: +0.79, Food: +1.05, Places: +0.16), which are small enough to be within run-to-run variation.

- **Anomalous EuroSAT result is not analyzed.** EuroSAT shows a dramatically larger improvement (+13.0% over CLIP, +9.86% over D-CLIP) than any other dataset. Yet EuroSAT has only 10 classes, so DefNTaxS falls back to using "EuroSAT dataset" as the single subcategory context (Section 3.3). The paper does not explain why this minimal context produces such outsized gains while larger taxonomic structures on other datasets produce smaller improvements.

### Trivial

None.

## Nice-to-Haves

- A controlled experiment holding prompt length and structure fixed while varying only whether the subcategory text carries taxonomic meaning (e.g., "category 1, category 2" vs. semantic subcategory names) would cleanly separate the differentiation effect from the semantic effect.
- Per-class accuracy breakdowns for ambiguous classes (e.g., ImageNet classes with multiple senses) would directly test the motivating "boxer/crane/mouse" scenario.
- Variance reporting for the main results in Table 1 (already done for ablations in Table 4) would help assess the significance of small-margin improvements.
- Analysis of why EuroSAT responds so differently from other datasets would strengthen the paper's scientific contribution.

## Removed Points

- **"Mechanism of improvement not identified" (original Issue 2):** The paper acknowledges that differentiation matters (Section 6.1.3) and does not claim to have fully isolated the mechanism; this is a request for additional analysis, not a weakness per se.
- **"No statistical characterization of main results":** Table 4 provides standard errors for the ablations; single-run reporting for main results is standard practice in this subfield.
- **"No analysis tying the method to the ambiguity problem":** The paper motivates with class-name ambiguity but does not evaluate it per-class. This is a valid suggestion but not a weakness given the paper's scope.
- **"Overstating SOTA status":** Already subsumed by the factual error about "six of seven" and the modest D-CLIP deltas.
- **Pure formatting/style nitpicks, missing appendix content, related work gaps, and reproducibility concerns about unreleased artifacts:** These are either parser artifacts, out of scope, or standard practice.

## Novel Insights

The WaffleTaxS ablation (Table 4) provides a nuanced picture that goes beyond the paper's own narrative: taxonomic semantics help on some datasets (Pets, DTD, ESAT) but not others (ImageNet, Places), suggesting that the benefit of DefNTaxS is dataset-dependent and not universally attributable to taxonomic context. The finding in Table 3 that removing descriptors entirely ("no desc.") barely hurts performance (e.g., ImageNet: 63.48 → 62.62, Food: 81.48 → 81.35) is also informative, as it suggests that the class descriptors inherited from D-CLIP are not the primary driver of gains either. Together, these ablations point toward prompt differentiation (longer, more structured text per class) as the most consistently beneficial ingredient, but the paper does not draw this conclusion explicitly.

## Suggestions

1. **Correct the factual error:** Change "six of seven" to "five of seven" or report more precise language about benchmark performance.
2. **Explain the Table 1 vs. Table 4 discrepancy** or report all main results with consistent methodology (e.g., 5-run averages with standard errors).
3. **Add the controlled experiment** suggested in Nice-to-Haves: compare DefNTaxS against a version where subcategory names are replaced with non-taxonomic but structured placeholders (e.g., "Group 1, Group 2") at equal length.
4. **Tone down the "essential" claim** or reframe the contribution as a practical automated prompt-engineering method rather than a demonstration that taxonomic semantics are causally necessary.
5. **Analyze the EuroSAT outlier** or acknowledge that the result may be dataset-specific.
6. **Report statistical variance** for the main results in Table 1, especially for comparisons where margins are <1%.

## Score and Decision

**Bracket information:**

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| DefNTaxS (prior version) | B2ChNpcEzZ | 4.00 | R1 | Same paper from prior submission; current version improves baselines/CHiLS comparison but retains overclaiming and adds new reporting inconsistencies |
| Embracing Diversity | WqeRtP2T3R | 4.67 | R1 | Rejected; similar issues: marginal gains over WaffleCLIP, questions about whether semantics drive improvements |
| Unclipping CLIP's Wings | DPp5GSohht | 4.25 | R1 | Rejected; CLIP prompt sensitivity analysis with similar methodological rigor |
| Exploiting Hierarchical Taxonomies | mLTbDVzHVh | 5.25 | R1 | Rejected; taxonomy-based method with stronger novelty on continual learning |
| PerceptionCLIP | 2Oiee202rd | 6.00 | R1 | Accepted; similar "context improves CLIP" theme but with stronger novelty (two-step inference) |
| Weak-to-Strong for CLIP | FwkYeLovHk | 3.33 | R2 | Rejected; weaker relevance and lower quality |

**Round 1 bracket:** [3.5, 5.5]

**Narrowing:** The prior version of this paper scored 4.00 with very similar content. The current version adds CHiLS comparisons and deeper ablations but introduces new issues (the WaffleTaxS contradiction, the "six of seven" error) and retains the central overclaiming problem. Comparable rejected papers in this space (Embracing Diversity at 4.67, Unclipping CLIP at 4.25) had analogous weaknesses: marginal improvements, insufficient evidence for the claimed mechanism. PerceptionCLIP (6.00, accepted) had stronger novelty and cleaner evidence. Within the calibrated range, the paper sits at the lower end of the 3.5–5.5 band.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>