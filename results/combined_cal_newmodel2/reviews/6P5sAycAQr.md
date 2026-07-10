Now I have a clear picture of the calibration landscape. Let me write the final review.

**Round 1 bracket**: The earlier version of this same paper (B2ChNpcEzZ.md) scored 4.00 with human reviewers citing missing CHiLS comparison, limited novelty, and presentation issues. The current version addresses several of those (adds CHiLS comparison, better ablations) placing it above 4.00. Comparable papers in the 4.67–5.33 range (Embracing Diversity, GIST, Text Descriptions) were all Rejected. Accepted papers like DeMul and TAP (both 6.40) have more sophisticated methodology and fewer concerning weaknesses. With the EuroSAT issue as a notable concern, this paper sits in the 4.5–5.5 range — above the prior version but below the accept threshold.

**Narrowing**: Comparing my draft's items against the same paper's human review (B2ChNpcEzZ.md): the earlier version's most damaging items were -5.06 (limited novelty) and -1.19 / -1.14 (baseline comparison, presentation). The current paper improves on those dramatically. However, my draft's weaknesses (EuroSAT at 2.95, error bars at 1.13, WaffleTaxS at 2.05) are genuine and, absent strong rebuttal from the authors, prevent the paper from crossing into the 6+ acceptance zone occupied by DeMul and TAP.

Here is my final review:

## Summary

This paper proposes DefNTaxS, a training-free framework for zero-shot image classification. It uses an LLM to cluster classes into taxonomic subcategories, then augments CLIP prompts with both class-level descriptors (following D-CLIP) and subcategory-level context phrases (e.g., "commonly found among kitchen utensils"). The method achieves the best average accuracy (61.17%) across seven standard benchmarks, is fully automated, and costs $0.38 in LLM API calls.

## Strengths

- **Clean and well-motivated idea.** The paper identifies a real limitation of descriptor-based approaches: they describe classes in isolation and miss the relational context humans use to resolve ambiguity. The running example of "boxer" as dog vs. sport makes the intuition concrete. The proposed solution — adding taxonomic context via LLM-generated subcategories — is a natural and principled extension.

- **Practical and low-cost.** The framework requires no training, no parameter updates, no manual prompt engineering, and costs $0.38 total in LLM API calls (line 158). This is a genuine practical advantage for deployment.

- **Generally positive results.** DefNTaxS achieves the best average accuracy (61.17%) across the benchmark suite, outperforming all baselines on mean performance by a clear margin (~3 points over D-CLIP, ~3.2 over CGPT-P). Gains on ImageNet (+4.59 over CLIP), Pets (+8.21), and EuroSAT (+12.96) are substantively large.

- **Relevant ablation work.** Section 6 makes a genuine attempt to disentangle the contributions of descriptors vs. taxonomic context vs. differentiation effects, including the k-means clustering comparison (Table 5) and the random-character variants (Table 4).

## Weaknesses

### Major

- **The EuroSAT result does not support the paper's central causal claim as stated.** EuroSAT has 10 classes, and the paper explicitly states: *"For datasets with fewer than 20 classes, we use the dataset name as the single subcategory context (e.g., 'EuroSAT dataset')"* (line 99). This means the taxonomic context is an identical suffix for all 10 classes, providing no discriminative information between them. Yet DefNTaxS improves over D-CLIP on EuroSAT by **+9.86 absolute points** (47.36 → 57.22) — the largest gain on any dataset. On datasets where differentiated subcategories are actually generated, the gains over D-CLIP are far smaller: +0.48 (IN), +0.79 (CUB), +0.66 (INV2), +0.16 (Places). The paper's explanation — *"taxonomic context helps distinguish land use categories that share visual similarities"* (line 199) — is contradicted by its own design. This does **not** invalidate the method (the domain-level context "EuroSAT dataset" could still help by grounding the classification task), but it means the paper's largest empirical win does not cleanly support the central thesis that *differentiated* taxonomic subcategories drive the improvement. The paper should either explain this result in a mechanism-consistent way or conduct additional controlled experiments (e.g., removing the dataset-name suffix for EuroSAT and measuring the drop).

### Minor

- **The "new state-of-the-art" claim is imprecise.** Table 1 shows CHiLS outperforms DefNTaxS on Food101 (83.53 vs. 81.48) and Places365 (40.45 vs. 40.00). The paper states DefNTaxS achieves *"the highest accuracy across six of seven benchmarks"* (line 197), but it wins on 5 of 7 (IN, CUB, Pets, DTD, ESAT). The abstract and contributions section claim *"establishing new state-of-the-art results"* without qualification. The accurate claim is that DefNTaxS achieves the **best average accuracy**, not universal SOTA.

- **Main results lack variance estimates.** Table 1 reports single numbers without error bars. Many gains over the strongest baselines are small: +0.48 over D-CLIP on ImageNet, +0.79 on CUB, +0.66 on INV2, +0.16 on Places. The ablation in Table 4 reports standard errors over 5 runs, where DefNTaxS on ImageNet shows a standard error of ~0.26, suggesting the +0.48 gain could be within one standard error. Without variance on the main table, readers cannot assess whether the headline improvements are reliable.

- **The descriptor generation pipeline is not fully controlled.** The paper uses *"a modified version of D-CLIP's generation pipeline"* (line 151) without describing the modification. It states baselines were recreated using the setup in Section 4.1, but does not explicitly confirm that the D-CLIP baseline used the same descriptor pipeline. If the descriptor quality varies between methods, the claimed improvement from taxonomic context could be confounded with descriptor quality differences.

