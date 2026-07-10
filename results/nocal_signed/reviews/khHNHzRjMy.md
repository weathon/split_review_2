Now let me write the final review.

## Summary

EmoSign introduces a dataset of 200 ASL video clips (~16 minutes) with sentiment, emotion intensity, and qualitative emotion cue annotations from three Deaf ASL signers, along with zero-shot benchmarks of four MLLMs. The paper targets an understudied problem — emotional expression in sign language — and provides valuable qualitative documentation of how emotions manifest through non-manual markers, modified kinematics, and narrative context.

## Strengths

- **Addresses a genuinely understudied problem.** Emotional expression in sign language receives far less attention than translation, and the paper correctly identifies the core challenge: facial expressions and hand movements serve dual grammatical and emotional functions (Section 1, lines 15–16). A dedicated resource for this problem is a positive step.
- **Deaf native signers as annotators.** This is the most important methodological decision in the paper and is correctly motivated (the paper critiques FePh for using hearing annotators). The qualitative cue descriptions (Section 3.4, lines 193–194) — documenting non-manual markers, sign modifications, and reliance on narrative context — are genuinely informative and would be difficult to obtain without native fluency.
- **Well-designed annotation pipeline.** The three-layer annotation process (7-point sentiment, 10-category emotion intensity, free-text cue descriptions) with confidence ratings, training sessions, and majority-vote consolidation is replicable and appropriate for the task.
- **Ablation design across input conditions.** Testing caption-only, video-only, and video+caption conditions cleanly reveals modality reliance patterns and is a useful analytic choice.
- **Transparent about limitations.** The paper acknowledges the VADER selection bias, lack of multi-signer scenarios, and small size (Section 6), which is commendable.

## Weaknesses

### Fatal
None.

### Major

1. **VADER-based selection creates a structural tension with the paper's central motivation.** The paper argues that emotional content in ASL is conveyed through visual cues not captured by text, motivating a *video* dataset. Yet the dataset was built by running VADER on text captions and selecting the 100 most positive and 100 most negative utterances (Section 3.1, lines 97–115). This biases the dataset toward utterances where *text already conveys the emotional valence*, squeezing out the very cases where visual cues might diverge from text — arguably the most interesting cases for the paper's thesis. The paper mentions this divergence qualitatively in Section 6 (line 330) but never quantifies it systematically. A direct analysis of how often VADER text sentiment disagrees with annotator video-level sentiment is the paper's most salient missing experiment.

2. **Inter-annotator agreement is too low for negative emotion categories to serve as reliable ground truth.** From Table 2 (lines 130–134): surprise_neg (α=0.119), disgust (α=0.166), frustration (α=0.330), sadness (α=0.333), fear (α=0.351), anger (α=0.370). Values below 0.20 are considered poor agreement; values around 0.33–0.37 are weak at best. The reported average of 0.593 pools high-agreement categories (sentiment 0.738, joy 0.699) with very low ones, masking this issue. Since the benchmark evaluations (Table 4) use these labels as ground truth, model performance on negative emotions is difficult to interpret: it is unclear whether models are failing to recognize these emotions, or whether the labels themselves are unreliable.

3. **The benchmarks do not establish the dataset's utility for improving models.** All evaluations are zero-shot on general-purpose MLLMs that are not trained on sign language video. The finding that these models perform poorly is predictable. A dataset paper's benchmarks should demonstrate the dataset's value — for instance, by including even a minimal fine-tuning experiment showing that the labels contain signal beyond what is available in text captions. Without this, the benchmarks primarily confirm task difficulty, which was already plausible from first principles.

4. **The dataset is small and homogeneous, limiting the generalizability of claims about model behavior.** 200 utterances, 4 signers, ~16 minutes, from a single source corpus (ASLLRP). The paper's conclusions about "bias towards positive emotions" and "failure to integrate visual cues" could be artifacts of which utterances VADER scored as extreme and which signers appeared in ASLLRP's recordings. While the size is acknowledged as a limitation, broad claims about model behavior are drawn from this sample without appropriate hedging.

### Minor

5. **The emotion cue grounding analysis (Section 5.3) is purely qualitative.** It manually inspects "several randomly selected videos" without specifying the count, uses no systematic metric, and lacks any inter-rater reliability for the evaluation. The paper defines this as a benchmark task in Section 4.1 but provides no quantitative results. This section should be reframed as exploratory analysis or replaced with a properly metric-based evaluation.

6. **MiniGPT4 shows anomalous results that are not discussed and the Table 3 caption contains a factual inaccuracy.** MiniGPT4 achieves 1.92 wAcc on 3-class sentiment in the caption-only condition — essentially random — and its video-only wAcc (34.68) exceeds its video+caption wAcc (21.65). Yet the caption under Table 3 (line 233) states "All models achieved highest weighted Accuracy and F1 scores with video + caption inputs," which is incorrect for this model. This exception should be discussed, and the caption should be corrected.

### Trivial
None.

## Nice-to-Haves

- Quantify the divergence between VADER text sentiment and annotator video-level sentiment. This single analysis would directly support (or refine) the paper's motivating thesis.
- Include a minimal fine-tuning experiment (e.g., fine-tuning an open-source video classifier or small MLLM on the 200 clips with held-out evaluation) to demonstrate that the visual emotion labels contain signal.
- Analyze inter-annotator disagreement patterns as a feature rather than noise — the low agreement on negative emotions may reflect genuine ambiguity in ASL emotional expression, which is itself interesting.
- Add per-signer performance analysis to check whether results are driven by signer-specific characteristics.
- Clarify what the confidence rating (collected after the sentiment and emotion tasks but before the free-text cue descriptions) is intended to capture.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Overstatement of novelty claim (abstract):** The Harsh Critic argued the abstract overstates novelty given FePh exists. The paper explicitly distinguishes itself from FePh in Section 2 (face-only crops, hearing annotators, binary labels), and the abstract's phrasing "first sign video dataset containing sentiment and emotion labels" is accurate since FePh does not include sentiment labels or intensity ratings. Removed as the paper already addresses this.
- **Confidence rating timing question:** The reviewer asked whether the confidence rating captured confidence in both tasks or just one. This is a minor clarification question, not a weakness. Moved to Nice-to-Haves.
- **MELD/IEMOCAP metric comparison:** The reviewer noted that comparing Krippendorff's alpha to Fleiss' kappa is methodologically imprecise. While technically correct, the paper uses this only for rough contextualization and it does not harm any core argument.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Quantify VADER-annotator divergence systematically. This is the single most informative analysis the paper could add.
- Include a fine-tuning experiment (even a lightweight one) to demonstrate that the dataset's labels capture signal not redundant with text.
- For the grounding analysis, either define a proper evaluation with quantitative metrics or clearly label it as exploratory qualitative analysis.
- Correct the Table 3 caption to accurately reflect MiniGPT4's results.
- Discuss the low inter-annotator agreement for negative emotions more thoroughly and consider whether those benchmark results should be caveated or separated.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>