Now let me write my final review.

## Summary

RetrievalFormer proposes a dual-encoder transformer architecture for sequential recommendation that replaces the standard ID-softmax classification head with a feature-based item tower and a transformer-based user tower. This reformulation enables ANN-based serving (sub-linear inference cost instead of O(N)) and zero-shot cold-start recommendation for items unseen during training. The architecture uses attention fusion for heterogeneous features, shared embedding tables, and InfoNCE + mixed negative sampling training. The paper reports competitive accuracy (86–91% of strong baselines) with dramatic latency improvements (288× speedup at 10M items).

## Strengths

1. **Clean, well-motivated architectural design (Sections 3.1–3.5).** The dual-encoder formulation with attention fusion, shared embedding tables, and InfoNCE training is internally coherent, with each component having a clear rationale. The paper correctly identifies two genuine limitations of ID-softmax transformers (O(Nd) inference cost and inability to score unseen items) and designs an architecture that directly addresses both.

2. **Strong latency evidence (Section 4.5, Figure 2).** The latency measurements are the paper's strongest empirical contribution. Documented measurements show 0.69ms (IVF-PQ + encode) vs 29.5ms (exhaustive) at 1M items, scaling to ~2.5ms vs ~292ms at 10M items. The 288× speedup claim at 10M items is substantiated with concrete ANN parameters (FAISS IVF-PQ, n_list=4096, n_probe=32, 64-bit PQ codes).

3. **Thoughtful cold-start diagnostic (Section 4.4, Table 2).** The LOOC protocol is a clean method for measuring cold-start capability. The honest reporting of a 25–35% drop from LOO to LOOC is informative and avoids cherry-picking. The email campaign dataset result (AUC 0.6854→0.7770) provides partial external validation.

4. **Comprehensive baseline comparison.** The paper compares against 12 baselines, including multiple attribute-aware models (AttrFormer, SASRecF, MT4SR, DIF-SR) in addition to ID-only models — going beyond what many comparable papers do.

## Weaknesses

### Major

1. **Inconsistent framing of the headline accuracy figure.** The paper's central quantitative claim — "86–91% of the Recall@20 of strong transformer-based sequential baselines" (Abstract, Conclusion) — mixes comparisons against both ID-only and attribute-aware models in a way that minimizes the perceived accuracy gap. On MovieLens-1M, the paper compares RetrievalFormer to SASRec (96.8%) rather than AttrFormer (81.6%), and dismisses AttrFormer's superior result as a "notable outlier" (lines 177–178). While AttrFormer is genuinely the strongest on ML-1M, calling it an "outlier" is a rhetorical choice, not an analytical one — especially since on Amazon Toys, AttrFormer is only ~1% ahead of DIF-SR. When measured against the best attribute-aware model on each dataset, the ratios are: 91.2% (Beauty vs AttrFormer), 86.1% (Toys vs AttrFormer), and 81.6% (ML-1M vs AttrFormer). The paper should present this trade-off transparently, not select a reference group that makes the gap look smallest.

2. **Missing cold-start baselines on public benchmarks.** Table 2 shows RetrievalFormer's LOOC performance (Recall@20: 0.0804 on Beauty, 0.0818 on Toys, 0.2267 on ML-1M) with no baseline comparison on any public dataset. The paper mentions a "Content-based KNN" baseline (Section 4.1) but only provides results on the proprietary email campaign dataset. Without baselines on public data, these numbers are uninterpretable — the reader has no way to tell whether 0.0804 Recall@20 on cold Beauty items is good, average, or poor. The paper's framing as a "capability diagnostic" (line 250) is appropriate caution, but the cold-start contribution claim — "zero-shot cold-start capability through feature-based encoding" — requires comparison against reasonable alternatives (e.g., category-KNN, text-similarity KNN, DropoutNet) on standard benchmarks to be properly supported.

3. **Imprecise explanation of the accuracy gap (lines 179–181).** The paper states: "the performance gap stems from replacing the exact softmax scoring over all items with approximate nearest neighbor search in the learned embedding space." This conflates two separate effects. The Table 1 results use exhaustive dot-product scoring (not ANN), so the gap comes from the dual-encoder formulation (dot-product in shared space) vs the softmax formulation, not from ANN approximation. The actual sources of the gap likely include: limited expressiveness of dot-product vs learned softmax weights, contrastive loss with in-batch negatives vs full softmax over the catalog, and information loss in the feature-based item tower vs learned per-item ID embeddings. The paper would benefit from being precise about which architectural choice causes which part of the trade-off.

### Minor

1. **Asymmetric ID-only comparison on Beauty.** The paper highlights that RetrievalFormer "outperforms SASRec (0.1107)" on Beauty (line 173). While factually true, this comparison is asymmetrical: RetrievalFormer uses rich item attributes while SASRec uses only IDs. The more informative comparisons are to attribute-aware models, where RetrievalFormer underperforms (91.2% of AttrFormer).

2. **Scattered ablation results.** The architectural ablations (Section 4.3) start from different baselines: attention fusion from 0.0960, uniformity loss from 0.1022 — making the cumulative contribution of all components invisible. The shared embeddings ablation reports only a "~3% improvement on MovieLens-1M" without a precise number. A single cumulative ablation table from a common baseline would be much more informative.

