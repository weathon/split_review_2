Now I have strong calibration across multiple anchors. Let me write the final consolidated review.

## Summary

This paper introduces TbLTA, the first weakly-supervised dense Long-Term Action Anticipation (LTA) method trained exclusively from video transcripts (ordered action lists without timing/duration). The architecture combines temporal alignment (ATBA) to generate pseudo-labels, CTC-based transcript supervision, cross-modal attention with local masking for feature grounding, a CRF for prediction coherence, and a self-supervised duration head. On Breakfast at Obs 30%, the deterministic variant outperforms all fully supervised baselines; on 50Salads and EGTEA the method is behind supervised approaches but establishes the first transcript-only LTA baselines.

## Strengths

- **Genuinely novel problem framing.** TbLTA is the first LTA method that uses only video transcripts, operating with no frame-level annotations whatsoever. Prior LTA work (including the semi-weakly supervised WS-DA) still requires frame-level labels for the observed segment. The paper correctly identifies and motivates this gap.

- **Strong results on Breakfast under deterministic evaluation.** At Obs 30%, TbLTA deterministic (29.03 avg MoC) outperforms all four supervised baselines (best: ActFusion at 28.45), with gains sustained across multiple horizons and observation levels. This is a non-marginal result on a standard benchmark.

- **Clean, well-integrated architecture.** The model combines temporal alignment, CTC supervision, cross-modal attention with local masking, CRF coherence, and self-supervised duration modeling. Each component has a clear role, and the ablation study (Table 4) confirms each contributes meaningfully to overall performance.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Ablation protocol mismatch with main results.** The ablation study (Table 4) uses the stochastic Top1 metric, while the main comparative results (Table 1) present the deterministic variant as the primary contribution. The ablation table's TbLTA values match the stochastic Top1 values from Table 1 (Breakfast avg 37.15→37.2, 50Salads avg 28.51→28.5), not the deterministic ones. The paper states it uses "Top-1 MoC for ablations as it provides a stable reference point" (line 231) but does not explicitly justify why the ablations follow a different protocol than the paper's main claims. This makes it unclear whether the observed ablation patterns (importance of CTC, cross-attention, CRF, duration) would hold under the deterministic protocol.

- **The headline claim is strongly supported on only one of three benchmarks.** On 50Salads, deterministic TbLTA (20.92 avg) trails the best supervised method ActFusion (28.39) by 7.5 points (~26%). On EGTEA, TbLTA (65.37 All mAP) trails Anticipatr (76.80) by over 11 points. While the paper acknowledges these gaps in the body text, the abstract describes transcript-based supervision as "a very robust and less costly alternative to its fully supervised counterpart" — a characterization that holds primarily on Breakfast, not across all three benchmarks.

- **Comparison with the only prior weakly-supervised LTA work is thin.** The paper compares against WS-DA (Zhang et al., 2021) at only one observation level (Obs 30%) with one horizon each for 50Salads and Breakfast. It does not state whether additional comparison points are available or unavailable. Given that WS-DA uses frame-level labels for the observed segment (more supervision), the comparison is favorable to TbLTA, but the limited data points weaken the analysis.

- **No variance or confidence intervals.** Results are averaged over multiple dataset splits (4 for Breakfast, 5 for 50Salads) but only point estimates are reported. Since several comparisons are within 1–2 points (e.g., TbLTA deterministic vs. ActFusion on Breakfast at several horizons), the lack of variance information makes it impossible to assess which differences are statistically meaningful.

- **No quantitative analysis of pseudo-label quality.** The ATBA module generates pseudo-labels that drive the entire pipeline, yet the paper does not report any measure of pseudo-label accuracy against ground-truth frame labels (available at test time). Systematic errors in pseudo-labels (over-segmentation, boundary misalignment) would affect all downstream results, and quantifying this would strengthen the analysis.

### Trivial
None.

## Nice-to-Haves

