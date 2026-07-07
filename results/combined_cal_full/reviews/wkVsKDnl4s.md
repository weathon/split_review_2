Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper presents HighClass, a metagenomic classification framework that replaces traditional alignment-based seed-and-extend operations with hash-based token-to-taxon lookups using variable-length QA-Token vocabularies. The system achieves 85.1% F1 on CAMI II (within 1.5 pp of state-of-the-art MetaTrinity) while delivering a 4.2× speedup and 68% memory reduction. The paper also presents a theoretical analysis with claimed generalization bounds, concentration inequalities under α-mixing, and consistency guarantees.

## Strengths

- **Conceptually clean architectural transformation.** The core idea—replacing alignment operations (seed-and-extend) with hash-based token-to-taxon lookups—is well-motivated and elegantly described (Sections 3.3–3.5). The argument that taxonomic classification does not strictly need positional alignment is defensible and, if validated, would be a useful insight.

- **Well-structured ablation study.** Table 3 cleanly isolates the contributions of the variable-length vocabulary (+6.8 pp over k-mers), quality weighting (+1.9 pp), and sparsification (99.5% relative accuracy retained). The additive decomposition of effects (<0.5 pp interaction) makes the contribution of each component transparent.

- **Rigorous statistical reporting.** The paper reports 95% bootstrap CIs, Wilcoxon signed-rank tests with Holm-Bonferroni correction, and Cohen's *d* effect sizes (Table 2, Section 5.3). This is a higher standard than typical in the field.

- **Practical memory efficiency.** The gradient-based sparsification reducing the index to 6.8 GB (Section 5.2, Table 1) is a genuine engineering contribution—it brings the system into a memory footprint where it could plausibly run on a single workstation.

## Weaknesses

### Fatal
None.

### Major

- **The claimed generalization bound rate is inconsistent with the reported numerical value.** The paper states the excess risk decreases at rate *O(√(V|𝒴|/n))* and, for *V=32,000*, *|𝒴|=100*, *n=10⁶*, yields a bound of ≈0.021 (lines 164, 174). However, plugging those parameters into the stated formula gives √(32,000 × 100 / 1,000,000) = √3.2 ≈ **1.79**. A bound of 1.79 on excess risk (defined on [0,1]) is vacuous, while the reported 0.021 is smaller by roughly 85×. The paper does not explain this gap (e.g., hidden constants or log factors). A similar inconsistency appears at line 306 (Section 6.1), where the rate is written as *O(√(V𝒴)/n)*—a different expression entirely. This undermines the theoretical contribution as presented. The theory is listed as the paper's first contribution and cannot be accepted at face value with this discrepancy.

- **The "Metalign" baseline used in Table 4 (scalability analysis) is never defined or cited.** The main comparison throughout the paper is with MetaTrinity; "Metalign" appears only in this one table with no reference, description, or citation. The reader cannot evaluate whether Metalign is a state-of-the-art method, a weaker baseline, or an internal/ablation baseline. This is a straightforward evidential gap—a comparison against an unidentified method is not informative.

### Minor

- **Multiple numeric inconsistencies across tables and text.** (a) Table 5 reports HighClass total at 1.9±0.1 ms/read, but line 298 states the speedup as "8.8ms → 2.1ms per read"—the 2.1 does not match the table and implies a different speedup (4.2× vs 4.63×). (b) Table 1 lists the sparsified index as 6.8 GB; Table 2 lists HighClass's index as 6.2 GB—these refer to the same sparsified index and should match. (c) Line 104 states "reduce our index from 19.3 GB to 6.8 GB," but Table 1 lists the full (unsparsified) index as 21.3 GB, not 19.3 GB (the 19.3 appears to be MetaTrinity's memory footprint from Table 2). These individually minor issues collectively indicate careless data reporting that erodes confidence in the numerical claims.

- **The QA-Token F1 discrepancy is unexplained.** The paper states QA-Token achieves 0.917 taxonomic F1 on CAMI II (line 100, citing Gollwitzer et al., 2025). Yet Table 3 shows that QA-Token vocabularies combined with MetaTrinity's alignment pipeline achieve only 86.2% F1 = 0.862—a gap of 5.5 pp. If QA-Token's own pipeline achieves 0.917, the paper should explain why the same vocabulary produces 0.862 in HighClass's pipeline, or specify whether these measurements are at different taxonomic ranks or on different subsets.

