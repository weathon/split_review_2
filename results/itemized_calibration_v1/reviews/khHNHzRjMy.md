Now I have all the calibration data I need. Let me finalize my review.

**Round 1 bracket:** Based on the anchors, EmoSign sits between the weaker dataset papers (EqCbc4wrzy.md at 2.50, T4VK4U4aKb.md at 4.50) and the stronger ones (f1uXrAjpOH.md at 5.40, L2kbdthX5M.md at 6.25). The VADER circularity and internal contradiction issues are comparable in severity to T4VK4U4aKb's lack-of-baselines problem (-5), but EmoSign's core annotation methodology is a genuine strength. **Bracket: 4.0–5.5.** Narrowing: the OV-MER anchor (5.40) had cleaner experimental design but also had severe label-quality issues. EmoSign has better human annotations but the VADER circularity is a structural weakness that paper doesn't properly acknowledge. This places EmoSign below 5.40 but above 4.50, giving a final score of **5.0**.

---

## Summary

EmoSign introduces a dataset of 200 ASL video clips with sentiment and emotion labels annotated by three Deaf native ASL signers, along with open-ended descriptions of emotion cues. The paper also provides zero-shot benchmarks of four multimodal LLMs on sentiment analysis, emotion classification, and a qualitative emotion cue grounding analysis. The core claim is that models fail to integrate visual cues and over-rely on text captions.

## Strengths

1. **Well-motivated and specific problem framing.** The paper correctly identifies that emotion in sign language is critically understudied, and that the dual grammatical-emotional function of facial expressions in ASL creates a modeling challenge distinct from conventional multimodal emotion recognition (Section 1, lines 13–28). This motivation is technically grounded and not generic.

2. **Annotation by qualified Deaf native ASL signers.** The annotators are Deaf native signers with professional interpretation experience (Section 3.2, lines 119–123), which is the correct methodological choice given that hearing annotators often conflate grammatical and emotional facial expressions (Lim et al., 2024). This cultural-linguistic validity is a genuine asset of the dataset.

3. **Open-ended cue descriptions are a genuinely novel contribution.** To the authors' knowledge, no prior sign language dataset includes free-text descriptions of *how* emotions manifest in signing (Section 3.4, lines 193–194). These descriptions could inform annotation schema for larger datasets and guide feature engineering, potentially outlasting the specific benchmark results in impact.

## Weaknesses

### Fatal
None.

### Major

1. **The paper's central claim about "failing to integrate visual cues" is internally contradicted by its own sentiment analysis results.** The abstract and introduction state that models "fail to integrate visual cues into emotional reasoning" (lines 9, 26). However, Table 3 shows that for sentiment analysis (3-class), video+caption substantially outperforms caption-only across all models (e.g., GPT-4o: 49.53→76.72 wF1; AffectGPT: 44.91→64.37; Qwen2.5: 33.72→54.29). The paper's own Section 5.1 (lines 227–229) acknowledges that "the large performance gains in the video + caption condition...demonstrates that visual information can contribute meaningfully." For emotion classification (Table 4), caption-only and video+caption do perform similarly, which supports text-dependence. The abstract-level claim conflates two distinct findings. The paper should precisely differentiate: models *can* integrate visual information for sentiment analysis but struggle for fine-grained emotion classification, while visual-only performance is near-chance across tasks.

2. **VADER-based selection creates a circularity that weakens the text-dependence finding.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances based *solely on VADER analysis of the text captions* (Section 3.1, line 115). This means the dataset explicitly excludes videos where the text is neutral but the signing is emotionally expressive — precisely the cases that would test whether models can recognize emotion from visual cues independently of text. The finding that models over-rely on text is partly a consequence of the data selection protocol. The paper acknowledges in limitations (line 330) that VADER-disagreement cases contain "rich non-manual markers," but does not discuss how this selection bias affects the interpretation of the benchmarks. The finding is not invalid, but it is substantially less informative than claimed.

