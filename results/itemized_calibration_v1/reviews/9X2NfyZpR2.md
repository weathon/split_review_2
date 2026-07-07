Now I have a clear picture from calibration. Let me write the final review.

## Summary

This paper introduces TbLTA, the first fully weakly-supervised approach for dense Long-Term Action Anticipation (LTA) that requires only video transcripts (ordered action lists without timing/duration information) rather than frame-level annotations. It combines a temporal alignment module (ATBA) to generate pseudo-labels, cross-modal attention with local masking for grounding video features in transcript semantics, and a transformer encoder-decoder trained with CTC, CRF, and duration losses. On Breakfast, TbLTA is competitive with fully-supervised methods, and on EGTEA it shows strength on rare classes.

## Strengths

1. **First fully weakly-supervised LTA method using only transcripts.** All prior LTA work requires frame-level annotations; the only prior attempt to reduce annotation cost (WS-DA, Zhang et al. 2021) still uses frame-level labels on the observed segment. TbLTA eliminates this requirement entirely, establishing a genuinely new paradigm for scalable LTA. This is a non-trivial advance with clear practical value.

2. **Competitive results on Breakfast.** TbLTA's deterministic variant achieves 29.03 Avg MoC at Obs 30% (Table 1), beating *all* supervised methods including ActFusion (28.45), FUTR (26.59), and Cycle Consistency (25.13). At Obs 30%/50% horizon it scores 28.79 vs ActFusion's 28.78. These results are the paper's strongest evidence that transcript-level supervision can capture the procedural structure of activities and are genuinely surprising for a weakly-supervised method.

3. **Well-motivated architecture with clean ablation hierarchy.** Each design component (ATBA for pseudo-labels, CTC for alignment, CRF for coherence, cross-modal attention with local masking, duration loss) is justified by a specific weakness. The ablations (Tables 3/4) show a consistent hierarchy *w/o cross-att < cross-att simplex < TbLTA*, confirming that the local masking and gated residual fusion add value beyond unconstrained cross-attention.

## Weaknesses

### Fatal
None.

### Major

1. **CTC ablation lacks tabular support.** The paper states (Section 4.3) "Removing the CTC supervision consistently degrades the quality, as shown in 3" — an ambiguous reference (Table 3? Figure 3?). The only quantitative evidence is approximate aggregated averages ("≈ 0.6 points" on 50Salads, "≈ 0.8 points" on Breakfast) with no per-horizon breakdown. CTC is one of the three main loss groups (Eq. 3) and is central to the claim that transcript-level alignment works for LTA, yet it is the only major component without a dedicated ablation table. The CRF, duration, and cross-attention ablations all get proper tables with full breakdowns; CTC does not. This is a significant evidential gap for a core design decision.

2. **No analysis of pseudo-label quality.** The entire pipeline depends on the ATBA temporal alignment module producing reasonable pseudo-labels to supervise both segmentation and anticipation, but the paper provides no quantitative assessment of pseudo-label quality (e.g., alignment accuracy or frame-level accuracy against ground truth on the observed segment). Without this, the central enabling assumption is validated only indirectly through downstream task performance.

### Minor

3. **Thin evaluation on EGTEA.** Table 2 compares TbLTA against only two supervised baselines (Timeception from 2019, Anticipatr). On the primary metric (All), TbLTA scores 65.37 vs Anticipatr's 76.80 — an 11-point gap. There is no weakly-supervised baseline, no breakdown across observation percentages, and the comparison set is too sparse to draw meaningful conclusions about whether TbLTA represents a genuine advance on this dataset. The paper's own framing makes EGTEA a secondary dataset, but even as such the experiment adds little.

4. **No variance reporting.** None of the tables report standard deviations or confidence intervals across runs. For a weakly-supervised method where pseudo-labels can introduce stochasticity during training, this weakens the statistical grounding of the comparative results.