- **The variance inflation factor (≈31.7) is stated but not reconciled with the generalization bound.** Section 4.3 reports that token dependencies inflate variance by a factor of approximately 31.7, implying an effective sample size of roughly n/31.7 ≈ 31,500 rather than n = 10⁶. The nominal generalization bound (line 174) uses n = 10⁶ as if observations were independent. The paper presents these two analyses side by side without addressing the tension, leaving the reader to wonder whether the bound would survive recomputation with the effective sample size.

### Trivial
None.

## Nice-to-Haves

- The F1/hour metric (Table 6) is reasonable as a combined accuracy-efficiency measure, but the paper could strengthen the efficiency comparison by also presenting Pareto-style analysis (accuracy vs. runtime scatter or iso-accuracy runtime comparisons). This is not a weakness of the current presentation but would make the efficiency claims more robust.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **F1/hour metric criticized as "non-standard and potentially misleading"**: REMOVED. F1/hour is a reasonable combined accuracy-efficiency metric in systems papers. The extreme hypothetical scenario (1% F1 at near-zero runtime) is not a realistic concern for this domain and does not correspond to any method evaluated.
- **"Table captions contain substantive analysis"**: REMOVED. This is a presentation preference; table captions in ICLR format often include brief interpretive comments and this is not a substantive weakness.
- **"Missing code/data availability"**: REMOVED per hard rules. The paper has a reproducibility statement promising release; questioning future releases is speculative.
- **"Missing appendix / proofs"**: REMOVED. The appendix is stripped by the parser for all papers; it exists in the original submission.
- **"QA-Token vocabularies don't outperform MetaTrinity's native approach"** (section-by-section note): REMOVED. The paper's vocabulary contribution (+6.8 pp) is measured against fixed k-mers, which is the appropriate comparison for a tokenization method. The comparison to MetaTrinity's full pipeline conflates different contributions.

## Novel Insights

The harsh critic's arithmetic verification of the generalization bound (√(V|𝒴|/n) with the paper's own parameters produces 1.79, not 0.021) is the most striking insight from the review process—it reveals a discrepancy that is verifiable from the main text without needing the appendix. This is not a matter of interpretation but of basic arithmetic, and the paper provides no resolution. Beyond this, the review surfaces the pragmatic importance of the "QA-Token + MetaTrinity alignment" row in Table 3 (86.2% F1, only 0.4 pp below full MetaTrinity), which cleanly quantifies what is gained and lost by removing alignment (1.1 pp accuracy for 3.8× speed), and which the paper under-discusses in favor of the more attention-grabbing but less informative "Full HighClass vs. MetaTrinity" comparison.

## Suggestions

1. **Resolve the generalization bound inconsistency.** Either correct the stated rate to match the numerical bound (and explain the actual formula, including any constant factors or log terms), or revise the bound value and acknowledge the implications. This is the single most important fix.

2. **Identify and cite the "Metalign" baseline in Table 4**, or replace it with a method that is properly defined in the paper.

3. **Reconcile the numeric discrepancies** (index sizes: Table 1 vs Table 2 vs line 104; per-read time: 1.9 vs 2.1 ms). Ensure all reported numbers are self-consistent.

4. **Explain the 5.5 pp gap** between QA-Token's reported 0.917 F1 and the 86.2% F1 achieved with QA-Token vocabularies in the paper's pipeline, or add a caveat specifying the taxonomic rank or evaluation subset.

5. **Discuss the variance inflation factor (31.7) in relation to the generalization bound**—either recompute the bound with the effective sample size, or explain why the nominal bound remains valid despite dependencies.

## Score and Decision

**Bracket (Round 1):** After draft weighting and initial calibration, the plausible range is [3.5, 5.5]. The paper sits below bio2token (5.00, net weighted sum -2.39) and HashOrder (5.50) due to the verifiable theoretical inconsistency, but above the metagenomic binning paper (4.33, stronger novelty concerns) and the multimodal structure preservation paper (2.50, much weaker evaluation).

**Final score: 4.0.** The paper has genuine empirical contributions (clean ablation, strong statistical reporting, practical efficiency) and a well-motivated core idea, but the theoretical contribution—presented as the paper's first advance—contains a verifiable arithmetic inconsistency between the stated convergence rate and the claimed numerical bound. Combined with the undefined "Metalign" baseline and multiple numeric inconsistencies, these issues warrant a borderline-reject decision for the current version. The empirical results may well be real and valuable, but the paper's presentation and theoretical framing prevent a clear acceptance recommendation. With the issues addressed, a resubmission could be competitive.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>