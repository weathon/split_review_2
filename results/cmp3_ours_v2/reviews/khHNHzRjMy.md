Now let me write the final consolidated review.

## Summary
This paper introduces EmoSign, a dataset of 200 American Sign Language (ASL) video clips annotated by three Deaf native signers with professional interpretation experience. Annotations cover 7-point sentiment, 10 emotion categories with intensity, and—most distinctively—open-ended qualitative descriptions of the specific visual cues (facial expressions, signing speed/modification, non-manual markers) that convey each emotion. The paper also presents zero-shot evaluation of four multimodal LLMs across sentiment analysis, emotion classification, and an informal emotion cue grounding analysis.

## Strengths
- **Addresses a genuine, underexplored gap.** Existing ASL datasets overwhelmingly focus on translation rather than affect, and the dual grammatical/emotional function of facial expressions in sign language makes this a non-trivial problem distinct from conventional multimodal emotion recognition. The paper motivates this well (Section 1).
- **Native Deaf signer annotators.** Using three Deaf ASL signers with professional interpretation experience is a real methodological differentiator from prior work (FePh used hearing annotators). Hearing individuals frequently misinterpret signers' facial expressions (Lim et al., 2024), so this gives the annotations genuine linguistic authority.
- **Rich three-layer annotation protocol with qualitative cue descriptions.** The combination of (1) sentiment on a 7-point scale, (2) 10 emotion categories with intensity, and (3) open-ended descriptions of emotion cues is well-designed. The qualitative descriptions in Section 3.4—documenting how non-manual markers, sign modification/speed, and context function in ASL emotional expression from the perspective of native signers—are the most novel and durable contribution, feasible at any dataset size.
- **Honest limitations section.** Section 6 acknowledges the VADER-based selection and the narrow scope of ASLLRP (lab setting, single signers, lack of real-world complexity).

## Weaknesses

### Fatal
None.

### Major
- **VADER-based selection confounds the headline findings about model behavior.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances based on VADER analysis of text captions (Section 3.1). This means: (a) the dataset systematically excludes cases where the text is neutral but signing carries clear emotion, or where text and visual emotion diverge; (b) the finding that models "fail to integrate visual cues and heavily rely on text captions" is partially an artifact of this selection—when text sentiment is deliberately made extreme and informative, of course models will exploit it. This does not tell us whether models would over-rely on text in naturally occurring ASL data where text and visual emotion are less correlated. The paper partially acknowledges this in Section 6 but does not analyze its implications for the central claims.

- **Dataset size (200 clips, ~16 minutes, 4 signers) limits what the benchmarks can support.** For a task as challenging as 11-class emotion classification with low inter-annotator agreement, 200 samples do not provide stable estimates of model capability. A single misclassification shifts accuracy by ~0.5%, yet no confidence intervals, standard errors, or significance tests are reported anywhere in Tables 3 or 4. The qualitative cue descriptions are valuable at any scale, but the benchmark conclusions about model comparisons and modality integration are not supported by the evidence as presented.

