## Summary

EmoSign is a dataset paper introducing the first ASL video dataset annotated with sentiment scores (7-point scale), fine-grained emotion categories (10 emotions with intensity ratings), and open-ended qualitative cue descriptions. Annotations were produced by 3 Deaf native ASL signers with professional interpretation experience on 200 video clips (16 minutes, 4 signers) sourced from ASLLRP. The paper also provides benchmark baselines using 4 multimodal LLMs under caption-only, video-only, and video+caption conditions, finding that models rely heavily on text captions and struggle to integrate visual cues for emotion recognition.

## Strengths

1. **Well-motivated gap addressed with strong annotation methodology.** The paper correctly identifies that emotion in ASL is understudied and that facial expressions in ASL serve dual grammatical/emotional functions, creating a distinct technical challenge. Using Deaf native ASL signers as annotators (rather than hearing annotators as in FePh) is a clear methodological improvement grounded in evidence that hearing individuals frequently misinterpret signers' facial expressions. The three-layer annotation pipeline (sentiment, fine-grained emotion categories with intensity, open-ended cue descriptions) is thoughtfully designed.

2. **Novel qualitative cue documentation.** The open-ended descriptions of emotion cues (Section 3.4) — documenting how mouth morphemes, sign modification (speed/size), head/body movements, and narrative framing convey emotion — capture domain knowledge not present in any prior dataset. This is the paper's most distinctive and valuable contribution.

3. **Informative ablation study design.** Testing caption-only, video-only, and video+caption conditions across all models is the correct experimental design to assess modality reliance, and the general finding that models perform similarly with caption-only and video+caption inputs (Table 4) supports the text-over-reliance conclusion.

## Weaknesses

### Major

1. **Benchmark conclusions are not statistically supported and are overclaimed.** The dataset contains 200 clips with per-class counts as low as 25 (anger, surprise_neg) and 30 (fear, disgust). The paper draws substantive conclusions from small numerical differences — e.g., "GPT-4o shows enhanced capacity to distinguish emotions such as worry and disgust" (Section 5.2), and "AffectGPT consistently output sentiment as Neutral" based on a 14.29% wAcc on 7-class sentiment (Section 5.1) — without any confidence intervals, standard deviations, or significance tests (grep confirms zero matches for any of these terms in the paper). The paper's framing ("establishes a new benchmark for understanding model capabilities") overstates what the data supports. These benchmarks are best understood as pilot observations.

2. **VADER-based selection confounds the headline text-over-reliance finding.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances based on VADER analysis of text captions (Section 3.1). The finding that models rely heavily on text captions is therefore partly a consequence of dataset construction: the text modality was explicitly used as the selection criterion. This confound is mentioned tangentially in Section 6 but its implications for the paper's strongest claim ("current multimodal models fail to integrate visual cues into emotional reasoning") are never discussed. A fairer assessment of visual emotion recognition would require either a dataset where text captions are emotionally neutral or an explicit analysis of how the VADER-text/annotator-visual agreement rate affects model behavior.

### Minor

3. **Inter-annotator agreement average appears miscalculated.** Table 2 reports an average Krippendorff's alpha of 0.593, but the mean of the 11 individual alpha values listed in the same table (0.738, 0.699, 0.552, 0.381, 0.119, 0.555, 0.333, 0.351, 0.166, 0.330, 0.370) is approximately **0.418**, not 0.593. The reported value 0.593 matches the average of only the first column (sentiment, joy, excited, surprise_pos). This affects the paper's claim that inter-annotator agreement exceeds MELD (Fleiss' kappa = 0.43) and IEMOCAP (Fleiss' kappa = 0.48) — with the corrected average of 0.418, the comparison is less favorable. The authors should verify this and correct the text.

4. **Signer-emotion confound not analyzed.** The dataset includes only 4 signers (Section 3.4) with an emotionally skewed selection (100 positive, 100 negative). Emotion labels may be confounded with signer identity and signing style — e.g., if one signer appears predominantly in negative clips and another in positive clips, a model could achieve above-chance performance by classifying signers rather than emotions. The paper does not report the emotion distribution per signer or discuss this potential confound.

### Trivial

5. **Multi-expression subset (37 clips) is described but never benchmarked.** Section 4.1 introduces a "multi-expression set" but it is never used in the results. This is a lost opportunity given that co-occurring emotions are a realistic feature of affective communication.

## Nice-to-Haves

- Foreground the qualitative cue analysis more prominently, perhaps as a systematic taxonomy or table mapping specific cues to emotions — this is the paper's most novel content and deserves more space.
- Analyze clips where VADER text sentiment and annotator visual emotion disagreed, as these are the most informative failure cases for testing whether models can override text cues.
- Add bootstrapped confidence intervals to benchmark results to clarify which numerical differences are meaningful vs. noise.
- A per-signer emotion distribution table would help assess the signer-emotion confound.

## Removed Points

