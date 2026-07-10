Now I have all the information I need. Let me compose the final review.

## Summary of calibration anchors used across rounds:

**Round 1 anchors (all sign language / emotion dataset papers):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md` (avg 1.00) — unrelated paper, not relevant
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EqCbc4wrzy.md` (avg 2.50) — MDPE multimodal deception dataset, itemized
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/f1uXrAjpOH.md` (avg 5.40) — OV-MER multimodal emotion recognition, itemized
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/L2kbdthX5M.md` (avg 6.25) — SignAvatars 3D SL dataset, itemized
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7gUrYE50Rb.md` (avg 8.00) — EQA-MX, not closely related

**Round 2 anchors (narrowing within 4-6 band):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/P8uOZmypb6.md` (avg 5.40) — BabyView dataset, itemized
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7kRFnSFN89.md` (avg 5.00) — SL translation
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LqaEEs3UxU.md` (avg 5.75) — Sign2GPT

## Position relative to anchors

The paper sits between MDPE (2.50) and SignAvatars (6.25), closest to OV-MER (5.40) and BabyView (5.40). Its strength items (avg favorability ~12.2) are substantially stronger than OV-MER's (~7-8) and comparable to SignAvatars' best items (~14). However, its major weaknesses (-1.91, -3.29 favorability) are more negative than OV-MER's worst weakness (-0.43) but less severe than SignAvatars' worst (-3.84). This is a high-variance paper: genuinely novel contribution with strong methodology for the annotation, but evaluation rigor falls short. The three major weaknesses (no CI, VADER confound, low IAA) are real and structural, but the core dataset contribution is clearly valuable and the annotation approach (Deaf native signers) is a strong differentiator.

**Final score: 5.0 (between borderline reject and borderline accept). Decision: Reject.** The paper makes a genuine contribution but needs substantial improvements in evaluation rigor, more honest scoping, and fuller treatment of known confounds before it meets the threshold for acceptance.

Here is the final review:

## Summary
This paper presents EmoSign, a multimodal dataset of 200 ASL video clips annotated for sentiment (7-point scale) and emotion categories (10 emotions) by 3 Deaf native ASL signers with professional interpretation experience. The dataset includes open-ended descriptions of emotion cues and benchmark evaluations of four multimodal LLMs under caption-only, video-only, and video+caption conditions. The paper identifies a genuine gap — no existing ASL dataset provides emotion annotations — and the annotation methodology is a clear strength.

## Strengths
- **Genuinely addresses an understudied problem.** The paper correctly identifies that existing ASL datasets focus on translation and lack emotional annotations, and that emotion recognition in sign language presents distinct challenges from spoken-language emotion recognition (facial expressions serving dual grammatical and affective functions). This motivation is well-supported by cited prior work (Lim et al., 2024; Reilly et al., 1992).

- **Deaf native signers as annotators.** Using 3 Deaf ASL signers with professional interpretation experience is a substantive methodological strength. The paper convincingly argues that hearing annotators (as used in FePh) may misinterpret signers' facial expressions, and that native fluency is required to distinguish grammatical from emotional facial expressions (Section 3). This is the dataset's strongest differentiator from prior work.

- **Rich annotation scheme beyond standard labels.** Beyond sentiment and emotion intensity ratings, the open-ended descriptions of emotion cues (e.g., 'mouth puffing emphasizes,' 'head tilt,' 'signing speed') are valuable and distinctive. Section 3.4's thematic summary of non-manual markers (furrowed brows, head thrusts, sign modification patterns) demonstrates that these descriptions capture genuine linguistic-pragmatic knowledge from native signers. This layer could support research directions beyond what the paper explores.

- **Clean ablation design (caption-only / video-only / video+caption).** The three-condition setup in Section 4.2 is well-motivated and directly tests the paper's central question about modality reliance. This design is cleaner than what many benchmark papers provide.

## Weaknesses

### Fatal
None.

### Major
- **No confidence intervals or measures of variance for any benchmark result.** With only 200 samples (140 for single-expression emotion classification across 11 classes), individual per-class counts are very small (e.g., neutral sentiment: 5 clips; anger: 25 clips; surprise_negative: 25 clips; disgust: 30 clips). A single misclassification can shift accuracy by several percentage points. The paper reports precise wF1 values (e.g., 76.72 for GPT-4o on 7-class sentiment) without bootstrap estimates, confidence intervals, or any measure of variance. This makes the benchmark numbers unreliable as performance estimates and gives a false impression of precision.

