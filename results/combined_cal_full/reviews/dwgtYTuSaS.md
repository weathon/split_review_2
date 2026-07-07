Now I have enough calibration data. Let me compose the final review.

## Summary

This paper introduces **Continuous Online Action Detection (COAD)**, a new task formulation where OAD models continuously learn and adapt from streaming egocentric video in a single pass without storing data. The authors curate **Ego-OAD**, a large-scale egocentric OAD benchmark derived from Ego4D MQ (87 classes, 22,991 instances, 263h of video). They propose three training strategies — state continuity, orthogonal gradient projection, and non-uniform loss weighting — and evaluate on Ego-OAD and EPIC-KITCHENS.

## Strengths

- **The problem framing is compelling and well-motivated.** Section 1 makes a clear case that offline-trained OAD models are mismatched to wearable-device deployment where user behavior and environments shift over time. The argument that continuous adaptation is a necessity for egocentric AI is well-reasoned and distinguishes this work from the bulk of OAD research.

- **Ego-OAD dataset fills a genuine gap.** The dataset (Section 3) provides 87 classes, 22,991 instances, 263 hours of egocentric video with multi-label temporal annotations (36% overlapping instances). No existing OAD dataset offers this combination of scale, egocentric perspective, and multi-label richness. Deriving it from Ego4D MQ is a sensible choice.

- **The three-way evaluation protocol is well-designed.** Splitting data into pretraining / in-stream / out-of-stream sets (following Carreira et al., 2024a) directly operationalizes the paper's two key claims — adaptation (in-stream performance) and generalization (out-of-stream performance). This is clean and appropriate for the question being asked.

## Weaknesses

### Major

**1. Headline improvement numbers are computed against a baseline that understates the marginal contribution of the proposed techniques.** The abstract and introduction claim "up to 20% improvement" (adaptation) and "up to 7% improvement" (generalization). These compare **COAD** against **Pretrained Only** (no adaptation at all). However, the **w/o COAD** baseline — which also performs continuous adaptation, just without the three proposed strategies — already achieves large gains over Pretrained Only. For in-stream Ego Top-5 (Table 1): w/o COAD gains +13.4 points over Pretrained Only; COAD adds only **+2.6 on top of that**. For out-of-stream: w/o COAD gains +2.5 points; COAD adds +4.4. Reporting improvements only against the no-adaptation baseline inflates the perceived contribution. The paper should prominently report incremental gains over the continuous-training baseline, not just the no-adaptation baseline.

**2. The in-stream mAP reversal is acknowledged but never explained.** On Ego-OAD with ego pretraining (Table 1), w/o COAD achieves **39.0 mAP** on in-stream while COAD achieves **36.8 mAP** (−2.2 points). The paper says the baseline "achieves competitive results" and that COAD trades this for generalization, but offers no mechanistic explanation for why gradient decorrelation and non-uniform loss *hurt* in-stream mAP. If these techniques improve generalization by preventing overfitting, why do they reduce in-stream performance? A clearer characterization of this trade-off is needed.

### Minor

**3. No variance or confidence intervals are reported.** All results appear to be single-run point estimates. Given the modest differences between COAD and w/o COAD on several metrics (e.g., out-of-stream mAP: 26.0 vs 25.5), it is impossible to assess statistical reliability. Multiple seeds with standard deviations are standard practice.

**4. The EPIC-KITCHENS results are mixed and the explanation is vague.** While COAD achieves the best out-of-stream generalization (e.g., Action mAP 9.9 vs Pretrained Only 8.6), on in-stream both adapted methods sometimes underperform no adaptation (e.g., in-stream Action mAP: COAD=7.9 vs Pretrained Only=9.6). The paper attributes this to "the fine-grained nature of the actions and annotations" without substantiation — no analysis of whether the issue is data quantity (202 in-stream videos vs 1,177 for Ego-OAD), action granularity, or something else.

**5. The non-uniform loss shows dramatic effects that are not analyzed.** The ablation (Table 3) shows that removing non-uniform loss drops out-of-stream Top-5 from 76.0 to 67.7 (−8.3) while in-stream mAP *rises* from 36.8 to 42.4 (+5.6). This suggests the loss is doing something more fundamental than "reducing the mismatch between training and inference dynamics," but no analysis is provided. The IID Training upper bound in Figure 4 is mentioned but never quantified.

**6. The orthogonal gradient method uses only single-step decorrelation with minimal justification.** Section 4.5 projects the current gradient against only the immediately preceding gradient. Temporal correlations in video can span many frames, yet the paper does not discuss why one-step decorrelation suffices or compare to alternatives with longer gradient buffers.

### Trivial

- The abstract contains a typo: "Countinuous" → "Continuous" (line 27).

## Nice-to-Haves

