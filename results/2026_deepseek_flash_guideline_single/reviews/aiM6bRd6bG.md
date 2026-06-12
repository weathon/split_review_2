Now I have enough calibration data. Let me write the final review.

## Summary

This paper introduces a PPI candidate ranking framework with two stages: (1) interpretability-guided retrieval that uses D-SCRIPT/Topsy-Turvy predicted contact maps to identify active residue regions and compute cosine similarity over those embeddings, and (2) multi-source re-ranking incorporating interaction scores, structural plausibility (pDockQ), functional annotations, and LLM-based signals. Evaluated prospectively on STRING v11→v12 (279,568 new positives), the method substantially outperforms raw interaction-score baselines.

## Strengths

- **Well-motivated problem formulation.** Framing PPI candidate ranking as distinct from PPI classification, with a prospective evaluation (STRING v11→v12), addresses a genuine gap in how computational methods are assessed. The motivation—that experimental validation is the bottleneck and prioritizing candidates is what matters—is practically significant and well-argued.

- **Creative and technically grounded retrieval method.** Using D-SCRIPT/Topsy-Turvy's predicted contact maps to identify active residue regions, then computing cosine similarity over those specific embedding regions (Equation 3), is a non-obvious design that leverages model structure beyond thresholding the final interaction probability. The sliding-window approach (Equation 3) reasonably handles unknown alignment between active regions.

- **Large-scale, principled evaluation.** The filtering pipeline (50–800 residue length, CD-HIT at 40% identity, 10:1 negative:positive ratio, only binding interactions with experimental support > 0) follows established protocols and produces a substantial test set of 279,568 new positives. The prospective design is more realistic than static single-release benchmarks.

- **Thorough exploration of re-ranking signals.** Testing 10 different re-rankers—from simple heuristics (token overlap, Jaccard on localization terms) through structure (pDockQ) to fine-tuned LLMs (PubMedBERT cross-encoder)—with pairwise comparisons (Table 2) provides informative insight into signal complementarity.

## Weaknesses

### Fatal
None.

### Major

**1. "Two orders of magnitude" claim is not supported by the reported data and constitutes an overstatement.**

The abstract (line 25) states "we improve ranking metrics by two orders of magnitude" and the conclusion (line 279) repeats "up to two orders of magnitude." However, Table 1 shows at most ~26× improvement (Recall@5: 0.0071→0.1832 for D-SCRIPT). MRR improves ~5× (0.0340→0.1685). Two orders of magnitude would require ≥100×. The paper's own results (line 233) say "MRR increases by 4-6 times," directly contradicting the "two orders of magnitude" framing. The actual improvements are genuinely impressive and do not need exaggeration. This discrepancy between headline claims and reported numbers undermines the paper's credibility.

**2. The active-residue selection is never ablated, so its benefit over simpler alternatives is unknown.**

The paper attributes its improvement to "interpretability-guided" selection of active residues. However, the baseline in Table 1 is the scalar interaction probability, not an embedding-based method without active-residue masking. Without comparing against (a) full-embedding cosine similarity without active-residue selection, (b) average-pooled embedding similarity, or (c) a learned embedding similarity metric, it is impossible to determine whether the improvement comes from switching to embedding-based similarity in general or from the active-residue masking specifically. The paper's central methodological claim—that interpretability-guided selection drives performance—remains unvalidated.

**3. The two-stage pipeline is never evaluated end-to-end.**

The retrieval stage (Table 1) and re-ranking (Table 2) are evaluated independently on different data slices. Re-ranking operates only on the top-10 retrieval candidates (line 109), and Recall@10 for D-SCRIPT is 26.4%, meaning 73.6% of true novel partners are excluded before re-ranking begins. Table 2 reports pairwise rank-shift fractions on the already-retrieved set of 2,280 candidate pairs, but this does not measure whether re-ranking improves the absolute metrics from Table 1 (Recall@k, Precision@k, MRR, nDCG). Without end-to-end metrics, the practical utility gain from the full pipeline is unclear.

### Minor

**1. Underspecified threshold for "highly activated" residues (Section 4.1).** The paper describes identifying "maximal contiguous segments of highly activated residues" (line 89) but does not state the threshold for what counts as "highly activated" (percentile? fixed probability value?). This affects reproducibility.

**2. Inconsistency in interaction score definition between Section 3 and Equation 6.** Section 3 describes D-SCRIPT's interaction probability $\hat{p}$ as a logistic output over aggregated contact map features. Section 4.2 (Equation 6) redefines $\hat{p}$ as $\max_{i,j} C(p,p_c)_{ij}$, the maximum contact map entry, while claiming it is the same score "directly predicted by D-SCRIPT" (line 111). These are not equivalent formulations.

**3. Re-ranking analysis limited to D-SCRIPT backbone.** The re-ranking experiments use only D-SCRIPT. Whether conclusions about PubMedBERT, pDockQ, etc. generalize to Topsy-Turvy—which also achieves strong retrieval results—is untested.

