## Summary

The paper introduces EmoSign, the first dataset of American Sign Language (ASL) videos annotated with sentiment labels (7-point scale), 10 emotion categories (intensity 0–3), and open-ended descriptions of emotion cues. Annotations were provided by three Deaf native ASL signers with professional interpretation experience. The authors benchmark four multimodal LLMs (GPT-4o, AffectGPT, Qwen2.5-VL, MiniGPT4) on sentiment analysis and emotion classification tasks, with ablation over input modalities (caption-only, video-only, video+caption). Results show that current models rely heavily on text captions, fail to integrate visual cues, and exhibit a positive-emotion bias.

## Strengths

- **Addresses an important and understudied problem.** Emotion recognition in sign language is a critical gap, with practical consequences in legal, medical, and everyday settings. The paper correctly identifies the unique challenge that facial expressions and hand movements serve both grammatical and emotional functions in sign languages.
- **High-quality annotation protocol.** Using Deaf native ASL signers with professional interpretation experience is a strong methodological choice, as hearing annotators often misinterpret signers’ facial expressions. The inclusion of open-ended descriptions of emotion cues provides rich qualitative information beyond simple labels.
- **Clear benchmark setup and ablation study.** The three-condition ablation (caption-only, video-only, video+caption) cleanly isolates the contribution of each modality. The benchmark results convincingly demonstrate that current MLLMs fail to leverage visual information for emotion recognition in sign language, and that they exhibit a positive/neutral bias.

## Weaknesses

### Fatal
None.

### Major
- **Very small dataset size (200 utterances, ~16 minutes).** While the authors argue that similar-sized datasets have proven valuable for benchmarking, emotion recognition is highly nuanced and 200 samples are insufficient to draw robust conclusions about model capabilities. The benchmark results are based on this small set, and the observed failure modes may not generalize. The dataset is too small to support training or fine-tuning, limiting its utility beyond zero-shot evaluation.
- **Selection bias from VADER filtering.** Videos were selected based on text caption sentiment (VADER scores), not on the emotional content of the signing itself. This introduces a confound: the dataset may reflect text-based emotional salience rather than natural ASL emotional expression. The authors acknowledge that VADER results often differed from annotators, but the selection process still biases the dataset toward utterances where text and emotion align.
- **Low inter-annotator agreement for several emotion categories.** Krippendorff’s alpha values for surprise_neg (0.119), disgust (0.166), frustration (0.330), and anger (0.370) are very low, indicating unreliable labels for these categories. The average alpha of 0.593 is moderate, but the low-agreement categories undermine the validity of the emotion classification benchmark, especially for fine-grained emotion prediction.
- **Benchmark models are not adapted to sign language.** The paper evaluates general-purpose MLLMs in a zero-shot setting. The finding that these models fail to recognize emotions from visual cues is expected and does not provide insight into whether specialized architectures (e.g., fine-tuned sign language models) could succeed. The absence of even a simple vision-only baseline trained on the dataset (e.g., a video classifier) weakens the claim that “current multimodal models fail to integrate visual cues.”

### Minor
- **Emotion cue grounding analysis is qualitative and based on manual inspection of a few examples.** This analysis is not systematic and does not provide quantitative grounding metrics (e.g., frame-level localization accuracy). The conclusions drawn from it are suggestive but not rigorous.
- **The paper claims to be the “first” dataset with emotion labels for ASL, but FePh (Alaghband et al., 2020) annotated facial expressions in sign language videos.** While the authors differentiate their work (full video vs. cropped face, hearing vs. Deaf annotators, binary vs. fine-grained labels), the claim of “first” should be more carefully qualified.

### Trivial
None.

## Nice-to-Haves

- Include a simple supervised baseline (e.g., a video classifier using I3D or a sign-language-specific model) trained on the dataset to provide a more meaningful lower bound for the benchmark.
- Provide a more detailed analysis of the open-ended emotion cue descriptions, e.g., by categorizing common cue types and their correlation with emotion labels.
- Release the dataset and code publicly to enable reproducibility and follow-up work.

## Novel Insights

The paper’s core insight—that current multimodal LLMs fail to integrate visual cues for emotion recognition in sign language and instead rely on text captions—is demonstrated in a new domain. The finding that models exhibit a positive/neutral bias, possibly due to RLHF training, is interesting but not deeply explored. The qualitative observation that the same visual cue can be interpreted oppositely depending on whether the text caption is provided (Figure 3) is a concrete illustration of the text-over-reliance problem. Beyond these, the paper does not offer a fundamentally new understanding of emotion recognition or multimodal learning.

## Suggestions

1. **Expand the dataset** to include more signers, scenarios, and a larger number of utterances (e.g., 500–1000) to improve statistical reliability and enable training.
2. **Use a more balanced selection method** that does not rely solely on text sentiment; consider sampling from a broader range of ASL content and having annotators pre-screen for emotional expressiveness.
3. **Fine-tune a sign-language-specific model** (e.g., LLaVA-SLT or a gloss-based model) on the dataset and compare its performance to the zero-shot MLLMs. This would provide a more informative baseline and test whether the failure is due to general MLLM limitations or lack of sign-language-specific training.
4. **Provide quantitative grounding evaluation** (e.g., using attention maps or human evaluation of model-generated cue descriptions) to support the qualitative grounding analysis.

## Score and Decision

The paper makes a valuable contribution by creating the first dedicated emotion-annotated ASL dataset and establishing initial benchmarks. However, the dataset is very small, the selection process introduces bias, and the benchmark experiments are limited to zero-shot evaluation of general models. The contribution is genuine but not strong enough for a high score. I recommend borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>