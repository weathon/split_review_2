## Summary

This paper presents a dual-encoder system for language-based audio retrieval on the CLOTHO dataset, combining three techniques: (1) soft-label distillation from an ensemble of teacher models, (2) LLM-driven caption augmentation (back-translation and LLM mix), and (3) cluster-guided auxiliary classification. The best single model achieves mAP@16 46.6, and a weighted ensemble reaches 48.8 on the development test split. The paper uses a clear five-configuration ablation structure (SID 1–5) tested across three audio backbones (PaSST, EAT, BEATs).

## Strengths

- **Clean, interpretable ablation design.** The five SID configurations (Table 1) form a logical incremental chain — baseline → add distillation → add augmentation → add cluster supervision (two variants) — tested across three audio backbones (PaSST, EAT, BEATs). This allows readers to isolate each component's contribution.
- **Transparent problem framing for multi-caption ambiguity.** The paper correctly identifies that standard contrastive loss with hard one-hot targets is restrictive for datasets like CLOTHO where audio clips have multiple captions and captions can match multiple clips. The motivation for soft targets from an ensemble is well-posed.
- **Candid about limitations.** The paper explicitly acknowledges (lines 205–206) reliance on proprietary LLMs and "mixed single-model gains from cluster supervision," which is consistent with the ablation data.

## Weaknesses

### Fatal
None.

### Major

1. **No comparison to any prior published result on the same benchmark.**  
   The paper reports results on CLOTHO but never cites or compares against any previously published method on this dataset. There is no prior-art table, no reproduction of an existing method, and no baseline from the literature. For an ICLR submission, the reader has no way to assess whether a mAP@16 of 46.6 or 48.8 represents a meaningful advance. This omission prevents the paper from establishing the significance of its contribution.

2. **The ablation data does not support the paper's "joint improvement" claim.**  
   The abstract claims that the three components "jointly improve robustness," but the ablation tells a more selective story. Distillation (SID 1→2) accounts for nearly all the gain (e.g., PaSST: +4.54 mAP@16). The novel components have mixed results:
   - **Augmentation** (SID 2→3): improves EAT (+0.70 mAP@16) and BEATs (+0.77), but *lowers* PaSST (−0.21).
   - **Cluster guidance** (SID 3→4/5): consistently fails to improve over SID 2 across all three backbones (e.g., PaSST 46.62→46.50, EAT 45.35→45.34, BEATs 43.89→43.88 on mAP@16).  
   The paper's own conclusion acknowledges "mixed single-model gains from cluster supervision," which is at odds with the introduction's stronger joint-improvement framing. A narrative that centers distillation as the effective component and honestly reports the mixed results of the other two would better match the evidence.

3. **Substantial evaluation-set performance drop without discussion.**  
   The ensemble achieves 48.83 mAP@16 on the development test split but only 42.1 on the held-out evaluation set (line 198) — a drop of 6.7 points. The paper does not remark on this gap, does not provide evaluation-set numbers for individual systems, and does not analyze whether this reflects overfitting, a distribution shift, or the different (larger) training set used for the evaluation run. This is a significant omission for a system paper.

4. **No variance or uncertainty estimates.**  
   All results in Table 2 are single point estimates with no error bars, standard deviations, or multiple-seed runs. Given that many configuration differences are small (e.g., PaSST SID 2 at 46.62 vs. SID 5 at 46.50), it is impossible to distinguish signal from training noise. While single-run evaluation is not uncommon in this benchmark's convention, the paper makes fine-grained comparative claims (e.g., that cluster guidance "contributed to additional performance gains") that are uninterpretable without some measure of variance.

### Minor

- **Reproducibility limitations from proprietary LLM usage.** The augmentation pipeline relies on GPT-4o without providing prompts, target languages for back-translation, examples of generated captions, or the 50,000 generated audio-text pairs. The paper acknowledges this as a limitation but takes no mitigation steps.  
- **Missing cluster analysis details.** The paper does not report: the number of clusters produced by HDBSCAN, the fraction of captions labeled as outliers and reassigned, the semantic coherence of clusters, or whether the auxiliary classification accuracy correlates with retrieval performance. Without this, the mechanism by which clustering "enhances fine-grained alignment" remains opaque.  
- **Text encoder trainability not specified.** It is unclear whether the RoBERTa-large text encoder is frozen or finetuned during training, which affects interpretation of the alignment learning.  
- **Choice of mAP@16 not justified.** The paper uses mAP@10 and mAP@16 without explaining what K=16 corresponds to or why it was chosen, leaving a general ICLR audience without context.  
- **Ensemble weight search risks overfitting.** The grid-search over 12 component models with free validation-set weights (Table 3) is described but validation scores are not reported, and potential overfitting is not discussed.

### Trivial
- Augmentation details (signal mixing ratio, combined method for LLM mix) are not specified.
- The text states "three audio models" for the teacher ensemble but the exact composition is implicit rather than explicit.

## Nice-to-Haves

- Adding a table of published CLOTHO results with comparable metrics would dramatically increase the paper's informativeness.
- An ablation sweep over the distillation weight λ₁ (currently fixed at 1.0) would show whether the teacher's soft labels are being used at optimal strength.
- Evaluation-set results for individual systems (not just the ensemble) would help diagnose the 6.7-point drop.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Two of the three claimed contributions produce at best flat or negative results when added on top of distillation."* — **Removed because it's an overstatement.** The reviewer's analysis focused almost entirely on PaSST mAP@16 and omitted that augmentation improves EAT (+0.70 mAP@16) and BEATs (+0.77). The more accurate statement is that augmentation helps on some backbones but not others, and cluster guidance is consistently flat.
- *"The paper offers no theoretical argument for why they should be expected to help when the data shows they do not."* — **Removed as inaccurate.** Section 2.3 provides motivation (cluster guidance enhances "fine-grained alignment between audio and text") and Section 2.4 motivates augmentation (increasing caption diversity). The problem is not missing motivation but weak empirical support.
- *Strengths about "sensible problem framing" in generic terms* — **Removed because it is too generic;** the concrete version is preserved above.
- *Section-by-section nitpicks about Style/form (e.g., "the paper does not discuss how this affects the comparison" for EAT/BEATs being SSL models)* — **Removed as low-value speculation,** though the related point about text encoder trainability is retained.

## Novel Insights

The key insight from the review process is that the paper's data reveals a sharp asymmetry between its components: distillation (adopted from Primus et al., 2024) drives nearly all the improvement, while the two proposed novel components produce inconsistent or flat results. This creates a mismatch between the paper's narrative ("jointly improve robustness") and the ablation evidence — a gap that is partially acknowledged in the conclusion but not reconciled in the claims. The ensemble result (48.8) does demonstrate that combining all components with tuned weights beats any single component alone, but this is engineering optimization rather than scientific validation of each proposed technique.

## Suggestions

1. Recenter the contribution narrative around what actually works (distillation), and reframe augmentation and cluster guidance as exploratory components with mixed empirical support.
2. Add a comparison table to prior published CLOTHO results — this is the single most impactful change the paper could make.
3. Report variance estimates (multiple seeds) for the key configurations to make the small differences interpretable.
4. Analyze the evaluation-set performance gap and provide per-system results on the evaluation set.
5. Provide the augmentation prompts, generated data, and cluster diagnostics (number of clusters, outlier rate) to improve reproducibility and transparency.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>