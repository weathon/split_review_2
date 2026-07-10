Now let me compile the final review with all the analysis integrated.

## Summary

This paper introduces EmoSign, the first dataset of ASL video clips annotated specifically for emotion and sentiment, comprising 200 utterances labeled by 3 Deaf native ASL signers with professional interpretation experience. The annotations cover a 7-point sentiment scale, 10 emotion categories with intensity ratings, and open-ended descriptions of emotion cues. The paper also presents zero-shot benchmark results on four MLLMs (GPT-4o, AffectGPT, Qwen2.5-VL, MiniGPT4) under three conditions (caption-only, video-only, video+caption), finding that models rely heavily on text and perform poorly on visual-only inputs.

## Strengths

- **Addresses a genuine, understudied gap** at the intersection of sign language and emotion recognition. The motivation about facial expressions simultaneously serving grammatical and emotional functions (Section 1) is specific, well-referenced, and compelling. [favorability=10.13]

- **Annotation methodology is thoughtfully designed:** Deaf native ASL signers with professional interpretation experience are the correct choice of annotators; the three-layer annotation (7-point sentiment, 10 emotion categories with intensity, open-ended cue descriptions) captures richer information than existing sign-language datasets; pilot testing with ASL-first individuals and IRB review demonstrate procedural care (Section 3.2). [favorability=9.96-11.79]

- **Ablation design** (caption-only, video-only, video+caption) is well-chosen to isolate modality contributions. The finding that video-only performance is poor across models, and that caption-only often matches video+caption performance, cleanly demonstrates that current MLLMs primarily rely on text for emotion recognition in sign language videos (Section 4.2, Tables 3-4). [favorability=11.00]

- **Honest reporting of inter-annotator agreement** — Table 2 reports Krippendorff's alpha with notably low values (surprise_neg = 0.119, disgust = 0.166) rather than suppressing them, and contextualizes these against MELD and IEMOCAP. This transparency is a strength for a dataset paper. [favorability=11.86]

- **Qualitative grounding analysis** (Figure 3) provides genuine insight into model failure modes, showing how models interpret the same visual cues differently depending on whether captions are provided, and how model reasoning contradicts Deaf annotator judgments. This goes beyond accuracy numbers to reveal *how* models fail (Section 5.3). [favorability=10.60]

## Weaknesses

### Major

**1. VADER-based text-sentiment selection creates a structural bias that undermines clean interpretation of the benchmarks.** The dataset was constructed by selecting the 100 most positive and 100 most negative utterances based on caption text using VADER scores (Section 3.1, line 115). This has several consequences: (a) the dataset systematically excludes cases where caption text is neutral but signing conveys emotion — precisely the cases most relevant for studying whether models can recognize emotion from visual cues alone; (b) the near-absence of neutral examples (5/200, Figure 2B) is a construction artifact, making the benchmark artificially structured as "distinguish positive from negative"; (c) since the dataset was selected to maximize text-sentiment signal, the central finding that models rely on text may be partially amplified by construction. Crucially, the paper never analyzes the agreement or divergence between VADER text-sentiment scores (used for selection) and the Deaf annotators' video-based labels — this analysis would be the most informative way to understand when visual and textual emotions diverge, which is the paper's stated central problem. The limitation is acknowledged in a single sentence in Section 6 but not quantified or systematically discussed. [favorability: sub-items range -0.55 to 2.35]

**2. Small dataset size severely limits the reliability of per-class benchmark results, and no uncertainty estimates are reported.** With 200 utterances (~16 minutes) from 4 signers and ~13 samples per class in the single-expression subset (140 clips across 11 classes, Section 4.1), many per-class accuracies in Table 4 are 0% (e.g., MiniGPT4 video-only: 7 of 11 classes at 0%). These zeros are as likely to reflect insufficient test data as genuine inability to recognize those emotions. No error bars, confidence intervals, or repeated trials are reported anywhere in the benchmark results, making it impossible to distinguish signal from noise in fine-grained results. The paper's defense citing "similar-sized" datasets (line 87; Arodi et al., Krojer et al., Li et al.) is vague — it does not specify the sizes, tasks, or why the analogy holds for 11-class emotion classification on 140 single-expression clips. [favorability=-0.37]

### Minor

**3. The "emotion cue grounding" is presented as a third benchmark task** alongside sentiment analysis and emotion classification (Section 4.1), but is evaluated only through qualitative manual inspection of "several randomly selected videos" (Section 5.3). There is no quantitative metric, protocol, or systematic comparison — it is a qualitative analysis, not a benchmark. The analysis itself is valuable (Figure 3 is genuinely informative), but the framing overstates what was done. [favorability=-0.27]