**4. No random baseline reported.** Given the extreme sparsity of true interactions, reporting expected random performance at each cutoff would calibrate interpretation of the results.

**5. Computational requirements underreported.** The paper states "hundreds of hours" (line 233) without specifying the number of target proteins, GPU/CPU hours per target, or how costs scale. This limits practical assessment of feasibility for biologists screening dozens or hundreds of targets.

**6. Table 2 caption incomplete.** The caption mentions a "‡" statistic that is never defined in the paper text (line 207). The reader must infer its meaning from context.

**7. Ground truth heterogeneity not stratified.** STRING v12 positives include structure-based predictions (line 194), but results are not stratified by whether positives are experiment-derived vs. prediction-derived. While this does not invalidate the evaluation, stratifying would strengthen it.

### Trivial
None.

## Nice-to-Haves

- Ablate active-residue selection by comparing against full-embedding cosine similarity and average-pooled embedding similarity without masking.
- Report end-to-end metrics: apply the best re-ranker (PubMedBERT) to the top-10 retrieval outputs and report Recall@k, MRR, etc. for the full pipeline.
- Replace "two orders of magnitude" with actual improvement ranges (e.g., "5–26× depending on metric").
- Define the activation threshold in Section 4.1 and clarify the IS formulation in Equation 6.
- Report the number of target proteins evaluated and the compute budget breakdown.

## Removed Points

These points from the harsh critic input are flagged as removed; treat with caution:

- **"The central claim of the method is not properly ablated"** — Already retained as Major Weakness #2.
- **"The two-stage pipeline is never evaluated end-to-end"** — Already retained as Major Weakness #3.
- **"Circularity concern for structural re-ranking (pDockQ vs STRING v12)"** — Removed because the data contradicts this concern: pDockQ is the worst-performing re-ranking signal (47.2% maintain/improve), which is inconsistent with circularity. The ground truth heterogeneity point is retained as Minor Weakness #7 in weakened form.
- **"xCAPT5 narrative confusion"** — Removed as a style nitpick; the paper's description of xCAPT5 precision is factual and not confusing.
- **"Prediction Coverage metric unclear"** — Removed; the metric is straightforwardly defined as a global value, and its interpretation alongside k-dependent metrics is standard practice.
- **"D-SCRIPT backbone selection not evaluated for Topsy-Turvy"** — Already retained as Minor Weakness #3.

## Novel Insights

None beyond the paper's own contributions. The harsh critic raises useful methodological critique points (ablation gap, disconnected evaluation stages) but these concern evidential holes, not novel observations about the domain.

## Suggestions

1. Add an ablation comparing active-residue-guided cosine similarity against full-embedding cosine similarity and average-pooled embedding similarity. This is the single highest-leverage improvement.
2. Report end-to-end metrics after re-ranking (Recall@k, MRR, Precision@k after applying PubMedBERT to retrieval outputs).
3. Correct the "two orders of magnitude" claim to actual improvement factors.
4. Define the "highly activated" threshold and clarify the IS definition in Equation 6.
5. Include a random baseline and stratify ground truth by origin (experimental vs. prediction-derived).

## Score and Decision

**Calibration bracket (Round 1):** Initial plausible range was 4.0–6.5, narrowed to 4.5–5.5 after anchor inspection.

**Anchor comparison (anchors retrieved across all rounds):**

| Anchor | Avg Score | Decision | Comparison |
|--------|-----------|----------|------------|
| MAPE-PPI (PPI prediction) | 5.67 | Accept | Similar PPI topic; the paper under review has a more novel problem formulation but comparable methodological gaps |
| Illuminating Protein Function | 5.25 | Reject | Similar benchmarking scope; the paper under review has a stronger method creative component |
| DeepSSInter (PPI contact) | 5.00 | Reject | Split reviews (3,3,8,6); the paper under review has broader evaluation but similar unablated claim issues |
| SMP (inter-chain contact) | 5.50 | Reject | Strong performance claims but questions about significance; comparable to this paper |
| PEEP (enzyme promiscuity) | 5.60 | Reject | Strong method but missing baselines; comparable evidential gaps |
| LLaPA (PPI with LLMs) | 6.00 | Reject | Higher avg score; the paper under review has a more novel problem formulation but greater evidential gaps |

**Final judgment:** The paper tackles a well-motivated problem with a creative method and large-scale evaluation. However, the three major weaknesses—overstated central claim, missing ablation of the core methodological component, and disconnected pipeline evaluation—leave the evidence incomplete for the paper's claimed contribution. The issues are fixable but, as presented, the paper does not fully support its own thesis.

**Score:** 5.0 — Borderline. The problem formulation, method creativity, and evaluation scale are genuine contributions, but the evidential support for the core claim is incomplete in ways that require at least moderate revision.

**Decision:** Reject

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>