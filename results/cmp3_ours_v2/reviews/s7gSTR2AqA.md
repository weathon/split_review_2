## Summary

This paper investigates whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB)-efficient semantic categorization, using color naming as the primary testbed. The authors evaluate 39 LLMs on English color naming, then simulate cultural transmission via Iterated In-Context Language Learning (IICLL) — adapting an iterated learning paradigm with pseudo-words to elicit models' inductive biases. They find that LLMs restructure initially random naming systems toward greater IB-efficiency over generations, with Gemini 2.0 best recapitulating the full range of human-like tradeoffs, while other frontier models converge to lower-complexity solutions. A preliminary Shepard-circles experiment suggests potential domain generality.

## Strengths

1. **Theoretically grounded framing.** The paper anchors the investigation in the Information Bottleneck principle (Zaslavsky et al., 2018) and iterated learning theory (Griffiths & Kalish, 2007), providing precise quantitative predictions (the IB bound) to test against, rather than relying on purely qualitative assessment. The connection between IB-efficiency and semantic systems is well-motivated in Section 2.2.

2. **Comprehensive model coverage.** Testing 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2) with variation in size, instruction-tuning, and modality is substantial. The inclusion of training checkpoints for Olmo (Appendix F) adds a developmental perspective that is rare in LLM evaluation papers.

3. **Careful experimental design to isolate inductive bias.** The IICLL paradigm (Section 4.2) uses pseudo-words and does not inform the model that stimuli are colors (only "features"). This goes beyond measuring whether models can parrot English naming patterns. The rotation analysis (Section 4.2, para 4) further checks that emergent structures are non-trivial.

4. **Direct comparison to human experimental data.** Replicating two specific human studies (Lindsey & Brown, 2014; Xu et al., 2013) and plotting LLM results alongside human data on the same axes (Figures 2–4) makes the comparison concrete and interpretable.

## Weaknesses

### Fatal

None.

### Major

1. **The IICLL method confounds inductive bias with in-context learning capability, weakening the central attribution claim.** The paper's headline conclusion is that LLMs "exhibit a human-like inductive bias toward IB-efficiency" and are "guided by the same IB-efficiency principle that underlies human languages." However, the IICLL task explicitly requires strong in-context learning: the paper notes that models must "integrate dozens of in-context training examples to generalize well" and that smaller models "struggle in IICLL to produce non-degenerate category systems" (Section 4.2, Appendix L). The key comparative result — that only Gemini 2.0 recapitulates the full range of IB tradeoffs while other models "converge to low-complexity solutions" — is partially attributed to Gemini having "strongest in-context capabilities." This creates a circularity: a model that lacks the ICL ability to learn from 84 in-context examples (k=14 condition) may still have an inductive bias toward IB-efficiency that the method cannot observe. The paper shows that *all* tested models restructure toward greater efficiency over generations (Figure 4), which partially mitigates this, but the causal attribution to a specific "IB-efficiency bias" — rather than general ICL capability interacting with training-data regularities — is not cleanly supported by the current design.

2. **The IB evaluation framework uses a human-derived perceptual model whose applicability to LLMs is uncertain.** The IB bound (Section 2.2) is computed using CIELAB perceptual space with Gaussian noise assumptions that model *human* color vision. The paper's own results show that all models "struggled to align with English naming when colors are presented in CIELAB" and that this "reveals a key difference between how LLMs represent color and how humans do" (Section 4.1). If the LLMs' internal organization of color space diverges from human perceptual geometry, then a naming system that appears "inefficient" by the human-derived IB bound could be efficient under the LLM's own (unknown) perceptual geometry. Since the paper's quantitative claims about "efficiency," "IB-optimality," and "alignment" all depend on the validity of this IB bound as a reference, this is a significant methodological gap that the paper does not address.

3. **Insufficient evidence for the "not merely mimicking" claim.** The IICLL paradigm rules out trivial memorization (recalling "red" for a specific RGB value), and the rotation analysis provides supporting evidence. However, the models could still be drawing on general statistical regularities learned from training data (e.g., categories tend to be contiguous in perceptual space, they partition space into roughly equal regions). The Shepard circles experiment (Section 4.3) is presented as evidence for domain generality but is explicitly preliminary: one model (Gemini), one condition (k=4), no IB analysis, no human comparison, only qualitative results. Yet the abstract and introduction use it to claim the result "could potentially apply also in other domains" — this overstates what the evidence supports.

### Minor

1. **Different output methods across models are a possible confound for cross-model comparisons.** The Gemini API uses controlled generation while open-weight models use log-prob scoring (Section 3). The paper mentions this but does not discuss whether this methodological difference affects the comparison between Gemini and other models, which drives the headline result.

