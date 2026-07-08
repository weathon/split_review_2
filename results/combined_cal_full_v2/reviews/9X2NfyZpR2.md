Now I have enough calibration data to finalize the score. Let me compose the complete review.

## Summary

This paper introduces TbLTA, the first framework for dense Long-Term Action Anticipation (LTA) trained exclusively from video transcripts (ordered action lists without timing/duration information) — eliminating the need for expensive frame-level annotations. The method combines a weakly-supervised temporal alignment module (ATBA) to generate pseudo-labels, a cross-modal attention mechanism to ground video features in transcript semantics, and CTC/CRF-based losses to enforce temporal coherence. Experiments on Breakfast, 50Salads, and EGTEA show that transcript-only supervision can match or exceed fully-supervised methods on Breakfast while remaining competitive on rare classes on EGTEA.

## Strengths

- **Genuinely novel problem framing.** The paper is the first to formulate dense LTA using *only* transcript-level supervision. The only prior weakly-supervised LTA work (Zhang et al., 2021) still relies on some frame-level labels. This distinction is real and meaningful — transcripts are substantially cheaper to obtain. [weight=8.31]

- **Competitive deterministic results on Breakfast.** In Table 1, deterministic TbLTA achieves an average MoC of 29.03 on Breakfast, outperforming all fully-supervised methods shown (ActFusion: 28.45, FUTR: 26.59, Cycle Cons.: 25.13). This is genuinely surprising for a weakly-supervised method and suggests transcript structure captures procedural regularities that dense labels do not. [weight=9.19]

- **Thorough ablation study.** Table 4 systematically removes each component (duration loss, cross-attention, CRF) on both datasets. The ablation on Breakfast shows meaningful drops (3.3–5.7 points) confirming each component contributes materially — stronger than typical ablation effects in this area. [weight=9.46]

- **Competitive rare-class performance on EGTEA.** Table 2 shows TbLTA achieves 60.11 mAP on rare classes, exceeding supervised Anticipatr (55.10) and Timeception (59.70). This non-obvious result — transcript-level supervision helping with tail classes — deserves more prominence. [weight=7.97]

## Weaknesses

### Fatal
None.

### Major