- **Low inter-annotator agreement on most emotion categories raises questions about ground truth reliability.** From Table 2: surprise_neg α=0.119, disgust 0.166, frustration 0.330, sadness 0.333, anger 0.370, fear 0.351—seven of ten emotion categories have Krippendorff's α < 0.4, conventionally considered poor agreement. The paper compares these to MELD (Fleiss' κ=0.43) and IEMOCAP (Fleiss' κ=0.48), but Krippendorff's α and Fleiss' κ are not directly comparable; α is more conservative for ordinal data. More importantly, if trained annotators cannot reliably distinguish frustration from anger from sadness in these clips, it is unclear what it means to evaluate model performance against majority-vote ground truth for these categories. Additionally, "Each clip was labeled by minimally 1, maximally 3 annotators" (Section 3.3) means some clips have only a single annotation—this is not acknowledged as a limitation.

- **Benchmark evaluation lacks basic statistical rigor.** With 200 samples, no confidence intervals, error bars, or significance tests are provided for any result in Tables 3 or 4. The difference between the best and second-best model in Table 3 (GPT-4o at 76.72 wF1 vs. AffectGPT at 64.37 wF1 on 3-class sentiment with video+caption) could be driven by a handful of samples. Without error estimates, the reader cannot assess whether reported differences are meaningful. This is a straightforward omission—bootstrap confidence intervals would be trivial to compute and would dramatically improve the value of the benchmark section.

### Minor
- **The "Emotion Cue Grounding" task (Section 5.3) is an informal qualitative inspection, not a benchmark.** The paper states: "we manually inspected several randomly selected videos alongside the ground truth and each model's corresponding reasoning outputs." There is no systematic protocol, no metrics, no inter-rater reliability on the manual inspection, and no clear definition of what constitutes correct grounding. The paper calls this a "task" in Section 4.1, which oversells what was done. This would be better framed as a qualitative observation or a case study, not a third benchmark task.

### Trivial
None.

## Nice-to-Haves
- A systematic content analysis of the qualitative cue descriptions (e.g., categorizing cue types, their frequency, correlation with specific emotions) would leverage the most unique part of the resource more fully than the current informal summary.
- Reporting the number of clips with single vs. multiple annotators would help readers assess ground truth reliability.
- Demographic information about the signers in the clips (beyond "4 different signers") would contextualize generalizability.

## Removed Points
These points from the input review were removed after verification against the paper:
- *"Tension between the two claims about multimodality"* — The paper actually reconciles this: "unless the video modality clearly conveys the signers' emotion, it may introduce noise rather than improve predictions" (lines 279-280). This explains why video helps for sentiment but not always for fine-grained emotion.
- *"No train/test split described"* — For zero-shot evaluation (which this is), using the full dataset for testing is standard; no split is needed.
- *"Positive bias is confounded by concentrated positive emotions"* — This conflates emotion categories (joy/excited) with sentiment. The sentiment distribution has more negative (115) than positive (70) examples.
- *"Grammar issues in limitations section"* — Parser artifact, not an author error.
- *"Confusion matrices should be in main paper"* — Presentation preference, not a substantive weakness.

## Novel Insights
The key observation across the reviews that goes beyond the paper's own framing is that the paper's two claimed contributions (the dataset itself and the benchmark findings about model behavior) are in tension: the VADER-based selection, which was necessary to get any emotional signal into a 200-clip dataset, systematically creates the very conditions that produce the "models rely on text" finding. A larger dataset that did not need such aggressive filtering would provide a cleaner test of whether multimodal models genuinely fail at ASL emotion recognition. The most valuable and least confounded part of the contribution is the qualitative cue descriptions, which are not undermined by any of the methodological concerns.

## Suggestions
1. **Reframe the contribution** around the qualitative emotion cue descriptions and the annotation protocol—this is the genuinely novel, unconfounded contribution.
2. **Add bootstrap confidence intervals** to all benchmark results (Tables 3 and 4).
3. **Acknowledge and analyze the VADER selection bias** explicitly rather than treating it as a straightforward preprocessing step. Frame the dataset as "ASL videos where text captions carry strong emotional valence" and discuss how this differs from the full distribution of ASL communication.
4. **Either compute Fleiss' κ for EmoSign** for a valid comparison with MELD/IEMOCAP, or acknowledge the methodological difference in the comparison.
5. **Drop or substantially reframe the emotion cue grounding analysis**—present it as qualitative observations in the discussion rather than a third benchmark task.

## Score and Decision
**Round 1 Bracket:** After reading the paper and the calibration anchors, the plausible range was 4.0–5.5.

**Anchors consulted (all rounds):**
- *MDPE* (avg 2.50, Reject) — multimodal deception+emotion dataset paper. Much larger (104h vs 16min) but fuzzier problem framing, weaker annotation methodology, worse writing. EmoSign is clearly stronger on problem clarity and annotation quality.
- *One-shot ISLR* (avg 4.00, Reject) — sign language recognition method paper. Comparable social impact motivation, but limited technical novelty. EmoSign has a more clearly novel contribution (first dedicated ASL emotion dataset) but a smaller empirical footprint.
- *VRG-SLT* (avg 5.00, Reject) — sign language translation method paper with very mixed scores (3,8,3,6). EmoSign's contribution type (dataset) is cleaner but its empirical rigor is weaker.
- *MIntRec2.0* (avg 6.50, Accept) — large-scale multimodal intent benchmark (15K samples). EmoSign is much smaller and less rigorous; this anchor defines the ceiling EmoSign does not reach.

**Final Score:** 4.5

The paper's core contribution—a first-of-its-kind ASL emotion dataset annotated by native Deaf signers with rich qualitative cue descriptions—is real and addresses an important gap. However, the dataset's small size (200 clips, 4 signers) and the VADER-based selection procedure limit the conclusions that can be drawn from the benchmarks. The lack of confidence intervals, the low inter-annotator agreement on most emotion categories, and the informal treatment of the grounding analysis all weaken the empirical claims. The paper would be stronger by reframing around the qualitative annotations (which are genuinely novel and not undermined by sample size) and adding proper statistical treatment of the benchmark results. In its current form, the gap between the strength of the claims and the strength of the evidence is too wide for acceptance.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>