- Report the ablation study under the deterministic protocol (or clearly report both deterministic and stochastic variants in parallel) so the reader can assess whether ablation patterns hold for the paper's primary contribution.
- Include a simple baseline that uses transcript ordering without temporal alignment to quantify the gain from the proposed architecture components.
- Analyze pseudo-label quality quantitatively against available ground-truth labels.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **"Stochastic variant not described in main paper"** — REMOVED per protocol. The paper states the stochastic protocol follows Abu Farha & Gall (2019) and is reported in the supplementary material (line 223). The parser strips supplementary sections; the description exists in the original submission.
- **"Cross-attention circular dependency stability not analyzed"** — REMOVED as speculative. The ablation confirms cross-attention's positive contribution; stability analysis is not a standard requirement for acceptance.
- **"Add naive weakly-supervised baseline"** — MOVED to Nice-to-Haves above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Align the ablation evaluation protocol with the main evaluation protocol, or explicitly report ablations under both deterministic and stochastic settings so the connection to the paper's main claims is clear.
- Report standard deviations over dataset splits to enable readers to assess the statistical significance of reported differences.
- Include a quantitative analysis of pseudo-label quality against ground-truth frame labels.
- Expand the WS-DA comparison to additional observation horizons and anticipation lengths if the data is available, or clearly state why it is not.

## Score and Decision

### Calibration

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `5lUdTogEL3.md` | 1.00 | R1 (strong reject) | No | Lifelong person ReID; unrelated topic |
| `u1cQYxRI1H.md` | 10.00 | R1 (strong reject) | No | Illumination harmonization; far topic, paper is clearly different tier |
| `2HdZPEQUig.md` | 3.00 | R1 (1.5–3.5) | Yes | Video object-centric learning; rejected due to evaluation mismatch and weak contribution |
| `dl34rOnbqJ.md` | 4.40 | R1 (3.5–5.5) | Yes | Action anticipation (short-term); rejected because key component did not contribute meaningfully. TbLTA has stronger novelty and cleaner ablation |
| `Bb21JPnhhr.md` | 6.25 | R1 (5.5–7.5), R2 | Yes | **AntGPT**: LTA with LLMs, SOTA on multiple benchmarks. TbLTA has stronger novelty (first weakly-supervised) but less consistent SOTA across datasets |
| `f3CdjpPkSq.md` | 6.50 | R1 (5.5–7.5), R2 | Yes | **Action Sequence Augmentation**: data augmentation for anticipation. Strong evaluation but novelty concerns (−4.28 favorability). TbLTA has clearer novelty |
| `GQgPj1H4pO.md` | 6.00 | R2 | Yes | **Weakly Supervised VidSGG**: introduces weak supervision to a fully-supervised task. Similar framing, weaker core ML contribution (−2.94 favorability). TbLTA has stronger methodological novelty |
| `JDd46WodYf.md` | 5.67 | R2 | No | Active procedure planning; related but different task framing |

**Round 1 bracket**: 5.5–7.5. The paper's genuine novelty (first weakly-supervised LTA) and impressive Breakfast results clearly place it above rejected papers like Actions-to-Action (4.40) and Efficient Object-Centric Learning (3.00).

**Round 2 narrowing**: The paper's weakness profile (favorabilities 0.42 to −1.01, all Minor severity) is milder than accepted anchors AntGPT (weaknesses down to −1.63) and Action Sequence Augmentation (−4.28). Its novelty is stronger than Weakly Supervised VidSGG (accepted at 6.00), whose weaknesses include −2.94 for limited methodological contribution. However, TbLTA's strong results are concentrated on Breakfast, and the ablation protocol mismatch tempers confidence. Placing it between the Weakly Supervised VidSGG (6.00) anchor and AntGPT (6.25) anchor is appropriate.

**Final score: 6.0** — a solid borderline-accept contribution with genuine novelty, strong (but dataset-specific) results, and fixable weaknesses.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>