Now I have a thorough calibration picture. Here is my final consolidated review.

---

## Summary

EmoSign introduces a multimodal dataset of 200 ASL videos annotated by three Deaf native ASL signers for sentiment (7-point scale), ten emotion categories with intensity ratings, and — most distinctively — open-ended qualitative descriptions of emotion cues (facial expressions, head/body movements, signing modifications). The paper also reports zero-shot benchmark evaluations of four multimodal LLMs on sentiment and emotion classification tasks. The qualitative cue descriptions from native signers (Section 3.4) are genuinely novel and the annotation protocol is well-designed. However, the benchmark evaluation has three serious confounds — VADER-based selection bias, unreliable ground truth for several emotion categories, and very small per-class sample sizes with no uncertainty estimates — that substantially undermine the paper's headline claims about model behavior.

## Strengths

- **Real, well-motivated gap, clearly documented.** The paper shows (Table 1) that no existing ASL dataset has emotion labels, and explains why ASL's dual grammatical/emotional use of facial expressions makes this nontrivial (Section 1). The problem framing is strong.

- **Annotation protocol is a methodological strength.** Hiring three Deaf native ASL signers with professional interpretation experience (rather than hearing annotators, as in FePh) is well justified. The three-layer annotation (sentiment on a 7-point scale, emotion intensity 0–3 for ten categories, open-ended cue descriptions) is substantially more informative than the binary presence/absence labels in prior work. The training session and pilot testing with ASL-first individuals demonstrate careful protocol design.

- **Qualitative emotion cue descriptions (Section 3.4) are genuinely novel and valuable.** This is the paper's strongest contribution. No prior ASL dataset includes native signers' open-ended descriptions of how emotions manifest through non-manual markers (facial expressions, head thrusts, mouth shapes, body movements) and modified signing (size, speed, repetition, finger-spelling). This material could inform both computational modeling and linguistic analysis of ASL affect expression.

## Weaknesses

### Major

- **VADER-based selection confounds the central benchmark finding.** The dataset selects the 100 most positive and 100 most negative utterances *by VADER text sentiment* (Section 3.1). This means: (a) the dataset systematically excludes videos where text is neutral but visual emotion is strong — arguably the most interesting cases for studying visual-emotion-as-opposed-to-textual-emotion; (b) the benchmark finding that "models rely on text captions" is partly an artifact, since text was deliberately selected for emotional extremity; (c) the sentiment distribution (only 5 neutral out of 200, Figure 2) is a construction artifact, not a property of ASL emotional expression. The paper acknowledges VADER–annotator divergence in passing (Limitations) but does not address how this selection procedure directly confounds the paper's central claim that "models fail to integrate visual cues."

- **Several emotion categories have near-random inter-annotator agreement yet are used as ground truth for model evaluation.** Krippendorff's alpha for surprise_neg is 0.119 (barely above chance) and disgust is 0.166 (Table 2). Frustration (0.330), sadness (0.333), fear (0.351), and anger (0.370) are also very low. The paper's comparison to MELD (Fleiss' kappa = 0.43) and IEMOCAP (Fleiss' kappa = 0.48) uses different agreement metrics (Krippendorff's alpha vs. Fleiss' kappa) on different annotation tasks and is not directly meaningful. Categories with alpha below ~0.3 should not be treated as reliable ground truth for model evaluation — the model's "success" or "failure" on surprise_negative (Table 4) primarily reflects label noise, not model capability.

- **Benchmark claims substantially outrun the statistical evidence.** Per-class sample sizes are very small: only 5 neutral samples for 7-class sentiment; ~12.7 samples per class on average for 11-class emotion classification on 140 videos. No confidence intervals, error bars, or statistical tests are reported anywhere. Despite this, the paper presents broad conclusions ("models fail to integrate visual cues," "exhibit bias towards positive emotions") as established findings rather than preliminary observations. The claim that video+caption outperforms caption-only — the paper's main argument that "visual information can contribute meaningfully" — is based on a few percentage points difference on tiny samples, with inconsistent patterns across models (e.g., MiniGPT4's video+caption wAcc of 21.65 is *lower* than its video-only 34.68 for 3-class, Table 3).

### Minor

- **The multi-expression subset (37 clips) is defined (Section 4.1) but never evaluated.** This is a stated benchmark task with no results reported.

- **MiniGPT4's caption-only wAcc of 1.92 on 3-class sentiment is far below chance (33%),** suggesting the model may not have understood the task in that condition. This is not noted in the results discussion.

