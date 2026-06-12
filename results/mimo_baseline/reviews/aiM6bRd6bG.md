## Summary

This paper introduces the problem of PPI candidate ranking—prioritizing novel protein-protein interactions for experimental testing—and proposes a two-stage framework: (1) an interpretability-guided retrieval step that uses contact-map-activated embedding regions from D-SCRIPT and Topsy-Turvy to rank candidates by cosine similarity to known interactors' active residues, and (2) a re-ranking module that incorporates interaction scores, structural plausibility (SpeedPPI/pDockQ), semantic annotation overlap, and LLM-based signals. Evaluated on the STRING v11→v12 prospective transition, the approach substantially improves early ranking metrics over raw model probability baselines.

## Strengths

- **Novel problem formulation with practical relevance.** Framing PPI prediction as a candidate ranking task for experimental prioritization is a meaningful reframing that directly addresses the discovery bottleneck. The formulation leverages known interactors of a target protein as anchors, which is a sensible inductive bias for guiding wet-lab experiments.

- **Large-scale prospective evaluation.** The v11→v12 STRING transition provides a genuinely prospective test, avoiding the retrospective evaluation pitfalls common in PPI prediction benchmarks. The evaluation covers thousands of proteins and hundreds of thousands of novel interactions, lending statistical credibility to the findings.

- **Comprehensive multi-signal re-ranking analysis.** Table 2's pairwise rank-shift analysis is a valuable contribution, systematically quantifying complementarity across sequence-based, structure-based, annotation-based, and LLM-based signals. The finding that PubMedBERT consistently improves rankings (75.5%) and that even lightweight heuristics like KeyTerm Jaccard similarity are surprisingly effective (69.3% improvement over cosine) provides actionable guidance for the community.

- **Significant improvement over naive baselines.** The interpretability-guided retrieval produces meaningful gains: Recall@10 jumps from ~1.2% to ~26.4% for D-SCRIPT, and MRR improves from 0.034 to 0.169. These are practically significant numbers for candidate screening.

## Weaknesses

### Fatal

None.

### Major

- **Overstated "two orders of magnitude" claim.** The paper claims improvements of "up to two orders of magnitude" over existing models. However, examining Table 1, the largest improvements are roughly 20-26× on Precision@5 and MAP@5 (0.0080→0.1924 and 0.0103→0.2714, respectively). MRR improves ~5×. No metric shows a 100× improvement. This claim appears in both the abstract and conclusions and should be corrected.

- **xCAPT5 comparison appears inconsistent.** xCAPT5 shows dramatically different behavior from D-SCRIPT and Topsy-Turvy: very high early precision (Precision@5=0.1943) but low prediction coverage (0.8088 vs. 0.95-0.97 for others) and poor MRR (0.0315) with a much higher average rank (900.11). This pattern suggests xCAPT5 may be operating on a different candidate space or under different evaluation conditions. The paper does not clarify whether the same candidate set and preprocessing were applied to xCAPT5, making the comparison potentially unfair or misleading.

- **Single database transition as the only evaluation.** The entire evaluation rests on one prospective transition (v11→v12). While this is valuable, the paper provides no robustness analysis: How sensitive are results to the CD-HIT threshold (40%), the interaction confidence cutoff, the sequence length filter (50-800), or the negative sampling ratio (10:1)? Without such analysis, it is difficult to assess whether the improvements are stable across reasonable experimental variations.

### Minor

- **Re-ranking limited to top-10 candidates.** The re-ranking module operates on only 10 candidates per protein (2,280 pairs total), which is a narrow window. The paper acknowledges this is due to computational costs of some signals (e.g., SpeedPPI), but does not analyze how re-ranking performance changes with candidate list size, limiting the practical implications of the re-ranking results.

- **Circularity in the ranking assumption.** The core assumption—that novel interactions follow patterns similar to known ones—is reasonable but has a fundamental limitation not experimentally explored: a target protein may recruit novel partners through entirely different binding interfaces than those used by known partners. The method would systematically miss such interactions. Quantifying performance stratified by the number of known partners would help assess this concern.

- **Confusing table presentation.** Table 1 mixes "Prediction Probability" and "Our Approach" rows with interleaved D-SCRIPT/Topsy-Turvy labels, making it difficult to parse which rows correspond to which backbone. The footnote text for Table 2 appears incomplete ("† reports... and ‡ is reported").

- **Baseline comparison fairness.** The raw D-SCRIPT and Topsy-Turvy probabilities are used as baselines, but these were not designed for ranking tasks. Comparing against dedicated ranking methods or a simple embedding-similarity baseline (without the active-region selection) would better isolate the contribution of the interpretability-guided component.

### Trivial

None worth noting beyond parser artifacts.

## Nice-to-Haves

- An ablation study isolating the contribution of the active-region selection mechanism (vs. using all residues for similarity computation) would strengthen the interpretability-guided retrieval claims.
- Performance breakdown by the number of known partners per protein would clarify when the method works best and when it degrades.
- A discussion of computational budget tradeoffs across re-ranking signals (Figure 3 is mentioned but not shown in the paper content) would help practitioners choose appropriate signals.

## Novel Insights

The paper makes a genuinely novel observation that leveraging interpretable model structures as a methodological device—not for explanation but for ranking—can substantially improve PPI candidate prioritization. The finding that PubMedBERT-based semantic re-ranking consistently outperforms both sequence-embedding similarity and structure-based pDockQ for re-ranking is surprising and suggests that functional annotations and textual context capture complementary biological signals not fully encoded in protein language model embeddings. The systematic demonstration that even lightweight textual overlap metrics (KeyTerm Jaccard) can meaningfully improve PPI rankings highlights that information beyond raw sequence—cellular localization, functional annotations, pathway membership—is currently underutilized in PPI prediction and provides a clear signal for the community to integrate such features.

## Suggestions

- Correct the "two orders of magnitude" claim throughout the paper to accurately reflect the observed ~5-25× improvements.
- Clarify the xCAPT5 evaluation setup to ensure fair comparison: specify whether identical candidate sets, preprocessing, and metrics were used.
- Add robustness analysis across at least 2-3 parameter variations (confidence threshold, clustering identity, negative ratio).
- Add an ablation comparing active-region similarity vs. whole-sequence cosine similarity to isolate the contribution of the interpretability-guided component.
- Restructure Table 1 for clarity, perhaps separating backbone comparison from approach comparison into distinct panels.

## Score and Decision

The paper addresses a practically important problem with a novel methodology and provides a thorough multi-signal evaluation on a realistic prospective benchmark. The core contribution—using model-internal representations for ranking rather than prediction—is a meaningful conceptual advance. However, the overstated claims, questionable xCAPT5 comparison, and single-transition evaluation without robustness analysis are notable shortcomings that weaken confidence in the generality of the results. The paper is above the median quality for the venue but falls short of clear acceptance.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>