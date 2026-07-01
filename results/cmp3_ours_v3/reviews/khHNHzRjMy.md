Now let me write the final review.

## Summary

EmoSign introduces the first ASL video dataset annotated for sentiment and emotion by Deaf native signers. It consists of 200 video clips with three annotation layers: 7-point sentiment, 10 emotion categories with intensity, and free-text cue descriptions. Benchmarks on four multimodal LLMs under caption-only, video-only, and video+caption conditions reveal that current models perform poorly on visual-only emotion recognition from signing and rely heavily on text captions.

## Strengths

- **Addresses a genuine, underexplored gap with the right methodology.** No prior ASL dataset provides emotion/sentiment labels, and the dual grammatical+emotional function of facial expressions makes this non-trivial. Using Deaf native ASL signers with professional interpretation experience (Section 3.2) is the correct methodological choice and directly addresses failures of prior work (FePh used hearing annotators).

- **Rich three-layer annotation structure.** The combination of 7-point sentiment, 10 emotion categories with intensity ratings, and open-ended cue descriptions (Section 3.2) is substantially richer than the binary labels in FePh. The qualitative findings in Section 3.4 — documenting non-manual markers, sign modifications, and the role of context — provide genuinely useful documentation of how emotions manifest in ASL from native signer perspectives.

- **Informative ablation design in benchmarks.** Testing caption-only, video-only, and video+caption conditions (Section 4.2) cleanly separates what models extract from each modality. This reveals the paper's most robust finding: current MLLMs are heavily text-reliant and perform near-chance on visual-only emotion recognition from sign videos.

## Weaknesses

### Major

1. **VADER-based selection confounds the dataset's stated purpose.** The dataset is constructed by selecting the 100 most positive and 100 most negative utterances based on VADER analysis of their English text captions (Section 3.1). This means the dataset filters on text sentiment, but a core claim is that visual emotional cues in signing are being studied. The selection may systematically exclude videos where visual signing conveys emotion but the caption is neutral — precisely the cases most informative for training visual-only emotion recognition. The paper acknowledges (Section 6) that VADER results "differed from the annotators' results" and that videos "contained rich non-manual markers that conveyed emotions differently than the text," which confirms that VADER is an imperfect proxy. This does not invalidate the dataset, but it is a significant limitation that the paper under-discusses in terms of its impact on the generality of the benchmarks and conclusions.

2. **Small sample size with very low per-class counts, no confidence intervals.** The dataset has 200 utterances from 4 signers (~16 minutes). Per-class counts are tiny for several categories: 5 neutral samples for sentiment, 25 for anger and surprise_negative, 30 for fear and disgust (Figure 2). No confidence intervals or significance tests are reported. A shift of 2–3 predictions changes per-class accuracy by 10+ percentage points. With only 4 signers, signer-specific mannerisms cannot be separated from general ASL emotional expression patterns. The paper acknowledges the size constraint (Section 3) but does not discuss how it affects the reliability of the benchmark metrics.

