## Summary

EmoSign introduces a dataset of 200 ASL video clips annotated with sentiment ratings (7-point scale), intensity for 10 emotion categories, and open-ended descriptions of emotion cues—all provided by three Deaf native ASL signers with professional interpretation experience. The paper also presents benchmark evaluations of four multimodal LLMs (GPT-4o, AffectGPT, Qwen2.5-VL, MiniGPT4) across three conditions (caption-only, video-only, video+caption) for sentiment analysis, emotion classification, and emotion cue grounding. The core contributions are the annotation methodology and the qualitative documentation of how emotions manifest in signing.

## Strengths

- **Annotation design that reflects genuine domain expertise.** Hiring Deaf native ASL signers with interpretation experience is well-motivated by evidence (Lim et al., 2024) that hearing individuals frequently misinterpret signers' facial expressions. The three-layer annotation structure—sentiment, fine-grained emotion categories with intensity, and open-ended cue descriptions—goes beyond what prior sign-language emotion datasets provide.

- **Qualitative documentation of emotion cues in ASL (Section 3.4).** The paper distills concrete patterns from annotator descriptions: specific non-manual markers (furrowed brows, pursed lips, head thrusts), sign modifications (size, speed, repetition, finger-spelling for emphasis), and the role of context in disambiguating emotion. This provides a useful foundation for future model design and is grounded in native-signer perspectives rather than external guesses.

- **Ablation study design across three input conditions.** Evaluating caption-only, video-only, and video+caption conditions cleanly separates the contributions of each modality and allows structured analysis of whether models use visual information for emotion recognition in sign language.

## Weaknesses

### Fatal
None.

### Major

- **VADER-based pre-selection confounds the central claim about modality reliance.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances *based on VADER analysis of the text captions* (Section 3.1, line 115: "we selected the 100 most positive and 100 most negative utterances based on the VADER scores"). This guarantees by construction that the text captions carry strong emotional signal. When the benchmarks then show that models perform similarly or better with text captions than with video alone—and the paper concludes that "models fail to integrate visual cues" (Abstract) and "exhibit bias towards positive emotions" (Abstract)—the finding is substantially weakened because the data was curated to maximize the emotional content of the text. The paper does acknowledge in the Limitations (line 330) that VADER results differed from annotators, but this confound is structural and not resolved by a brief mention. A proper test of whether models fail to use visual cues would require decoupling visual and textual emotional signals, not artificially aligning them. This undermines the paper's headline claim.

- **The 200-sample/4-signer size and lack of statistical rigor limit the benchmark conclusions.** With 200 utterances from 4 signers, per-category accuracies in Table 4 are based on tiny denominators (e.g., surprise_neg: 25 clips, where a 14% vs. 0% accuracy swing reflects 1–3 samples). No confidence intervals, standard deviations, significance tests, or number of runs are reported across any of the quantitative benchmarks (Tables 3, 4). The paper does not describe how the data was partitioned for evaluation (Section 4.2 describes inference settings but never states whether all 200 samples were used as test, whether any were held out, or whether results are from single or multiple runs). With only 4 signers, signer-specific visual characteristics are confounded with emotion-related patterns. While the paper cites similarly sized datasets (Arodi et al., 2024; Krojer et al., 2024; Li et al., 2024b), those serve as diagnostic probes for specific phenomena rather than general-purpose benchmarks for establishing model capabilities—which is the role EmoSign claims for itself ("establishes a new benchmark," Abstract). These issues collectively mean the quantitative results cannot support broad conclusions about model behavior.

### Minor

