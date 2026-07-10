Now I have all the information I need. Let me compile the final review.

## Summary

This paper studies whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB)-efficient categorization, using color naming as a testbed. It conducts two main studies: (1) an English color naming study across 39 models showing that larger instruction-tuned models better approximate English color categories and their IB tradeoffs; (2) an iterated in-context language learning (IICLL) experiment showing that four top-performing LLMs restructure randomly-initialized pseudo-category systems toward greater IB-efficiency and human-alignment over generations. Key findings include that only Gemini 2.0 recapitulates the full range of human IB-tradeoffs, while the paper also provides initial generalization evidence with Shepard circles.

## Strengths

- **Two-study design that directly addresses mimicry vs. genuine bias.** The English naming study (which models can reproduce English categories) and the IICLL study (which tests whether models possess a deeper inductive bias) form a clean, cognitively-motivated experimental logic. The IICLL paradigm itself is a methodological contribution — extending prior I-ICL (Zhu & Griffiths, 2024) to iterated language learning with pseudo-labels enables direct comparison to human cultural evolution data (Xu et al., 2013).
- **Comprehensive model scope for a behavioral study.** Testing 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2) with varying sizes, training stages, and input modalities provides useful granularity. The inclusion of Olmo training checkpoints and the analysis of pre-training vs. instruction-tuning stages (Section 4.1) yields concrete insights into when and how these capabilities emerge.
- **Rotation analysis as a control (Section 4.2, Appendix H).** Rotating the hue mapping and showing that this degrades efficiency and alignment for Gemini rules out the trivial explanation that any random partition would score well on IB metrics. This strengthens the non-triviality of the IICLL trajectories.
- **Learning trajectory analysis (Olmo checkpoints, Appendix F).** The finding that English-alignment increases only slightly during pre-training and most substantially during instruction-tuning is an informative, concrete result about capability development.

## Weaknesses

### Major

- **The IB efficiency bound uses human perceptual (CIELAB) geometry that may not match LLM-internal representations, and this limitation is not discussed.** The IB bound (Zaslavsky et al., 2018) assumes speakers' mental representations are Gaussian distributions over CIELAB perceptual space (Section 2.2, p. 3). The paper reports that presenting colors in CIELAB coordinates *hurts* LLM performance and notes "this reveals a key difference between how LLMs represent color and how humans do" (Section 4.1, p. 6). However, the paper never discusses the implication: IB efficiency scores for LLMs measure efficiency *relative to a human perceptual model*, not relative to the model's own internal representation geometry. An LLM whose internal color geometry differs from CIELAB could appear suboptimal when evaluated against the human IB bound, or could appear to converge toward it for reasons related to training data statistics rather than a general compression bias. This gap is most consequential for the IICLL experiment, where the central claim is that models restructure systems toward IB-efficiency *in general*. The paper should openly address this as a limitation.

### Minor

- **The framing overgeneralizes from Gemini 2.0 to "LLMs" as a class in places.** The title ("Evolution and Compression in LLMs") and statements like "LLMs are capable of evolving perceptually grounded, human-like semantic systems" (Discussion, p. 9) imply a general finding. In reality, only Gemini 2.0 recapitulates the full range of IB-tradeoffs observed in humans (Figure 3); the other three models (Gemma 3 27B, Llama 3.3 70B, Qwen 2.5 32B) converge to low-complexity solutions covering a small region of the information plane. The rotation analysis is also "less conclusive" for these models (Section 4.2, p. 7). While the abstract and results sections do acknowledge this asymmetry, the broader framing could be more precisely calibrated. The paper would be stronger if it explicitly discussed the qualitative difference — do the non-Gemini models' low-complexity convergence reflect a genuinely human-like bias (some WCS languages are low-complexity) or a truncation effect (inability to handle high k conditions)?