5. **Stochastic Top1 results could invite over-interpretation.** TbLTA* - Top1 values (e.g., 38.27 on Breakfast Obs 30%/50% vs ActFusion's 28.78) represent oracle selection over 10 diverse samples — you do not know which sample is correct at test time. The table caption does distinguish deterministic (bold) from probabilistic (gray) and uses an asterisk, and the paper separately reports Mean values. However, placing Top1 numbers in the same table alongside deterministic methods without an explicit caveat that they are oracle selections risks misleading readers into thinking the method performs far beyond supervised approaches on both datasets. The Mean numbers (28.67 at Obs 30%/50%) are considerably lower.

6. **ATBA module is used but not explained.** The paper adopts ATBA from Xu & Zheng (2024) but provides no high-level summary of how it works (e.g., how it partitions transcripts into observed/future or generates soft pseudo-labels). Since ATBA is central to the entire pseudo-labeling pipeline, a 2-3 sentence summary would improve self-containedness.

7. **Self-supervision loop in duration loss not analyzed.** The duration loss (Eq. 7) trains a regression head using class-wise priors computed from the model's own pseudo-labeled segmentations. If the segmentation head systematically mislabels certain frames, the duration priors will encode those errors and reinforce them. The paper acknowledges this as a "weak prior" but provides no analysis of whether error accumulation actually occurs.

### Trivial
- The CTC ablation reference "as shown in 3" in Section 4.3 is ambiguous and should specify which table or figure.

## Nice-to-Haves
- Quantify annotation cost differences between transcripts and frame-level labels to strengthen the practical motivation.
- Add a proper weakly-supervised baseline on EGTEA (e.g., from a TAS method) to contextualize results.
- Analyze learned duration priors against ground-truth durations at evaluation time to validate the self-supervision loop.
- Add sensitivity analysis of the three-stage training procedure (epoch counts per stage).

## Removed Points
- **Missing related works / references**: Removed per hard rule — cannot verify from external sources.
- **Formatting/style nitpicks**: Removed per hard rule — parser artifacts, not author errors.
- **Reproducibility concerns about undisclosed hyperparameters**: Removed per hard rule — trivial implementation details.
- **Missing appendix content (stochastic protocol details, etc.)**: Removed per hard rule — parser strips appendix sections.
- **Concerns about code/model availability or unreleased references**: Removed per hard rule — cited entities are assumed to exist.
- **Generic scope-creep criticisms** (e.g., "should address problems outside stated scope"): Removed per soft rule — paper focuses on LTA and evaluates on standard benchmarks.
- **Generic "no confidence intervals" framing as fatal**: Downgraded from major to minor — single-run evaluation is standard in this benchmark setting.
- **"Misleading Top1 comparison" framed as critical/evidential**: Downgraded to minor — the paper does label stochastic vs deterministic in the table caption with bold/gray and asterisk notation; the prose is careful. The concern is real but not as severe as originally framed.

## Novel Insights from the Review Process

The key insight that emerges from cross-referencing the reviews is that the paper's strongest evidence for its core claim comes from a single dataset (Breakfast). On 50Salads, TbLTA underperforms relative to supervised methods (20.92 vs ActFusion's 28.39), and on EGTEA the gap is even wider. The paper is transparent about this, but it means the claim "transcript-only supervision can match full supervision" rests heavily on Breakfast results. Understanding why Breakfast works so well (shorter videos, stronger procedural regularities, coarser action classes) while 50Salads and EGTEA do not would be a valuable analysis the paper does not provide. The CTC ablation gap is notable because CTC is arguably the most distinctive loss for transcript-level supervision — it is the loss that directly enforces alignment without any boundary information — and yet its contribution is the least documented.

## Suggestions
1. Add a full tabular CTC ablation with per-horizon breakdown matching the format of Tables 3/4, and disambiguate the reference in Section 4.3.
2. Report standard deviations (or at minimum, run results multiple times) for all main results.
3. Add quantitative analysis of pseudo-label quality (e.g., alignment accuracy of ATBA pseudo-labels against ground truth on the observed segment).
4. Add a brief (2-3 sentence) description of how ATBA works to improve self-containedness.
5. Expand the EGTEA evaluation with more baselines and/or a breakdown across observation percentages.
6. Add a sentence in the table caption explicitly noting that "Top1 selects the best among K stochastic samples and is an oracle upper bound."

## Score and Decision

**Calibration details:**

Retrieved anchors and their avg scores:
- **AntGPT** (Bb21JPnhhr.md, 6.25): LTA paper using LLMs. Key weakness: limited novelty (-4). Our paper has stronger novelty. 
- **Action Sequence Augmentation** (f3CdjpPkSq.md, 6.50): Action anticipation paper with data augmentation. Similar experimental rigor, our paper has slightly stronger novelty.
- **Weakly Supervised Video Scene Graph** (GQgPj1H4pO.md, 6.00): Weakly supervised video understanding. Our paper's contribution is cleaner and better evidenced.
- **LASER** (HEXtydywnE.md, 6.00): Weakly supervised video with neuro-symbolic approach. Similar weak-supervision framing, comparable quality.
- **Actions-to-Action** (dl34rOnbqJ.md, 4.40): Rejected action anticipation paper. Core weakness: marginal improvement with core design not mattering in ablation. Our paper's contributions are much more substantial.

**Bracket determination (Round 1):** The paper's closest topical matches — AntGPT (6.25) and Action Sequence Augmentation (6.50) — both received Accept decisions. Our paper has a stronger novelty claim than AntGPT (first weakly-supervised LTA vs. applying LLMs to LTA) but has some evidential gaps (missing CTC table, no pseudo-label quality analysis) that the Action Sequence Augmentation paper did not have to the same degree. The initial bracket is **6.0–7.0**.

**Narrowing:** Compared to AntGPT (6.25), our paper shares the heavy-weight positive of SOTA-competitive results on a primary benchmark, but has a stronger novelty claim (+3/+4 weight vs AntGPT's -4 "limited novelty"). The missing CTC table and absent pseudo-label analysis are analogous to AntGPT's "marginal improvement" concern (-3 weight) but are fixable rather than structural. Compared to Action Sequence Augmentation (6.50), the experimental rigor is comparable but with different weaknesses (missing table vs. missing comparisons). The paper's contribution (first transcript-only LTA) is more clearly novel and complete than either anchor's, warranting placement slightly above AntGPT.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>