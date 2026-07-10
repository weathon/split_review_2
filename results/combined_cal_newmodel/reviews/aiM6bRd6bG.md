## Summary

This paper introduces the problem of PPI candidate ranking — prioritizing novel interaction partners for experimental validation — rather than the standard binary PPI classification task. It proposes an interpretability-guided retrieval method that extracts active residue regions from predicted contact maps of known interaction pairs (using D-SCRIPT or Topsy-Turvy), computes cosine similarity between those activated embeddings and sliding windows of candidate protein embeddings, and then re-ranks the top candidates using 10 different biological signals (functional annotations, structural scores, LLM-based semantic similarity). The evaluation uses a prospective temporal split (STRING v11 → v12) where interactions newly appearing in v12 serve as ground truth. The core retrieval results show meaningful improvements — e.g., D-SCRIPT Recall@10 rises from 1.24% to 26.41%.

## Strengths

- **Well-motivated problem formulation.** The paper reframes PPI prediction as a ranking problem for experimental prioritization, directly addressing the bottleneck of costly validation. The task setup (Section 4, Equations 1–2) cleanly separates known interactors from novel candidates, giving the problem clear operational meaning.

- **Principled prospective evaluation.** Using successive STRING releases (v11 → v12) as a temporal train/test split is a genuinely stronger evaluation design than the typical static benchmark. It tests whether a method can anticipate interactions that receive experimental support only in a later release.

- **The embedding-activation retrieval idea is clever and well-motivated.** Rather than using D-SCRIPT/Topsy-Turvy's scalar interaction score, the method extracts residue-level contact maps, identifies the most active contiguous region for each known interaction pair, and computes cosine similarity between those activated embedding regions and sliding windows of candidate embeddings (Section 4.1, Equation 3). This is a principled way to exploit internal model representations for a ranking task the model was not trained for.

- **Large-scale, multi-signal re-ranking analysis.** The paper evaluates ten different re-ranking signals (Table 2), from lightweight heuristics (token overlap, TF-IDF) to structure-based scores (pDockQ) to LLM-based methods (BioBERT, PubMedBERT). The pairwise rank-shift comparison provides a useful characterization of which signals are complementary.

- **Quantitatively meaningful improvements.** The core retrieval results in Table 1 are solid — for D-SCRIPT, Recall@10 goes from 1.24% to 26.41% and MRR from 0.034 to 0.1685. These are practically meaningful for the proposed task of candidate screening.

## Weaknesses

### Major

- **The "two orders of magnitude" claim is contradicted by the paper's own results.** The introduction (line 25) and conclusion (line 279) claim improvements of "two orders of magnitude" (~100×), but the results section (line 233) states MRR increases by "4-6 times." The largest ratio in Table 1 is approximately 25× (D-SCRIPT Recall@5: 0.0071→0.1832). Claiming "two orders of magnitude" when the data shows at most ~25× overstates the result by a factor of 4. The core finding (that improvements are practically meaningful) remains valid, but this hyperbolic claim should be corrected.

- **The LLM-based re-ranking improvements are of uncertain validity due to potential data leakage.** The cross-encoder (PubMedBERT backbone) is fine-tuned on STRING v11 and evaluated on v12 novel interactions. However, PubMedBERT was pretrained on the full PubMed corpus, which includes literature contemporaneous with v12 interactions. The paper acknowledges this (lines 262–264: "it is uncertain if their gains reflect not only semantic generalization but also latent knowledge of interactions from the training data") but does not attempt to control for it experimentally — e.g., by restricting to interactions whose discovery postdates the model's pretraining data. This does not affect the core interpretability-guided retrieval results (which do not use LLMs), but it undermines the re-ranking conclusions for the most performant signals (PubMedBERT, BioBERT, BioMedRoBERTa).

### Minor

- **The baseline comparison is structurally uneven.** The baselines (D-SCRIPT, Topsy-Turvy, xCAPT5) use raw pairwise interaction probabilities, while the proposed method conditions on the full set of known interactors KP(p) — strictly more information. The paper's framing ("outperforms existing methods") conflates two questions: (a) is conditioning on known partners helpful? (b) is the contact-map-guided residue selection better than simpler ways of using known partners? Adding a baseline that also uses known partners but without contact-map gating (e.g., average embedding of known partners + nearest-neighbor search) would isolate the specific contribution of the residue-level activation analysis.

- **The D-SCRIPT interaction score definition is inconsistent.** Section 3 describes the IS as produced by convolutional and pooling operations followed by logistic activation. However, Section 4.2 Equation 6 defines the IS as simply max(C(p,p_c)) ("sharpened through a logistic activation"). These describe different operations — in the actual D-SCRIPT model, the IS is not just the maximum of the contact map. This discrepancy should be clarified.

