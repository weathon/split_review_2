## Summary

This paper introduces a PPI candidate ranking framework that (1) uses known interaction partners as anchors and contact-map-predicted "active regions" to guide embedding-similarity retrieval, and (2) refines rankings by incorporating multiple biological signals (interaction scores, structural plausibility, functional annotations, LLM-based semantic similarity). The method is evaluated prospectively using STRING v11 as training data and STRING v12 novel interactions as ground truth.

## Strengths

- **Temporal evaluation design (Section 5.1, Table 1).** Using successive STRING versions (v11 → v12) as a prospective benchmark is a genuinely strong methodological choice. Testing on interactions confirmed *after* the model's training cutoff directly measures whether a method can anticipate future discoveries, which is the practical use case the paper motivates.

- **Interpretability-guided retrieval is a well-motivated idea (Section 4.1).** The core mechanism — using predicted contact maps from D-SCRIPT/Topsy-Turvy to identify active residue regions from known partners, then measuring cosine similarity only over those regions — is creatively grounded in the biological intuition that novel interactions should follow mechanisms similar to known ones.

- **Wide survey of re-ranking signals (Section 4.2, Table 2).** The paper studies a diverse set of biological signals (interaction scores, pDockQ structural plausibility, GO terms, TF-IDF on annotations, multiple LLMs) and provides a systematic pairwise comparison. This yields useful empirical evidence about which signals are complementary to sequence-based retrieval.

## Weaknesses

### Fatal
None.

### Major

- **Overstated quantitative claim (Abstract Line 25, Conclusion Lines 278–279).** The paper states it achieves "two orders of magnitude" improvement over baselines. Verifying against Table 1: the largest improvement is MAP@5 for D-SCRIPT (0.0103 → 0.2714, ~26×), followed by Recall@5 (0.0071 → 0.1832, ~26×). These are roughly 1.4 orders of magnitude, not 2. For Topsy-Turvy the improvements are smaller (MRR ~3.6×, Recall@5 ~9×). "Two orders of magnitude" implies ~100×; the best case is off by a factor of ~4. This is not a rounding issue — it is the headline figure in the abstract and conclusion, and it meaningfully misrepresents the results.

- **Missing critical ablation: what does the active-region masking contribute? (Section 4.1).** The proposed retrieval has two components: (a) using known partners as anchors, and (b) restricting cosine similarity to residues identified by predicted contact maps. The paper compares the full method against raw interaction probabilities (which use neither component). A natural and necessary baseline is missing: full-embedding cosine similarity (i.e., using the same known-partner-anchor strategy but computing similarity over *all* residues, not just active-region residues). Without this ablation, the reader cannot tell whether the improvement comes from the trivial nearest-neighbor effect of having any retrieval over known partners, or from the specific contact-map-guided residue selection that is the paper's primary methodological novelty.

### Minor

- **Re-ranking analysis reports only direction, not magnitude (Table 2, Section 5.3).** The pairwise rank-shift analysis reports only the fraction of true positives whose rank maintained/improved or worsened when switching between methods. A candidate moving from position 9→2 is treated the same as one moving from 10→9. Reporting mean/median rank shift or rank correlation would substantially increase informativeness. Additionally, the paper does not clearly state how many of the 2,280 protein-candidate pairs are true positives (novel v12 interactions), which would help contextualize the improvement fractions.

- **No variance or confidence intervals (Table 1).** All metrics are reported as single point estimates. Given the large candidate space and likely per-protein variation in how many novel partners exist, it is not possible to assess whether improvements are consistent across proteins or driven by a subset. Per-protein breakdowns or bootstrap intervals would strengthen the reliability of the main result.

- **Comparison between pipeline and raw models conflates problem framings (Table 1).** The baselines (D-SCRIPT, Topsy-Turvy, xCAPT5) rank candidates using only pairwise interaction probabilities without access to known partners. The proposed method uses known partners as anchors. While comparing the full pipeline against raw models is reasonable for an end-to-end evaluation, the paper would benefit from including a baseline that uses known-partner-aware retrieval with the original PPI models (e.g., rank candidates by max interaction probability with any known partner) to separate the effect of the retrieval strategy from the effect of the PPI model.

- **Missing details on evaluation scope (Section 5.1).** The paper reports 279,568 additional positives in v12 but does not state how many *target proteins* are evaluated or the distribution of novel partners per target. Without this, it is difficult to know whether a few well-connected proteins drive the aggregate metrics.

- **Retrieval runtime not contextualized (Line 233).** The paper states that retrieval runtimes are "in the order of hundreds of hours" but does not discuss whether this is acceptable for practical use or what approximations could reduce it.

### Trivial

- **Unclear prediction coverage figures (Table 1).** D-SCRIPT's prediction probability baseline has 95.4% coverage while the proposed D-SCRIPT method has 92.3%. This difference is not explained — does the method sacrifice coverage for ranking quality? Clarifying would help the reader interpret the trade-off.

## Nice-to-Haves

- **Combining re-ranking signals.** The paper motivates the re-ranking module as "integrating complementary sources of evidence" but tests each signal independently. A simple ensemble or rank aggregation across the best-performing signals would directly support this stated motivation.
- **Justification or ablation of the contiguous-segment assumption (Equation 3).** The sliding-window approach assumes active residues form a single contiguous block in the candidate. This is a non-trivial modeling choice that could miss non-contiguous binding interfaces.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Grammar/parsing artifact criticisms.** The reviewer flagged "Both baselines recover and xCAPT5" and "Topsy-Turvy achieving the broadest achieves the broadest prediction coverage" as prose issues. These are parser-induced artifacts, not author errors. Removed.

- **xCAPT5 discussion is too brief (Section 2).** The reviewer criticizes the xCAPT5 discussion as cursory. This is a minor presentation point about one baseline; removing it because it does not materially affect the paper's evaluation.

- **"Significant improvements" is vague (Abstract).** The reviewer calls out the phrase "yields significant improvements" as vague. This is generic language common in abstracts and does not constitute a substantive weakness.

- **Precision below 0.2 at k=5.** The reviewer notes that precision is below 0.2 and questions practical significance for wet-lab screening. This is a standard operating point in large-scale retrieval; the paper's framing is about ranking quality (recall, MRR), not absolute precision. Removed as scope creep.

- **Orphan protein coverage limitation should be quantified.** The paper acknowledges this limitation in Section 6. Requesting a specific fraction of the human proteome that would be covered is a reasonable enhancement but not a weakness of the presented work.

## Novel Insights

The most valuable insight from the reviews is that the "two orders of magnitude" claim is materially overstated by roughly a factor of 4, which changes how impressive the reported numbers appear. Beyond this, no genuinely novel insight emerges from the reviews beyond the paper's own contributions — the paper itself identifies the key limitations (reliance on known partners, non-interpretability of rankings) and the remaining weaknesses are standard areas for improvement (ablation analysis, variance reporting, more informative re-ranking analysis).

## Suggestions

1. Correct the "two orders of magnitude" claim to an accurate characterization (e.g., "up to 26-fold improvement" or "over an order of magnitude").
2. Add the key ablation: compare active-region cosine similarity against full-embedding cosine similarity (both using known partners as anchors) to isolate the contribution of the contact-map-guided masking.
3. Report per-protein variance or confidence intervals for the main retrieval metrics.
4. In the re-ranking analysis, report mean/median rank shift in addition to fraction improved/worsened.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>