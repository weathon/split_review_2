Now let me read the remaining sections to verify all reviewer claims thoroughly.Now I have carefully verified all reviewer claims against the paper text. Let me compile the draft review.Now let me run calibration Round 1 — bracketing across score bands with topic-relevant queries.Very interesting — one of the calibration results (`B2ChNpcEzZ.md`) appears to be the same DefNTaxS paper! Let me read the full reviews for key anchors.Now let me read one anchor from the 6.0 band for comparison.Now I have all the information needed. Let me compile the final review.

Remarkably, the calibration search returned `B2ChNpcEzZ.md` which appears to be the **same DefNTaxS paper** (or a very close version), with human scores of 3, 5, 3, 5 → average 4.00, Decision: Reject. This provides an excellent calibration anchor.

**Round 1 bracket**: Based on comparisons:
- The paper clearly sits above the strong-reject band (1.0) — it has a coherent idea and real experiments
- It aligns closely with the 3.0–5.0 band: modest gains, overclaiming, evaluation concerns
- It falls well below the 6.0+ band (PerceptionCLIP had 11 datasets, multiple settings, less overclaiming)
- **Initial bracket: 3.0–4.5**

The earlier version of this paper received 4.0 from humans. The current version adds some ablations (Tables 2–5) and more baselines (CGPT-P, CHILS, CuPL), but also introduces the training-split evaluation concern and escalates the overclaiming ("paradigm shift"). These roughly cancel, anchoring my estimate near 3.5–4.0.

---

## Summary
DefNTaxS introduces a training-free framework that uses LLMs to discover taxonomic subcategories among dataset classes and integrates this hierarchical context into CLIP text prompts for zero-shot image classification. The method clusters classes into semantically meaningful groups (~20 per subcategory), generates connecting phrases, and appends them to standard descriptor-based prompts. Evaluated across seven benchmarks using ViT-B/32, it reports an average +5.5% gain over vanilla CLIP and +2.44% over D-CLIP, with the largest gain (+13.0%) on EuroSAT.

## Strengths
- **Practical simplicity and very low cost**: The pipeline is fully automated, training-free, and costs only $0.38 total for all seven benchmarks (Section 4.1). No model modification, no additional training data, immediately deployable. This is concretely useful.
- **Well-designed ablation studies**: Section 6 systematically tests reduced refinement (Table 2), descriptor removal vs. taxonomic-only prompts (Table 3), random-character substitution for both descriptors and taxonomy labels (Table 4), and LLM vs. k-means clustering (Table 5). These ask the right diagnostic questions and are more informative than ablations in many comparable papers.
- **Substantial EuroSAT gain**: The +13.0% absolute improvement on EuroSAT (44.26% → 57.22%, Table 1) is large and plausible given that taxonomic grouping should help disambiguate visually similar satellite land-use categories (e.g., "annual crop" vs. "permanent crop").

## Weaknesses

### Fatal
None

### Major
1. **Evaluation on training split with no justification (Section 4.1)** — The paper explicitly states: "The classification accuracy is reported as the primary evaluation metric in a pure zero-shot setting on each dataset's standard training split." Standard practice in zero-shot CLIP evaluation (including in D-CLIP, WaffleCLIP, and all baselines the paper compares against in the original literature) is to use the test or validation split. While the authors re-ran all baselines under the same conditions (Section 4.3, line 175), which preserves internal comparability, the use of training splits prevents comparison with any numbers in the broader literature and undermines the paper's SOTA claims. No justification is offered for this non-standard choice.

2. **Overclaiming substantially exceeds what ablations support** — The paper claims taxonomy is "not merely helpful but essential" (Section 5), "a fundamental requirement" (Section 7), and represents "a paradigm shift toward context-aware zero-shot learning" (Section 7). However, the paper's own ablations directly contradict the "essential" framing:
   - Table 4: W-TaxS (random characters replacing taxonomy labels, preserving descriptors) beats DefNTaxS on ImageNet (63.24 vs. 62.96) and Places (40.05 vs. 39.34), showing that *semantic* taxonomy content is not essential — random token differentiation sometimes suffices.
   - Table 3: Removing all fine-grained descriptors ("no desc.") while keeping only taxonomy yields near-equivalent or better performance on Food101 (81.35 vs. 81.26) and close results elsewhere.
   - The evidence supports a defensible but much weaker claim: "some form of inter-class differentiation in prompts helps, and well-chosen taxonomy is one effective way to achieve this." The gap between this and "paradigm shift" is large.