- Report per-class performance to show which classes benefit most from COAD (e.g., frequent vs. rare actions).
- Probe in-stream set size sensitivity by subsampling Ego-OAD to match EPIC-KITCHENS scale.
- Analyze performance on overlapping vs. non-overlapping action regions, since 36% of instances have overlaps.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"No comparison to existing OAD methods"**: REMOVED. The paper's contribution is the continuous adaptation setting, not achieving SOTA on standard benchmarks. The w/o COAD baseline correctly isolates the effect of the proposed training strategies. Evaluating published OAD methods would test architecture quality, not the adaptation claim. The paper explicitly scopes to lightweight RNNs for resource-constrained deployment.

- **"EPIC-KITCHENS results undermine the paper's claims" / specific claim about "Action mAP 7.9 vs 9.6 on out-of-stream"**: REMOVED as factually incorrect. The table format is (out/in): 7.9 is the **in-stream** value. The out-of-stream comparison is COAD 9.9 vs Pretrained Only 8.6, favoring COAD. The broader concern about mixed results is retained above as a Minor weakness.

- **"Section 5.4 (Feature Extractors) purpose unclear"**: REMOVED. Comparing TSN vs TimeSformer is relevant context for backbone choice in this setting.

- **Various formatting/style nitpicks and grammar complaints**: REMOVED per instructions (parser artifacts, not author errors).

- **Missing related works**: REMOVED per instructions (cannot verify external knowledge).

- **Speculative concerns about missing appendix content**: REMOVED per instructions.

## Novel Insights

The harsh critic's most valuable observation is that the headline numbers conflate two distinct effects: the benefit of *any* continuous training (w/o COAD already captures most gains) versus the marginal benefit of the specific proposed strategies (orthogonal gradient, non-uniform loss). This distinction is critical for correctly interpreting the paper's contribution and is not clearly communicated in the current framing.

## Suggestions

1. Reframe headline numbers to report gains over the w/o COAD baseline alongside gains over Pretrained Only.
2. Provide a mechanistic explanation for why COAD's components trade off in-stream mAP for out-of-stream generalization.
3. Report results with multiple random seeds and standard deviations.
4. Analyze the EPIC-KITCHENS results more carefully — test whether data quantity is the limiting factor by subsampling Ego-OAD.
5. Discuss why one-step gradient decorrelation suffices, or compare against a multi-step variant.

## Score and Decision

### Calibration

All anchor papers retrieved across rounds:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| PrAViC | jawV7vhGHw.md | 4.25 | R1 | Yes | Similar structure (new task formulation + method), similar issues with overclaimed contributions and missing analysis. Our paper has a stronger dataset contribution. |
| Continual Learning After Model Deployment | BrqFB8Nl7e.md | 3.75 | R1 | Yes | Also suffers from missing comparisons and limited evaluation. Our paper has more thorough experiments. |
| EgoHOIBench | M8gXSFGkn2.md | 7.00 | R1 | Yes | Stronger benchmark contribution and more rigorous evaluation. An upper-bound comparison. |
| Online Weight Approximation | HCCkCjClO0.md | 3.00 | R1 | Yes | Weaker baselines and simpler experiments. Our paper is stronger. |
| Large Scale Video Continual Learning | 7L2bpe7lfm.md | 4.50 | R2 | Yes | Similar score band. Both have solid problem statements but method novelty/rigor concerns. |
| StreamingBench | qnAZqlMGTB.md | 5.75 | R2 | Yes | Stronger benchmark paper with more comprehensive evaluation. Higher than our paper. |

**Bracket rationale**: Round 1 bracketing placed the paper between 3.5 and 5.5. The most directly comparable papers (PrAViC at 4.25, Video Continual Learning at 4.50) share the same profile: well-motivated problem + dataset contribution, but methodology claims that outpace the evidence. Our paper's strongest negative item (headline inflation, weight -5.69) is less severe than the -8+ items pulling down those anchors, but there are more accumulated moderate negatives. The paper's strongest positive (evaluation split, +4.12) is also more moderate than the +7.10 observed for the 4.50 anchor. The 5.75 StreamingBench paper is clearly stronger (more comprehensive evaluation, clearer contributions). The 3.00-3.75 papers are weaker (simpler baselines, less thorough evaluation). This places our paper solidly in the 4.0-5.0 range, with 4.5 as the best point estimate.

**Final score grounded in weighted-item comparison**: The paper shares with PrAViC (4.25) the pattern of an overclaimed contribution relative to the main baseline (their missing baselines at -8.86 mirror our headline inflation at -5.69). It shares with Video Continual Learning (4.50) the pattern of missing variance/uncertainty estimates. Where our paper differs from the 3.75 anchor is in having a concrete dataset contribution and a cleaner evaluation protocol. Where it falls short of the 5.75 anchor is in the thoroughness of analysis and the clarity of the contribution separation. The net weighted sum of -9.29 for our draft's items aligns with a score slightly above 4 (where moderate negatives outweigh moderate positives but no item is individually fatal).

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>