- **The WaffleTaxS ablation partially weakens the "essential" framing.** Table 4 shows WaffleTaxS (random characters replacing subcategory labels) outperforms full DefNTaxS on ImageNet (63.24 vs. 62.96) and Places365 (40.05 vs. 39.34), and is effectively tied on CUB. The paper acknowledges "mixed results" (line 269), but the claim that *"taxonomic context is not just helpful but essential"* (line 179) is at odds with random characters sometimes working better than real taxonomic labels. This suggests that on some datasets, differentiation structure matters more than semantic content — a finding that deserves deeper engagement rather than acknowledgment in passing.

### Trivial

- The conclusion's claim that DefNTaxS represents *"a paradigm shift toward context-aware zero-shot learning"* (line 297) is disproportionate to the contribution, which is a useful but incremental extension of existing LLM-prompting and hierarchy-based methods.

## Nice-to-Haves

- Test sensitivity to LLM capability (e.g., does a weaker/cheaper LLM produce less useful taxonomies?).
- Show examples of the actual subcategories generated for full datasets (e.g., what does the taxonomic structure look like for ImageNet's 1000 classes?).
- Add per-class analysis to verify whether improvements concentrate on ambiguous classes (as the motivation predicts) or are spread uniformly.

## Removed Points

- *"Failure modes not novel"*: This is an opinion about novelty framing that is not clearly verifiable; the paper's synthesis of known observations into a systematic framework is itself a contribution.
- *"Missing sensitivity to LLM choice"*: A nice-to-have rather than a core weakness given the paper's focus on a framework that could work with any LLM.
- *"Missing qualitative taxonomy examples"*: A presentation improvement, not a structural weakness.
- *"Missing per-class analysis"*: Would strengthen the analysis but is not required for validity.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the EuroSAT puzzle.** Either provide a mechanism-consistent explanation (e.g., the dataset-name suffix grounds the domain even without differentiation) or conduct controlled experiments (e.g., removing the suffix, comparing with a generic non-informative suffix) to isolate what drives the gain. The current explanation contradicts the method's design.
2. **Add error bars to Table 1.** Run at least 3–5 trials with different LLM samples (temperature) and report mean ± standard error.
3. **Clarify the descriptor pipeline modification.** Specify how the modified D-CLIP generation pipeline differs from the original, and confirm explicitly that all baselines (especially D-CLIP) used the same pipeline.
4. **Temper the claims.** Replace "essential" and "paradigm shift" with more measured language. Rephrase the SOTA claim as "best average accuracy" rather than universal SOTA.
5. **Engage more deeply with the WaffleTaxS finding.** Discuss what the mixed results imply about when taxonomic semantics vs. differentiation structure drives improvements.

## All Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|------|-----------|-------|----------|------------------------|
| B2ChNpcEzZ.md | 4.00 (3,5,3,5) | R1 | Yes | Earlier version of the same paper; lacked CHiLS comparison and had presentation issues. Current version is a clear improvement. |
| HfJxXbXlYJ.md | 3.00 (3,3,3,3) | R1 | No | LLM2CLIP — more limited approach; lower quality. |
| WqeRtP2T3R.md | 4.67 (3,6,5) | R2 | Yes | Embracing Diversity — similar in using LLM subclasses for zero-shot CLIP; marginal gains and novelty concerns. Comparable quality but this paper has stronger ablations. |
| t84UBRhhvp.md | 4.75 (5,3,6,5) | R1 | Yes | Text Descriptions — similar LLM-descriptor augmentation; very marginal improvements. This paper shows larger gains. |
| w49jlMWDSA.md | 5.33 (6,5,5) | R1 | Yes | GIST — generates descriptions for fine-tuning; similar approach space but requires training. This paper is training-free. |
| DPp5GSohht.md | 4.25 (3,3,3,8) | R1 | Yes | Unclipping CLIP's Wings — different focus (robustness/spurious correlations); comparable methodological quality but this paper has better coverage. |
| NDLmZZWATc.md | 6.40 (6,6,8,6,6) | R1 | Yes | DeMul — accepted paper with prompt learning; more sophisticated methodology, fewer concerning weaknesses. This paper is not at same quality level. |
| wFs2E5wCw6.md | 6.40 (6,6,6,6,8) | R2 | Yes | TAP — accepted paper with tree-of-attributes prompt learning; more thorough evaluation on 11 datasets. This paper has weaker evaluation methodology. |
| aMfdN4ZQVx.md | 5.75 (6,6,5,6) | R3 | No | Training-free Deep Concept Injection — different crossmodal task; similar training-free paradigm. |

**Score placement relative to anchors**: The earlier version of this paper scored 4.00, and the current version addresses several of its major weaknesses (now includes CHiLS comparison, better ablations). Compared to papers at 4.67–5.33 (Embracing Diversity, GIST, Text Descriptions), this paper has: (a) better average gains over baselines (vs. marginal gains in those papers), (b) more thorough ablations, and (c) a cleaner methodological contribution. However, the EuroSAT puzzle is a more concerning anomaly than anything those papers faced, and the missing error bars on main results weaken the evidence for small-but-claimed improvements. This paper is clearly above the 4.0 prior version and above the typical reject-range papers at ~4.7, but the EuroSAT issue and missing error bars keep it from reaching the 6+ acceptance zone occupied by DeMul and TAP.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>