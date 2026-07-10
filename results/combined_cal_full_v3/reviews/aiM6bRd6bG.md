## Summary

This paper introduces a two-stage framework for PPI candidate ranking: (1) an "interpretability-guided" retrieval step that uses contact maps from D-SCRIPT/Topsy-Turvy to identify active residue regions and computes cosine similarity over those regions for ranking, followed by (2) a re-ranking module that integrates interaction scores, structural plausibility (pDockQ), functional annotations, and LLM-based semantic scores. The key methodological strength is the prospective evaluation design — using STRING v11 as known interactions and STRING v12 as a held-out test set — which is genuinely forward-looking compared to standard retrospective PPI benchmarks. The paper also provides a comprehensive comparison of re-ranking signals.

## Strengths

- **Prospective evaluation design (Section 5.1, Table 1).** Using STRING v11 interactions as known and v12 interactions as a held-out prospective test set is a genuinely forward-looking assessment. Most PPI evaluations are retrospective splits within a single database release, so this design directly addresses whether computational methods can anticipate yet-undiscovered interactions — raising the bar for PPI evaluation.

- **Well-motivated problem formulation (Section 4, lines 63–71).** The formalization of PPI candidate ranking — given a target protein and its known partners, rank the remaining candidates — cleanly separates the task from standard binary classification or link prediction. The framing around guiding in vitro experiments toward promising candidates is concrete and practically significant.

- **Comprehensive exploration of re-ranking signals (Section 4.2, Table 2).** The paper evaluates a diverse set of complementary signals: interaction scores, structural plausibility (SpeedPPI/pDockQ), functional annotation overlaps (TF-IDF, Jaccard on GO terms, domains, pathways, localization), and multiple LLM-based approaches (BioBERT, BioMedRoBERTa, PubMedBERT cross-encoder). The pairwise rank-shift analysis provides a structured comparison of which signals add the most value.

- **Candid limitations section (Section 6, lines 284–294).** The paper acknowledges key limitations: reliance on known partners (fails for underexplored proteins), that the rankings are not truly interpretable, and that embeddings remain a black-box representation.

## Weaknesses

### Fatal
None.

### Major

- **Headline quantitative claim is unsupported by the paper's own data.** The abstract (line 25) states that the approach "improve[s] ranking metrics by two orders of magnitude" and the conclusion (line 278–279) says "up to two orders of magnitude." "Two orders of magnitude" means 100×. The largest improvement in Table 1 (D-SCRIPT MAP@5: 0.0103 → 0.2714) is ≈26×, roughly 1.4 orders of magnitude. Most improvements range from 5× to 26×. While the gains are substantial and practically meaningful, the paper overstates their scale and must correct this claim.

- **Missing ablation confounds the core contribution.** The comparison against baselines conflates two differences: using internal embeddings vs. output probabilities, and using active-region selection. The baselines rank by raw interaction probabilities from D-SCRIPT/Topsy-Turvy/xCAPT5. The proposed method uses the same models' internal embeddings with cosine similarity. Without an ablation comparing (a) raw output probabilities, (b) full-embedding cosine similarity without active-region selection, and (c) active-region cosine similarity (the proposed method), the paper cannot attribute its improvements to the active-region mechanism. The gains could partially reflect that embedding-based similarity is a stronger ranking signal than classifier output probabilities, independent of the active-region selection. This is the single most important missing experiment.

### Minor

- **No statistical significance or variance reporting.** The evaluation (Table 1, Table 2) is a single run on a single train/test split (STRING v11 → v12). No confidence intervals, standard deviations, or error bars are reported. Given the computational costs (hundreds of hours) this is understandable, but it limits confidence in the precision of the reported metrics.

- **Re-ranking operates only on top-10 candidates (Section 4.2).** The re-ranking analysis covers only a small fraction of the overall ranking problem. The improvements in Table 2 apply only to this restricted set.

- **Potential PubMedBERT leakage acknowledged but not quantified (lines 262–264).** LLMs pretrained on biomedical corpora may encode information about interactions later confirmed in STRING v12. The strong PubMedBERT performance (75.5–79.7% maintain/improve) could be partially confounded.