3. **Single backbone, no variance in main results** — All main results (Table 1) use only ViT-B/32, the smallest standard CLIP backbone. Prompt-enrichment gains often diminish with stronger encoders. Table 5's caption mentions "multiple CLIP backbones" but displays only a single set of results (one row for k-means, one for LLM), making this claim unverifiable from the main text. Critically, no confidence intervals appear in Table 1, yet Table 4 (which does report standard errors over 5 runs) reveals DefNTaxS on ImageNet is 62.96 ± 0.26 — notably lower than Table 1's reported 63.48. Many claimed gains over D-CLIP (+0.48 on IN, +0.16 on Places, +0.66 on INV2) fall within this noise range.

### Minor
1. **Modest gains on most benchmarks** — Over D-CLIP, the improvements are: +0.48 (IN), +0.79 (CUB), +1.05 (Food), +0.16 (Places), +0.66 (INV2) — all under 1.1 percentage points. The headline +2.44% average over D-CLIP is heavily skewed by EuroSAT (+9.86) and Pets (+4.25). On the largest and most commonly cited benchmarks (ImageNet, Food101, Places365), improvement is marginal and likely within noise.

2. **Method fragility with respect to refinement heuristic** — Table 2 demonstrates that without sufficient taxonomic refinement, DefNTaxS (61.23 on IN) falls *below* D-CLIP (63.26), showing the method is sensitive to the heuristic ~20-classes-per-subcategory threshold. This threshold is determined by an empirical sweep (deferred to Appendix D) without principled justification.

3. **Factual inaccuracy in results claim** — Section 5 states DefNTaxS "achiev[es] the highest accuracy across six of seven benchmarks." Counting the seven standard benchmarks (excluding INV2), Table 1 shows CHILS outperforms DefNTaxS on both Food101 (83.53 vs. 81.48) and Places365 (40.45 vs. 40.00), making it 5 of 7, not 6 of 7.

### Trivial
None

## Nice-to-Haves
- Results across at least two CLIP backbones (e.g., ViT-B/32 and ViT-L/14) to test whether gains persist with stronger encoders
- Per-class or per-subcategory analysis showing which classes benefit most from taxonomic context
- Deeper investigation of the W-TaxS finding — understanding *when* semantic taxonomy helps vs. when mere token differentiation suffices would be a genuinely useful contribution to understanding how CLIP processes text

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"Method is technically thin / just prompting"**: The paper explicitly proposes a training-free framework; simplicity and low cost are features, not bugs. This criticism demands a different kind of paper than the one submitted.
- **"LLM prompts should appear in main text"**: Deferred to Appendix A, which is standard practice. The appendix exists in the original submission.
- **"WaffleCLIP+Concept already does this"**: While WaffleCLIP+Concept appends a high-level concept, DefNTaxS does something structurally different — it discovers and assigns dataset-specific subcategories with connecting phrases, not a single global concept. The overlap is partial, not complete. However, the incremental novelty over WaffleCLIP+Concept is indeed limited, which is reflected in the modest gains.
- **"CGPT-P already uses hierarchical taxonomies"**: CGPT-P uses a multi-level fused scoring system with separate hierarchical levels, while DefNTaxS integrates taxonomy into a single prompt. The approaches are architecturally different, though conceptually related.

## Novel Insights
The most interesting finding comes from the paper's own Table 4: random characters substituted for taxonomy labels (W-TaxS) sometimes match or beat meaningful taxonomy, suggesting CLIP's text encoder may benefit more from inter-class token differentiation than from semantic content per se. This finding, if properly investigated rather than deflected, could advance the community's understanding of how vision-language models process text prompts. The paper also provides useful evidence (Table 3) that fine-grained descriptors contribute marginally on top of taxonomic context, complementing WaffleCLIP's finding about descriptor semantics from the opposite direction.

