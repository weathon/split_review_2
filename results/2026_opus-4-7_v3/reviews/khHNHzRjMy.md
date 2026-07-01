Now I've read the full paper. Let me verify each claim and construct the draft review.Now let me run Round 1 calibration search to bracket the score:Let me read some key anchor papers to calibrate:Now I have enough calibration data. Let me synthesize the final review.

**Round 1 Bracket Analysis:**

- **Strong reject anchors (1-1.5)**: Papers with fundamental problems (pseudoscience, no real contribution). EmoSign is clearly above these.
- **Reject anchors (2-3.5)**: MDPE (2.50) — multimodal dataset with fuzzy concepts, marginal gains. EmoSign is better motivated with a clearer gap.
- **Borderline (3.5-5.5)**: OV-MER (5.40) — much more comprehensive emotion recognition dataset with novel metrics, still rejected. Representing Signs (4.00) — sign language paper with community engagement but methodological issues. Sign Language Translation (5.00), MMToM-QA (4.75).
- **Borderline accept (5.5-7.5)**: SignAvatars (6.25, 70K videos, rejected), Uni-Sign (6.40, 1985 hours, accepted), MIntRec2.0 (6.50, 15K samples, accepted). All are orders of magnitude larger in scale.
- **Accept (7.5-8.5)**: Strong benchmark papers with comprehensive contributions.

**Initial bracket: 3.5 – 5.0.** EmoSign fills a genuine niche but its benchmarking is confounded, its scale (200 clips) is far below accepted dataset papers, and several categories have unreliable ground truth. It sits below the OV-MER paper (5.40) which had more comprehensive methodology and was still rejected.

---

## Summary
EmoSign introduces a 200-clip ASL video dataset annotated with sentiment labels (7-point scale), emotion categories (10 emotions with intensity ratings), and free-text emotion cue descriptions by 3 Deaf native ASL signers. The paper benchmarks four multimodal LLMs (GPT-4o, AffectGPT, Qwen2.5, MiniGPT4) in zero-shot settings across sentiment analysis, emotion classification, and emotion cue grounding, finding that current models struggle to leverage visual cues from sign language video and rely heavily on text captions.

## Strengths
- **Genuine, well-documented research gap.** Table 1 confirms no existing ASL dataset contains emotion or sentiment labels. FePh — the closest prior work — used cropped face images, binary labels, and hearing annotators (Section 2). EmoSign directly addresses all three limitations, and the practical consequences of the gap (misinterpretation in legal/emergency settings, Section 1) are concrete.
- **Community-centered annotation methodology is essential, not decorative.** Recruiting Deaf native signers with professional interpretation experience (Section 3.2) is methodologically necessary given evidence that hearing annotators systematically misinterpret signers' facial expressions (Lim et al., 2024, cited in Section 2). The months of community engagement described in Section 3 demonstrate genuine investment.
- **Three-layer annotation yields novel qualitative findings.** The free-text emotion cue descriptions (Section 3.4) produce substantive insights about how non-manual markers (furrowed brows, head thrusts, mouth shapes), sign modification (size, speed, repetition), and narrative context (eye gaze shifts, perspective changes) convey emotion in ASL. This documentation from native signer perspectives is genuinely novel and not available elsewhere.
- **Three-condition ablation is well-designed.** The caption-only / video-only / video+caption ablation across all four models and three tasks (Section 4.2) produces clear, consistent patterns. The finding that models produce generic or incorrect outputs in the video-only condition (Section 5.2, 5.3) — e.g., AffectGPT consistently outputting "Neutral," Qwen2.5 requesting "audio context" for sign language — reveals specific model failure modes.

## Weaknesses

### Fatal
None.

### Major
- **VADER-based selection introduces a structural confound in benchmarking.** The 200 utterances were selected as the top-100 positive and top-100 negative clips by VADER text sentiment scores applied to English captions (Section 3.1: "we selected the 100 most positive and 100 most negative utterances based on the VADER scores"). This means text sentiment is bimodally distributed and maximally informative by construction. When the paper then reports that "caption-only condition showed similar and, sometimes, better performance to the video + caption condition" (Section 5.2), this is at least partly an artifact of selecting clips *because* their captions had extreme sentiment. The most scientifically interesting cases — where visual emotional cues diverge from or supplement text — are systematically underrepresented. The paper acknowledges VADER/annotator divergence in Section 6 but does not analyze its implications for benchmarking or stratify results accordingly. This undermines the benchmark conclusions about visual cue failure, though not the dataset's intrinsic value as a resource.

