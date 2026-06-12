Now I have enough calibration data. Let me finalize the review.

**Calibration Analysis:**

**Round 1 Bracket:** Based on the retrieved anchors, I place this paper between 4.5 and 5.5.

- The paper is clearly better than MDPE (2.50) and VRG-SLT (5.00), which have overclaimed results and poor writing.
- It's comparable to OV-MER (5.40), another emotion recognition dataset/benchmark paper that was rejected despite a novel paradigm — both have genuine contributions but significant methodological concerns.
- It's weaker than SignAvatars (6.25, rejected), Uni-Sign (6.40, accepted), and MIntRec2.0 (6.50, accepted), which are larger-scale, more comprehensive datasets with stronger experimental support.
- The VADER confound, low inter-annotator agreement on key categories, and small sample sizes without baselines are substantive limitations. However, the paper's genuine novelty (first ASL emotion dataset with Deaf native signers), insightful qualitative findings, and honest limitations discussion prevent it from scoring lower.

The paper sits firmly in the 5.0 range — a borderline reject with real contributions but limitations that prevent acceptance in its current form.

---

## Summary
EmoSign introduces the first ASL dataset with fine-grained sentiment, emotion category, and open-ended emotion cue annotations by 3 Deaf native signers, applied to 200 video clips from ASLLRP. The paper benchmarks 4 multimodal LLMs across sentiment analysis, emotion classification, and emotion cue grounding, finding that current models rely heavily on text captions and fail to leverage visual cues for emotion recognition in sign language.

## Strengths
- **First ASL dataset with Deaf native signer emotion annotations**: Table 1 systematically compares EmoSign against 6 existing ASL datasets, demonstrating that none contain fine-grained emotion or sentiment labels annotated by Deaf native signers. The closest prior work (FePh) used hearing annotators and face-cropped data. This is a genuine gap.
- **Rich multi-layer annotation scheme**: Each utterance receives three layers: 7-point sentiment scale, presence/intensity (0–3) for 10 emotion categories, and open-ended natural-language descriptions of emotion cues. This is richer than FePh's binary labels and standard emotion datasets lacking cue descriptions.
- **Three-condition ablation reveals informative failure patterns**: The caption-only/video-only/video+caption design across 4 MLLMs shows that for sentiment analysis (Table 3), video+caption outperforms both unimodal conditions, while for emotion classification (Table 4), caption-only performs comparably to or better than video+caption — demonstrating that models rely on text shortcuts for fine-grained emotion.
- **Emotion cue grounding analysis exposes text-visual dependence**: Section 5.3 and Figure 3 show that models interpret identical visual cues in contradictory ways depending on whether text captions are available (e.g., "neutral facial expression" in video-only vs. specific emotional cues in video+caption for the same video), providing direct evidence of post-hoc visual explanation construction.
- **Domain-appropriate annotation methodology**: Recruiting Deaf native ASL signers with professional interpretation experience addresses a documented problem — hearing individuals frequently misinterpret signers' facial expressions — and enables distinguishing grammatical from emotional facial markers.

## Weaknesses

### Fatal
None.

### Major
- **VADER text-based pre-selection creates a text-visual confound**: The dataset was constructed by filtering ASLLRP videos through VADER (a text-based sentiment analyzer) to select the 100 most positive and 100 most negative utterances based on their English captions (Section 3.1, line 115). The paper's core motivation is that sign language emotions manifest through *visual cues* that may diverge from textual content. Yet the construction pipeline systematically excludes videos where visual emotional expression is strong but the caption is textually neutral. The finding that models "heavily rely on text captions" (Table 4) is partly a consequence: the dataset was selected so text sentiment *would* be predictive. The paper acknowledges in Section 6 (line 330) that "VADER results differed from the annotators' results often" but frames this positively rather than recognizing it as a confound.

- **Very low inter-annotator agreement on several emotion categories**: Krippendorff's alpha scores are near or below 0.2 for surprise_neg (0.119), disgust (0.166), and frustration (0.330) (Table 2). With only 3 annotators and majority vote, a 2-1 split is treated as ground truth — but for surprise_neg (alpha=0.119), this majority is essentially arbitrary. The paper contextualizes by comparing to MELD and IEMOCAP, but those use Fleiss' kappa (not directly comparable) and involve different annotation paradigms (dialogue with speaker context vs. isolated video clips). The benchmark (Table 4) evaluates models against these noisy labels without stratifying by agreement level.

- **Underpowered benchmark without naive baselines**: With 200 videos total and uneven class distributions (surprise_neg: 25, anger: 25, neutral sentiment: 5 — Figure 2B/C), per-class accuracy in Table 4 is computed on very few examples, especially for the single-expression set (140 clips across 11 classes). The paper does not report per-class sample counts alongside accuracy, does not provide confidence intervals, and does not establish any naive baselines (majority class, random, or text-only heuristics), making it impossible to judge whether reported numbers reflect signal or noise.