## Suggestions
1. Re-run all experiments on standard test/validation splits to enable direct comparison with the broader literature.
2. Report variance on Table 1 results — either via multiple LLM generation seeds or by confirming deterministic generation at temperature 0. The discrepancy between Table 1 (63.48 on IN) and Table 4 (62.96 ± 0.26 on IN) needs explanation.
3. Reframe the contribution honestly: "taxonomic context is an effective, cheap, complementary strategy for zero-shot classification" rather than "essential" or "a paradigm shift." The evidence supports the former; it does not support the latter.
4. Investigate the W-TaxS finding seriously: when does semantic taxonomy help vs. mere differentiation? This analysis would strengthen the paper significantly.
5. Include results on at least one additional CLIP backbone (e.g., ViT-L/14) in the main results table.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| DefNTaxS (earlier version) | B2ChNpcEzZ.md | 4.00 | R1 | Same paper; human reviewers flagged limited novelty, minor gains, overclaiming |
| LLM2CLIP | HfJxXbXlYJ.md | 3.00 | R1 | More technically ambitious but methodologically flawed; DefNTaxS is slightly better executed |
| Multi-Vision Multi-Prompt | j1FLTvgyAh.md | 2.50 | R1 | Weaker paper overall; DefNTaxS is clearly above this |
| Close the Gap (Retrieval Captioning) | hgayrNSbri.md | 3.40 | R1 | Similar limited-novelty concerns; DefNTaxS is comparable |
| Text Descriptions (SLR-AVD) | t84UBRhhvp.md | 4.75 | R1 | Similar domain, marginal zero-shot gains but stronger theoretical grounding; DefNTaxS is somewhat weaker |
| Embracing Diversity (multi-vector) | WqeRtP2T3R.md | 4.67 | R1 | Similar zero-shot CLIP work with modest gains; DefNTaxS is comparable or slightly weaker |
| Unclipping CLIP's Wings | DPp5GSohht.md | 4.25 | R1 | Investigates CLIP prompt sensitivity; more analytical depth; DefNTaxS is comparable |
| PerceptionCLIP | 2Oiee202rd.md | 6.00 | R1 | Training-free CLIP method but with 11 datasets, multiple settings, less overclaiming; DefNTaxS is notably weaker |
| DVDet (descriptors for detection) | usrChqw6yK.md | 6.00 | R1 | More technically novel hierarchical descriptor approach; DefNTaxS is weaker |
| DeMul (weighted multi-prompt) | NDLmZZWATc.md | 6.40 | R1 | Stronger technical contribution and evaluation; DefNTaxS is clearly weaker |
| Chinese NLP for Robots | gwZ90hFSL2.md | 1.00 | R1 | Clearly weaker; DefNTaxS is well above this |
| Clothing-Irrelevant ReID | 5lUdTogEL3.md | 1.00 | R1 | Clearly weaker; DefNTaxS is well above this |
| Systematic LLM Review | 8QTpYC4smR.md | 1.00 | R1 | Survey paper, strong reject; DefNTaxS is well above this |

**Round 1 bracket**: 3.0–4.5

**Narrowing**: The earlier version of this same paper received 4.0 from human reviewers. The current version adds useful ablations (Tables 2–5) and more baselines (CGPT-P, CHILS, CuPL), which marginally improve the contribution. However, it also introduces the training-split evaluation concern (not present or not flagged in the earlier review) and escalates the overclaiming to "paradigm shift." The discrepancy between Table 1 and Table 4 numbers further erodes confidence. The paper sits near 3.5–4.0.

**Final assessment**: DefNTaxS presents a reasonable and practical idea — augmenting CLIP prompts with LLM-generated taxonomic context — that produces a large gain on EuroSAT and modest-to-negligible improvements elsewhere. The paper's primary weakness is not the idea but the gap between claims and evidence: "essential" and "paradigm shift" language is not supported by ablations showing random-token differentiation sometimes works equally well. The non-standard evaluation protocol (training split, single backbone, no variance) further undermines confidence. The contribution is real but bounded, and the framing inflates it beyond what the evidence warrants.

**Score: 3.5** — Between reject and borderline reject. The practical idea and informative ablations prevent a full reject, but the evaluation protocol issues, significant overclaiming contradicted by own ablations, and marginal gains on most benchmarks fall short of the borderline-accept threshold.

**Decision: Reject**

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>