- **The "not merely mimicking" claim would benefit from sharper framing.** The paper frames the question as a binary (mimicry vs. inductive bias toward IB-efficiency, Abstract, p. 1). The IICLL experiment shows models restructure random partitions toward efficient solutions, which does go beyond simple pattern mimicry. However, the binary framing does not acknowledge an intermediate possibility: LLMs could have *learned* from training data that human category systems tend to be IB-efficient, acquiring this as a higher-order statistical prior. The IICLL paradigm reveals this learned prior (as the paper's own Bayesian framing in Section 2.3 notes), which is consistent with both an "architectural bias" and a "learned statistical regularity" account. The Discussion mentions "the precise origins of the bias... are unclear" (p. 9) but the main narrative presents a sharper contrast than the evidence cleanly supports.

- **The Shepard Circles study (Section 4.3) is qualitatively preliminary.** It tests only one model (Gemini) under one condition (k=4) with purely qualitative evaluation (categories becoming "increasingly compact") and no IB-efficiency computation. The paper labels it appropriately as a "preliminary investigation" (p. 8), but its placement alongside the main color results risks overstating the generality of the findings. A quantitative evaluation (e.g., measuring whether the emergent partitions approach any known optimal tradeoff for the stimulus space) would substantially strengthen this section.

### Trivial

- **Several methodological details are not stated in the main text:** the number of IICLL chains/initializations per condition, the sampling procedure for in-context examples (how many per generation, how they are selected from the full system), and the temperature/decoding parameters for LLM responses. These appear only by reference to the appendix (Section 3, p. 4; Appendix G). While common in conference papers, these details affect the dynamics of IICLL and should at least be summarized in the main text.

## Nice-to-Haves

- The paper reports 95% confidence intervals in Figure 4 but does not state the number of chains these are based on. If the confidence intervals come from few runs, reporting this would help readers assess reliability.
- Exploring the k=14 condition in more detail for all models (it currently receives one sentence) could illuminate when the non-Gemini models' complexity ceiling emerges.

## Removed Points

These points were considered but removed from the main weaknesses:

- **"Selection bias" in IICLL models:** The paper explicitly states it only tested models that "performed well in the English color naming task" (Section 4.2, p. 6). This is an acknowledged design choice, not an undiscussed flaw.
- **Statistical significance claims:** Requesting specific test statistics for every comparison goes beyond what is standard for this type of behavioral study.
- **The critique that the abstract is false for 3/4 models:** The abstract's claim about "LLMs iteratively restructure initially random systems towards greater IB-efficiency" refers to the trend toward the IB bound (Figure 4a confirms all four models decrease efficiency loss), not about covering the full complexity range. The paper correctly separates these two claims.
- **Rotation analysis being inconclusive for non-Gemini models:** This is the paper's own stated finding (p. 7), not a gap the reviewer discovered. It is reflected in the overgeneralization weakness above.

## Novel Insights

The review's most valuable observation beyond the paper's own analysis is the asymmetry between Gemini and the other three models: the non-Gemini models converge to low-complexity solutions that fall *within* the human range but do not *span* it. The paper reports this fact but does not deeply explore whether this reflects a genuine human-like bias (some WCS languages also have low complexity) or a truncation effect (models cannot handle high k conditions like k=14). This asymmetry is potentially more interesting than a simple "Gemini is better" narrative and could be the basis for a sharper contribution if unpacked.

## Suggestions

1. Add a Discussion subsection explicitly addressing the CIELAB/sRGB mismatch and its implications for IB efficiency evaluation: state that the IB bound uses human perceptual geometry, acknowledge that this is both a strength (enabling direct comparison to human data) and a limitation (the metric may not capture efficiency in the model's own representational space), and discuss what alternative IB bounds (if computable) might look like.
2. Calibrate the title and framing: consider whether "Some LLMs" more accurately reflects the evidence, or explicitly characterize the Gemini/non-Gemini asymmetry as an important finding rather than a footnote.
3. Add the number of IICLL chains and key decoding parameters to the main experimental setup section.
4. Either expand the Shepard circles analysis with quantitative evaluation of category structure (compactness metrics, IB-efficiency if feasible) or clearly relegate it to future work with a brief mention.
5. Discuss the "learned prior vs. architectural bias" question more explicitly, acknowledging that the current design cannot cleanly distinguish these.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fN8yLc3eA7.md` (Telephone Game) | 6.00 | R1, R2 | Yes | Most similar: iterated cultural transmission with LLMs. This paper has stronger strengths (all 10.87-13.40 vs. 4.51-12.05) and no negative-weakness items (vs. -4.13, -3.10, -1.40). Clear upward comparison. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/62K7mALO2q.md` (Binary Sequences) | 6.00 | R1, R2 | Yes | Similar cognitive-science framing. This paper has higher strength favorability and no negative weaknesses. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xIUUnzrUtD.md` (Abstract Representations) | 6.50 | R1, R2 | Yes | Cognitive science + compression. Comparable strength profile. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2xRTdzmQ6C.md` (Concept IB Models) | 4.40 | R1 | Yes | Uses IB principle but a different setting (concept bottleneck models). Not directly comparable. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KlalQu2423.md` (CtD Emergent Comm.) | 6.67 | R2 | Yes | Emergent communication + compositionality. Comparable strength range but has a negative weakness (-0.33). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XrsOu4KgDE.md` (Culture Attribution) | 7.00 | R2 | Yes | LLM culture bias study. Higher top strength (14.99) but has several negative-weakness items and split reviewer scores (5,6,8,8,8). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Sy8upuD6Bw.md` (Emergent Comm. with Repair) | 6.33 | R2 | No | Emergent communication. Less directly relevant. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HC0msxE3sf.md` (Lewis's Signaling) | 6.00 | R2 | No | Emergent communication + statistical properties of language. |

**Round-1 bracket:** 5.5–7.5 (based on initial sweep showing the paper's strength and weakness profile sits above the 6.00 anchors but below the 7.00 anchor on most dimensions).

**Round-2 narrowing:** Compared against the Telephone Game (6.00), CtD (6.67), Culture Attribution (7.00), and Abstract Representations (6.50) anchors via itemized favorability. The paper's strengths (10.87–13.40) are consistently higher than the Telephone Game's (4.51–12.05) and comparable to CtD's (5.73–14.60) and Abstract Representations' (8.02–17.21). Critically, all five of this paper's weakness items have positive favorability (1.03–6.51), meaning none are seen as severely damaging by the scoring model. In contrast, the Telephone Game has weaknesses at -4.13 and -3.10, CtD has a weakness at -0.33, and Culture Attribution has weaknesses at -2.28 and -1.35. This clean weakness profile places the paper above 6.00. The major weakness (IB bound / CIELAB mismatch, favorability 1.03) is the main drag but remains mild relative to the anchors' structural issues. The comparison to Abstract Representations (6.50) is the tightest: both have strong methodology and mild weaknesses, placing this paper at a similar level.

**Final position:** Between the Telephone Game (6.00) and Culture Attribution (7.00), closely aligned with Abstract Representations (6.50) and CtD (6.67). The paper contributes a novel methodology (IICLL) and large-scale behavioral evaluation with clear cognitive-science grounding. The weaknesses are real but addressable — primarily claim calibration and one unaddressed methodological limitation — rather than structural flaws.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>