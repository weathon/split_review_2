## Summary

EmoSign introduces a multimodal dataset of 200 American Sign Language (ASL) video clips annotated for sentiment and emotion by Deaf native signers, including open-ended descriptions of emotion cues. The paper provides baseline benchmarks on four multimodal LLMs across three conditions (caption-only, video-only, video+caption) for sentiment analysis, emotion classification, and a qualitative emotion cue grounding analysis. Results show that current models rely heavily on text captions and exhibit positive/neutral biases, failing to integrate visual emotional cues from sign language.

## Strengths

- **Addresses an important, understudied gap**: Emotion recognition in sign language is critically under-researched despite real-world consequences in legal and medical settings. The paper clearly motivates why sign language emotion is distinct from spoken-language emotion recognition.
- **Careful annotation protocol with Deaf native signers**: Annotations by three Deaf ASL signers with professional interpretation experience, plus pilot testing with the Deaf community, ensures cultural and linguistic validity. The inclusion of open-ended emotion cue descriptions adds valuable qualitative depth beyond typical categorical labels.
- **Systematic multimodal ablation design**: Evaluating four models under three modality conditions (video-only, caption-only, video+caption) cleanly isolates how models use each modality, revealing that text dominates and visual cues are poorly integrated.
- **Clear presentation of limitations and bias analysis**: The paper transparently discusses model biases (positive bias, neutral default), selection biases from VADER, and the difficulty of grounding, showing awareness of the dataset's limitations.

## Weaknesses

### Fatal

None.

### Major

1.  **Very small dataset size**: 200 utterances totaling ~16 minutes is insufficient to serve as a reliable benchmark for emotion recognition. The small sample limits statistical power, makes results sensitive to sampling, and precludes meaningful per-class analysis for emotion categories with few samples. While the paper argues that similar-sized datasets have proven valuable (citing Arodi et al., Krojer et al., Li et al.), those are for different tasks (anomaly detection, compositional reasoning) where smaller N is more typical; for emotion recognition with 10 fine-grained categories, 200 clips is notably small.
2.  **Selection bias from VADER text filtering**: The dataset was constructed by selecting the top 100 positive and 100 negative utterances based on VADER text sentiment analysis of captions. This procedure introduces a strong textual bias, meaning the dataset is not representative of natural emotional expression in ASL independent of text. The resulting strong correlation between text and emotion labels partly explains why caption-only models perform similarly to video+caption models, and limits the dataset's value for studying visual-only emotion recognition.
3.  **Low inter-annotator agreement on several emotion categories**: Krippendorff's alpha for surprise_neg (0.119), disgust (0.166), frustration (0.330), sadness (0.333), and anger (0.370) indicate poor reliability. The paper compares to MELD and IEMOCAP but those use different metrics (Fleiss' kappa) and have much larger sample sizes. The low agreement undermines the quality of ground truth for these categories and raises questions about the validity of benchmark evaluations on them.
4.  **Benchmark evaluation is shallow**: The emotion cue grounding analysis is purely qualitative with a single example shown. No quantitative metrics for grounding (e.g., attention alignment, spatial/temporal IoU) are provided. The single-label emotion classification task discards the multi-label structure present in the annotations. The small dataset also prevents meaningful train/validation/test splits for fine-tuning experiments, so all evaluations are zero-shot on general-purpose models.

### Minor

1.  **Limited signer and source diversity**: The dataset includes only 4 signers from a single corpus (ASLLRP), which features mostly news/educational content. This limits variation in signing styles, demographics, and emotional contexts.
2.  **No fine-tuned or sign-language-specific baselines**: The paper does not evaluate models fine-tuned on sign language (e.g., LLaVA-SLT, SignLLM) or simple feature-based methods (e.g., facial landmark classifiers), which would better contextualize the MLLM zero-shot results.
3.  **No multi-label emotion classification benchmark**: The annotations include intensity ratings for all 10 emotions, but only single-label classification is benchmarked, missing the opportunity to evaluate a more realistic and challenging task.

### Trivial

None.

## Nice-to-Haves

- Expand the dataset significantly (e.g., to 1000+ utterances) to improve statistical reliability and enable model fine-tuning with proper train/validation/test splits.
- Include quantitative grounding metrics, such as attention map alignment with annotator-described cues or frame-level relevance scores.
- Provide baselines from models fine-tuned on sign language data or simple visual feature extractors (e.g., facial action units, motion features) to better understand the difficulty of the visual task.
- Analyze inter-annotator disagreement patterns to identify which emotion cues are ambiguous and how they relate to grammatical vs. affective functions.

## Novel Insights

The paper's core insight is that multimodal LLMs, when applied to sign language emotion recognition, exhibit a strong textual bias that overwhelms visual information—even though visual cues (facial expressions, sign modifications, body movements) are the primary carriers of emotion in sign language. This is not merely a replication of known biases in MLLMs but reveals a deeper challenge: in sign language, visual signals serve dual grammatical and emotional functions, so models that treat all facial expressions as emotional will fail. The qualitative analysis shows models confabulate visual evidence to match text sentiment (e.g., interpreting the same facial expression as "frustration" with a negative caption and "excitement" with a positive caption). This suggests that disentangling syntactic from affective visual cues is a fundamental modeling problem unique to sign language, with potential implications for understanding MLLM reliance on linguistic shortcuts more broadly.

## Suggestions

1.  Significantly increase the dataset size, either by annotating more clips from ASLLRP or by incorporating other corpora with native signer annotations, to enable reliable model evaluation and fine-tuning.
2.  Provide a systematic analysis of how VADER text selection affects the distribution of visual emotion cues, and consider augmenting with clips where text sentiment and visual emotion diverge.
3.  Report benchmark results with confidence intervals (e.g., bootstrapped) to reflect the uncertainty from the small sample size.
4.  Include a multi-label emotion classification benchmark (with appropriate metrics like micro/macro F1) to fully utilize the annotation richness.
5.  Perform controlled experiments on emotion cue grounding, e.g., by asking models to highlight relevant frames or regions and measuring overlap with annotator descriptions.

## Score and Decision

Score: 4 (borderline reject). The paper identifies a meaningful gap and the annotation protocol is rigorous, but the dataset is too small and textually biased to serve as a reliable benchmark. The conclusions about model limitations are consistent with known MLLM biases and do not provide strong new insights beyond what the dataset's small scale can support. The contribution is promising but insufficient for acceptance at a top venue in its current form.

MY FINAL SCORE: 4
MY FINAL DECISION: Reject