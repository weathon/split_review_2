Now let me finalize the review with a calibrated score.

## Summary

EmoSign introduces a dataset of 200 ASL video utterances annotated by Deaf native signers with sentiment labels (7-point scale), 10 emotion categories (intensity 0–3), and open-ended descriptions of emotion cues. The paper also benchmarks four multimodal LLMs across caption-only, video-only, and video+caption conditions, finding that models rely heavily on text and perform poorly on video-only input. The dataset addresses a genuinely underserved problem.

## Strengths

- **Annotation by Deaf native signers with professional interpretation experience** is a genuine methodological differentiator. The paper correctly identifies that prior work (FePh) used hearing annotators, which is problematic because hearing individuals frequently misinterpret signers' facial expressions (Section 3.2, line 119; comparison with FePh at lines 77–83). This is the right way to do this kind of annotation work.

- **The open-ended emotion cue descriptions** (Section 3.4, last two paragraphs) documenting how emotions manifest through non-manual markers, sign modification, and contextual cues provide information that goes beyond label-based datasets. The three thematic findings (non-manual markers as primary cues, sign modification for emphasis, role of context for disambiguation) are grounded in concrete annotator responses and could genuinely advance the field.

## Weaknesses

### Fatal
None.

### Major

1. **VADER-based selection confounds the headline claim about visual cue integration.** The 200 utterances were selected as the 100 most positive and 100 most negative clips *as judged by VADER sentiment analysis of their text captions* (lines 115–116, Figure 1). This means the dataset was curated to make text a strong emotion signal, while the visual emotional expressiveness of the selected videos was not independently controlled. The paper's central finding — that models "fail to integrate visual cues into emotional reasoning" (Abstract) — is partly confounded: the dataset cannot distinguish between "models cannot perceive emotion in sign videos" and "these particular videos were not selected for having visually discernible emotion independent of text captions." Section 6 (line 330) mentions this issue obliquely but does not reckon with it as a confound to the paper's core claim.

2. **Inappropriate comparison of inter-annotator agreement metrics and near-random agreement on several categories.** The paper states: "existing widely-used emotion recognition datasets had lower inter-annotator agreement compared to ours: MELD (Fleiss' kappa = 0.43), IEMOCAP (Fleiss' kappa = 0.48)" (line 140). This compares **Krippendorff's alpha** (used for EmoSign throughout Table 2) with **Fleiss' kappa** (cited for MELD and IEMOCAP). These are mathematically distinct measures and are not directly comparable. Separately, several emotion categories have very low Krippendorff's alpha: surprise_negative (0.119), disgust (0.166), frustration (0.330), sadness (0.333), anger (0.370) (Table 2). For a dataset intended as ground truth, categories with α < 0.2 (surprise_negative, disgust) indicate near-random agreement and provide an unreliable training/evaluation signal.

3. **No uncertainty quantification on benchmark results, with per-class sample sizes in the low tens.** All benchmark results in Tables 3 and 4 are reported as point estimates without confidence intervals, bootstrap estimates, or statistical significance tests (confirmed by grep — no matches for "confidence interval," "bootstrap," "significance," or "variance" anywhere in the paper). With per-class sample sizes of 25–50 for several emotion categories, the reported accuracy swings (e.g., Qwen2.5 getting 70% on sadness with captions alone but 0% on sadness with video+caption; GPT-4o getting 86% on worry with captions but 0% with video+caption in Table 4) are likely dominated by sampling noise. The reader cannot determine which differences reflect genuine model behavior versus random variation.

### Minor

1. **Only 4 signers appear in the video data** (line 144), while Table 1 reports "3" in the signers column — a minor inconsistency. With so few signers, model performance could be influenced by signer identity rather than emotion; no signer-based analysis or cross-signer evaluation is provided.

2. **The "emotion cue grounding" task is presented as a formal benchmark** (Section 4.1, third task) but evaluated entirely qualitatively — manual inspection of a few randomly selected videos with no systematic metric, no inter-rater reliability, no formal protocol (Section 5.3). This should be presented as exploratory analysis, not as a benchmark task alongside the quantitative sentiment and emotion classification.

