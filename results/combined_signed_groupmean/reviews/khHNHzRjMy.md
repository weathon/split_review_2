Now let me write the final consolidated review.

## Summary

This paper introduces EmoSign, a dataset of 200 ASL video clips (~16 minutes, 4 signers) annotated by Deaf native signers for sentiment (7-point scale), 10 emotion categories, and open-ended qualitative descriptions of emotion cues. Benchmarks with four general-purpose MLLMs (GPT-4o, AffectGPT, Qwen2.5-VL, MiniGPT4) in zero-shot settings reveal that models perform poorly on vision-only emotion recognition and rely heavily on text captions. The qualitative descriptions documenting how emotions manifest in ASL (facial expressions, mouth morphemes, signing speed, head tilts) are a novel contribution.

## Strengths

- **Genuinely underserved research gap.** No existing ASL dataset has emotion labels annotated by Deaf native signers. The comparison against FePh (Alaghband et al., 2020) makes a clear case: FePh crops faces, uses hearing annotators, and has only binary labels. EmoSign addresses all three weaknesses. The gap is real and the motivation is well-articulated (Section 1).

- **Annotation methodology that respects the target community.** The paper documents months of community engagement (attending events, learning ASL, collaborating with Deaf universities) and recruited Deaf native signers with professional interpretation experience — annotators who can distinguish grammatical from emotional facial expressions. This is the most important design decision and the authors get it right.

- **Qualitative descriptions of emotion cues (Section 3.4).** The open-ended annotations documenting how emotions manifest in ASL (furrowed brows, mouth morphemes, signing speed, head tilts) from native signers are a genuinely novel contribution that goes beyond label-only datasets. These descriptions could inform future work on disentangling grammatical from affective facial expressions — the core technical challenge the paper identifies.

- **Clear documentation of the annotation pipeline.** The paper describes pilot testing, training sessions, iterative refinement of the annotation interface (Section 3.2), and a three-layer annotation process (sentiment, emotions, cue descriptions), establishing a methodology future work can replicate.

- **The paper is transparent about several limitations** (lines 328-334), including acknowledging that VADER results differed from annotator judgments and that future work should fine-tune ASL-specific models.

## Weaknesses

### Fatal
None.

### Major

- **Small dataset size severely limits the strength of conclusions about model behavior.** The dataset contains 200 utterances (~16 minutes) from 4 signers. The single-expression emotion classification subset has only 140 clips across 11 categories, making per-class counts tiny (e.g., Surprise_neg=25, Anger=25, Fear=30, Disgust=30 in the full set, even fewer after splitting). Per-class accuracies in Table 4 show many 0% values, reflecting unstable results at this scale. Claims about model "bias" and "over-reliance on text" may reflect properties of these 200 specific clips rather than general model behavior. The paper cites precedents of small datasets (Arodi et al., 2024; Krojer et al., 2024; Li et al., 2024b), but those address different tasks where 200 examples can be sufficient; for emotion recognition in ASL — where the task requires disentangling grammatical from affective signals and visual cues are subtle — this scale cannot support robust conclusions about model capabilities.

- **VADER-based selection creates a confound between text sentiment and visual emotion that undermines the central benchmark finding.** The pipeline selects the 100 most positive and 100 most negative utterances based on VADER sentiment of the *text captions* (lines 115-116), creating an artificially bimodal distribution (only 5 neutral clips out of 200). Since videos were included because their *translation* is emotionally valenced — not because the signing itself is emotionally expressive — the dataset's construction makes text a reliable signal by design. The benchmark's central finding (models rely on text captions) is partly an artifact of this design choice. The paper acknowledges this tension obliquely (lines 330-331: "VADER results differed from the annotators' results") but does not quantify the extent of agreement/disagreement between VADER text sentiment and Deaf annotators' visual sentiment labels, which would be the most informative analysis to validate or refute the confound.

- **Inter-annotator agreement is poor for most negative emotion categories, making ground-truth labels unreliable.** Krippendorff's alpha values (Table 2): surprise_neg=0.119, disgust=0.166, frustration=0.330, sadness=0.333, fear=0.351, anger=0.370 — all well below the conventional threshold of 0.67 for reliable conclusions. When agreement approaches randomness (0.119, 0.166), the majority-vote labels for those categories are essentially arbitrary, making model performance on those categories uninterpretable. The paper's comparison to MELD (Fleiss' kappa=0.43) and IEMOCAP (Fleiss' kappa=0.48) is misleading because (a) Krippendorff's alpha and Fleiss' kappa are not directly comparable metrics, and (b) those are overall scores, not worst-category scores. The paper reports an average alpha of 0.593 but this average masks that several individual categories are near-random.

- **No explicit train/test split or evaluation protocol is described.** For a benchmark dataset with only 200 samples, it is essential to specify how data was partitioned for evaluation, whether cross-validation was used, and how hyperparameters were selected. This is a significant omission for a paper that reports quantitative benchmark results and draws conclusions about model behavior from them.