- **Low inter-annotator agreement on several emotion categories compromises ground truth for those labels.** Krippendorff's alpha values for surprise_neg (0.119), disgust (0.166), frustration (0.330), sadness (0.333), anger (0.370), and fear (0.351) are very low (Table 2). When annotators cannot reliably agree on whether these emotions are present, the majority-vote ground truth (with only 3 annotators, some clips having 1–2 annotators due to skipping) is unreliable for these categories. The benchmark results for these specific emotions (Table 4) may partly reflect noise rather than model capability. The comparison to MELD (Fleiss' kappa = 0.43) and IEMOCAP (Fleiss' kappa = 0.48) uses a different agreement statistic without acknowledging the metric difference.

- **The "emotion cue grounding" task is labeled as a benchmark but evaluated only qualitatively.** Section 4.1 introduces emotion cue grounding as one of three benchmark tasks, but Section 5.3 evaluates it through manual inspection of "several randomly selected videos" (line 284) without specifying how many, what selection criteria were used, or any quantitative metric. This is exploratory analysis, not a benchmark evaluation, and should be labeled as such.

- **VADER-annotator disagreement is mentioned but never systematically analyzed.** The Limitations section notes that "VADER results differed from the annotators' results" (line 330), but the paper does not analyze this disagreement. A systematic comparison of clips where text sentiment and video-based sentiment diverge could have directly tested whether models use visual cues when text is uninformative or misleading—which would be the most probative evidence for the paper's central claim.

### Trivial

- No train/test split is explicitly described for the zero-shot evaluation (Section 4.2). Since models are evaluated zero-shot, the split should be stated explicitly rather than left implicit.

- Some per-class accuracy values in Table 4 (e.g., 0%, 14%, 17%) would benefit from noting the absolute counts given the small denominators.

## Nice-to-Haves

- **Signer-level breakdown.** With only 4 signers, a per-signer analysis of model accuracy would help determine whether apparent emotion recognition is confounded with signer identity.
- **Multi-label emotion classification evaluation.** The paper acknowledges this as missing (Section 6), but since multi-label annotations are a designed feature of the dataset, evaluating this would better leverage the dataset's richness.
- **Reframe the contribution around the annotation resource.** The strongest version of this paper would position EmoSign as a carefully annotated diagnostic probe for studying how emotion manifests in ASL, rather than as a comprehensive benchmark for model evaluation. The qualitative cue descriptions (Section 3.4) are genuinely novel and robust to the confounds that affect the quantitative benchmarks.

## Removed Points

- **Criticism that "first dataset" claim contradicts FePh.** The paper explicitly distinguishes EmoSign from FePh on three grounds (face-cropped vs. full video, hearing vs. Deaf annotators, binary vs. fine-grained labels; Section 2, lines 77–83). The claim is appropriately qualified.
- **Criticism about "extreme bimodality" of sentiment distribution being unacknowledged.** The paper states that this is expected from the VADER selection process (Section 3.4, line 146: "there are relatively few clips with neutral sentiment, but this is expected, since we selected clips with captions that had salient positive or negative emotions based on VADER").
- **Criticism about MELD/IEMOCAP metric comparison being "misleading."** The paper says "To contextualize" (line 140), which is a reasonable qualitative comparision of agreement levels even though the specific statistics differ. This does not rise to a substantive weakness.

## Novel Insights

The most genuinely useful observations come from the harsh critic's framing of *what analysis is missing.* The insight that VADER-annotator disagreement could be leveraged—comparing model behavior on clips where text and visual emotion signals diverge vs. align—is a concrete, actionable path that would either support or refute the paper's main claim and is already latent in the collected data. Additionally, the observation that the qualitative cue descriptions (Section 3.4) are the most robust and novel contribution, while the quantitative benchmarks are the most fragile, provides a useful reframing lens that the paper itself does not fully adopt.

## Suggestions

1. **Directly analyze the VADER-annotator disagreement.** Split the dataset into clips where VADER text sentiment aligns with annotator video-based sentiment versus clips where they diverge, then compare model performance across these subsets. This would directly test whether models use visual cues when text is misleading.
2. **Report uncertainty estimates.** Provide bootstrapped confidence intervals or standard deviations for the key metrics in Tables 3 and 4, and explicitly state how many runs were performed.
3. **Explicitly state the train/test split** (or confirm that all 200 samples were used as test in zero-shot evaluation).
4. **Clearly label the emotion cue grounding analysis as qualitative/exploratory** rather than a benchmark task.
5. **Reframe the central contribution** around the annotation methodology and qualitative findings rather than the benchmark numbers. The dataset is best positioned as a diagnostic probe, not a comprehensive benchmark.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>