Now let me write the final consolidated review.

## Summary

EmoSign introduces the first emotion-labeled ASL video dataset (200 clips, ~16 min, 4 signers, sourced from ASLLRP), annotated by 3 Deaf native signers with professional interpretation experience. The annotation covers 7-point sentiment, 10 emotion categories with intensity, and open-ended cue descriptions. The paper also provides baseline benchmarks with 4 multimodal LLMs under caption-only, video-only, and video+caption conditions, finding that models fail to integrate visual cues and exhibit positive bias.

## Strengths

- **Addresses a genuinely understudied problem** — the intersection of emotion recognition and sign language is nearly absent from the literature. The paper correctly identifies that facial expressions in ASL serve dual grammatical and emotional functions, creating a modeling challenge distinct from conventional multimodal emotion recognition.

- **Annotation by Deaf native ASL signers with professional interpretation experience** — This is the paper's most important methodological choice and a clear improvement over prior work (FePh), which used hearing annotators. The distinction between grammatical and emotional facial expressions requires native fluency.

- **Multi-faceted annotation design** — The three-layer annotation (7-point sentiment, 10 emotion categories with intensity, open-ended cue descriptions) provides richer signal than existing sign language datasets.

- **Ablation design in benchmarks** — Testing models under caption-only, video-only, and video+caption conditions is well-motivated and directly addresses whether models actually use visual information. The finding that video+caption often underperforms caption-only for emotion classification (Table 4) is a meaningful empirical observation.

- **Qualitative documentation of emotion cues from native ASL signers** (Section 3.4) — documenting non-manual markers, sign modification, and the role of context is a genuine contribution that comes directly from the paper's methodological choices.

## Weaknesses

### Fatal
None.

### Major

- **Dataset too small and claims disproportionate to scale.** 200 utterances (~16 min) from 4 signers drawn from a single source dataset (ASLLRP). The paper calls itself "the first comprehensive dataset" (line 17) and claims to "establish a new benchmark" (abstract), but these claims are overstated for this scale. The paper acknowledges the size limitation ("we start with 200 utterances," line 87) and cites other small datasets as precedent, but those are not introducing a new task domain requiring generalization across diverse signing styles and recording conditions. With only 4 signers, the benchmark cannot distinguish whether a model fails at emotion recognition in ASL or simply does not generalize beyond those 4 individuals' signing styles. The benchmark results (Tables 3, 4) report no confidence intervals or variance measures, so score stability cannot be assessed — a critical gap when per-class samples can be as small as 25.