**4. The inter-annotator agreement comparison** (Section 3.3) compares the paper's Krippendorff's alpha (0.593 average) to MELD and IEMOCAP's Fleiss' kappa (0.43 and 0.48). These are different agreement metrics, making the comparison only approximate. While useful for context, this distinction should be noted. [favorability=0.90]

### Trivial

None.

## Nice-to-Haves

- Systematically analyze the agreement/divergence between VADER text-sentiment scores and Deaf annotator video-based labels — this would be the single highest-value addition using existing data.
- Report bootstrap confidence intervals or similar uncertainty estimates on benchmark numbers.
- Provide structured coding or a table of the annotator cue descriptions (Section 3.4), currently presented as unstructured paragraphs.
- Reframe the emotion cue grounding as a qualitative analysis rather than a third benchmark task.

## Removed Points

These points from the input review were removed and should be treated with caution:

1. **Criticism about unspecified train/test split** — REMOVED because the models are evaluated zero-shot (Section 4.2). No training or fine-tuning is conducted, so no train/test split is applicable. The criticism was based on an incorrect assumption.

2. **Request for cross-validation** — REMOVED because cross-validation presumes a training setting; this is zero-shot evaluation.

3. **Claim that VADER selection makes the video-only finding "partially an artifact"** — WEAKENED and merged into Major Weakness 1. The VADER bias is real and structural, but the specific claim of artifact is speculative without further analysis of VADER-annotator divergence. The core concern is retained.

4. **Request for signer-specific analysis** — REMOVED as scope creep for a first-of-its-kind 200-clip dataset.

## Novel Insights

None beyond the paper's own contributions. The qualitative analysis of model failure modes (Figure 3) is itself a novel finding, and the reviews do surface the structural VADER bias concern sharply.

## Suggestions

1. **Address the VADER–annotator divergence.** This is the single most valuable analysis the paper could add using existing data. A confusion matrix or agreement table between VADER sentiment scores and Deaf annotator sentiment labels would directly illuminate when visual and textual emotions diverge — the paper's central research question.
2. **Report uncertainty.** Add bootstrap confidence intervals or similar to all benchmark numbers to honestly convey reliability given the small sample size.
3. **Reframe the emotion cue grounding** as a qualitative analysis rather than a benchmark task. The content is valuable without that label.
4. **Add structure to the cue descriptions** (Section 3.4) with a systematic coding scheme or table rather than paragraphs of themes.

## Score and Decision

**Calibration anchors used:**

| Paper Path | Avg Score | Round | Itemized? | Comparison to EmoSign |
|---|---|---|---|---|
| SignAvatars (L2kbdthX5M) | 6.25 | R1 | Yes | Much larger scale (70K videos), stronger technical contribution, but criticized for being derivative data. EmoSign has stronger novelty (first-of-its-kind emotion labels) but much smaller scale and VADER bias. |
| Open-vocabulary MER (f1uXrAjpOH) | 5.40 | R1/R2 | Yes | Novel task formulation for emotion recognition. EmoSign has cleaner human-annotation methodology but smaller scale. Both have structural limitations that weaken claims. |
| Vinoground (a1P5kh2oo8) | 5.75 | R2 | Yes | Cleaner benchmark methodology (1000 pairs, no selection bias) but criticized for incremental novelty. EmoSign has stronger novelty but weaker evaluation rigor. |
| FHA-Kitchens (otoggKnn0A) | 4.00 | R1 | Yes | Small-scale niche dataset with careful annotation. Similar contribution type; EmoSign has stronger novelty (first-of-its-kind vs. incremental). |
| IndianRoad (8gCgXG40Wn) | 4.00 | R2 | No | Traffic dataset with 13M annotations; different domain, rejected for various quality concerns. |
| MDPE (EqCbc4wrzy) | 2.50 | R1 | Yes | Poorly motivated deception dataset with fuzzy concepts. EmoSign is substantially stronger in clarity and methodology. |

**Bracket justification:** Round 1 placed EmoSign between FHA-Kitchens (4.00) and SignAvatars (6.25). Round 2 narrowed between FHA-Kitchens (4.00) and Vinoground/Open-vocabulary MER (~5.4-5.75). EmoSign's strongest items (annotation methodology, honest IAA reporting, qualitative analysis) have favorability comparable to the better anchors (~10-12). Its most damaging items (VADER bias with no divergence analysis, no error bars, vague size defense) have lower favorability (-0.55 to -0.37) than most anchors' worst items but are structural rather than cosmetic. The paper addresses a genuine gap with thoughtful methodology, but the VADER selection bias and small size with no uncertainty estimates fundamentally limit what can be concluded from the benchmarks.

**Final Score: 4.5 — borderline reject.** The dataset contribution is real and the annotation methodology is sound, but the VADER-based selection structurally biases the dataset in ways that complicate the benchmark conclusions, and the small size with no error bars prevents reliable fine-grained evaluation. These are not fixable with clarifications alone.

**Final Decision: Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>