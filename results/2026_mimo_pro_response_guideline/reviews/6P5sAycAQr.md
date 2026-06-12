## Summary
DefNTaxS proposes a training-free framework that uses LLMs to discover taxonomic subcategories and integrate them into CLIP prompts for zero-shot image classification. It clusters classes into lateral semantic groups, refines subcategory granularity (~20 classes per group), and generates prompts combining class descriptors with subcategory context. Evaluated on 7 benchmarks with ViT-B/32 CLIP, it claims +5.5% average accuracy improvement over vanilla CLIP.

## Strengths
1. **Thorough multi-faceted ablation design (Tables 2–5):** Four distinct ablation studies decompose the contributions: reduced taxonomic refinement (Table 2), descriptor vs. subcategory modifications (Table 3), random-character substitutions separating semantic from differentiation effects (Table 4 with 5-run mean ± SE), and LLM vs. k-means clustering (Table 5). This goes well beyond a single comparison table and provides genuine mechanistic insight into why the method works.
2. **Context-dependent class assignment (Section 3.2):** The same class label (e.g., "boxer") gets assigned to different subcategories depending on the full set of classes in the dataset. This is a genuine design novelty over prior methods (D-CLIP, CHiLS, CGPT-P) that treat each class independently, illustrated with concrete sports-vs-dogs examples.
3. **Low cost and training-free ($0.38, Section 4.2):** Total text generation cost of $0.38 using GPT-4o-mini makes the method immediately practical and deployable without model modification.
4. **Real gains on several benchmarks:** DefNTaxS shows meaningful improvements on Pets (+8.2% over CLIP), DTD (+4.8%), and ESAT (+13.0%, though see EuroSAT caveat below).

## Weaknesses

### Fatal
None.

### Major
- **Table 1 Mean column is computed incorrectly for DefNTaxS.** Every other row's Mean equals the sum of all 8 columns (including INV2) divided by 8 (CLIP: 441.04/8 = 55.13 ✓; D-CLIP: 465.07/8 = 58.13 ✓). For DefNTaxS, the sum of all 8 values is 484.59, yielding 484.59/8 = **60.57**, but the table reports **61.17** = 428.16/7 (excluding INV2). This inflates the displayed headline mean by ~0.6 points. Notably, the Δ CLIP row's Mean of +5.44 is consistent with the correct 60.57 (60.57 − 55.13 = 5.44), not with 61.17 (which would give +6.04). This is a verified computational error in the paper's primary results table.

- **Table 1 appears to report a single run, not mean ± SE.** Table 4 reports DefNTaxS over 5 runs with mean ± SE. Comparing Table 1 to Table 4 means: IN: 63.48 vs 62.96±0.26 (+2.0 SE); Food: 81.48 vs 81.10±0.09 (+4.2 SE); Places: 40.00 vs 39.34±0.26 (+2.5 SE); ESAT: 57.22 vs 55.99±0.36 (+3.4 SE). Five of seven Table 1 values exceed the 5-run means, with several significantly so. The paper never states what statistic Table 1 reports. The headline results may be systematically inflated and are not directly comparable to the baselines' reproduced values.

- **Factual error: "six of seven benchmarks" is actually five of seven.** The paper states (line 197): "DefNTaxS achieving the highest accuracy across six of seven benchmarks." From Table 1, DefNTaxS is best on IN, CUB, Pets, DTD, and ESAT (5 of 7). CHILS outperforms DefNTaxS on both Food (83.53 vs. 81.48) and Places (40.45 vs. 40.00). This is a straightforward factual misstatement of the paper's own table.

- **EuroSAT headline gain bypasses the core taxonomic pipeline.** The paper's largest gain is +13.0% on EuroSAT. However, Section 3.3 states: "For datasets with fewer than 20 classes, we use the dataset name as the single subcategory context (e.g., 'EuroSAT dataset')." EuroSAT has 10 classes, so the entire taxonomic discovery, assignment, and refinement pipeline is bypassed. The +13% gain is better described as a domain-context fix than evidence for the taxonomic framework. Excluding EuroSAT, the average gain over D-CLIP drops to approximately +1.1%.

### Minor
- **WaffleTaxS outperforms DefNTaxS on 3/7 benchmarks (Table 4).** From the 5-run data: WaffleTaxS (random characters replacing subcategory labels) beats DefNTaxS on IN (+0.28), CUB (+0.06), and Places (+0.71). The paper's framing that "taxonomic context is not just helpful but essential" (line 179) is undermined by random-character variants being competitive. The paper acknowledges "mixed results" but under-discusses the implications.