### Minor
- **Prompting asymmetry between GPT-4o and other models**: GPT-4o was prompted with all three tasks simultaneously while other models were prompted task-by-task (Section 4.2). The paper explains this was due to other models' inability to produce clean multi-task output, but this confound is not controlled for.
- **Limited generalizability from single source**: Only 4 signers from ASLLRP (lab recordings), limiting diversity of signing styles and contexts. Acknowledged in Section 6 but still a limitation.

### Trivial
None.

## Nice-to-Haves
- Reporting results stratified by inter-annotator agreement level would distinguish signal from noise for low-agreement categories.
- A text-only baseline (e.g., sentiment classification from captions alone) would quantify how much benchmark performance is driven by text shortcuts.
- Documenting how many VADER-excluded videos had visually expressive signing but neutral captions would quantify the text-visual confound.
- Augmenting the dataset with visually-expressive but textually-neutral videos would break the VADER confound.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **"First comprehensive dataset" overstatement in Introduction**: The paper does acknowledge FePh in Related Work, and the differences (Deaf annotators, more fine-grained labels, full body vs. face-only) are substantive. This is a minor phrasing issue.
- **Section 5.3 qualitative analysis being informal**: The paper explicitly says "several randomly selected videos" and frames this as preliminary. Appropriate for scope.
- **Strength finder claim that VADER pre-selection is a "pragmatic and transparent strategy"**: This conflicts with the verified weakness about VADER confounding text and visual emotion. The paper's own acknowledgment that "VADER results differed from the annotators' results often" validates the concern.

## Novel Insights
The paper's most genuinely novel insight is the demonstration that MLLMs construct post-hoc visual explanations consistent with text sentiment rather than genuinely reading visual emotion cues from sign language. The finding in Section 5.3/Figure 3 that models interpret the same visual cue in contradictory ways depending on caption availability is thought-provoking and has implications beyond sign language for understanding how multimodal models process visual information.

## Suggestions
- Add a text-only baseline to quantify how much model performance is attributable to text shortcuts vs. visual information.
- Report per-class sample counts alongside accuracy in Table 4 and add bootstrap variance estimates.
- Consider augmenting the dataset with visually-expressive but textually-neutral videos to break the VADER text-visual confound.
- Report benchmark results separately for high-agreement vs. low-agreement emotion categories.

## Score and Decision

**All retrieved anchors across rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| gwZ90hFSL2 | 1.00 | R1 | Clearly much worse — nonsensical paper |
| 5lUdTogEL3 | 1.00 | R1 | Clearly worse — poorly motivated |
| u1cQYxRI1H | 0.50 | R1 | Outlier (scored 10 despite avg 0.5) |
| 5kMwiMnUip | 1.40 | R1 | Clearly worse — low quality jailbreaking paper |
| EqCbc4wrzy | 2.50 | R1 | Worse — MDPE has fuzzy concepts, poor writing, marginal results |
| gNoqEdT2wO | 2.33 | R1 | Worse — generic multimodal CL benchmark |
| lMW9d1AqC9 | 1.67 | R1 | Worse — sign language to SQL, poorly motivated |
| YrxhSkfHh0 | 3.33 | R1 | Worse — method paper with limited novelty |
| f1uXrAjpOH | 5.40 | R1 | Comparable — OV-MER has novel paradigm but LLM dependency concerns; rejected |
| 7kRFnSFN89 | 5.00 | R1 | Comparable — VRG-SLT overclaims SOTA, poor writing; rejected |
| sMFqEror1b | 4.75 | R1 | Comparable — MMToM-QA is a benchmark paper; rejected |
| Tgsc0KEkN6 | 4.50 | R1 | Slightly worse — ViML is a multimodal dataset paper; rejected |
| L2kbdthX5M | 6.25 | R1 | Stronger — SignAvatars is larger scale sign language dataset; still rejected |
| qnlG3zPQUy | 6.00 | R1 | Stronger — ILLUSION is comprehensive deepfake dataset; accepted |
| 0Xt7uT04cQ | 6.40 | R1 | Stronger — Uni-Sign has SOTA results + large dataset; accepted |
| nY9nITZQjc | 6.50 | R1 | Stronger — MIntRec2.0 is larger scale benchmark; accepted |
| z8sxoCYgmd | 8.00 | R1 | Much stronger — LOKI is comprehensive benchmark |
| 7gUrYE50Rb | 8.00 | R1 | Much stronger — EQA-MX is novel + large scale |
| HnhNRrLPwm | 8.00 | R1 | Much stronger — MMIE is large-scale benchmark |
| TPZRq4FALB | 8.00 | R1 | Much stronger — novel method with strong results |

**Round 1 bracket:** 4.5–5.5. The paper is clearly better than the 2.5 band (MDPE) and comparable to OV-MER (5.40). It's weaker than SignAvatars (6.25, rejected) and the accepted papers at 6.0+. No round 2 needed — the bracket is clear.

**Final score: 5.0.** The paper has genuine novelty (first ASL emotion dataset with Deaf native signers, insightful qualitative findings about model text-visual dependence) but the VADER pre-selection confound, low inter-annotator agreement on key emotion categories, and underpowered benchmark without naive baselines are substantive limitations. The paper sits in the borderline-reject range alongside OV-MER (5.40) and VRG-SLT (5.00).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>