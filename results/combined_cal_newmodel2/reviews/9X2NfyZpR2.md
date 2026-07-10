## Summary

This paper introduces TbLTA, the first weakly-supervised approach for dense Long-Term Action Anticipation (LTA) that uses only video transcripts (ordered action lists without timing) during training, eliminating the need for costly frame-level annotations. The model generates frame-level pseudo-labels via temporal alignment (ATBA), enriches video features through cross-modal attention with transcript embeddings, and supervises both segmentation and anticipation using a three-way loss (alignment + CTC + CRF+duration). Experiments on Breakfast, 50Salads, and EGTEA show that transcript-only supervision can be competitive with fully-supervised methods on Breakfast (+0.58 avg MoC over ActFusion), though results trail on the other two datasets.

## Strengths

**1. Genuinely novel problem framing with a clear motivation.** Prior LTA work uniformly requires dense frame-level annotations. The paper correctly identifies that transcripts (ordered action lists without timing) are far cheaper to collect and may carry enough procedural information for LTA. This carves out a new weakly-supervised sub-problem and demonstrates feasibility — a legitimate contribution. [favorability: 11.04]

**2. Competitive deterministic results on Breakfast.** TbLTA achieves an average MoC of 29.03 across all observation/prediction horizons, slightly exceeding ActFusion's 28.45 (Table 1). At Obs 30%, the gap widens — TbLTA scores 40.28 at 10% horizon vs. ActFusion's 35.79. That a weakly-supervised method can match or exceed supervised methods on this benchmark is a nontrivial finding. [favorability: 14.78]

**3. Coherent architectural design with individually motivated components.** Each component (ATBA for pseudo-labels, CTC for transcript-level consistency, cross-modal attention for feature grounding, CRF for temporal coherence) addresses a specific challenge arising from the absence of frame annotations. The three-way loss decomposition (alignment, segmentation, anticipation) is clean and principled. [favorability: 12.93]

## Weaknesses

### Major

**Ablation study uses the stochastic Top-1 (oracle) protocol while the main comparisons use the deterministic protocol.** Section 4.3 states: "All ablations are conducted on both Breakfast and 50Salads, and we report results using the Top-1 MoC metric." However, the headline results in Table 1 report deterministic MoC (single-output setting). Top-1 stochastic MoC selects the best of multiple sampled futures (an oracle choice), so a component's measured contribution under this setting may not transfer to the deterministic single-output setting where the paper's core claims are made. For example, removing the CRF might degrade the *distribution* of sampled futures while the oracle selector still finds one good trajectory, masking the CRF's true importance for deterministic evaluation. The paper's justification — that Top-1 "provides a stable reference point" — does not address this evidential gap. This is the paper's most significant methodological weakness and should be addressed (e.g., by running ablations on the deterministic protocol and comparing). [favorability: 2.90]

### Minor

**Abstract overstates the results relative to the full evidence.** The abstract claims "transcript-based supervision offers a very robust and less costly alternative to its fully supervised counterpart." However, the method is competitive (+0.58 avg MoC) on Breakfast, but substantially behind on 50Salads (-7.47 vs ActFusion) and EGTEA (-11.43 mAP All vs Anticipatr). The Conclusion uses the more measured phrasing "competitive with, and in certain settings even superior to." The abstract should be revised to match the actual scope of the evidence. [favorability: 2.26]

**A key methodological detail about the ATBA transcript split is underspecified.** Section 3.1 states that ATBA "partition[s] the full transcript Y into observed and future sub-transcripts, Y_obs and Y_future," and Section 3.2.1 mentions "dynamic programming over candidate boundaries." But the mechanism for determining which transcript actions belong to the observed vs. future portion is not explained. Since transcripts have no timing and k^* (the boundary index) is unknown (Problem Definition), it is central to the method to clarify how this split is determined — e.g., whether the model infers a boundary index per video, uses DP over observed feature length, or learns a boundary predictor. [favorability: 4.89]

**EGTEA evaluation is thin.** Table 2 compares against only two baselines — Timeception (2019) and Anticipatr (2022) — without explaining why more recent methods are absent. The evaluation also uses verb-only mAP (reducing 106 verb-noun classes to 19 verbs), a different protocol from the MoC used on Breakfast/50Salads. While the paper is transparent about these choices, the limited baseline coverage makes the EGTEA comparison less informative than it could be. [favorability: 1.41]

### Trivial

**Key hyperparameter values not reported in the main text.** The loss weighting coefficients γ₁, γ₂, γ₃ appear in the objective but their numerical values are absent from the main text. The paper states "More details in the supplementary material" but key training hyperparameters (learning rate, batch size, optimizer) are not given. [favorability: 3.02]

## Nice-to-Haves