### Minor

- **Benchmark evaluates only general-purpose MLLMs in zero-shot settings.** None of the four models (GPT-4o, AffectGPT, Qwen2.5-VL, MiniGPT4) are designed for sign language understanding. The finding that they perform poorly on ASL emotion recognition is unsurprising. Including at least one ASL-specific model (e.g., LLaVA-SLT, which the paper itself cites) would transform this from a negative result to an informative comparison. The paper acknowledges this in limitations but it remains a gap in the current contribution.

- **The emotion cue grounding analysis (Section 5.3) is purely qualitative** — manual inspection of a few randomly selected videos with no quantitative metrics, systematic evaluation protocol, or inter-rater reliability. The paper describes three "benchmark tasks of increasing complexity" (line 199) but this one does not meet the standard of a benchmark.

- **GPT-4o was prompted for all three tasks simultaneously while other models were run per-task** (line 217). This difference in prompting protocol could affect cross-model comparability.

- **Per-class accuracies in emotion classification (Table 4) are unstable** — many 0% or extreme values for minority classes — reflecting tiny sample sizes rather than meaningful model capabilities.

### Trivial
None.

## Nice-to-Haves

- Report the extent of agreement/disagreement between VADER text sentiment and Deaf annotators' visual sentiment labels, which directly tests whether visual emotion signals diverge from textual content.
- Add an ASL-specific baseline model (e.g., LLaVA-SLT) to the benchmark.
- Explicitly describe the train/test split or cross-validation protocol used.
- Report per-annotator agreement patterns on the qualitative cue descriptions.
- Add confidence intervals to metrics given the small sample sizes.
- Check for signer-specific effects with only 4 signers.

## Removed Points

- **"The VADER claim contradicts the sentiment finding"**: The harsh critic claimed the paper's finding about sentiment analysis was "undercut" by emotion classification results where caption-only outperforms video+caption. This is factually incorrect — the paper's claim (line 229) is specifically about *sentiment analysis* (Table 3), where video+caption *does* consistently beat caption-only. The critic conflated the two tasks. However, the broader VADER confound concern (retained above) is valid independently of this erroneous sub-argument.

- **"10 fps may miss micro-expressions"**: Speculative criticism without evidence; the paper cites Bigand et al. (2021) to justify the sampling rate.

- **"Missing analysis of signer-specific effects"**: Nice-to-have, not a core weakness.

- **Generic framing concerns about FePh comparison**: The critic's note about "first" claims being imprecise is a presentation-level concern that does not affect the paper's core contribution.

- **The limitations transparency was scored as very low impact (+1.02) by the draft model**, suggesting it is not a meaningful strength in reviewers' assessment.

## Novel Insights

The most valuable insight emerging from reading this review alongside the paper is the tension between the paper's two central claims. The paper argues (a) that EmoSign fills a critical gap because it captures visual emotion signals that text cannot convey, yet (b) the dataset construction pipeline selects videos based on extreme text sentiment. This means the dataset is optimized to demonstrate exactly what the benchmarks then find — that text predicts emotion well. The confound could have been addressed directly by analyzing how often VADER text sentiment and Deaf annotators' visual sentiment diverge, which would either validate or refute the paper's core thesis. This pattern (designing a dataset to test modality independence while inadvertently making modalities correlated) is a recurring challenge in multimodal benchmarks and the paper would benefit from engaging with it explicitly.

## Suggestions

1. **Quantify the VADER confound explicitly.** Report the agreement/disagreement rate between VADER text sentiment and Deaf annotators' visual sentiment labels. If they often diverge, this is a strength (the dataset captures non-textual emotion); if they align, the confound needs honest acknowledgment.

2. **Add at least one ASL-specific baseline.** Fine-tuning or zero-shot evaluation of a model designed for ASL (e.g., LLaVA-SLT) would make the benchmark informative rather than merely documenting that general MLLMs fail at ASL emotion recognition.

3. **Specify the evaluation protocol.** Describe the train/test split or cross-validation methodology used.

4. **Report per-class sample sizes for the single-expression subset** alongside accuracy figures, so readers can assess which metrics are reliable.

5. **Tone down the scope of claims about model behavior.** Frame findings as observations on these 200 specific clips rather than general conclusions about multimodal model architectures.

## Score and Decision

### Calibration