- **The pairwise rank-shift analysis in Table 2 reports only the fraction of interactions improved vs. worsened, not the magnitude of rank shifts.** A method that moves a protein from rank 7 to rank 8 and another from rank 7 to rank 1 both count as "worsened" and "improved," but the practical significance differs. Reporting median or mean rank change would strengthen the analysis.

- **No analysis by protein properties.** The paper acknowledges (lines 284–288) that the method may not work for underexplored proteins with few known partners, but does not empirically evaluate this. Grouping proteins by number of known partners and reporting Recall@k per group would characterize this limitation.

### Trivial

None.

## Nice-to-Haves

- Adding confidence intervals or bootstrap estimates for Table 1 metrics across proteins would help assess reliability, though this is not standard practice for evaluations at this scale.
- The re-ranking analysis is limited to top-10 candidates (2,280 protein-candidate pairs) due to SpeedPPI's cost. The conclusions about which re-ranking signals are most effective may not generalize beyond this selected subset.
- Testing whether the core assumption (novel interactions follow similar mechanisms to known ones) holds by comparing interaction interfaces of known vs. novel partners for the same protein would strengthen the paper's conceptual foundation.

## Removed Points

- Criticism about "structure-based predictions in v12 data" — REMOVED because the paper explicitly states they filter to interactions with "experimental support > 0" (line 194), which addresses the concern. The mention of structure-based predictions is a citation of the STRING publication's description of its data sources, not the paper's own data.
- Criticism about runtime figures missing — REMOVED per instructions (parser strips appendix/figures; they exist in the original submission).
- Criticism about the paper never testing whether novel interactions follow similar mechanisms — while true that no direct interface comparison is done, the empirical results (Table 1) demonstrate the assumption's practical utility, and the paper acknowledges this as a limitation. Demoted to Nice-to-have.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the overstated claim.** Replace "two orders of magnitude" in the introduction and conclusion with an accurate characterization (e.g., "4-25× improvement" or the specific metric ratios).
2. **Add a simple known-partner baseline.** Compare against ranking by average cosine similarity of full (non-gated) embeddings between known partners and candidates, without contact-map-guided residue selection. This would isolate the specific contribution of the activation gating.
3. **Control for LLM data leakage.** For the PubMedBERT/BioBERT re-ranking, test whether improvements persist when restricting to text published before v12 interactions were reported, or compare against a baseline LLM trained only on pre-v11 data.
4. **Report magnitude of rank shifts in Table 2**, not just the fraction improved.
5. **Stratify results by number of known partners** to characterize the method's failure cases for sparsely annotated proteins.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| eh1fL0zw8o.md (LLaPA) | 6.00 | R1/R2 | Yes | Similar PPI prediction domain; LLaPA had more damaging weaknesses (unclear LLM benefit, fundamental data leakage). My paper's core method does not depend on the questionable LLM analysis, making it stronger. |
| itGkF993gz.md (MAPE-PPI) | 5.67 | R1/R2 | Yes | Similar domain; MAPE-PPI has unclear efficiency claims and limited related work discussion. My paper has stronger task framing and evaluation design. |
| jsQPjIaNNh.md (ProtIR) | 5.25 | R1 | Yes | Protein function prediction with retrieval; had missing baseline criticisms. My paper has more complete evaluation. |
| xcMmebCT7s.md (PPIformer) | 5.80 | R1 | Yes | PPI mutation effect prediction; strong contributions but data leakage concerns. Comparable weakness profile. |
| IxmWIkcKs5.md (Light-DDG) | 6.75 | R2 | Yes | Higher-scoring anchor; had severe data leakage concerns (fav=-2.41) and overclaimed contributions (fav=-2.42). My paper's weaknesses are less severe in comparison. |
| S8gbnkCgxZ.md (Bioactivity Redefinition) | 7.00 | R2 | Yes | Higher-scoring; had only minor weaknesses, more polished presentation, clearer methodological contribution. My paper doesn't reach this level. |

**Round-1 bracket:** 5.5–7.5  
**Round-2 narrowing:** After comparing my draft's item favorabilities against the anchors, my paper sits above the 5.25–5.80 anchors (which have more damaging low-favorability items such as missing baselines with ~ -2.5 and fundamental methodological concerns) but below the 6.75–7.00 anchors (which have cleaner contributions and only minor weaknesses). My paper's two major weaknesses (overclaim at favorability 1.19, LLM leakage at 1.53) are real but addressable, while its core contributions (task framing, prospective evaluation design, activation-guided retrieval) are supported by strong favorability evidence (10.59–12.42). This places the paper in the mid-to-high end of the 5.5–7.5 bracket.

**Final score:** 6.0. The paper has genuine contributions — a practically motivated task reframing, a clever method leveraging model internals for ranking, and a strong temporal evaluation design. However, it is held back by the unsupported "two orders of magnitude" claim and the unresolved LLM data leakage concern in the re-ranking analysis. With these issues corrected, the paper would be significantly stronger.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>