- **Overclaimed conclusions.** Claims of "paradigm shift toward context-aware zero-shot learning" (line 297) and "fundamental advancement in zero-shot classification" (line 205) are excessive for a method averaging ~1-2% improvement over D-CLIP (excluding the EuroSAT special case) that is outperformed by random-character variants on several benchmarks.

- **No error bars or variance reporting on Table 1.** Given that LLM outputs are non-deterministic and Table 4 shows non-trivial variance (especially ESAT SE = 0.36), the headline table should report mean ± SE.

- **No prompt length analysis.** DefNTaxS prompts are longer than vanilla CLIP prompts. The paper cites the effective CLIP context window limitation (~20 tokens) but does not disentangle prompt length effects from semantic content.

- **Baselines re-generated with GPT-4o-mini rather than original LLMs.** All baselines were re-implemented with GPT-4o-mini due to GPT-3 API deprecation (Section 4.1–4.2). While same-LLM-for-all has a fairness rationale, this should be discussed as a limitation affecting comparability to originally published results.

## Nice-to-Haves
- Error analysis or class-level breakdowns on datasets where DefNTaxS clearly outperforms both D-CLIP and WaffleTaxS (Pets, DTD, ESAT) would strengthen the contribution.
- Prominently noting the EuroSAT special case in the main results section rather than in a method subsection.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Generic formatting/style nitpicks — removed per rules.
- Criticisms about missing appendix content (prompts, proofs) — stripped by parser; these exist in the original submission.
- Any reproducibility concerns about cited models/tools — removed per rules.

## Novel Insights
The ablation showing that WaffleTaxS (random characters + taxonomic structure) outperforms DefNTaxS on 3/7 benchmarks is a genuinely important empirical finding. It suggests much of the benefit comes from structural differentiation (having distinct subcategory groupings) rather than the semantic content of subcategory labels. This finding, buried in Section 6.1.3, has implications for the broader understanding of how context helps CLIP and should be foregrounded more prominently.

## Suggestions
1. Fix the Mean column computation in Table 1 to correctly average all 8 columns (or explicitly exclude INV2 and document this).
2. Report mean ± SE across multiple runs in Table 1, matching the reporting standard in Table 4.
3. Correct the "six of seven" claim to "five of seven."
4. Either exclude EuroSAT from headline averages or prominently note it uses a fundamentally different code path (dataset-name context rather than taxonomic pipeline).
5. Expand discussion of WaffleTaxS results — what does it mean that random subcategory labels are competitive on several benchmarks?

## Calibration Anchors
**Round 1 retrieval** (all bands, same query: "zero-shot image classification prompt engineering CLIP taxonomic hierarchical context"):
- **B2ChNpcEzZ.md** (DefNTaxS, previous version): avg 4.00, Reject — **same paper, earlier submission**; scores 3, 5, 3, 5. My version is revised with more baselines and ablations but also new errors.
- **WqeRtP2T3R.md** (Embracing Diversity): avg 4.67, Reject — similar topic, marginal improvements over WaffleCLIP, rejected.
- **bOoHGBwFoo.md** (Hierarchical divide-and-conquer): avg 4.50, Reject — related topic, rejected.
- **mLTbDVzHVh.md** (Hierarchical Taxonomies): avg 5.25, Reject — related topic, rejected.
- **2Oiee202rd.md** (PerceptionCLIP): avg 6.00, Accept — similar topic, stronger narrative, 11 datasets, accepted.
- **wFs2E5wCw6.md** (Tree of Attributes): avg 6.40, Accept — similar topic, stronger results, accepted.
- **Pp2j9BvpgC.md** (Attribute Recognition): avg 5.75, Reject.
- **FwkYeLovHk.md** (Weak-to-Strong CLIP): avg 3.33, Reject.
- **ZVOGMy8Sd8.md** (Fashion Captioning): avg 3.00, Reject.
- **3i13Gev2hV.md** (Compositional Entailment): avg 8.00, Accept — clearly stronger.
- **5Ca9sSzuDp.md** (Interpreting CLIP): avg 8.00, Accept — clearly stronger.

**Round 1 bracket:** 3.5–5.0. The exact same paper anchor is 4.00. Comparable accepted papers are at 6.0+. The revised version has improvements (more baselines, better ablations with 5-run SE) but also new integrity issues (Mean computation error, likely single-run reporting in headline table, factual misstatement of benchmark wins). These roughly cancel, placing the score at the previous version's level. **Final score: 4.0.**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>