3. **No end-to-end accuracy impact of ANN search.** Figure 2 reports ANN latency with "≥0.95 recall of exact search," but does not translate this to actual recommendation Recall@K. If 95% recall of exact ANN means recommendation Recall@20 drops from 0.337 to, say, 0.33 vs 0.28 makes a material difference to the paper's claims. Reporting end-to-end accuracy at various speed-accuracy trade-off settings (different n_probe values) would strengthen the evaluation.

4. **Mixed negative sampling details not specified.** Section 3.5 mentions augmenting batches with uniformly sampled items but does not specify the ratio of in-batch negatives to uniformly sampled negatives. This makes the training setup partially unreproducible from the main text.

### Trivial

None.

## Nice-to-Haves

- Add a controlled experiment isolating the dual-encoder vs softmax gap while holding attributes constant (e.g., train SASRecF with the same features, or train a version of RetrievalFormer with learned item ID embeddings instead of feature-based encoding).
- Add simple cold-start baselines on public benchmarks (category-KNN, text-similarity KNN, or DropoutNet).
- Report end-to-end recommendation accuracy with ANN search at various n_probe settings.
- Provide feature statistics per dataset (vocabulary sizes, feature coverage) for reproducibility.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The 86-91% figure excludes attribute-aware models"** — Removed as factually incorrect for Beauty and Toys, where the paper explicitly compares to AttrFormer to compute these ratios (91.2% on Beauty, 86.1% on Toys). The issue is limited to ML-1M where a different reference is chosen.
- **"Missing related work on efficient transformer inference (hierarchical softmax, early exit, etc.)"** — Removed per rules; the paper covers two-stage retrieval, sampled/approximate softmax, and model compression (end of Section 2), which is adequate for its scope.
- **"Reproducibility concerns about missing hyperparameters"** — Removed per rules; hyperparameters are in Appendix J (stripped from provided text but present in original submission).
- **"Formatting nitpicks and typos"** — Removed as parser artifacts.
- **"Reference availability concerns"** — Removed per hard rules; all cited entities exist.

## Novel Insights

The harsh critic usefully identifies that the paper's analytical framing selectively minimizes the accuracy gap: by defaulting to SASRec comparison on ML-1M and calling AttrFormer "a notable outlier," the paper presents the accuracy-efficiency trade-off in a systematically favorable light. This goes beyond a mere missing baseline — it is a rhetorical choice that affects how readers interpret the paper's central claim. Additionally, the observation that the paper conflates the dual-encoder formulation with ANN search (lines 179–181) in explaining the accuracy gap is a meaningful analytical imprecision that the authors should correct.

## Suggestions

1. **Reframe the accuracy claim transparently.** Report "81.6–91.2% of the best attribute-aware model (AttrFormer)" rather than the selectively mixed "86–91% of strong baselines."
2. **Add cold-start baselines on public benchmarks.** Even a simple content-based KNN or category-match baseline would make the LOOC results interpretable.
3. **Add end-to-end ANN accuracy impact.** Show how different n_probe values affect recommendation Recall@K, not just ANN recall.
4. **Produce a single cumulative ablation table** from a common minimal baseline to the full RetrievalFormer.
5. **Correct the imprecise statement in lines 179–181** about the source of the accuracy gap.

## Score and Decision

Let me calibrate using retrieved anchors.

**Round 1 bracket:** I identified this paper as sitting between 3.0 (QCR: rejected, weak results vs SOTA) and 6.5 (NCL-SR: accepted, strong evaluation). The paper under review has stronger contributions than QCR (which scored 1,3,5,3) — its architecture is clean, its latency evidence is genuinely strong, and it compares against 12 baselines. But it has weaker evaluation than NCL-SR (scored 6,6,6,8) — the accuracy framing is selectively favorable and cold-start baselines are missing on public data. Most similar in quality to "Relevance-based embeddings for efficient relevance retrieval" (5.75, scored 5,6,6,6) and "Making Transformer Decoders Better Differentiable Indexers" (6.0, scored 6,6,6,6,6), both of which had real contributions but evaluation gaps.

**Final score: 5.5.** The paper has genuine contributions (architecture design, latency benchmarks, cold-start protocol) that outweigh its weaknesses. However, the accuracy framing issues and missing cold-start baselines are substantive enough that the paper should not be ranked with papers scoring 6.5+. With revisions addressing the transparency of the accuracy comparison and adding cold-start baselines on public data, this would be a clear accept.

**Anchor papers consulted:**
- QCR (3.00, Round 1): Much weaker results vs SOTA; lower novelty. Our paper is stronger.
- Relevance-based embeddings (5.75, Round 1): Similar dual-encoder + retrieval topic; comparable score. Our paper has cleaner architecture and stronger latency evidence but similar evaluation gaps.
- NCL-SR (6.50, Round 1): Stronger evaluation and novelty; our paper's evaluation weaknesses prevent reaching this level.
- Making Transformers Better Differentiable Indexers (6.00, Round 1): Similar evaluation weaknesses (missing baselines, insufficient analysis) but accepted. Our paper has comparable contribution level.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>