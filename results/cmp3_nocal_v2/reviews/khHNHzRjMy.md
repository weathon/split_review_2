## Summary

EmoSign introduces the first dedicated ASL video dataset with sentiment and emotion annotations (200 clips, ~16 minutes), annotated by three Deaf native signers who also provided open-ended descriptions of emotion cues. The paper documents how emotions manifest through non-manual markers and sign modifications in ASL, and reports zero-shot benchmarks of four multimodal LLMs across sentiment analysis, emotion classification, and a qualitative grounding analysis.

## Strengths

- **Addresses a genuine and underserved gap.** The paper correctly identifies that existing ASL datasets focus on translation, not affect, and that ASL's conflation of grammatical and emotional facial expressions creates a distinct modeling challenge. This motivation is well-articulated and timely.

- **Annotation design shows appropriate domain sensitivity.** Recruiting Deaf native ASL signers with professional interpretation experience (rather than hearing crowdworkers) is the right methodological choice, and the paper documents the community engagement process (months of interviews, attending events, collaborating with Deaf universities). The multi-layered scheme (sentiment, 10 emotion categories with intensity, open-ended cue descriptions) is richer than typical binary or categorical schemes.

- **Qualitative findings about emotion cues in ASL are genuinely informative.** Section 3.4's discussion of non-manual markers (furrowed brows, head thrusts, mouth movements), sign modification (size, speed, repetition), and context dependence provides concrete documentation that is useful to both computational and linguistic audiences — and is the most novel part of the paper.

- **Ablation experiment design is well-conceived.** The caption-only, video-only, and video+caption conditions cleanly test whether models use visual information or lean on linguistic shortcuts. The finding that video+caption often does not beat caption-only for emotion classification is meaningful even if not surprising.

## Weaknesses

### Fatal

None.

### Major

- **VADER-based selection confounds the central benchmark finding.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances based on VADER sentiment analysis of the *text captions*. This means the dataset is not a naturalistic sample of ASL emotion — it is a sample whose captions were cherry-picked for emotional intensity. The paper's headline finding — that models rely on text captions — is partially an artifact of this construction: a caption-only baseline performing competitively with video+caption is less surprising when the captions were selected to be maximally emotionally salient. The paper acknowledges one VADER issue ("VADER results differed from the annotators' results") but does not grapple with how the selection method confounds the benchmark story. This weakens the paper's main empirical claim about model behavior.

