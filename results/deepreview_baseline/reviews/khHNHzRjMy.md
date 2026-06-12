## Summary

This paper introduces EmoSign, the first dataset specifically designed for studying emotional expression in American Sign Language (ASL). It contains 200 ASL video clips annotated by three Deaf native signers with sentiment ratings, intensity scores for 10 emotion categories, and open-ended descriptions of emotion cues. The authors benchmark four multimodal LLMs on sentiment analysis, emotion classification, and emotion cue grounding tasks, finding that these models struggle to integrate visual information and rely heavily on text captions, while exhibiting a positive bias. The dataset addresses a critical gap in sign language research and establishes baseline performance for emotion recognition in ASL.

## Strengths

- **Addresses an important, underexplored problem**: Emotional expression in sign language is poorly understood and has practical consequences in legal and medical settings. This paper directly targets that gap with a dedicated dataset.
- **High-quality annotations from Deaf native signers**: The use of three professional Deaf ASL signers for annotation is a strong methodological choice, as hearing annotators may misinterpret grammatical facial expressions as emotional ones. The inclusion of qualitative cue descriptions adds unique value beyond simple labels.
- **Benchmarking reveals meaningful insights**: Through systematic ablation (caption-only, video-only, video+caption), the paper convincingly shows that current multimodal LLMs fail to leverage visual cues for emotion recognition in ASL and default to text-based reasoning. This finding motivates future research on better visual encoders and architectures that prevent text dominance.
- **Well-structured dataset construction**: The annotation pipeline is carefully designed, with training sessions, pilot tests, and the option to skip content. The post-processing using majority vote and tie-breaking is appropriate.

## Weaknesses

### Major

- **Very small dataset size (200 clips, ~16 minutes) severely limits utility as a benchmark**. With 10 emotion categories plus 7 sentiment levels, the per-class sample counts are tiny. Many emotion categories appear in only 25–65 clips, making statistical evaluation unreliable (e.g., per-class accuracy in Table 4 often based on single-digit samples). While the authors cite examples of small high-quality datasets, those are typically for controlled tasks (anomaly detection) where the small size is acceptable; for multi-class emotion recognition with high class imbalance, 200 clips is insufficient to draw robust conclusions about model capabilities or to serve as a reliable benchmark for the community.
- **VADER-based pre-selection introduces selection bias and weakens the dataset’s naturalistic value**. The dataset was constructed by taking the top-100 most positive and top-100 most negative utterances based on text caption sentiment, explicitly discarding neutral ones and not sampling representative proportions. This creates an artificial distribution that does not reflect real-world ASL communication. The paper acknowledges this limitation but does not adequately address how it undermines claims about general emotional expression in ASL.
- **Inter-annotator agreement is moderate to low on several key categories**. Krippendorff’s alpha for surprise_negative (0.119), disgust (0.166), frustration (0.330), sadness (0.333), anger (0.370), and fear (0.351) are all below 0.4, indicating problematic reliability for these fundamental emotions. The dataset's ground truth labels are therefore suspect for these categories, which limits the validity of benchmark evaluations on them.
- **Benchmark experiments are exclusively zero-shot; no sign-language-specific models or fine-tuning are tested**. The paper claims to establish "baseline model performance" but only evaluates generic multimodal LLMs without any adaptation to sign language. It is well-known that general-purpose models perform poorly on specialized visual domains. A more informative baseline would have included fine-tuning on sign language data or using sign-language-specific visual encoders. The claim "first to establish benchmarks and baseline metrics for emotion recognition in ASL" is overstated given these constraints.

### Minor

- **Emotion cue grounding analysis is purely qualitative on a handful of examples**. The manual inspection approach provides anecdotal illustration but no systematic evaluation metric or quantitative result. This limits the grounding analysis to interesting observation rather than rigorous benchmarking.
- **The paper does not analyze the qualitative cue descriptions from annotators beyond a brief summary**. Given that the collection of these descriptions is listed as a core contribution, more structured analysis (e.g., taxonomy of cue types, frequency analysis) would strengthen the paper.

### Trivial

- None.

## Nice-to-Haves

- Releasing the full annotation interface and training materials would enable reproducible dataset expansion by other researchers.
- Including optical flow or facial landmark features as additional modality in benchmarks could provide insight into what visual information models fail to use.
- Fine-tuning one of the benchmarked models on EmoSign or a related sign language dataset would strengthen the conclusions about the role of visual information.

## Novel Insights

Beyond the paper's own contributions, the key insight is that current multimodal LLMs exhibit a strong text-dominance even when the visual modality carries critical emotional information. The fact that GPT-4o can visually identify specific facial expressions (e.g., furrowed brows, pursed lips) but interprets those cues opposite ways depending on whether the text caption is available demonstrates that these models engage in post-hoc rationalization rather than genuine multimodal integration. This finding aligns with prior work on language shortcuts in vision-language models and highlights the need for architectures that force visual grounding, with implications beyond sign language to any domain where visual and textual modalities may convey conflicting affective signals.

## Suggestions

- Address the small dataset size by either (a) substantially expanding the dataset before publication, or (b) reframing the contribution as a pilot/exploratory study rather than a definitive benchmark. If keeping the current size, include confidence intervals for all benchmark metrics and clearly state the statistical limitations.
- Recompute benchmarks after removing emotion categories with very low inter-annotator agreement (e.g., surprise_negative, disgust) or analyze sensitivity of results to label noise.
- Add at least one fine-tuning baseline using a sign-language-aware model (e.g., a model pre-trained on SLT data) to provide a more meaningful lower bound on achievable performance.

## Score and Decision

The paper tackles an important and genuinely underexplored problem with a well-conceived annotation methodology. However, the very small dataset size, moderate-to-low inter-annotator agreement on several emotion categories, and the exclusive reliance on zero-shot evaluation of generic models significantly limit the contribution's impact and reliability as a benchmark. The work is better suited as a focused research paper that might inspire larger-scale data collection, but as presented, it does not provide a sufficiently robust resource for the community.

Score: 4 (borderline reject)

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>