- **No confidence intervals or uncertainty estimates are reported,** despite very small per-class sample sizes where a single prediction change can shift accuracy by 5–15 percentage points.

### Trivial

None.

## Nice-to-Haves

- Expand Section 3.4's qualitative analysis with systematic frequency counts of which cues were associated with which emotions, rather than purely anecdotal themes.
- Define standard train/validation/test splits to support fine-tuning.
- Include bootstrap confidence intervals for all metrics.

## Removed Points

The following points from the input review were verified against the paper and removed or downgraded:

- **"Abstract claim of 'first' is misleading without qualification"**: The paper qualifies this in Related Work (Section 2), where FePh is discussed and differentiated. EmoSign is indeed the first to include sentiment + emotion intensity + qualitative cue descriptions. Kept as a minor accuracy note but downgraded — the qualification exists in the paper.
- **"Line 53 grammatical issue"**: Parser/formatting artifact, not author error. Removed.
- **"Phrasing suggests 200 labels rather than 200 videos"**: Overly nitpicky interpretation; the sentence is clear in context. Removed.
- **"No train/validation/test split"**: For zero-shot evaluation benchmarks, standard splits are not essential. Removed.
- **"Cannot verify analogy to cited small datasets"**: The reviewer admits inability to verify; this is a knowledge gap, not a paper flaw. Removed.
- **"No ablation of VADER filter"**: A reasonable suggestion but goes beyond the paper's stated scope as a first dataset release. Removed.
- **"No aggregate statistics over annotator cue descriptions"**: Would strengthen the paper but the qualitative themes are already a contribution. Moved to Nice-to-Haves.
- **"No discussion of recommended use cases"**: Partially addressed implicitly. Removed.
- **"Dataset cannot be used for fine-tuning"**: 200 samples can be split by users. Removed.

## Novel Insights

The key insight emerging from cross-referencing the reviews is that this paper has two separable contributions of very different strength: the qualitative ethnographic-style emotion cue documentation (Section 3.4) is genuinely novel and the most robust part of the paper, while the quantitative benchmark evaluation is underpowered and contains known confounds (VADER pre-filter, low-agreement label categories, no uncertainty estimates). The paper would be substantially stronger if it recentered on the qualitative contribution and positioned the benchmarks as illustrative pilots rather than conclusive findings. None beyond the paper's own contributions.

## Suggestions

1. Reframe the paper to center the dataset and qualitative annotations as the primary contribution; position the benchmarks explicitly as pilot/proof-of-concept baselines rather than definitive findings.
2. Drop or aggregate emotion categories with Krippendorff's alpha below 0.3 from benchmark evaluation, or report results with a strong caveat that these categories have near-random ground truth.
3. Add bootstrap confidence intervals to all reported metrics.
4. Evaluate (or explicitly defer to future work) the multi-expression subset that is currently defined but not analyzed.
5. Acknowledge that the VADER pre-filter partly explains the observed text-over-reliance in models and discuss what this means for the interpretation of the benchmark results.

## Score and Decision

**Round-1 bracket:** Based on weighted-item comparison against calibration anchors — the paper is clearly above MDPE (2.5, weight of -14.29 on concept confusion vs. -7.20 on inter-annotator agreement for EmoSign) but below OV-MER (5.4, which had comprehensive benchmarks and weaker negative weights) and below EmpathyRobot (6.0, 10K samples). The most comparable anchors are Representing Signs as Signs (4.0) and FHA-Kitchens (4.0), both dataset papers with similar quality profiles — real contributions but significant limitations.

**Narrowing:** The inter-annotator agreement weakness (-7.20) and benchmark overclaiming (-4.78) are substantially heavier than the negatives in comparable papers at 4.0-5.0. The qualitative contributions (+3.42, +3.53) are genuine but do not compensate for flawed quantitative evidence. Placing below OV-MER (5.4) and below sign language papers at 5.0, but above MDPE (2.5). The bracket narrows to 3.5–4.5.

**Final score: 4.0.** The paper fills a real gap and has a well-designed annotation protocol with genuinely novel qualitative annotations. However, the benchmark conclusions are undermined by the VADER selection confound, the use of near-random-agreement categories as ground truth, and the absence of any uncertainty quantification on very small per-class samples. The paper's claims substantially outrun what the evidence supports. With substantial reframing and more honest characterization of the evidence, the core dataset contribution could warrant a higher score.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>