2. **The Gemini vs. other-models comparison is not controlled.** No public information is available about Gemini 2.0's parameter count, training data, or architecture. The paper shows that model size and instruction-tuning are primary predictors of English color naming performance (Section 4.1, Figure 2c). Without controlling for these factors, the finding that "only Gemini 2.0" recapitulates the full range could simply reflect differences in scale or data quality rather than a qualitatively different inductive bias.

3. **Several interesting findings are under-analyzed.** Some models (Olmo 2 32B inst., Qwen 2.5 VL 7B inst.) produced systems resembling very low-resource WCS languages rather than English (Section 4.1), but the paper does not analyze why this happens or what it implies about the models' representational strategies.

### Trivial

None.

## Nice-to-Haves

- Disentangle ICL ability from IB bias by measuring each model's ICL capability on an unrelated task and using it as a covariate in the analysis.
- Recompute the IB bound under the models' own representational similarity space (rather than CIELAB) to test whether the efficiency results are robust to perceptual geometry assumptions.
- Calibrate the Shepard circles framing to match the preliminary nature of the evidence, rather than using it to support domain-generality claims in the abstract.
- Report significance testing details (e.g., p-values, effect sizes) for the rotation analysis.

## Removed Points

These points from the input review were identified as better placed in Nice-to-Haves or merged into existing weaknesses:
- "The paper lacks explicit significance testing for the rotation analysis" → Moved to Nice-to-Haves; this is a presentation preference rather than a substantive flaw.
- "No discussion of how training data could account for IICLL results" → Merged into Weakness #3 (insufficient evidence for non-mimicking claim).
- "Humans in Xu et al. did not perform in-context learning" → Merged into Weakness #1 (ICL confound); it is part of the same concern, not a standalone issue.
- "The paper would benefit from either (a) a more careful disentanglement... or (b) a more modest framing" → This is an editorial suggestion, not a weakness; implicitly addressed across the Major weaknesses above.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the ICL-confound and perceptual-geometry concerns, but these are methodological critiques rather than novel observations about the paper's empirical findings.

## Suggestions

1. Either control for ICL ability (covariate analysis or matched-pair design) or moderate the central claim from "exhibiting an inductive bias toward IB-efficiency" to "exhibiting behavior consistent with IB-efficiency under the current experimental paradigm."
2. Address the perceptual geometry mismatch by testing whether results hold under alternative reference frames (e.g., using the models' own internal representational distances).
3. Expand the Shepard circles analysis or temper the domain-generality claim to match the preliminary nature of the evidence.

### Calibration

**Round-1 bracket:** 5.0–6.5.

Anchors retrieved:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fN8yLc3eA7.md` (When LLMs Play the Telephone Game) | 6.00 (Accept) | Bracketing | Most comparable: same iterated-cultural-transmission methodology. That paper had weaker theoretical grounding and smaller model coverage but was accepted. The reviewed paper is stronger in theory and scope but has more central methodological concerns → comparable quality. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iVMcYxTiVM.md` (Can we talk models into seeing the world differently?) | 7.00 (Accept) | Bracketing | Cleaner experimental design and fewer confounds → higher score. The reviewed paper is weaker by comparison. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QQt0MwXA81.md` (Do LLMs exhibit human-like response biases?) | 6.20 (Reject) | Bracketing | Similar topic (LLM-human cognitive alignment), but that paper's negative finding presented a different evidentiary challenge. The reviewed paper has more positive evidence but also more methodological issues. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jOmk0uS1hl.md` (Training on the Test Task Confounds Evaluation) | 8.00 (Accept) | Bracketing | Very clean, tightly-argued paper with clear contribution → significantly stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RC5FPYVQaH.md` (Concept Bottleneck LLM) | 5.75 (Accept) | Narrowing | Weaker theoretical grounding but fewer confounds; comparable overall quality. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bEbQBiMpUI.md` (Convergence Towards Stable Intrinsic Self-correction) | 5.40 (Reject) | Narrowing | More significant methodological gaps → lower score. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xIUUnzrUtD.md` (Building, Reusing, and Generalizing Abstract Representations) | 6.50 (Accept) | Narrowing | Cleaner cognitive-science + ML paper → slightly higher score. |

The reviewed paper sits slightly above the 5.4–5.75 range (stronger theoretical framing and more comprehensive evaluation) but below the 6.5–7.0 range (central methodological concerns remain unaddressed). The closest anchor is the Telephone Game paper (6.00), which was accepted with a mixed review profile and comparable-quality weaknesses. This paper has a stronger theoretical contribution but more central methodological issues, placing it at the same level.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>