All anchors retrieved across all rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| gwZ90hFSL2.md (unrelated paper) | 1.00 | R1 | No | Not comparable — unrelated topic |
| u1cQYxRI1H.md (unrelated) | 0.50 | R1 | No | Not comparable |
| 5lUdTogEL3.md (unrelated) | 1.00 | R1 | No | Not comparable |
| P49gSPmrvN.md (unrelated) | 1.00 | R1 | No | Not comparable |
| lMW9d1AqC9.md (SL→SQL) | 1.67 | R1 | No | Not comparable — different task, lower quality |
| EqCbc4wrzy.md (MDPE deception) | 2.50 | R1 | Yes | Lower quality. Weaker methodology, poor writing. EmoSign's community engagement and annotation rigor are stronger. |
| Jq8HYNZG9s.md (ShadowPunch) | 3.00 | R1 | No | Similar category (small benchmark dataset) but different domain. ShadowPunch has no community engagement dimension. |
| TadxJc1XAE.md (TeacherActivityNet) | 3.00 | R1 | No | Lower quality dataset paper with limited contribution |
| 7kRFnSFN89.md (VRG-SLT) | 5.00 | R2 | No | Sign language method paper, not dataset paper |
| flgrH5nK4H.md (One-shot ISLR) | 4.00 | R1 | Yes | Comparable — both address sign language gaps. ISLR paper had limited technical novelty. EmoSign has stronger community contribution but the ISLR paper's technical evaluation was more rigorous. |
| eeaKRQIaYd.md (USLNet) | 5.00 | R2 | No | Sign language method paper |
| f1uXrAjpOH.md (OV-MER) | 5.40 | R1,R2 | Yes | **Closest anchor.** Emotion recognition dataset with benchmark. OV-MER had a novel paradigm but data leakage concerns and unclear evaluation. EmoSign has cleaner methodology but smaller scale and different issues (IAA, VADER confound). Comparable overall quality. |
| P8uOZmypb6.md (BabyView) | 5.40 | R2 | Yes | Large-scale (493h) developmental dataset but reviewers questioned its value over existing datasets. EmoSign has clearer value proposition but is vastly smaller. |
| ybiwT2yP1c.md (BIRB) | 5.00 | R2 | Yes | Benchmark paper with clarity issues. Comparable quality level — both have genuine contributions undermined by evaluation concerns. |
| Wto5U7q6I2.md (TemporalBench) | 4.20 | R2 | No | Video benchmark, different domain |
| b2fhCbhe62.md (EmoGrowth) | 5.25 | R2 | No | Emotion recognition method paper |
| L2kbdthX5M.md (SignAvatars) | 6.25 | R1 | Yes | **Stronger anchor.** Much larger scale (70K videos), technical contribution (3D pose estimation). However, criticized for not being a "true" dataset (derived data). EmoSign has genuinely new data but significantly smaller scale. |
| 0Xt7uT04cQ.md (Uni-Sign) | 6.40 | R1 | No | Sign language pre-training, larger scale |
| LqaEEs3UxU.md (Sign2GPT) | 5.75 | R2 | No | Sign language translation method |
| qnlG3zPQUy.md (ILLUSION) | 6.00 | R1 | No | Larger-scale multimodal deepfake dataset |
| 7gUrYE50Rb.md (EQA-MX) | 8.00 | R1 | No | Top-tier dataset, incomparable quality |
| SctfBCLmWo.md (Dataset Bias) | 8.00 | R1 | No | Analysis paper, not comparable |
| WyEdX2R4er.md (Visual Data-Type) | 8.00 | R1 | No | Analysis paper |
| uAFHCZRmXk.md (Modality Gap) | 8.00 | R1 | No | Analysis paper |

**Round 1 bracket**: 4.0–5.5.

**Narrowing**: The closest comparable anchors are OV-MER (5.40) and the one-shot ISLR paper (4.00). EmoSign's strengths (community engagement, qualitative descriptions) are comparable in impact to OV-MER's novelty (+9.68 to +9.99 vs OV-MER's +9.97 to +9.99). Its weaknesses (small size, VADER confound, poor IAA, no train/test split) together match OV-MER's evaluation concerns (data leakage, label reliability, small frame sampling) in severity. The one-shot ISLR paper (4.00) had more limited contribution. EmoSign sits between these two, closer to OV-MER.

The paper's four major weaknesses (each scoring -9.97 to -10.00 in the impact model) collectively pull harder than its four strongest strengths (+9.19 to +9.99), and the weaknesses are structural (data construction choices, ground truth reliability, evaluation protocol) rather than addressable in a rebuttal. This places the paper slightly below OV-MER.

### Final Score and Decision

**Score: 4.5** — Borderline reject. The paper has genuine contributions (especially the community-engaged annotation methodology and qualitative descriptions of emotion cues) and addresses a real gap. However, the structural limitations (200 clips from 4 signers, VADER confound making the benchmark's central finding partly circular, near-random inter-annotator agreement on several emotion categories, and no specified evaluation protocol) collectively prevent the benchmark results from supporting the conclusions the paper draws. The qualitative contributions are valuable and should be preserved, but as presented the paper over-claims what the dataset and benchmarks can demonstrate.

**Decision: Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>