### Trivial
None.

## Nice-to-Haves

- Include confidence intervals or bootstrap estimates for all benchmark results.
- Provide a per-signer breakdown of model performance to check whether signer identity drives results.
- Analyze which videos show disagreement between VADER and annotators and what visual cues explain that disagreement — this would address the VADER confound constructively rather than treating it as a minor point.

## Removed Points

- **"The problem is real and underserved"** — removed as generic (praises the problem area, not the paper's specific contribution).
- **"The paper is honestly written about limitations"** — removed as superficial; all papers should be honest, and the paper does not actually address the VADER confound as a confound.
- **"Dataset is too small" framed as standalone fatal weakness** — subsumed into weakness #3 about missing uncertainty quantification. The core issue is not that 200 clips is inherently insufficient (the paper acknowledges size constraints) but that the results are reported without any variance estimation, making them uninterpretable.
- **VADER criticism labeled "fatal/structural"** — downgraded to Major because: the annotators did identify rich visual emotional cues in these same videos (Section 3.4), so poor video-only model performance is still informative; the dataset's primary value (qualitative descriptions) is not undermined by the confound.

## Novel Insights

The most valuable insight emerging from cross-referencing the review with the paper is that EmoSign's strongest contribution is structurally at odds with its own framing. The qualitative annotation study — documenting how Deaf native signers perceive emotion through specific non-manual markers, sign modifications, and contextual cues — is a genuine, difficult-to-replicate contribution that does not depend on the VADER selection or the dataset size. The benchmark evaluation, which the paper foregrounds, is underpowered and confounded. A version of this paper that centered the qualitative findings and repositioned the benchmarks as suggestive pilot results would be substantially stronger.

## Suggestions

1. **Reframe the contribution** to center the qualitative annotation study and the three thematic findings about ASL emotion cues (Section 3.4), treating the benchmarks as secondary/suggestive.
2. **Address the VADER confound directly** — analyze which videos show VADER-annotator disagreement and what visual cues explain that disagreement.
3. **Add confidence intervals or bootstrap estimates** to all benchmark results.
4. **Either remove the "emotion cue grounding" from the benchmark suite** or develop a quantitative evaluation protocol.
5. **Correct the inter-annotator agreement comparison** by either computing Fleiss' kappa for EmoSign or citing Krippendorff's alpha for MELD/IEMOCAP.
6. **Resolve the inconsistency** between "4 signers" (line 144) and "3 signers" (Table 1).

## Score and Decision

**Calibration anchors used** (all rounds combined):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| MDPE (deception detection dataset) | 2.50 | 1 | Rejected; larger dataset (104h) but weaker motivation than EmoSign |
| ShadowPunch (shadowboxing benchmark) | 3.00 | 1 | Rejected; narrow scope, 27 videos, solved performance |
| Representing Signs as Signs (one-shot ISLR) | 4.00 | 1 | Rejected; novel method but insufficient evaluation |
| FHA-Kitchens (hand action dataset) | 4.00 | 1 | Rejected; 2,377 clips, more data than EmoSign but similar dataset-paper profile |
| Unsupervised SLT (sign language method) | 5.00 | 1 | All 5s; method paper, not a dataset contribution |
| SignAvatars (3D SL motion dataset) | 6.25 | 1 | Rejected despite 6.25 avg; much larger scale (70K videos) |
| ILLUSION (deepfake detection dataset) | 6.00 | 1 | Accepted; 1.3M samples, large-scale |

**Round 1 bracket:** 2.5–4.5 (based on comparison with MDPE/ShadowPunch at the low end and FHA-Kitchens/Representing Signs at the upper end).

**Narrowing:** EmoSign has a more novel problem and stronger annotation methodology than the low-end anchors (MDPE, ShadowPunch), placing it above 3.0. However, the VADER confound, small size with no uncertainty quantification, and flawed inter-annotator comparison prevent it from reaching the quality of FHA-Kitchens (4.0) which had 10× more data. Final score: **3.5**.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>