- Analyze how pseudo-label quality evolves during training and how it correlates with downstream anticipation accuracy — this would directly address the paper's central question about whether transcript-level information can substitute for frame-level annotations.
- Provide variance or standard deviations across standard splits to help assess whether small numerical differences (e.g., +0.58 on Breakfast) are meaningful.
- Report computational cost (training time, model size) to help readers assess the practical trade-off.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Table duplication / formatting artifacts** in the extracted PDF (Table 4 appears twice) — parser artifact, not an author issue.
- **Critique of missing appendix content** — the parser strips supplementary material from all submissions.
- **Missing related works** — all cited references are assumed to exist and be released.
- **Request for statistical significance measures** — not standard practice in LTA evaluation; moved to Nice-to-Haves.
- **General section-by-section commentary** that did not identify specific, anchored problems.
- **Critique of missing CRF table alignment** — parser artifact; verified the table values are coherent.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Run ablations on the deterministic protocol.** The ablation mismatch is the most impactful issue to fix. Even if the conclusions remain the same, the evidence becomes directly relevant to the paper's headline claims.
- **Revise the abstract** to match the Conclusion's more measured framing ("competitive with, and in certain settings even superior to") rather than claiming a "very robust alternative."
- **Clarify the ATBA transcript-split mechanism** in Section 3.1. A short algorithmic sketch or diagram would suffice.
- **Expand the EGTEA baseline set** if more recent methods report results on this dataset with the same protocol; otherwise, acknowledge the limitation explicitly.

## Calibration Anchors

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 5lUdTogEL3.md (Re-identification) | 1.00 | R1 | No | Irrelevant topic, far below |
| gwZ90hFSL2.md (Cross-lingual robotics) | 1.00 | R1 | No | Irrelevant topic, far below |
| u1cQYxRI1H.md (Diffusion illumination) | 0.50/10.00 | R1 | No | Mixed extremes, irrelevant |
| nSDOkm0SKo.md (Financial markets) | 1.00 | R1 | No | Irrelevant topic |
| 2HdZPEQUig.md (Object-centric learning) | 3.00 | R1 | No | Weaker contribution, below |
| MSxCBXD5C8.md (Anomalous action) | 3.00 | R1 | No | Different task, below |
| 3ZdGSTxKuy.md (Atypical videos) | 2.00 | R1 | No | Not comparable, below |
| TEjXRrhqtJ.md (Video explanation) | 3.00 | R1 | No | Different task, below |
| **dl34rOnbqJ.md** (Action anticipation) | **4.40** | **R1** | **Yes** | Weaker architecture/narrative; our paper is stronger. Rejected. |
| **Bb21JPnhhr.md** (AntGPT - LTA with LLMs) | **6.25** | **R1, R2** | **Yes** | Best topical match. Both have ~LTA + novel supervision. AntGPT has SOTA on 3 benchmarks but worse low-favorability items (-3.97, -2.92) than our paper (1.41, 2.26). Our paper has stronger novelty but weaker empirical breadth. |
| VYOe2eBQeh.md (Latent action pretraining) | 5.83 | R1 | No | Robotics-focused, different setting |
| **f3CdjpPkSq.md** (Action Sequence Augmentation) | **6.50** | **R1, R2** | **Yes** | Good comparison. Data augmentation for anticipation. Stronger results, similar score band. |
| qHGgNyQk31.md (Seer - video prediction) | 6.50 | R1, R2 | No | Different task (video generation) |
| 9Cu8MRmhq2.md (Multi-granularity correspondence) | 8.00 | R1 | No | Strong video-language paper, above ours |
| PdaPky8MUn.md (Long-sequence models) | 8.00 | R1 | No | Architecture-focused, above ours |
| d8w0pmvXbZ.md (Training instabilities) | 8.00 | R1 | No | Training-focused, above ours |
| STUGfUz8ob.md (Transformer reasoning) | 7.60 | R1 | No | Theory paper, above ours |
| 1DEHVMDBaO.md (Adaptive memory ViT) | 4.60 | R2 | No | Video understanding but different task |
| 4j9plQoOH1.md (LongViTU) | 4.75 | R2 | No | Dataset/benchmark paper |
| uHgVrGF2Wn.md (LVBench) | 4.50 | R2 | No | Benchmark paper |
| **IryGDUHxDE.md** (Unsupervised action recognition) | **5.25** | **R2** | **Yes** | Rejected. Has extreme low-favorability items (-5.11) that our paper lacks. Our paper is stronger. |
| GQgPj1H4pO.md (Weakly supervised VidSGG) | 6.00 | R2 | No | Different task (scene graphs) |
| HEXtydywnE.md (LASER) | 6.00 | R2 | No | Different task |
| 14fFV0chUS.md (TRACE) | 6.75 | R2 | No | Different task |

**Score placement rationale:** The paper's strongest items (Breakfast competitiveness at 14.78, loss decomposition at 13.30) are comparable to AntGPT's strongest (15.15, 13.40), and our worst items (EGTEA at 1.41, abstract overclaim at 2.26) are less severe than AntGPT's worst (-3.97, -2.92). However, AntGPT achieves SOTA on 3 benchmarks while our paper is competitive on only 1 of 3 datasets. The ablation mismatch is a structural weakness that, while fixable, currently weakens the evidential value of the component analysis. This places the paper at the accept threshold but below strong accept.

**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**