3. **Inter-annotator agreement is too low for several emotion categories to yield reliable ground-truth labels, and the comparison to prior datasets uses a different metric.** Krippendorff's alpha for surprise_negative (0.119), disgust (0.166), frustration (0.330), sadness (0.333), anger (0.370), and fear (0.351) are well below conventional thresholds for tentative conclusions (Table 2). The paper contextualizes these by comparing to MELD (Fleiss' kappa = 0.43) and IEMOCAP (Fleiss' kappa = 0.48), but Krippendorff's alpha and Fleiss' kappa are different statistics with different scales and cannot be directly numerically compared (line 140). For these negative-emotion categories, majority-vote labels from three annotators with near-random agreement are unreliable, and results involving these individual categories should be interpreted with caution.

4. **Zero-shot-only evaluation without a human baseline limits what the benchmarks can tell us.** All four models are evaluated zero-shot; none are fine-tuned on sign language data or on this task. A human baseline (hearing non-signers labeling the videos from video alone) would calibrate the task difficulty and make the model results interpretable. Without it, the benchmarks primarily show that off-the-shelf VLMs are not pre-trained for this task — a weak result. The abstract's claim that this dataset "establishes a new benchmark for understanding model capabilities" (line 9) is not fully supported by a zero-shot-only evaluation.

### Minor

5. **23 video clips are unaccounted for.** The paper states 200 utterances total but reports 140 clips in the single-expression set and 37 in the multi-expression set (line 207), totaling 177. The remaining 23 clips are not explained. Additionally, the multi-expression set filtering procedure ("to exclude combinations only present in a single sample," line 207) and its impact on the dataset are not described.

6. **Emotion cue grounding analysis is purely qualitative.** Section 5.3 (line 284) reports manual inspection of "several randomly selected videos" with no systematic coding scheme, inter-rater reliability, or quantification. This is labeled as preliminary, but it does not reach the standard of evaluation the rest of the paper aims for.

7. **"Comprehensive" is overstated for the dataset scale.** The abstract describes EmoSign as "the first comprehensive dataset" (line 17). With 200 clips, 16 minutes, 4 signers, and a single source (ASLLRP), the resource is better described as a focused pilot or the first dedicated dataset. The open-ended cue descriptions are genuinely valuable, but the dataset is not comprehensive in coverage.

8. **MiniGPT4's near-zero caption-only performance suggests a protocol issue.** MiniGPT4 achieves 1.92 wAcc / 5.92 wF1 for 3-class sentiment (caption-only) and 0.00 for both metrics for 7-class sentiment (caption-only) in Table 3, essentially non-functional results that likely reflect an inability to follow the output format rather than a meaningful baseline. Including these numbers without commentary is misleading.

### Trivial

- The text states "4 different signers" (line 144) but Table 1 reports "3" in the Signers column for EmoSign — a factual discrepancy.
- The paper does not report whether the joy/excited → happiness merge (line 207) was done before or after agreement analysis, which could affect perceived per-category agreement.

## Nice-to-Haves

- **Human baseline:** A small study with hearing non-signers labeling the videos from video alone would calibrate the task difficulty and is the single most informative addition.
- **Fine-tuned evaluation:** Even a small-scale fine-tuning experiment with cross-validation on the 200 clips would test whether the dataset can support learning.
- **Per-emotion breakdown with caveats:** Given low agreement for several negative emotions, per-category results should explicitly flag unreliable categories.
- **Signer-stratified analysis:** With only 4 signers, signer-specific variation should be reported and train/test splits stratified.
- **Multi-label evaluation:** The natural formulation for this dataset; the paper acknowledges this as future work.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *Criticism about FePh as a comparative benchmark:* Asks the paper to address a problem outside its stated scope. The paper correctly identifies three differences from FePh; whether models behave similarly on FePh is not a required analysis.
- *Criticism about "not yet released" or availability concerns for cited models:* Per hard rules, all cited models, datasets, and references are assumed to exist.
- *Criticism about missing appendix content (e.g., hyperparameters, full prompts):* Parser strips appendix content from all papers; these exist in the original submission.
- *Criticism that the limitations section is too narrow regarding items already listed:* The paper does list several limitations (VADER as simple filter, lack of multi-label evaluation, need for fine-tuning). However, the specific omissions noted are retained as part of other weaknesses.

## Novel Insights

The reviews surface an insight not fully articulated in the paper: the paper conflates two distinct model behaviors — (a) failure to extract emotion from visual cues when **no** text is available (video-only condition) and (b) failure to *integrate* visual information when text **is** available (video+caption vs. caption-only comparison). These are different failures with different implications, and the paper would be stronger if it separated them. The VADER-selection circularity insight — that the sampling frame pre-commits the dataset to text-emotion alignment and then the benchmarks "discover" text-dependence — is also not discussed in the paper.

## Suggestions

1. Reframe the central claim to be precise: "Models struggle to recognize emotion from visual-only sign language input (near-chance), and for fine-grained emotion classification, adding video to text does not consistently improve over text alone." Remove "fail to integrate" language for sentiment analysis, where video+caption clearly helps.
2. Explicitly acknowledge the VADER selection circularity as a limitation and discuss the types of videos systematically excluded.
3. Add a supplementary human non-signer baseline study.
4. Report per-category results with caveats for low-agreement negative emotions.
5. Explain the 23 unaccounted clips and the multi-expression filtering procedure.
6. Either fix MiniGPT4's evaluation protocol or exclude it, as its near-zero scores are not informative baselines.

## Anchors Used

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| f1uXrAjpOH.md (OV-MER) | 5.40 | 1 | Yes | Emotion recognition dataset paper; had data leakage and label quality issues; EmoSign has cleaner human annotations but weaker evaluation |
| EqCbc4wrzy.md (MDPE) | 2.50 | 1 | Yes | Multimodal deception dataset; too limited for ICLR; EmoSign is clearly stronger |
| cpGPPLLYYx.md (VL-ICL Bench) | 6.50 | 1 | Yes | Well-executed benchmark with thorough experiments; EmoSign is weaker in evaluation depth |
| L2kbdthX5M.md (SignAvatars) | 6.25 | 2 | Yes | Large-scale sign language 3D motion dataset; much larger scale but different focus; EmoSign has unique emotion annotation contribution |
| T4VK4U4aKb.md (Short-video dataset) | 4.50 | 2 | Yes | Large-scale dataset paper with no task baselines; similar severity of evaluation weakness |

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>