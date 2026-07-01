## Summary

This paper introduces EmoSign, a multimodal dataset of 200 American Sign Language (ASL) video clips annotated for sentiment (7-point scale), emotion categories (10 classes with intensity), and open-ended descriptions of emotion cues. The annotations were performed by three Deaf native signers with professional interpretation experience. The paper also presents benchmark evaluations of four multimodal LLMs (GPT-4o, AffectGPT, Qwen2.5-VL-7B, MiniGPT4-Video) on sentiment analysis, emotion classification, and a qualitative emotion cue grounding analysis.

## Strengths

1. **Novel qualitative emotion cue descriptions from Deaf native signers.** The open-ended descriptions of how emotions manifest in signing (Section 3.4) — non-manual markers, modified sign production, contextual disambiguation — are the most distinctive contribution. No prior sign language dataset includes this kind of native-signer perspective on emotion expression.

2. **Methodologically appropriate annotation protocol.** Using Deaf native signers (rather than hearing annotators) to label emotional content is a clear strength. The paper correctly notes (Section 2) that hearing individuals frequently misinterpret signers' facial expressions. The three-round annotation process (sentiment → emotion categories → open-ended descriptions) with confidence ratings and a skip option is thoughtfully designed and culturally appropriate.

3. **Clear differentiation from the closest prior work (FePh).** The paper explicitly distinguishes itself from FePh on three concrete dimensions (Section 2): full-frame video rather than cropped faces, Deaf rather than hearing annotators, and intensity ratings rather than binary labels. These are real improvements.

## Weaknesses

### Fatal

None.

### Major

1. **VADER-based selection confounds the central benchmark interpretation.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances based on VADER analysis of English text captions (Section 3.1, line 115). This creates a highly skewed sentiment distribution with only 5 neutral samples out of 200 (Figure 2). The benchmark finding that models perform much better with text than with video alone is partly attributable to this selection — the text captions were intentionally polarized. The paper's Limitations section (line 330) briefly notes that "VADER results differed from the annotators' results" but does not quantify this discrepancy or discuss its implications for the validity of the benchmark conclusions. The claim that "current multimodal models fail to integrate visual cues into emotional reasoning" (abstract) is overstated given that the evaluation set is biased toward text-extreme cases. The authors should quantify the VADER-annotator sentiment discrepancy across all 200 clips — this single analysis would directly address the core confound.

2. **Ambiguity about whether annotators had access to text captions, which affects what the ground truth represents.** The paper does not clarify in the main text (Section 3.2) whether the Deaf annotators were shown the English text captions while labeling videos. The annotation interface is described only via a reference to Appendix 4 (line 119). If annotators saw text captions, their emotion judgments could be influenced by text content — meaning the ground truth is not purely a measure of visual emotional expression. If they did not see captions, that should be explicitly stated, and the discrepancy between annotator labels and VADER scores (alluded to in Limitations) would be a valuable quantitative finding in its own right. This information belongs in the main body.

3. **Invalid comparison of inter-annotator agreement metrics.** Section 3.3 (line 140) compares Krippendorff's alpha (0.593 average for EmoSign) against Fleiss' kappa from other datasets (0.43 for MELD, 0.48 for IEMOCAP) and claims higher agreement. These are different metrics with different properties and scales; direct numeric comparison is not meaningful without justification. Moreover, several individual emotion categories have very low alpha values (surprise_neg: 0.119, disgust: 0.166, frustration: 0.330, anger: 0.370), calling into question the reliability of ground truth for these specific categories.

### Minor

4. **No uncertainty quantification for benchmark results.** With only 200 total clips and per-class samples as small as 5 (neutral sentiment, Figure 2), the accuracies and F1 scores in Tables 3 and 4 have high variance. No confidence intervals, error bars, or significance tests are reported. Many per-class accuracies in Table 4 are 0% across multiple models, and the paper does not report per-class test sample sizes, making it impossible to assess whether observed differences between models or conditions are meaningful.