3. **Inter-annotator agreement is very low for several emotion categories, with implications for ground-truth reliability.** Krippendorff's alpha for surprise_negative (0.119), disgust (0.166), frustration (0.330), sadness (0.333), fear (0.351), and anger (0.370) (Table 2) indicate that annotators could not reliably agree on the presence of these emotions. The paper compares the average alpha (0.593) to MELD (Fleiss' kappa = 0.43) and IEMOCAP (Fleiss' kappa = 0.48), but these are different metrics (Krippendorff's alpha vs. Fleiss' kappa) and not directly comparable. The paper does not discuss how unreliable ground truth for these classes affects benchmark interpretation — when a model fails on disgust, is it because the model is wrong, or because the ground truth is unreliable for that class?

4. **Benchmark evaluation lacks basic reference points and SL-specific models.** No majority-class or random baselines are reported. For 3-class sentiment with distribution ~115 negative / ~5 neutral / ~70 positive, an always-"negative" classifier would achieve ~60% simple accuracy and 33% macro-wAcc — but these baselines are absent (Table 3). Additionally, no sign-language-specific model (e.g., fine-tuned LLaVA-SLT) is evaluated; all conclusions about model failure are drawn from zero-shot evaluation of general-purpose MLLMs.

### Minor

5. **Anomalous near-zero benchmark numbers are unexplained.** MiniGPT4 caption-only achieves wAcc = 1.92 and wF1 = 5.92 on 3-class sentiment (Table 3). Since wAcc is macro-averaged per-class recall, a score of 1.92% for a 3-class problem suggests most outputs were unparseable or the evaluation pipeline collapsed. The paper does not discuss these floor-level results. Without clarification, this metric cannot be confidently interpreted.

6. **Emotion cue grounding is described as a benchmark task but receives only qualitative inspection.** Section 4.1 presents it as one of three benchmark tasks, but Section 5.3 reports only manual inspection of "several randomly selected videos" with no quantitative protocol, metric, or systematic evaluation. This is acceptable as exploratory analysis but should not be framed as a benchmark task.

7. **Minor inconsistency in signer counts.** Table 1 lists "3" signers for EmoSign, but Section 3.4 states "The dataset includes 4 different signers." The "Signers" column for EmoSign apparently refers to the 3 annotators, while for other datasets it refers to people appearing in the videos. This should be clarified.

### Trivial

None.

## Nice-to-Haves

- Include a supplementary set of clips selected without text-based VADER filtering, even if small, to compare text-congruent vs. text-orthogonal emotional expressions.
- Include at least one sign-language-aware model baseline (e.g., fine-tuning LLaVA-SLT).
- Report bootstrapped confidence intervals for all benchmark metrics.
- Provide majority-class and random baselines in benchmark tables.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"Paper should discuss how ties were broken"** — Already discussed in Section 3.3 ("we selected the label from the most confident annotator"). The speculation that one annotator might dominate is not supported by evidence.
- **"The broader 'multimodal emotion recognition' discussion reads as a generic survey"** — Style observation, not a substantive weakness affecting the paper's contribution.
- **"No train/validation/test split described"** — All evaluations are zero-shot on the full set; this is standard for a benchmark dataset paper and is implicitly clear.
- **"Strengthening the Paper on Its Own Terms" suggestions** — Moved to Nice-to-Haves as they are constructive suggestions, not weaknesses.
- **Various Section-by-Section Notes** (e.g., "The limitations section is thin") — General observations that do not identify specific factual errors or gaps beyond what is already captured in the major weaknesses above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify the impact of the VADER selection on the dataset's representativeness. If possible, add a small set of clips selected without text-based filtering.
- Report bootstrapped confidence intervals for all benchmark metrics given the small sample size.
- Add majority-class and random baselines to benchmark tables to contextualize model performance.
- Explain the near-zero MiniGPT4 results (Table 3) — distinguish parse failures from genuine model behavior.
- Clarify the discrepancy between Table 1 ("3" signers) and Section 3.4 ("4 different signers").
- Discuss how low inter-annotator agreement for specific emotion categories affects the interpretation of benchmark results for those categories.
- Consider whether merging 'joy' and 'excited' into 'happiness' (Section 4.1) discards useful information about co-occurrence patterns; justify this decision more carefully.

## Score and Decision

**Score: 4.0 — Borderline Reject**

The paper fills a genuine gap: no prior ASL dataset has emotion annotations by Deaf signers, and the annotation methodology is well-designed in principle. The qualitative findings about emotion cues in ASL (Section 3.4) are a real contribution. However, the paper has structural limitations that significantly weaken its contribution: (1) the VADER-based selection strategy is at odds with the stated goal of studying visual emotional cues in ASL; (2) the small sample size (200 clips, 4 signers) with tiny per-class counts makes the benchmark statistics unreliable; (3) low inter-annotator agreement on several emotion categories raises questions about ground-truth quality for those classes; (4) the benchmark evaluation lacks basic references (no baselines, no confidence intervals, unexplained near-zero results). The dataset itself is a useful resource, but the paper's framing overstates what the evidence supports. Substantial additional work (larger scale, addressing the VADER confound, more rigorous evaluation) would be needed to meet the acceptance bar.

**Calibration Anchors (all ICLR 2026):**
| Anchor | Avg Score | Comparison |
|--------|-----------|------------|
| MDPE (multimodal deception dataset) | 2.50 | Larger but weaker motivation; EmoSign has clearer contribution |
| ViML (music-video-language dataset) | 4.50 | Larger scale (3M clips) but less novelty; roughly comparable |
| Open-vocab MER (emotion recognition) | 5.40 | Stronger evaluation but similar methodological concerns; mixed reviews |
| SignAvatars (3D SL motion dataset) | 6.25 | Much larger (70K videos), more comprehensive; EmoSign below this |
| Uni-Sign (SL understanding at scale) | 6.40 | 1,985h dataset with SOTA results; EmoSign not in this league |

**Initial bracket:** 3.5–5.0. Final score narrowed to 4.0 based on structural (not cosmetic) limitations.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>