- **Inter-annotator agreement is poor for most emotion categories, and the comparison to MELD/IEMOCAP is invalid.** Table 2 shows Krippendorff's alpha below 0.4 for 7 of 10 emotion categories (surprise_neg: 0.119, disgust: 0.166, frustration: 0.330, sadness: 0.333, anger: 0.370, fear: 0.351, surprise_pos: 0.381). An alpha of 0.119 for surprise_negative is essentially chance-level agreement. The paper then claims MELD (Fleiss' kappa = 0.43) and IEMOCAP (Fleiss' kappa = 0.48) have "lower inter-annotator agreement compared to ours" (line 140), but this compares Krippendorff's alpha to Fleiss' kappa — different statistics with different scales and interpretations — making the comparison invalid and potentially misleading. The paper does not discuss whether the majority-vote consensus labels are reliable for the 7 categories below 0.4.

- **Missing data not accounted for.** The single-expression set (140 clips) and multi-expression set (37 clips, filtered to exclude combinations appearing in only one sample) sum to 177 clips, not 200 (Section 4.1, line 207). The remaining 23 clips are never explained — whether they were multi-expression clips with rare combinations, clips where annotators disagreed on single vs. multiple emotions, or skipped clips. The benchmark results in Tables 3 and 4 are computed on subsets whose selection criteria and representativeness relative to the full dataset are unclear.

### Minor

- **VADER selection bias not quantified.** The dataset uses VADER text sentiment to select clips (top 100 positive and 100 negative by caption text). The paper acknowledges VADER results "differed from the annotators' results" (Section 6, line 330) but never quantifies this discrepancy. Without knowing how often text sentiment and perceived visual emotion diverge, readers cannot assess whether the benchmark tests visual emotion recognition or primarily reflects text-based signal. The selection may bias the dataset toward emotions easily expressed in English, potentially missing ASL-specific emotional expressions.

- **No statistical uncertainty on benchmark results.** No confidence intervals, standard deviations, or significance tests are reported for any benchmark result. With 200 clips and per-class samples as small as 25, reported scores could be unstable across different random seeds or data splits — the models were seeded but run without multiple trials.

- **Emotion cue grounding analysis is purely qualitative with no systematic protocol.** The paper states "we manually inspected several randomly selected videos" (Section 5.3, line 284) without specifying how many, who performed the inspection, whether it was blinded, or the sampling procedure. The conclusions drawn ("models attempt to construct explanations consistent with text sentiment") are interesting but cannot be substantiated without a systematic methodology.

- **The RLHF-based explanation for positive bias is speculative.** The paper suggests positive bias arises because "foundational models are pre-trained with an emphasis on being helpful, harmless and honest" (Section 5.1, line 231). No evidence connects RLHF training to emotion label bias, and the paper itself notes "more research is required," making this an unsupported hypothesis rather than a finding.

- **Table 1 conflates annotator count with signer count.** The "Signers" column for EmoSign lists "3" (the number of annotators), but the text states the dataset includes "4 different signers" in the videos (line 144). This is ambiguous.

- **Model selection is questionable for a benchmark.** MiniGPT4 (not a video-native model, limited temporal reasoning) and AffectGPT (which consistently defaults to "neutral") are included alongside GPT-4o and Qwen2.5. Including models known to be weak for video inflates apparent benchmark difficulty without providing informative baselines.

### Trivial
None.

## Nice-to-Haves

- Quantify the VADER-annotator disagreement and specifically analyze cases where text and visual emotion diverge — those are the cases that actually test whether models use visual information.
- Report per-signer clip distribution and check whether results are driven by one signer's style.
- Expand the dataset to at least 500–1,000 clips from more signers and more source datasets before positioning it as a benchmark.
- Develop the qualitative themes (Section 3.4) into a structured taxonomy of emotion cues with examples from specific clips, organized by emotion category.
- Report the full co-occurrence matrix for all emotion category pairs.

## Removed Points

- **"VADER circularity" framing** — REMOVED: The harsh critic claimed the ground truth labels may have been "influenced by the same text used for selection." This is inaccurate: annotators labeled based on watching videos, not from text. VADER was used only for selection, not labeling. The valid concern about selection bias is retained in Minor weaknesses.
- **No per-signer analysis** — REMOVED as a standalone weakness (merged into Nice-to-Haves); per-signer breakdown is not standard for all dataset papers.
- **Missing per-class F1 scores** — REMOVED: total weighted accuracy and F1 are reported per standard practice; per-class accuracy is shown in Table 4.
- **Formatting/style nitpicks** — REMOVED per instructions (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the paper as a pilot study / annotation methodology contribution rather than a comprehensive benchmark, and calibrate all claims in the abstract and introduction to the 200-clip, 4-signer scale.
- Quantify the VADER-annotator disagreement, particularly analyzing cases where text sentiment and visual emotion diverge.
- Report Krippendorff's alpha alongside percentage agreement or another more interpretable metric to give readers a fuller picture of label reliability.
- Account for all 200 clips — explain the disposition of the 23 clips not in the single-expression or multi-expression subsets.

## Score and Decision

The paper identifies a genuine gap and takes a principled approach to annotation — the use of Deaf native ASL signers and the qualitative documentation of emotion cues are real contributions. However, the dataset is too small (200 clips, 4 signers, single source) to support the "comprehensive benchmark" framing. Inter-annotator agreement is below acceptable thresholds for 7 of 10 emotion categories, and the comparison to MELD/IEMOCAP mixes incompatible metrics. The benchmark evaluation lacks statistical rigor, and 23 clips are unaccounted for. The core contributions (annotation protocol, qualitative taxonomy) are salvageable but require substantial reframing and several evidentiary gaps to be addressed before the paper meets the acceptance bar.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>