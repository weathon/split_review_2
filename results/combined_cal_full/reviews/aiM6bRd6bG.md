Now I have sufficient calibration data. Let me write the final consolidated review.

## Summary

This paper introduces a two-stage framework for ranking unconfirmed protein-protein interaction (PPI) candidates for experimental testing. The first stage uses interpretability-guided retrieval: given a target protein and its known interaction partners, it extracts "active residue regions" from predicted contact maps (using D-SCRIPT or Topsy-Turvy) and ranks novel candidates by cosine similarity of their embeddings to these active regions. The second stage re-ranks the top-10 candidates using 10 complementary signals (interaction scores, structural plausibility via SpeedPPI, functional/semantic scores, and LLM-based similarity). Evaluation uses a prospective design: known interactions from STRING v11 are used for retrieval, and novel interactions from STRING v12 serve as held-out ground truth.

## Strengths

- **Prospective evaluation design (Sections 5.1–5.3).** Training on STRING v11 and testing on novel v12 interactions is sound and addresses a genuine limitation of static, single-release PPI benchmarks. This tests whether the method can anticipate future discoveries rather than merely fit existing data. The paper correctly notes that most prior evaluations are retrospective.

- **Systematic enumeration of re-ranking signals (Section 4.2, Table 2).** The paper evaluates 10 distinct re-ranking strategies under a unified pairwise comparison framework (Cosine, IS, pDockQ, TF-IDF, Token, Location, KeyTerm, BioBERT, BioMedRoBERTa, PubMedBERT). The rank-shift analysis is a reasonable way to measure complementarity, and the finding that PubMedBERT (cross-encoder) provides the most consistent improvement is informative.

- **Clear practical motivation.** The problem of prioritizing PPI candidates for in vitro validation is well-motivated and directly relevant to experimental biology workflows. The paper's framing around the discovery gap is precise.

## Weaknesses

### Major

- **Table 1 contains a pervasive mathematical inconsistency between Precision@k and Success@k.** Section 5.2 defines Precision@k as "Fraction of the top-k candidates that are true partners" and Success@k as "Fraction of proteins where at least one true partner was found within the top-k." Under either micro- or macro-averaging, Precision@k ≤ Success@k is a necessary inequality (the maximum Precision occurs when every protein with a hit has all k slots filled). Yet in **every row** of Table 1, Precision@k > Success@k — often by a large factor. Examples: xCAPT5 at k=5 has Precision=0.1943 vs Success=0.0059 (a 33× violation); D-SCRIPT Prediction Probability at k=5 has Precision=0.0080 vs Success=0.0000, which is impossible under any standard interpretation since Success=0 means no protein has any true partner in the top-5, forcing Precision=0. This is not a single typo — it affects every model and every k-value. The paper's core quantitative evidence is uninterpretable until this is resolved. This weakness is verified by direct arithmetic on Table 1 (lines 163–192) against the definitions in lines 200–223.

- **The "two orders of magnitude" claim is unsupported by the reported numbers, even when taken at face value.** The abstract (line 25) and conclusion (line 279) claim improvements of "up to two orders of magnitude" (i.e., 100×). Reading Table 1: D-SCRIPT Recall@5 improves 26× (0.0071→0.1832), Recall@10 improves 21× (0.0124→0.2641), MRR improves 5× (0.0340→0.1685). Topsy-Turvy MRR improves 3.6× (0.0256→0.0925). The largest observed improvement is ~26×. This is hyperbolic and should be corrected.

### Minor

- **The re-ranking analysis is limited to the top-10 candidates, constraining the scope of its conclusions.** Section 4.2 states "due to the heavy processing of some of the techniques, we focus on the top 10 ranked candidates." While acknowledged, this means the re-ranking evaluation only assesses signals within an already-filtered pool of promising candidates. It does not test whether re-ranking could rescue genuinely novel partners ranked outside the top-10. The conclusions about re-ranking effectiveness should be stated with this caveat.

- **The xCAPT5 baseline is included in Table 1 but barely discussed.** xCAPT5 appears once in Related Work (Section 2, line 45) and in Table 1, but no description of its configuration or how it was applied is given. This is especially problematic because xCAPT5 has the most extreme Precision/Success inconsistency (k=5: 0.1943 vs 0.0059), making its results hard to assess.

- **The claim of "introduc[ing] the problem of PPI Candidate Ranking" (line 29) overstates novelty.** Prioritizing PPIs for experimental validation is an implicit goal of most PPI prediction work; STRING itself provides confidence scores designed for prioritization. The paper's specific formulation (ranking by similarity to known partners via embedding activations) is novel, but the problem framing should be more precise.