- **Inter-annotator agreement for negative emotions is below conventional thresholds, and the comparison with MELD/IEMOCAP is misleading.** Krippendorff's alpha values for most negative emotion categories fall well below the recommended ≥0.667 threshold (surprise_negative: 0.119, disgust: 0.166, sadness: 0.333, fear: 0.351, anger: 0.370). The paper states that "existing widely-used emotion recognition datasets had lower inter-annotator agreement compared to ours: MELD (Fleiss' kappa = 0.43), IEMOCAP (Fleiss' kappa = 0.48)" — but Krippendorff's alpha and Fleiss' kappa are different statistics with different definitions and scales, making the direct comparison unsound. The low agreement on negative emotions means the ground-truth labels for these categories are statistically unreliable, which undermines the evaluation benchmark for those classes.

- **Benchmark conclusions are overclaimed relative to the evaluation setup.** All four models are evaluated zero-shot — none are fine-tuned on the dataset or any ASL-specific data. The paper concludes that "current multimodal models fail to integrate visual cues" and that there is a "significant performance gap between ground-truth labels and MLLM predictions." But zero-shot performance of general-purpose MLLMs on a specialized, low-resource task is expected to be poor. These results establish that off-the-shelf models have not been trained for this task, not that multimodal models have a fundamental limitation in integrating visual cues. The paper's own suggestion that "future work could investigate fine-tuning" undercuts the strength of the conclusions drawn from the zero-shot evaluation.

- **Dataset scale fundamentally limits what the benchmarks can demonstrate.** With 200 utterances from 3–4 signers (~16 minutes), 11 emotion classes, and per-class counts as low as 5 (neutral) and 25 (anger, surprise_negative), the evaluation rests on very small samples. No confidence intervals or variance estimates are reported anywhere, so it is impossible to know whether reported differences between models or conditions are meaningful. The per-class accuracies in Table 4 swing widely — GPT-4o caption-only gets 87% on happiness but 0% on neutral, 14% on surprise_negative — which likely reflects data sparsity as much as model capability. A dataset paper whose dataset can only support zero-shot evaluation on such small per-class counts should be more circumspect about its benchmark conclusions.

### Minor

- **Signer count inconsistency.** The paper body says "4 different signers" (line 144) while Table 1 reports "3 signers." This should be reconciled.

- **The Krippendorff's alpha / Fleiss' kappa comparison is methodologically unsound.** Raised under Major but worth noting separately: comparing two different agreement statistics without justification is misleading.

- **Emotion cue grounding task has no quantitative metric.** Section 5.3 evaluates grounding purely qualitatively ("manually inspected several randomly selected videos"). The grounding task is listed as a benchmark task on par with the classification tasks but has no quantitative evaluation.

- **No confidence intervals on any benchmark result.** With per-class counts as low as 5, reporting point estimates without error bars makes it difficult to assess whether observed differences are meaningful.

### Trivial

None.

## Nice-to-Haves

- A simple supervised baseline (e.g., video classifier using I3D or facial landmarks) trained on this data would provide a meaningful lower bound for the zero-shot results.
- Human non-signer performance on the same tasks (watching videos without captions) would disentangle whether the models' poor visual performance reflects general opacity of ASL emotion expression or a specific model limitation.
- Masking facial regions in the video as an additional ablation would directly test the claim that models fail to use visual cues.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Reviewer claimed GPT-4o gets "0% on anger, fear" in caption-only.** The actual values from Table 4 are anger=33%, fear=29%. Only neutral=0%. The specific numbers are factually wrong; the broader point about highly variable per-class accuracies from small samples is retained in the Major section above.

2. **Reviewer stated "I cannot verify these citations" (Arodi et al., Krojer et al., Li et al.) when questioning the paper's claim about similar-sized datasets.** Removed per policy: cited references are assumed to exist; this doubt reflects reviewer knowledge gaps, not author errors.

3. **Suggestion that the paper "would be more credible as a short paper or workshop contribution."** This is an opinion about venue suitability, not a weakness of the paper's technical content.

4. **Section-by-section note about the abstract claiming "first" — suggesting the claim should be qualified more carefully regarding FePh.** This is overly pedantic; the paper clearly distinguishes its contribution from FePh along multiple dimensions (full video vs. cropped faces, Deaf vs. hearing annotators, fine-grained vs. binary labels). The "first" claim is defensible as stated.

## Novel Insights

The harsh critic's most penetrating observation is that the VADER-based selection strategy creates a confound that the paper does not adequately address: because the captions were deliberately chosen to be the most emotionally extreme in the source corpus, the finding that models rely on text is partly an artifact of dataset construction. The paper treats this as a minor limitation but it cuts to the heart of the benchmark's main claim. A second novel observation is that the low inter-annotator agreement for negative emotions (surprise_negative α=0.119, disgust α=0.166) may not be merely a measurement issue — it could reflect a genuine property of ASL where negative emotions are more ambiguously expressed or harder to disambiguate, which would itself be an interesting finding that the paper should discuss rather than gloss over.

## Suggestions

1. **Address the VADER confound directly.** Acknowledge that the caption-based selection strategy creates a circularity in the benchmark's main finding about text reliance. Consider re-running the key analysis on a random (non-VADER-filtered) subset if feasible, or at minimum discuss how this confound limits the conclusions that can be drawn.

2. **Reconsider the IAA framing.** Either report only Krippendorff's alpha and discuss the low values for negative emotions candidly, or provide a justified comparison instead of the current Krippendorff's-alpha-to-Fleiss'-kappa comparison. The low agreement for negative emotions should be discussed as a limitation of the ground truth, not minimized.

3. **Temper the benchmark claims.** The paper should clearly state that all evaluations are zero-shot and that the findings reflect the limitations of current off-the-shelf MLLMs, not a fundamental incapacity of multimodal models for this task.

4. **Resolve the 3 vs. 4 signer inconsistency** in the final version.

5. **Add confidence intervals or bootstrap estimates** to all benchmark results, given the small per-class counts.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>