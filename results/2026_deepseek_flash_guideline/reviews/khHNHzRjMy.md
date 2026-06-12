## Summary

EmoSign introduces the first ASL video dataset annotated with sentiment and emotion labels by Deaf native signers. It comprises 200 clips (16 minutes, 4 signers) annotated by 3 Deaf ASL signers with interpretation experience, who provided: (1) 7-point sentiment ratings, (2) intensity ratings for 10 emotion categories, and (3) open-ended descriptions of emotion cues. The paper also benchmarks 4 MLLMs (GPT-4o, AffectGPT, Qwen2.5, MiniGPT4) under caption-only, video-only, and video+caption conditions on sentiment analysis, emotion classification, and qualitative cue grounding.

## Strengths

1. **First ASL dataset with fine-grained emotion and sentiment labels annotated by Deaf native signers.** Table 1 systematically shows that six existing ASL datasets lack emotion labels, sentiment labels, and emotion cue descriptions. The annotation by Deaf signers with interpretation experience is a meaningful methodological improvement over prior work like FePh (which used hearing annotators).

2. **Three-condition ablation reveals that current MLLMs cannot reliably recognize emotions from ASL videos alone.** Tables 3 and 4 show video-only performance is dramatically lower than caption-only or video+caption across all models (e.g., GPT-4o on 7-class sentiment: video-only wF1=5.97 vs caption-only 18.23 vs video+caption 26.35). This concretely demonstrates the gap between current MLLMs and human-level emotion understanding in sign language.

3. **Qualitative emotion cue descriptions from native signers are a genuinely novel contribution.** Section 3.4 documents thematic findings — non-manual markers (facial expressions, head/body movements), sign modification (size, speed, repetition), and contextual disambiguation — that no prior ASL dataset provides. This is the aspect of the work most likely to have lasting research value.

4. **Dataset construction uses natural continuous signing rather than acted emotions.** Section 3.1 explains the principled choice to use existing ASLLRP clips, citing evidence that acted emotions may not represent real communication (McKeown et al., 2011), improving ecological validity.

5. **Emotion taxonomy grounded in established frameworks.** Section 3.2 builds on Ekman's basic emotions and the circumplex model of affect (Russell, 1980), with the 7-point sentiment scale following Zadeh et al. (2018), rather than inventing ad-hoc categories.

## Weaknesses

### Fatal
None.

### Major

1. **Dataset scale limits conclusiveness of the main claims.** At 200 clips from 4 signers (~16 minutes), per-class counts for several emotions are only 25–30 (e.g., anger: 25, surprise_negative: 25, disgust: 30). The "multi-expression" evaluation subset is only 37 clips. Benchmark metrics would shift measurably if 2–3 samples changed category. The abstract's characterization of the dataset as "comprehensive" is an overstatement — this is a proof-of-concept scale. The paper acknowledges constraints ("Considering the cost of time and budget") but does not temper downstream claims accordingly.

2. **VADER-based selection creates an implicit confound for the headline benchmark finding.** The dataset is explicitly constructed by selecting the 100 most positive and 100 most negative utterances *by VADER text sentiment scores* (Section 3.1). This means text is a strong cue by construction. The paper's central claim — that "models fail to integrate visual cues and heavily rely on text captions" — is partially an artifact of this selection. A counterfactual evaluation on clips where text sentiment and visual emotion diverge would be needed to genuinely test whether models can use visual cues. The limitations section (Section 6) acknowledges VADER results "differed from the annotators' results" but does not carry this awareness forward to how the benchmark conclusions are framed in Sections 5.1 and 5.2.

3. **Low inter-annotator agreement on several emotion categories undermines ground-truth reliability for those labels.** Krippendorff's alpha is very low for several categories: surprise_negative (0.119), disgust (0.166), anger (0.370), sadness (0.333), frustration (0.330). With only 3 annotators, majority-vote labels for these categories may be unreliable. The paper's comparison to MELD (Fleiss' kappa=0.43) and IEMOCAP (Fleiss' kappa=0.48) mixes different agreement statistics (Krippendorff's alpha vs. Fleiss' kappa), which are not directly comparable.

4. **Evaluation protocol is asymmetric across models.** GPT-4o received all three tasks in a single API call with structured output, while AffectGPT, Qwen2.5, and MiniGPT4 were run on each task separately with adapted prompts (Section 4.2). This confounds cross-model comparisons — observed differences could stem from the protocol rather than model capability.

### Minor

1. **No confidence intervals, error bars, or significance tests on any benchmark metric.** With only 200 samples and per-class counts as low as 25, bootstrapped confidence intervals are necessary to assess whether observed performance differences between conditions or models are meaningful.

2. **No analysis of annotator disagreement patterns for low-agreement categories.** With alpha values below 0.2 for some categories, the paper should analyze *why* annotators disagree — whether due to genuine ambiguity, signer-specific effects, or confusable emotion categories — as this would inform future use of the dataset.

3. **Format for releasing the qualitative emotion cue descriptions is not specified.** The paper does not state whether these will be released as raw text, coded into categories, or linked to specific clips in a structured way, which affects their usability as a research resource.

4. **"Most confident annotator" tie-breaking may introduce systematic bias.** Section 3.3 notes that ties are broken by selecting "the most confident annotator," but no analysis is provided of whether one annotator consistently reports higher confidence, which would systematically skew labels.