- **VADER-based text-sentiment filtering introduces a confound that undermines interpretation of the key experimental finding.** The paper selects the 100 most positive and 100 most negative utterances based on VADER analysis of the English caption text. Since the dataset is deliberately skewed toward emotionally charged captions, the central finding that models largely rely on text (caption-only ≈ video+caption) may partly reflect the dataset construction rather than being a general property of models' visual understanding. The paper acknowledges this issue in Section 6 but does not quantify or control for it in the analysis. Additionally, the unnatural distribution (only 5 neutral clips out of 200) means the dataset cannot support claims about how models handle emotionally neutral signing.

- **Low inter-annotator agreement on several negative emotion categories raises concerns about ground-truth reliability.** Krippendorff's alpha values in Table 2 show near-random agreement for surprise_negative (0.119) and disgust (0.166), and low agreement for frustration (0.330), sadness (0.333), anger (0.370), and fear (0.351). The paper's comparison to MELD (Fleiss' kappa=0.43) and IEMOCAP (Fleiss' kappa=0.48) is partly misleading because those are different agreement metrics not directly comparable to Krippendorff's alpha. For categories with near-random agreement, the ground-truth labels are unreliable, making the per-class benchmark results in Table 4 uninformative for those categories. The paper should be transparent about which categories have reliable labels.

### Minor
- **The 'emotion cue grounding' task is described as a benchmark task but evaluated only via qualitative inspection of a few examples.** Section 4.1 lists emotion cue grounding as one of three benchmark tasks. However, Section 5.3 describes a manual inspection of "several randomly selected videos" with qualitative commentary and no quantitative metrics. This is a useful qualitative analysis, but it is not a benchmark. The paper should clearly frame it as a preliminary qualitative analysis rather than implying it is a properly evaluated task.

- **The dataset includes only 4 signers from a single corpus (ASLLRP).** With 200 clips from just 4 signers, signer-specific mannerisms, facial morphology, and expressive styles could substantially influence the visual features available for emotion recognition. The benchmarks may partly measure how well models recognize these 4 specific individuals' emotional expressions rather than general properties of ASL emotion communication.

### Trivial
None.

## Nice-to-Haves
- Provide a per-signer breakdown of label distributions and model performance to help assess generalizability.
- Reframe the paper to center the open-ended cue descriptions as a primary contribution — they are arguably the most distinctive and reusable part of the dataset.
- Discuss the implications of the VADER confound more thoroughly and consider whether analysis could control for it (e.g., treating caption sentiment as a covariate).

## Removed Points
- *The comparison to Arodi et al./Krojer et al./Li et al. being "not apt" because those are different domains* — this is the reviewer's opinion; the paper's claim that small high-quality datasets can be valuable for benchmarking is reasonable, and the reviewer does not provide evidence that emotion recognition fundamentally requires larger samples than other tasks.
- *No discussion of "why" behind model biases* — the paper does discuss positive bias and speculates about RLHF (Section 5.1), which is a reasonable hypothesis.
- *Criticism about missing per-signer breakdown* — this is a reasonable suggestion but not a core weakness.
- *Multi-expression classification mentioned but not evaluated* — the paper explicitly defers this to future work.
- *Section-by-section commentary notes* — these are observations, not verified weaknesses.
- *Formatting/style nitpicks, typos, and grammar notes* — parser artifacts, not author errors.

## Novel Insights
None beyond the paper's own contributions. The reviews confirm the paper's core strengths (novel dataset, strong annotation protocol) but surface important methodological concerns about evaluation rigor that are not sufficiently addressed in the paper itself.

## Suggestions
1. Report bootstrap confidence intervals for all benchmark metrics given the small sample sizes.
2. Be more transparent about which emotion categories have reliable labels (based on IAA thresholds) and which do not when interpreting per-class results.
3. Either develop a proper quantitative protocol for the emotion cue grounding task or clearly label it as qualitative analysis.
4. Acknowledge the VADER selection confound more squarely as a limitation affecting the interpretation of the modality ablation results, not just as a design choice.
5. Consider whether the open-ended cue descriptions could be used more directly as an evaluation target rather than treating the benchmarks as the primary contribution.

## Score and Decision
**Score: 5.0 / Decision: Reject**

The paper addresses a genuine gap and its annotation methodology (Deaf native signers, rich annotation scheme) is a clear strength. However, the evaluation section lacks statistical rigor appropriate for its small sample size (no confidence intervals), the central experimental finding about modality reliance is partly confounded by the VADER-based dataset construction, and the ground-truth labels for several emotion categories have near-random inter-annotator agreement without sufficient transparency. These issues are addressable but the paper as presented does not meet the bar for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>