- **No analysis of pseudo-label quality.** The entire method hinges on a temporal alignment module producing pseudo-labels that supervise both the TAS head and anticipation decoder (Section 3.1, Figure 2). Yet the paper provides **no evaluation** of pseudo-label accuracy against ground-truth segmentation, even though ground-truth frame labels exist for all three datasets during training. On 50Salads, where the method underperforms (20.92 vs ActFusion's 28.39), the paper attributes this to "longer videos, denser action distributions, and frequent transitions yield weaker temporal regularities, amplifying the impact of imprecise temporal alignment" — but this is speculation without evidence. Reporting per-frame pseudo-label F1 or IoU against ground truth would diagnose whether alignment quality correlates with downstream performance, and is essential for understanding the method's failure modes. [weight=1.60]

### Minor

- **Headline claim overstatement in abstract.** The abstract states transcript-based supervision "offers a very robust and less costly alternative to its fully supervised counterpart." This holds on Breakfast (TbLTA 29.03 vs ActFusion 28.45) but not on 50Salads (20.92 vs 28.39, a 7.5-point gap) or EGTEA (65.37 vs Anticipatr 76.80). The conclusion is better qualified ("competitive with, and in certain settings even superior to"), but the abstract's unqualified framing could mislead readers about the breadth of the method's competitiveness. [weight=4.04]

- **Stochastic/deterministic results mixed in the same table.** Table 1 reports both deterministic and stochastic (Top1/Mean) variants together. The stochastic Top1 numbers are substantially higher (Breakfast: 37.15 vs deterministic 29.03) but arise from a protocol that allows multiple attempts. While marked with `*` and noted in the caption, the presentation risks conflating the two regimes. Separating them into distinct tables or clearly flagging in every comparison sentence which variant is discussed would be cleaner. [weight=4.98]

- **Thin weak-supervision baseline comparison.** The only weakly-supervised baseline, WS-DA (Zhang et al., 2021), is reported at a single point (Obs 30%) without horizon breakdown, and uses some frame-level labels — making the comparison asymmetric. A natural pipeline baseline is missing: use ATBA (or another weakly-supervised TAS method) to generate pseudo-labels, then train a standard LTA decoder on those pseudo-labels. This would isolate whether performance comes from transcript supervision *per se* or from the joint architecture. [weight=2.56]

- **No variance reporting across splits.** Results are averaged over 4 splits (Breakfast) and 5 splits (50Salads) but no standard deviations or confidence intervals are given (confirmed by grep: no "variance"/"standard deviation"/"std" in paper). Given the small margin on Breakfast (29.03 vs ActFusion's 28.45), the reader cannot assess whether these differences are robust or an artifact of a particular split configuration. [weight=3.94]

- **Duration loss self-supervised cycle fragility.** The duration loss (Eq. 7) uses momentum-based class priors computed from the model's own pseudo-labels as targets: noisy pseudo-labels produce noisy duration priors, creating a risk of confirmation bias. The ablation shows minimal gain on 50Salads (0.2 points, Table 4), suggesting limited impact. This fragility should be discussed more explicitly. [weight=6.34]

- **Insufficient positioning of Kim et al. (2024).** The related work mentions Kim et al. (2024) as exploring "language-based anticipation without explicit time annotations, using a vision-language model with in-context learning" — which sounds like a closely related setting. The paper should explain why this setting differs and why comparison is infeasible, or include the comparison. [weight=2.77]

### Trivial
None.

## Nice-to-Haves

- **Add a pipeline baseline**: Train ATBA (or another weakly-supervised TAS method) to generate pseudo-labels from transcripts, then train a standard LTA decoder on those pseudo-labels. This would disentangle whether gains come from transcript supervision or the joint architecture.
- **Report pseudo-label accuracy**: Per-frame F1 or IoU against ground-truth segmentation to diagnose when/why the temporal alignment module fails — especially important for understanding the 50Salads underperformance.
- **Report variance / standard deviation across splits** for key results.
- **Temper the abstract's claim** to match the evidence — e.g., "competitive with fully supervised methods on certain datasets."
- **Explicitly discuss limitations**: When is transcript-only supervision likely to fail (high intra-class duration variability, activities with weak temporal ordering, permutable action sequences)?

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **EGTEA verb-only metric choice questioned.** The paper explicitly states "restricting evaluation to verb prediction" following the protocol of Nagarajan et al. (2020). This is a clear, justified choice for comparison. *Removed: criticism addressed in the paper.*

2. **Qualitative results description too generic.** The qualitative description says "the model produces accurate and temporally coherent segmentations" — this is common in the field and adds reasonable context to the figure. *Removed: minor presentation nitpick without substantive impact.*

3. **Hyperparameters deferred to supplementary.** The paper states loss weights γ₁, γ₂, γ₃ are detailed in supplementary material. Per review guidelines, the supplementary exists in the original submission and deferring implementation details there is standard practice. *Removed: parser strips appendix content; not a valid weakness.*

4. **ATBA adaptation underspecified.** The paper states ATBA "partition[s] the full transcript Y into observed and future sub-transcripts." Since the observation ratio α is known and ATBA aligns transcript labels to frames, the split mechanism is implicit from which aligned labels fall in the observed vs. predicted frame ranges. The level of detail is reasonable for a module adopted from prior work. *Demoted to Nice-to-Have.*

## Novel Insights

None beyond the paper's own contributions. The core observations — that the method's strength is asymmetric across datasets, that pseudo-label quality is unexamined, and that the abstract overclaims — are already surfaced in the weaknesses above.

## Suggestions

1. Add pseudo-label accuracy analysis (per-frame F1/IoU against ground truth) to diagnose failure modes, especially for 50Salads.
2. Add a pipeline baseline: weakly-supervised TAS → standard LTA decoder, to isolate the benefit of the joint architecture.
3. Report variance/std across splits for key results.
4. Temper abstract claims to match the evidence across all three datasets.
5. Separate deterministic and stochastic results more clearly (distinct tables or sections).

## Score and Decision

### Calibration Summary

**Anchors retrieved (all rounds):**

| File | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `5lUdTogEL3.md` (Person ReID) | 1.00 | R1 | No | Unrelated topic; reject-level |
| `gwZ90hFSL2.md` (Cross-lingual Robots) | 1.00 | R1 | No | Unrelated topic; reject-level |
| `u1cQYxRI1H.md` (Diffusion) | 0.50 | R1 | No | Unrelated topic; score anomaly (10,10,10,10 avg 10 but returned as 0.5, likely data issue) |
| `2HdZPEQUig.md` (Object-Centric Video) | 3.00 | R1 | No | Weakly related; stronger methodological concerns |
| `YGWxpOI6Y0.md` (VideoGPT+) | 3.40 | R1 | No | Marginally related; baseline-level |
| `dl34rOnbqJ.md` (Actions-to-Action) | 4.40 | R1 | Yes | Directly on action anticipation; weaker novelty, modest gains |
| `Bb21JPnhhr.md` (AntGPT) | 6.25 | R1+R2 | Yes | Directly on LTA; SOTA results, less novel framing |
| `f3CdjpPkSq.md` (Action Seq Aug) | 6.50 | R1+R2 | Yes | Directly on action anticipation; strong evaluation, novelty concern (-5.57) |
| `GQgPj1H4pO.md` (VSNLS) | 6.00 | R2 | Yes | Weakly supervised video task using language; similar profile of strengths/weaknesses |
| `HEXtydywnE.md` (LASER) | 6.00 | R2 | No | Weakly supervised video; different task |
| `4j9plQoOH1.md` (LongViTU) | 4.75 | R1 | No | Video understanding; different task |
| `xYzOkOGD96.md` (Grounded Video Caption) | 3.83 | R1 | No | Different task |

**Round 1 bracket:** The paper sits between the 4.40–6.50 range. It has substantially stronger conceptual novelty and better-validated contributions than the 4.40 Action-to-Action anchor (which had negative-weight weakness items about limited novelty and marginal improvements). It is most similar to the 6.00–6.50 band papers — AntGPT (SOTA results but straightforward LLM application), Action Sequence Augmentation (solid method with novelty concern), and VSNLS (weakly supervised video with language, similar weakness profile).

**Round 2 narrowing:** Comparing weighted items:
- My paper's strengths (7.97–9.46) are comparable to AntGPT's (7.32–9.89) and VSNLS's (6.88–8.44).
- My paper's weakest weakness item (pseudo-label quality, weight 1.60) is nearly identical to VSNLS's "no failure case analysis" (1.60) — both papers got 6.0.
- My paper has no negative-weight weaknesses (none <0), unlike AntGPT (-2.42 for positioning) and Action Sequence Augmentation (-5.57 for novelty). This pushes weakly toward 6+.
- However, my paper's empirical results are more mixed than AntGPT's (which claims SOTA on three benchmarks), which pulls it slightly down from 6.25.

**Final score:** **6.0** — The paper makes a genuine contribution (first transcript-only LTA) with a well-designed architecture and thorough ablation, but the empirical support is uneven across datasets, the pseudo-label quality is unexamined, and the abstract overclaims. This places it at borderline accept level, comparable to other weakly-supervised video papers at this score that have similar gap profiles.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>