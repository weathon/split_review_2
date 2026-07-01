## Summary

RetrievalFormer proposes a dual-encoder transformer architecture for sequential recommendation that replaces the standard ID-softmax output layer with an ANN-compatible embedding space. The item tower encodes items from heterogeneous features (categories, text, tags, brands) via an attention-based fusion mechanism, while the user tower encodes interaction sequences through a transformer. The two towers are jointly trained with InfoNCE + mixed negative sampling. The paper demonstrates that this design enables sub-linear serving latency via ANN (up to 288× speedup at 10M items) and zero-shot cold-start recommendation for items unseen during training, while maintaining what the authors characterize as competitive accuracy.

## Strengths

1. **Well-motivated problem with concrete deployment relevance.** The paper clearly identifies two real bottlenecks of ID-softmax transformers — the O(Nd) inference cost that dominates at large catalog sizes, and the inability to score unseen items. These are grounded in specific evidence (the Kersbergen et al. latency report, the 50ms p90 industry target).

2. **Well-designed cold-start evaluation protocol (LOOC).** The Leave-One-Out Cold protocol (Section 4.4) cleanly separates cold-start from standard evaluation by ensuring test items have zero interactions in training. This is a genuine methodological contribution — most prior work on cold-start holds out user-item pairs rather than entire items, introducing leakage. The protocol is transparently described.

3. **Latency scaling data is informative and well-presented.** Figure 2 and the associated table provide clear quantitative evidence that the dual-encoder + ANN approach changes inference scaling behavior. At 10M items, IVF-PQ achieves 1.02ms vs. 292ms for exhaustive scoring — a practically meaningful gap.

4. **Attention fusion with shared embeddings shows clear ablation improvement.** The ablation (Section 4.3) showing +10.1% over mean pooling provides evidence that the attention mechanism is doing useful work. The shared embedding design across towers is a sensible architectural choice.

## Weaknesses

### Fatal
None.

### Major

1. **Uncontrolled accuracy comparison undermines the central "competitive accuracy" claim.** RetrievalFormer uses rich item features (text descriptions, categories, tags, brands) as input to its item tower. The key baselines — SASRec, BERT4Rec, GRU4Rec, LightSANs, TiSASRec, FEARc, DIF-SR — use only item IDs. These are listed under "N.A. for Attribute" in Table 1. Despite this informational advantage, RetrievalFormer ranks in the lower half of Table 1 across all three datasets:
   - **Amazon Beauty Recall@20**: RetrievalFormer (0.1208) is beaten by 5 methods (FEARc, TiSASRec, DIF-SR, AttrFormer) — ranks 8th out of 13.
   - **Amazon Toys Recall@20**: RetrievalFormer (0.1169) is beaten by 7 methods — ranks 8th out of 13.
   - **MovieLens-1M Recall@20**: RetrievalFormer (0.337) is below the established cluster of 0.348-0.359 — ranks 8th out of 13.

   The paper's "86-91%" framing selectively compares against AttrFormer (the single best result), which the paper itself calls a "notable outlier" achieving ~15% higher recall than the next best method. A proper controlled comparison would include a version of SASRec (or another baseline) augmented with the same item features. Without this, it is impossible to attribute RetrievalFormer's accuracy to the dual-encoder architecture rather than to the additional feature signal. This is the paper's most significant weakness.

### Minor

2. **Cold-start evaluation on public benchmarks lacks baselines.** Table 2 shows only RetrievalFormer's own performance under LOOC. The paper mentions a "Content-based KNN" baseline in Section 4.1 (experimental setup) and evaluates against one on the proprietary email dataset (Appendix G), but no baseline comparison appears on the public LOOC benchmarks. The paper transparently acknowledges that "LOOC is used here as a capability diagnostic rather than as a head-to-head accuracy comparison," but even a simple KNN on item features would provide a meaningful anchor for interpreting the LOOC numbers on public datasets.