5. **Emotion cue grounding is presented as a benchmark task but evaluated only qualitatively.** Section 4.1 describes emotion cue grounding as one of three benchmark tasks, yet Section 5.3 evaluates it solely through informal inspection of "several randomly selected videos" with no ground-truth dataset, no quantitative metric, and no systematic evaluation. This should be framed as a qualitative analysis, not a benchmark task.

6. **Several anomalous results in Table 3 are unexplained.** MiniGPT4's caption-only wF1 (5.92 on 3-class) is much lower than its video-only wF1 (40.00), yet video+caption produces 36.89 — a non-monotonic pattern that warrants explanation. AffectGPT's video-only wF1 of 0.04 on 3-class sentiment is essentially random and requires clarification (e.g., is the model predicting a single class for all samples?).

### Trivial

7. The abstract's claim that EmoSign is "the first sign video dataset containing sentiment and emotion labels" should be qualified — FePh (Alaghband et al., 2020) did contain emotion labels on cropped sign-language face images, though the paper already distinguishes itself from FePh on multiple grounds (full-frame video, Deaf annotators, intensity ratings). A more precise framing would avoid unnecessary debate.

8. The number of clips that received only 2 annotator judgments (because one annotator skipped) is not reported. Section 3.3 states "minimally 1, maximally 3" annotators per clip but says skips were "a very small fraction" without quantifying this.

## Nice-to-Haves

- A quantitative comparison between VADER-predicted sentiment (from text captions) and Deaf annotator-judged sentiment (from video) across all 200 clips would directly address the core confound about what the dataset captures and would likely strengthen the paper's claims.
- Reporting confidence intervals (e.g., via bootstrap) for the metrics in Tables 3 and 4 would provide honest communication of reliability given the small sample size, without requiring more data.

## Removed Points

These points were surfaced in the input review but are removed with justification:

- **"VADER is designed for social media text, not ASL translations"**: This is speculative — the paper uses VADER only as a rough filter for emotional salience, not as a ground-truth label. No evidence is offered that VADER's performance degrades on ASL-caption text specifically.
- **"Emotion category scheme may not be optimal (joy/excited overlap)"**: The paper already identifies and addresses this — Section 4.1 merges them into "happiness" due to their Jaccard similarity of 0.81.
- **Several section-by-section notes** (e.g., "the related work discussion is competent but generic," "using only 4 models is acceptable") are subjective opinions without concrete evidence and do not constitute actionable weaknesses.
- **"FePh hiring hearing annotators"** is acknowledged as a strength by the paper itself and is subsumed under Strength #2.

## Novel Insights

The reviews surface one insight not fully articulated by the paper itself: the VADER-based selection strategy means the text-only vs. video-only benchmark comparison inherits a design confound — clips were deliberately chosen for text sentiment extremity, so text-based models are naturally advantaged. The most impactful corrective action would be to present the VADER-vs.-annotator discrepancy as a primary analysis rather than a brief limitation note. This discrepancy is the evidence that would either validate or undermine the paper's central claim that visual emotion signals in sign language differ from and complement text sentiment.

## Suggestions

1. Add a quantitative comparison table showing VADER sentiment scores vs. Deaf annotator sentiment labels for all 200 clips. This directly addresses the core confound and would likely strengthen the paper.
2. Clarify in the main text (Section 3.2) whether annotators had access to text captions, and discuss the implications.
3. Add confidence intervals (bootstrap) to Tables 3 and 4, or at minimum report per-class test sample sizes.
4. Remove the invalid Krippendorff's alpha vs. Fleiss' kappa comparison, or re-compute both on a common metric.
5. Reframe the emotion cue grounding section as qualitative analysis, not a benchmark task.
6. Explain the non-monotonic MiniGPT4 results and AffectGPT's near-random video-only performance in Table 3.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>