- **Low inter-annotator agreement for many emotion categories undermines ground-truth reliability.** Table 2 shows Krippendorff's alpha values of 0.119 (surprise_neg), 0.166 (disgust), 0.330 (frustration), 0.333 (sadness), 0.351 (fear). With only 3 annotators and majority-vote aggregation, the "ground truth" for these categories is essentially one annotator's judgment against near-chance disagreement. The paper contextualizes this by comparing to MELD (Fleiss' kappa = 0.43) and IEMOCAP (0.48) (Section 3.3), but this comparison is misleading: different agreement metrics on different annotation schemas with much larger sample sizes are not directly comparable. Benchmark results for categories like surprise_neg and disgust are not evaluating against a stable target.

### Minor
- **Per-category benchmark numbers are statistically fragile.** The single-expression subset has 140 clips across 11 categories. Based on Figure 2C distributions, categories like anger (~25 clips in the full dataset, fewer in the single-expression subset) likely have under 10 samples each. Per-category accuracy in Table 4 is computed over these tiny denominators — a single clip can swing accuracy by 10+ percentage points. Per-category sample sizes are not reported alongside accuracy figures, making interpretation impossible.

- **Emotion cue grounding is qualitative-only but framed as a benchmark task.** Section 5.3 describes manually inspecting "several randomly selected videos" — there is no quantitative evaluation, no metrics, no systematic assessment. Yet the paper lists this as one of three "benchmark tasks" (Section 4.1). The qualitative observations (e.g., Figure 3 showing how models interpret the same visual cue differently with/without captions) are genuinely interesting but do not constitute a benchmark.

- **Abstract overclaims relative to evidence.** The abstract states "current multimodal models fail to integrate visual cues into emotional reasoning," but Table 3 shows video+caption consistently outperforms both unimodal conditions for sentiment analysis across nearly all models, suggesting models *do* integrate visual information when available. The claim holds for emotion classification (Table 4) but contradicts the sentiment results.

- **No defined evaluation protocol limits benchmark reusability.** All benchmarking is zero-shot with no train/test split, cross-validation procedure, or recommended evaluation protocol. Future papers cannot compare results on a common test set, limiting the dataset's utility as the reusable benchmark the paper positions it as.

### Trivial
None.

## Nice-to-Haves
- Stratifying benchmark analysis by VADER-annotator agreement/disagreement would partially address the selection confound and sharpen the argument about visual cue importance — this requires no new data.
- Developing a taxonomy of emotion cues in ASL (non-manual markers, sign modification, context signals) grounded in the annotators' free-text descriptions would elevate the qualitative layer to a first-class contribution.
- Defining concrete evaluation protocols (fixed test splits, cross-validation scheme) would increase benchmark utility even at 200 samples.
- Reporting per-category sample sizes in the single-expression subset alongside Table 4 accuracy figures.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Garbled sentence in Section 6** ("we found VADER results differed from the annotators' results often contained rich non-manual markers") — this is a parser/extraction artifact, not an author error. REMOVED per formatting rules.
- **Missing appendix content and references** — the parser strips appendix sections from all papers. REMOVED per rules.
- **Request for confidence intervals on benchmark results** — while helpful, single-run zero-shot evaluation is standard practice for MLLM benchmarking, and the paper follows established norms (e.g., Lian et al., 2025). MOVED to nice-to-have.
- **Under-specification of how many clips had fewer than 3 annotators** — the paper states "a very small fraction of the clips were skipped" (Section 3.3). While more precision would be helpful, the paper's honest disclosure is adequate. REMOVED as minor since paper addresses it.
- **Concern about no fine-tuning** — given the 200-sample size, zero-shot evaluation is the only reasonable approach. This is not a weakness of the paper but a constraint of the dataset size that the paper handles appropriately. REMOVED.

## Novel Insights
The paper's systematic documentation of how Deaf native signers identify and describe emotion cues in ASL (Section 3.4) — including the dual function of facial expressions for grammar vs. emotion, sign modification patterns for emotional intensity, and narrative context disambiguation through gaze shifts — represents genuinely novel qualitative knowledge not available in prior computational work. The finding that all four tested MLLMs fundamentally lack visual understanding of sign language emotion cues, with specific failure modes (AffectGPT defaulting to "Neutral," Qwen2.5 requesting audio context for a visual-only language, GPT-4o repeating "relaxed body language"), is an informative negative result that exposes concrete gaps in current multimodal architectures.

## Suggestions
- **Stratify by VADER-annotator concordance:** Identify clips where text sentiment and annotated visual sentiment diverge and separately benchmark model performance on concordant vs. discordant clips. This would disentangle the selection confound without requiring new data.
- **Reframe emotion cue grounding:** Either develop quantitative metrics for grounding evaluation or honestly label Section 5.3 as a qualitative case study rather than a benchmark task.
- **Soften abstract claims:** Align the abstract's claim about visual cue integration failure with the nuanced evidence — sentiment analysis shows integration helps (Table 3), emotion classification does not (Table 4).
- **Report per-category sample sizes:** Include category-level N alongside accuracy figures in Table 4 so readers can assess statistical reliability.
- **Consider expanding scope of dataset construction:** Include clips with neutral or mid-range VADER scores to diversify the text-visual relationship and enable studying cases where visual cues carry emotion independent of text.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to EmoSign |
|-------|------|-----------|-------|-----------------------|
| MDPE (deception dataset) | EqCbc4wrzy | 2.50 | R1 | EmoSign is better motivated with a clearer gap and more thoughtful annotation design |
| Multimodal class-incremental learning benchmark | gNoqEdT2wO | 2.33 | R1 | EmoSign has a more novel contribution and better community engagement |
| Bridging Visual Communication (sign language to SQL) | lMW9d1AqC9 | 1.67 | R1 | EmoSign is substantially more rigorous and addresses a real problem |
| HGR multimodal feature extraction | YrxhSkfHh0 | 3.33 | R1 | Different type of paper; EmoSign has clearer motivation but less technical depth |
| Open-vocabulary MER | f1uXrAjpOH | 5.40 | R1 | OV-MER is more technically ambitious with novel metrics, larger scale, comprehensive benchmarks; EmoSign is below this |
| Sign Language Translation VQ-VAE | 7kRFnSFN89 | 5.00 | R1 | More technical novelty; EmoSign has unique niche but less methodological rigor |
| Representing Signs as Signs | flgrH5nK4H | 4.00 | R1 | Similar community engagement; comparable methodological issues; EmoSign has equally novel but smaller contribution |
| MMToM-QA | sMFqEror1b | 4.75 | R1 | More comprehensive benchmark design; EmoSign is narrower and smaller |
| SignAvatars (3D SL dataset) | L2kbdthX5M | 6.25 | R1 | Much larger scale (70K videos vs 200 clips), automated pipeline; EmoSign is well below |
| Uni-Sign | 0Xt7uT04cQ | 6.40 | R1 | Large-scale unified framework (1985 hrs); EmoSign is far below in scope |
| MIntRec2.0 | nY9nITZQjc | 6.50 | R1 | 15,040 samples with comprehensive framework; EmoSign's 200 clips and zero-shot-only evaluation is much less comprehensive |
| ILLUSION (deepfake dataset) | qnlG3zPQUy | 6.00 | R1 | 1.3M samples across modalities; EmoSign is far smaller in scale |
| Humanoid robots Chinese NLP | gwZ90hFSL2 | 1.00 | R1 | EmoSign is clearly above this level |
| Balancing Differential Knowledge | 5lUdTogEL3 | 1.00 | R1 | EmoSign is clearly above this level |
| NEMESIS jailbreaking | 5kMwiMnUip | 1.40 | R1 | EmoSign is clearly above this level |
| EQA-MX | 7gUrYE50Rb | 8.00 | R1 | 8M samples, comprehensive tasks; EmoSign is far below |
| MMIE | HnhNRrLPwm | 8.00 | R1 | 20K curated queries, comprehensive benchmark; EmoSign far below |
| Test-time Adaptation | TPZRq4FALB | 8.00 | R1 | Novel method with strong theoretical grounding; different paper type |
| LOKI | z8sxoCYgmd | 8.00 | R1 | Comprehensive multi-modal benchmark; EmoSign far below in scope |

**Round 1 bracket: 3.5 – 5.0**

EmoSign fills a genuine and important niche — it is the first emotion-annotated ASL video dataset with Deaf annotators, and its qualitative findings are novel. However, the VADER selection confound undermines the benchmark conclusions, the dataset is very small (200 clips vs. thousands to millions in accepted dataset papers), low IAA for many categories weakens ground-truth reliability, and the paper overclaims its benchmark utility. The paper sits below the Open-vocabulary MER paper (5.40, rejected) which had a more comprehensive contribution, and near the Representing Signs paper (4.00, rejected) which had comparable methodological issues. EmoSign's unique community engagement and genuine gap pull it slightly above the 4.00 anchor, but the compounding methodological issues (confound + small scale + low IAA + no evaluation protocol + qualitative-only third task) prevent it from reaching the 5.0 range.

**Final Score: 4.0**

The paper makes a meaningful first step toward an underserved problem, and the dataset — particularly the emotion cue descriptions — has real value as a pilot resource. However, the VADER selection confound systematically inflates text-based baselines and undermines the central claim about visual cue importance; the dataset is too small for per-category benchmark reliability; and several emotion categories have ground truth that is not stable enough to benchmark against. The paper positions EmoSign as a definitive benchmark, but in its current form it functions more as a valuable pilot contribution. For a top venue, the benchmarking methodology needs to be more rigorous, and the scale needs to support the claims being made.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>