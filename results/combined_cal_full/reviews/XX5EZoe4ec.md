Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes RetrievalFormer, a dual-encoder architecture for sequential recommendation that replaces the standard softmax output layer (with its O(N) inference cost and inability to score unseen items) with a transformer-based user tower and a feature-based item tower trained via InfoNCE. At serving time, items are retrieved via approximate nearest neighbor search over pre-computed item embeddings. The paper introduces an AttentionFusion mechanism for heterogeneous feature aggregation, shared embedding tables across towers, and a Leave-One-Out Cold (LOOC) evaluation protocol. Experiments on Amazon Beauty, Amazon Toys & Games, and MovieLens-1M report competitive accuracy (advertised as 86–91% of strong transformer baselines' Recall@20) and up to 288× latency reduction at 10M-item scale.

## Strengths

- **LOOC evaluation protocol (Section 4.4.1) is a genuine methodological contribution.** Standard leave-one-out tests hold out interactions; LOOC holds out entire items so no item ID seen during training appears in the test set. This is a more realistic test of cold-start generalization, and the paper is transparent that ID-softmax models cannot participate (line 240). [weight: +3.68]

- **The latency benchmark (Figure 2) clearly demonstrates sub-linear scaling** of IVF-PQ versus linear scaling of exhaustive scoring across catalog sizes from 10K to 10M items. The direction of the result is correct and the 1.02ms at 10M is a practically meaningful number. [weight: +4.25]

- **The ablation study (Section 4.3.1) isolates the three most important design choices** — attention fusion vs mean pooling (+10.1% on Toys), shared embeddings (~3% on MovieLens), and uniformity through InfoNCE (+4.1%) — and provides clean evidence for each. [weight: +4.98]

- **The problem framing is well-motivated.** Section 1 correctly identifies the double liability of the softmax output layer (linear inference cost + inability to score unseen items) with concrete operational references. [weight: +2.38]

## Weaknesses

### Major

- **Accuracy comparison relies on published numbers from another paper, not re-implemented baselines.** Table 1 states "Baseline results are from Liu et al. (2025)… RetrievalFormer results are from our experiments." All 12 baselines across three datasets are taken from a single external codebase with no controlled replication in the authors' own environment (lines 163–165). Preprocessing details, feature handling, and evaluation pipeline variations can shift results by 1–3%, which matters because the gap to SASRec on MovieLens-1M is only 3.3% (0.337 vs 0.3483). Moreover, the paper reports no variance for RetrievalFormer's own results (only baselines' std. is noted), making it impossible to assess statistical significance. No re-implementation is provided even for the closest baselines (SASRec, BERT4Rec). [weight: -5.19]

- **The "86–91%" accuracy claim is materially imprecise.** The abstract and conclusion state that RetrievalFormer "reaches 86–91% of the Recall@20 of strong transformer-based sequential baselines." This range is constructed by comparing against AttrFormer on Amazon Beauty (0.1208/0.1324 = 91.2%) and Amazon Toys (0.1169/0.1357 = 86.1%). On MovieLens-1M, comparing against AttrFormer gives 0.337/0.4128 = 81.6%, which falls outside the advertised range. Rather than reporting this, the paper switches the reference to SASRec (96.8%) and dismisses AttrFormer's result as "a notable outlier" (line 177) without explaining why it is invalid as a comparison point. The full range across all three datasets against the strongest baseline is 81.6–91.2%. [weight: -1.72]

- **Cold-start evaluation on public datasets lacks baselines.** Table 2 reports only RetrievalFormer's own LOOC numbers. While ID-softmax models cannot participate, the paper does not compare against any other feature-based method that can score unseen items (e.g., content-based MF, DropoutNet, simple feature averaging). The only direct cold-start comparison is on a proprietary dataset against an unspecified "strong content-based baseline" (line 250) that cannot be independently assessed. The paper scopes LOOC as a "capability diagnostic" (line 250), but this limits what can be concluded about cold-start superiority on public data. [weight: -9.00]

### Minor

- **The 288× speedup confounds multiple factors.** The ratio (292ms ÷ 1.02ms) compares SASRec with full softmax on CPU (ETUDE benchmark) against RetrievalFormer with IVF-PQ on GPU — differing simultaneously in architecture, search strategy, hardware, and codebase. The text at line 273 says the figure "compares exhaustive dot-product scoring… for the same dual-encoder scoring function" but the exhaustive numbers in the table are SASRec from ETUDE, not RetrievalFormer with exhaustive search. The paper does not provide a decomposition isolating the ANN contribution (e.g., RetrievalFormer exhaustive vs RetrievalFormer ANN on identical hardware). The qualitative claim (ANN is faster) is directionally correct, but the specific factor 288× is a confounded number. [weight: -3.76]

- **Inconsistent latency citation.** Line 271 states "the ETUDE benchmark demonstrates that SASRec exceeds the industry-standard 50ms p90 latency threshold at just 10K items on CPU" citing Kersbergen et al. (2024). However, Figure 2's own table shows SASRec CPU at 10K items as 0.76ms — well under 50ms. Additionally, the exhaustive timing numbers in the text (3.4ms at 100K, 29.5ms at 1M; line 203) do not match the SASRec numbers in Figure 2 (7.6ms at 100K, 76ms at 1M), suggesting different measurement conditions are being conflated. [weight: -1.61]

## Nice-to-Haves

- Re-implement the top 2–3 baselines (SASRec, BERT4Rec, AttrFormer) in the same codebase to eliminate the cross-codebase comparison concern. If results replicate closely, the paper's claims become substantially stronger.
- Decompose the speedup into architecture contribution (exhaustive dual-encoder vs exhaustive softmax on same hardware) and search contribution (ANN vs exhaustive for the same dual-encoder) on identical hardware.
- Add a simple public-dataset cold-start baseline (e.g., mean feature embedding or content-based KNN) to provide comparative context for the LOOC results.
- Report mean and standard deviation over multiple seeds for RetrievalFormer.

## Removed Points

These points from the input review are removed with justifications:

1. **"Ablation starting point not defined"** — The paper reports component-by-component improvements (mean pooling 0.0960 → attention fusion 0.1057, etc.) which is standard ablation practice. The full model score (0.1169) is available in Table 1 for context.

2. **"Related work missing dual-encoder retrieval recommenders"** — Section 2 already discusses two-tower neural networks (Yi et al., 2019; Huang et al., 2020a; Eksombatchai et al., 2018; Grbovic & Cheng, 2018) and correctly distinguishes the paper's contribution (combining a transformer user tower with feature-based item tower).

3. **"Unclear whether Table 1 uses exhaustive or ANN scoring"** — The paper's architecture and RQ4 framing imply exhaustive scoring for accuracy evaluation (since ANN would introduce ≤95% recall degradation), but this is a presentation ambiguity, not an evidential flaw. The model-assigned weight (+2.47) indicates this is not considered a genuine weakness.

4. **Generic speculation about preprocessing differences** — While the cross-codebase concern is valid, the reviewer's framing about "systematic preprocessing differences" is a generic risk that applies to any reproduction, not a specific identified problem in this paper. The core concern (relying on another paper's numbers) is retained.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-implement SASRec and AttrFormer in the same codebase — this single change would address the most serious weakness.
2. Report RetrievalFormer's variance (mean ± std over ≥3 seeds) and state explicitly whether Table 1 uses exhaustive or ANN scoring.
3. Add a controlled ablation for the speedup (RetrievalFormer exhaustive vs RetrievalFormer ANN on the same GPU).
4. Add a simple feature-based cold-start baseline (e.g., mean item-feature embedding) on public data to complement the proprietary dataset comparison.

## Score and Decision

**Bracket (Round 1):** After comparing my draft's weighted items against calibration anchors, the plausible range is 3.5–5.5. The EHI paper (avg 6.00) had stronger positive weights (+5.19 to +5.90) and less severe baseline concerns; ConvFormer (avg 4.67) had similar baseline weaknesses (-11.18 on missing baselines) with weaker strengths. RetrievalFormer sits between these: its strengths (ablation +4.98, latency benchmark +4.25, LOOC protocol +3.68) are comparable to ConvFormer's, but its cross-codebase comparison weakness (-5.19) and cold-start baseline gap (-9.00) are significant.

**Final placement:** The paper addresses a well-motivated problem with a sensible architecture and a novel evaluation protocol (LOOC). However, the experimental evidence for the core accuracy claims is weakened by the reliance on another paper's numbers (no controlled replication), imprecise headline claims (86–91% excludes the strongest baseline on one dataset), and absent cold-start baselines on public data. These are evidential rather than structural weaknesses — they do not invalidate the approach — but they prevent the advertised quantitative claims from being taken at face value. The paper would need substantial experimental strengthening (controlled baseline re-implementations, variance reporting, public cold-start baselines) to be acceptable at a top venue.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>