### Trivial

None.

## Nice-to-Haves

- **Active-region ablation.** The paper's core claim is that focusing on *active residues* (identified via contact maps) improves ranking. Adding a comparison between full-embedding cosine similarity (without the contact-map filter) and the proposed active-region similarity would isolate the contribution of the contact-map guidance and strengthen the paper's internal evidence.
- **Variance or significance estimates.** Table 1 reports point estimates with no indication of variance. Bootstrap confidence intervals or per-protein standard deviations would help assess reliability.
- **Distribution of novel partners.** Clarifying how many novel partners a typical target protein has would help interpret the aggregate metrics (e.g., whether a small number of hub proteins dominate the results).

## Removed Points

These points are flagged to be removed; treat them with caution:

1. *Missing ablation of full-embedding vs active-region similarity.* Kept as a nice-to-have; not a genuine weakness since the comparison to raw interaction probabilities is the relevant baseline.
2. *Circularity concern about AlphaFold2-based predictions in the test set.* Removed as speculative — the paper states it retains only interactions with "experimental support > 0" and does not provide evidence of actual leakage.
3. *Section 5.3 selection reasoning could be more quantitative.* Removed — the paper provides sufficient quantitative support (D-SCRIPT Recall@5=0.1832 vs Topsy-Turvy 0.0562) for selecting D-SCRIPT.
4. *Table 2 formatting symbols missing.* Removed — this is a parser artifact, not an author error.
5. *Statistical significance/variance missing.* Moved to nice-to-haves; standard deviation reporting is not a universal expectation for large-scale benchmarks.
6. *Distribution of novel partners per protein.* Moved to nice-to-haves; informative but not a flaw.
7. *The critic's "fatal" framing of the Table 1 issue.* Downgraded to Major — the inconsistency is real but could potentially be resolved with corrected definitions or a corrected table; the re-ranking analysis (Table 2) is unaffected, and other metrics (Recall, MAP, nDCG, MRR) may still be valid.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the Precision@k vs Success@k inconsistency.** Provide exact formulas for how each metric was computed. If the computation differs from the written definition, correct the definitions in Section 5.2. If the computation contains an error, produce a corrected table. This is the single highest-priority fix — the paper's core empirical contribution depends on Table 1.
2. **Replace "two orders of magnitude" with precise improvement factors** throughout the abstract, introduction, and conclusion. The data supports improvements of 5×–26×, not 100×.
3. **Add an ablation study** comparing full-embedding similarity (without contact-map filtering) against the proposed active-region similarity to isolate the contribution of the contact-map guidance.
4. **Provide a brief description of the xCAPT5 setup,** including how predictions were obtained and what configuration was used, to allow readers to assess this baseline.

## Score and Decision

**Score calibration:** Round 1 bracketing placed the paper between the 3.0 anchors (S2WHlhvFGg.md avg 3.00, An87ZnPbkT.md avg 3.00) and the 5.25–6.0 anchors (jsQPjIaNNh.md avg 5.25, eh1fL0zw8o.md avg 6.00). Weighted-item comparison:

- **vs. 3.0 anchors (S2WHlhvFGg.md, An87ZnPbkT.md):** Those papers have severe structural issues (e.g., data leakage in An87ZnPbkT.md at -11.39, confusing presentation at -12.02) that my paper does not share. My paper's strengths (+2.80, +2.45, +3.78) are stronger than the 3.0 anchors' strengths. So this paper is above 3.0.

- **vs. 5.25–6.0 anchors (jsQPjIaNNh.md 5.25, eh1fL0zw8o.md 6.00):** Those papers' weaknesses are about missing comparisons or novelty concerns (-9.87, -10.14). My paper's -6.21 (Table 1 inconsistency) is more damaging because it undermines the primary empirical evidence rather than peripheral issues. None of those anchors have a mathematical inconsistency in their primary results table. So this paper is below 5.25.

**Final score: 4.0.** The paper has a well-motivated problem, a sound prospective evaluation design, and a useful systematic comparison of re-ranking signals. However, the primary quantitative evidence (Table 1) contains a pervasive mathematical inconsistency between Precision@k and Success@k that makes the core results uninterpretable as presented. The "two orders of magnitude" claim is also unsupported. Without a corrected Table 1, the paper's central empirical claims cannot be confirmed.

**Decision: Reject**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>