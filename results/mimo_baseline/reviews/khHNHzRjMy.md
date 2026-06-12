## Summary
The paper introduces EmoSign, the first dataset containing sentiment and emotion labels for 200 ASL video clips, annotated by 3 Deaf native ASL signers with professional interpretation experience. The annotations include 7-point sentiment ratings, presence/intensity ratings for 10 emotion categories, and qualitative descriptions of emotion cues (e.g., facial expressions, signing speed). The authors benchmark four multimodal LLMs under caption-only, video-only, and video+caption conditions, finding that current models rely heavily on text captions and exhibit bias toward positive emotions.

## Strengths
- **Genuinely novel and important research gap**: Sign language emotion recognition is critically under-studied with real-world consequences in legal and medical settings. To my knowledge, this is indeed the first ASL dataset with fine-grained emotion and sentiment annotations, making the contribution original and well-motivated.
- **Thoughtful and community-centered methodology**: The authors spent months building trust with the D/deaf community, recruited Deaf native signers with professional interpretation experience (rather than hearing annotators, as in FePh), and designed a multi-layered annotation pipeline covering sentiment, emotion categories, and open-ended cue descriptions. This is methodologically rigorous.
- **Insightful qualitative analysis of emotion cues**: The annotator-provided descriptions of how emotions manifest in ASL (non-manual markers, modified signs, contextual cues) provide genuinely valuable qualitative data that goes beyond typical emotion datasets.
- **Well-designed ablation study**: The three-condition benchmark (caption-only, video-only, video+caption) across four models provides clear evidence that models rely on text shortcuts and struggle with visual-only emotion reasoning—a finding that has broader implications for multimodal model design.

## Weaknesses
### Fatal
None.

### Major
- **Very small dataset**: 200 utterances totaling 16 minutes of video is quite limited for a benchmark intended to drive a new research direction. Class imbalance is severe for some categories (e.g., anger at 25 samples, surprise_neg at 25 samples), which affects the reliability of per-class metrics. The comparisons to CableInspect-AD and similar small datasets are somewhat inapposite since those operate in different domains with different statistical properties.
- **Low inter-annotator agreement on several key emotion categories**: Krippendorff's alpha for surprise_neg (0.119), disgust (0.166), and frustration (0.330) is quite low, raising questions about the reliability of ground-truth labels for these categories. While the authors contextualize against MELD and IEMOCAP, the comparison uses different agreement metrics (Fleiss' kappa vs. Krippendorff's alpha), making direct comparison difficult.
- **No statistical significance testing or confidence intervals**: With only 200 samples and significant class imbalance, model performance differences may not be statistically significant. The benchmark tables report single-point metrics without uncertainty estimates, weakening the conclusions drawn from the experiments.

### Minor
- **VADER-based pre-filtering introduces potential bias**: Selecting the 100 most positive and 100 most negative utterances based on text sentiment may create a dataset where text-emotion alignment is over-represented, potentially inflating caption-only model performance and skewing benchmark conclusions.
- **Emotion cue grounding evaluation is only qualitative**: Manual inspection of "several randomly selected videos" is not a rigorous evaluation methodology. This task is conceptually valuable but lacks any quantitative evaluation protocol.
- **Single source dataset**: All videos come from ASLLRP, which has only 19 signers in laboratory settings, limiting diversity of signing styles and ecological validity.

### Trivial
- Figure 2 and its caption appear duplicated with slightly different textual descriptions.

## Nice-to-Haves
- Quantitative evaluation of the emotion cue grounding task, e.g., via temporal localization metrics or IoU-based spatial grounding measures.
- Multi-label emotion classification benchmarking, since the annotation data is already collected.
- Analysis of how the number of annotators (1 vs. 2 vs. 3) affects label quality and model benchmark results.

## Novel Insights
The paper reveals that multimodal LLMs exhibit a systematic text-shortcut problem in sign language emotion recognition: visual-only performance is dramatically worse than caption-only, yet video+caption fusion yields the largest gains, suggesting models can integrate visual information but fail to extract it independently. The qualitative analysis further shows that models reinterpret the same visual cues in opposite emotional directions depending on whether captions are available, providing concrete evidence that visual reasoning in these models is subordinated to linguistic context rather than independently grounded.

## Suggestions
- Expand the dataset size, even modestly (e.g., to 500+ samples), to improve statistical reliability and enable more robust cross-validation.
- Report confidence intervals via bootstrapping across benchmark results to support claims about model performance differences.
- Include a discussion of how VADER-based pre-filtering may affect benchmark conclusions, and consider releasing a companion set of randomly sampled (non-VADER-filtered) videos for comparison.

## Score and Decision
The paper makes a genuinely novel and important contribution by creating the first emotion-annotated ASL dataset with careful community-centered methodology. The research question is well-motivated and the benchmark findings are informative. However, the small dataset size (200 samples), low inter-annotator agreement on several emotion categories, and lack of statistical rigor in benchmarking limit the strength of the conclusions. This is a solid first contribution to an important area, but the scale and reliability concerns place it at the borderline.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>