5. **Number of clips skipped by annotators is not quantified.** Section 3.3 mentions "a very small fraction" were skipped, but without quantification, the potential impact on majority-vote label quality (some clips may have been annotated by only 1–2 annotators) cannot be assessed.

### Trivial

1. "Comprehensive" in the abstract is overstated for 200 clips from 4 signers — recommend replacing with "first dedicated" or "proof-of-concept" as a more accurate framing.

## Nice-to-Haves

- Per-signer breakdown of benchmark results would be informative (some signers may be more emotionally expressive, affecting model performance).
- A small counterfactual set of 20–30 clips where text sentiment and visual emotion diverge would substantially strengthen the benchmark conclusions.
- Systematic coding of the qualitative cue descriptions with inter-coder agreement would increase their value as a structured contribution.

## Removed Points

- **Criticism about data availability ("data will be released after acceptance"):** Removed per hard rules — the paper states data will be released, and questioning future release status of a paper's own contribution is not a valid weakness.
- **Criticism about missing appendix content:** The parser strips appendix sections from all papers; these exist in the original submission.
- **Strength about inter-annotator agreement being "higher than MELD/IEMOCAP":** Qualified because the comparison mixes different statistics (Krippendorff's alpha vs. Fleiss' kappa). The reporting itself is good practice, so this is noted implicitly in the strengths but without the overstated comparison.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the paper's contribution.** The qualitative emotion cue descriptions from Deaf native signers are the most novel and durable contribution. Consider positioning the benchmarks as illustrative baselines rather than the headline finding, which would better match the dataset's actual strengths and reduce the impact of the VADER confound.
2. **Add bootstrapped confidence intervals** to all benchmark tables (sentiment and emotion classification).
3. **Address the VADER confound explicitly** when presenting the "models fail to integrate visual cues" finding in Sections 5.1 and 5.2, not just in the limitations section.
4. **Acknowledge the Krippendorff's alpha vs. Fleiss' kappa comparison issue** and either add a proper comparison using the same statistic or remove the direct comparison.
5. **Quantify skipped clips and analyze tie-breaking annotator confidence** to increase transparency about label quality.

## Score and Decision

**Calibration Anchor Papers** (all rounds):

| Path | Avg Score | Round | Comparison to EmoSign |
|---|---|---|---|
| MDPE — deception dataset (EqCbc4wrzy.md) | 2.50 | Bracketing (2) | Larger-scale (104h, 193 subjects) but poorly executed; EmoSign has clearer methodology and stronger ecological validity |
| Representing Signs as Signs (flgrH5nK4H.md) | 4.00 | Narrowing | ASL-related but different task (ISLR); EmoSign is less about method and more about dataset |
| FHA-Kitchens (otoggKnn0A.md) | 4.00 | Narrowing | Similar-sized dataset (2,377 clips) but niche focus; EmoSign fills a more clearly identified gap |
| VRG-SLT (7kRFnSFN89.md) | 5.00 | Bracketing (3) | SLT method paper; EmoSign has more novel dataset contribution but no SOTA method |
| Open-vocabulary MER (f1uXrAjpOH.md) | 5.40 | Bracketing (3) | Emotion recognition paradigm paper; most comparable in ambition-level; EmoSign has stronger ecological validity but smaller scale |
| OmniBench (Rc8z5wLzBF.md) | 5.75 | Bracketing (4) | Multimodal benchmark, larger scale, rejected due to methodological concerns |
| SignAvatars (L2kbdthX5M.md) | 6.25 | Narrowing | Large-scale 3D SL dataset (70K videos); EmoSign is far smaller but fills a different gap |
| MIntRec2.0 (nY9nITZQjc.md) | 6.50 | Bracketing (4) | Large-scale benchmark dataset (15,040 samples), accepted with "no obvious flaws"; EmoSign is substantially smaller and has more methodological issues |
| ILLUSION (qnlG3zPQUy.md) | 6.00 | Bracketing (4) | Large-scale deepfake dataset (1.3M samples); scale gap is prohibitive |
| LOKI (z8sxoCYgmd.md) | 8.00 | Bracketing (5) | High-scoring benchmark paper; EmoSign is not at this rigor/scale level |

**Round 1 bracket:** 4–6. The paper's genuine novelty (first emotion-labeled ASL dataset with Deaf native signers and qualitative cue descriptions) anchors it above pure reject territory, but scale and methodological issues prevent it from reaching the "strong accept" range.

**Narrowing:** The most comparable anchors are FHA-Kitchens (4.00), Open-vocabulary MER (5.40), and MIntRec2.0 (6.50). EmoSign has a more novel and clearly motivated contribution than FHA-Kitchens, but significantly smaller scale and more methodological confounds than MIntRec2.0. The Open-vocabulary MER paper (5.40, rejected overall with mixed scores) is the closest in type — novel emotion dataset with methodological concerns.

**Final score: 5.0** — Borderline. The qualitative emotion cue descriptions and annotation by Deaf native signers are genuinely valuable contributions that fill a real gap. However, the dataset's small scale, the VADER selection confound on the headline benchmark claim, low inter-annotator agreement on several categories, and asymmetric evaluation protocol prevent stronger acceptance. The paper would benefit substantially from either (a) expanding the dataset before publication, or (b) reframing around the qualitative contributions and treating the benchmarks as secondary.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>