- **"Dataset scale fundamentally limits claims"** — kept as Major #1, but reframed to acknowledge that the dataset itself remains a valid contribution; only the benchmark conclusions are weakened by the small N.
- **"MiniGPT4 video+caption being worse than video-only never discussed"** — removed because the paper does partially address this at line 280: "unless the video modality clearly conveys the signers' emotion, it may introduce noise rather than improve predictions."
- **"Manual inspection of randomly selected videos too informal"** — removed as a minor presentation detail that does not affect the paper's core validity.
- **"Missing analysis of VADER-annotator disagreement"** — kept as a nice-to-have; the paper acknowledges this but does not analyze it in depth.
- **"No confidence intervals"** — merged into Major #1.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any fundamentally new interpretation that the authors do not already partially acknowledge in their limitations section.

## Suggestions

1. Correct the inter-annotator agreement average in Table 2 and revise the comparison to MELD/IEMOCAP accordingly.
2. Add a per-signer emotion distribution analysis to assess potential signer-emotion confounding.
3. Add bootstrapped confidence intervals to all benchmark results.
4. Reframe benchmark conclusions more cautiously, presenting them as pilot observations given the small N and lack of statistical support.
5. Explicitly discuss how the VADER-based text selection affects the interpretation of the text-over-reliance findings.
6. Either evaluate the multi-expression subset or remove the description to avoid unmet reader expectations.

**Calibration anchors.** All retrieved from the deepreview_13k_calibration corpus via vector similarity search on "sign language ASL dataset emotion recognition":

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| gwZ90hFSL2 (Humanoid Robots/Chinese NLP) | 1.00 | R1 (< 1.5) | Unrelated topic, strong reject quality |
| u1cQYxRI1H (IC-Light) | 0.50 | R1 (< 1.5) | Erroneous low score (actual 10.0); irrelevant to this paper |
| 5lUdTogEL3 (Person ReID) | 1.00 | R1 (< 1.5) | Unrelated topic, strong reject |
| nSDOkm0SKo (Financial Markets) | 1.00 | R1 (< 1.5) | Unrelated topic, strong reject |
| lMW9d1AqC9 (Sign→SQL) | 1.67 | R1 (1.5–3.5) | Sign-language related but narrower scope |
| EqCbc4wrzy (MDPE Deception Dataset) | 2.50 | R1 (1.5–3.5) | Multimodal emotion dataset, but poor writing and unclear contributions |
| TadxJc1XAE (TeacherActivityNet) | 3.00 | R1 (1.5–3.5) | Small dataset, narrow scope |
| Jq8HYNZG9s (ShadowPunch) | 3.00 | R1 (1.5–3.5) | Very narrow dataset, solved accuracy |
| flgrH5nK4H (Representing Signs) | 4.00 | R2 (3.5–5.5) | Sign language method paper with limited novelty and insufficient evaluation |
| f1uXrAjpOH (Open-vocab MER) | 5.40 | R2 (3.5–5.5) | Emotion recognition dataset with larger scope, but LLM-feedback-loop concerns |
| 7kRFnSFN89 (VRG-SLT) | 5.00 | R2 (3.5–5.5) | Sign language translation method with mixed reviews |
| otoggKnn0A (FHA-Kitchens) | 4.00 | R2 (3.5–5.5) | Small fine-grained action dataset, limited novelty |
| Uj2Wjv0pMY (Detective Hat) | 4.33 | R2 (3.5–5.5) | Procedural activity dataset, moderate quality |
| L2kbdthX5M (SignAvatars) | 6.25 | R1 (5.5–7.5) | Large-scale 3D SL motion dataset (70K videos, 153 signers); much larger and more comprehensive than EmoSign |
| 0Xt7uT04cQ (Uni-Sign) | 6.40 | R1 (5.5–7.5) | Large-scale CSL dataset (1,985 hours); significantly larger resource |
| LqaEEs3UxU (Sign2GPT) | 5.75 | R1 (5.5–7.5) | SL translation method with pretrained adapters |
| qnlG3zPQUy (ILLUSION Deepfake) | 6.00 | R1 (5.5–7.5) | Large-scale deepfake dataset (1.3M samples); accepted |
| 79ZkWgY2FI (Small→Large Generalization) | 5.25 | R2 (4.0–6.0) | Accepted at 5.25; training data analysis paper, different domain |

**Round-1 bracket:** [3.5, 5.5]. EmoSign is clearly above the 1.5–3.5 band (MDPE at 2.50, ShadowPunch at 3.00) because it addresses a genuine gap with thoughtful annotation design and novel qualitative documentation. It is below the 5.5–7.5 band (SignAvatars at 6.25, Uni-Sign at 6.40) because those papers offer substantially larger-scale resources (70K videos / 1,985 hours vs. 16 minutes). **Round-2 narrowing:** Within [3.5, 5.5], EmoSign sits near the lower-middle, comparable to Representing Signs (4.00) and FHA-Kitchens (4.00) — genuine contributions that have real limitations (scale, overclaiming, verifiable errors) that prevent a stronger rating. It is weaker than Open-vocab MER (5.40) which had a larger scope and clearer methodological innovation but similar concerns. **Final score: 4.0**, reflecting a real but modest dataset contribution undermined by overclaimed benchmark conclusions, a miscalculated agreement metric, and a confound in the experimental design that is not adequately discussed.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>