- **Post-hoc selection of D-SCRIPT for re-ranking (lines 241–242).** D-SCRIPT is chosen because it performs better on early ranking metrics. Reasonable, but limits the generality of the re-ranking conclusions to this one model.

- **Table 2 reports fraction not magnitude of improvement.** Reporting only the fraction of interactions whose rank was maintained/improved misses the magnitude. A method could improve a large fraction by small amounts while another improves a smaller fraction by larger amounts, making head-to-head comparisons incomplete.

### Trivial

- **Active-region selection heuristics are not analyzed.** The method uses maximum contact probability and selects a single best contiguous segment. A protein's binding interface could consist of multiple non-contiguous segments; the method selects only one contiguous region, potentially missing biologically relevant signals.

## Nice-to-Haves

- Stratify results by number of known partners per target protein to test the method's core assumption.
- For the re-ranking analysis, report mean/median rank-change magnitude alongside the fraction maintained/improved.
- Quantify potential PubMedBERT leakage by analyzing whether v12 interactions have distinctive textual fingerprints in the pretraining corpus.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"Interpretability-guided" framing is misleading:** REMOVED because the paper explicitly addresses this. Lines 21–22 clarify: "we do not frame interpretability here as a means to generate explanations for users; rather, we leverage interpretable model structures as a methodological device." The contact maps ARE interpretable (residue-level predictions), making this a reasonable characterization given the paper's own definition.
- **"Fundamentally unfair" baseline comparison (wording):** The comparison IS confounded (captured in Major above) but calling it "fundamentally unfair" or "structural" overstates the issue. The baselines are natural approaches for the task; the paper needs an ablation, not a correction of unfairness.
- **Formatting/style nitpicks and parser artifacts:** REMOVED per instructions.
- **Speculative concerns about evaluation stability:** WEAKENED to the "no variance reporting" minor weakness.
- **Missing related works:** REMOVED per instructions.
- **Section-by-section notes about heuristic design choices:** REMOVED as these are minor design decisions that don't threaten core claims.
- **xCAPT5 results being "puzzling":** REMOVED; the reviewer acknowledged this is internally consistent.
- **pDockQ computational cost:** REMOVED; paper acknowledges this; not a method weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Most important:** Add an ablation comparing (a) raw output probabilities, (b) full-embedding cosine similarity without active-region selection, and (c) active-region cosine similarity. This isolates the contribution of the active-region mechanism from the general advantage of embedding-based similarity.
2. Correct the "two orders of magnitude" claim to accurately reflect the 5–26× improvement range shown in Table 1.
3. Report variance (e.g., bootstrap confidence intervals) or justify why single-run evaluation is standard at this computational scale.

## Score and Decision

**Round 1 bracket**: 4.0–6.5 (based on closest topical anchors ProtIR 5.25, MAPE-PPI 5.67, LLaPA 6.00, NovoBench 4.60).

**Narrowing**: The paper's lowest weakness favorability (0.32 → 1.26 for missing ablation after refinement) is notably better than MAPE-PPI (-4.13 for missing references) and ProtIR (-4.87 for missing baselines), and comparable to LLaPA (0.22 for unfair comparison). Its top strengths (8.86–9.12) are well above the anchor averages. The two major weaknesses (overclaim at 2.98 favorability, missing ablation at 1.26) are genuine but correctable — they don't invalidate the method, but they prevent acceptance in the current form. The prospective evaluation design is a genuinely valuable contribution that sets the paper apart from typical PPI work. Against anchors: stronger than NovoBench (4.60) and ProtIR (5.25), comparable in weakness severity to LLaPA (6.00, rejected) but with cleaner methodology, weaker than MAPE-PPI (5.67, accepted) in terms of overall contribution density. The paper is borderline — the core idea has clear merit but the overclaim and missing ablation are significant issues that require revision.

**Final score**: 5.0

**Final decision**: Reject

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>