3. **No variance reporting for RetrievalFormer results.** The caption of Table 1 reports that baselines are "averaged over five runs with std. < 0.001 not reported." For RetrievalFormer, it only says "results are from our experiments" with no mention of number of runs or variance. Given that some metric differences are tiny (e.g., Amazon Beauty NDCG@20: RetrievalFormer 0.0541 vs. SASRec 0.0540 — a 0.0001 difference), single-run results cannot establish reliable ranking against baselines.

4. **Latency comparison in Figure 2 conflates architecture change and ANN.** The 288× speedup at 10M items compares SASRec's full softmax latency (from the ETUDE benchmark) against RetrievalFormer's IVF-PQ retrieval time. This mixes two distinct efficiency sources: (a) replacing the softmax output layer with dot-product similarity, and (b) replacing exhaustive scoring with ANN search. The paper's text describes the comparison as "exhaustive dot-product scoring over all items and ANN-based retrieval using an IVF-PQ index for the same dual-encoder scoring function" (Section 4.5), but the table actually shows SASRec softmax times, not dual-encoder exhaustive dot-product times. Decomposing the speedup into architecture-change and ANN components would make the contribution clearer and more honest.

5. **Clarify whether item IDs are used as features during regular training.** The methodology describes a purely feature-based item tower (Section 3.3), but the paper does not explicitly state whether item IDs are included among the features during standard LOO evaluation. If IDs are used during standard training but withheld during LOOC, part of the observed 25-35% performance drop could reflect feature absence rather than cold-start difficulty per se. This should be explicitly addressed.

### Trivial

6. The paper characterizes AttrFormer's strong results as a "notable outlier" (Section 4.2). AttrFormer is a legitimate near-contemporary method that also uses item attributes; the paper would benefit from engaging with its architectural differences rather than treating its performance as anomalous.

## Nice-to-Haves

- Decompose the latency speedup into: (a) softmax → exhaustive dual-encoder dot-product, and (b) exhaustive dual-encoder → ANN, to cleanly separate the two sources of efficiency gain.
- Add at least one simple feature-based baseline (e.g., KNN on item features, feature-only MLP) to the public LOOC evaluation in Table 2.
- Discuss how the use of one in-batch negative per positive example interacts with the MNS strategy at the reported catalog sizes.

## Removed Points

These points from the input review were flagged for removal (treated with caution):
- *"Code or reproducibility commitment not mentioned"* — removed per the hard rule that questioning existence/release status of cited artifacts is not valid. The paper cites Liu et al. (2025) and adopts their protocol.
- *"Novelty of the architecture is modest"* — removed as a general opinion rather than a specific verifiable weakness. The paper's combination of well-known components with systematic evaluation is a valid engineering contribution.
- *"The comparison to AttrFormer is handled oddly"* — retained only the specific criticism about calling it an "outlier" (Trivial #6); the broader "oddly handled" framing was too subjective to keep as a standalone weakness.
- *"No discussion of how in-batch negatives interact with MNS"* — moved to Nice-to-Haves; it is a reasonable question but not a demonstrated flaw.

## Novel Insights

None beyond the paper's own contributions. The review analysis surfaces a significant methodological concern that the paper itself does not adequately address: the accuracy comparison is confounded by asymmetric feature access, which the authors could address with a controlled baseline.

## Suggestions

1. **Add a controlled comparison where baselines have the same features.** The most impactful addition would be SASRec augmented with the same item features as RetrievalFormer. This would isolate the contribution of the dual-encoder design from the contribution of the features themselves.
2. **Report multi-run statistics for RetrievalFormer.** At minimum, state the number of runs and provide variance for key metrics, especially where differences to baselines are small.
3. **Include a feature-based baseline in the public LOOC evaluation.** Even a simple KNN or feature-MLP would provide a meaningful anchor.
4. **Decompose the latency analysis** to separate architecture-driven gains from ANN-driven gains.
5. **Explicitly state** whether item IDs are used as features during standard training.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>