Now I have all the calibration data I need. Let me compile the final review.

## Summary

This paper combines the Information Bottleneck framework with iterated learning to study whether LLMs develop human-aligned, efficient color category systems. It conducts two experiments: (1) an English color naming study across 39 models from 6 families, finding that size and instruction-tuning improve alignment and IB-efficiency but many models struggle; and (2) an Iterated In-Context Language Learning (IICLL) paradigm where models iteratively transmit pseudo-color-naming systems, showing that some models evolve toward IB-efficient systems. The paper's descriptive contributions are substantial, but its central interpretive claim — that LLMs exhibit an intrinsic inductive bias toward IB-efficiency — is not fully separable from the alternative explanation that models propagate statistical regularities already present in their training data.

## Strengths

- **Theory-driven approach with falsifiable predictions.** The paper grounds its investigation in the Information Bottleneck (IB) framework (Zaslavsky et al., 2018), which provides a well-defined objective function, a predicted optimality bound, and principled evaluation metrics (efficiency loss ε, NID-based alignment). This allows the paper to ask a sharp, falsifiable question rather than a vague one about whether LLMs "name colors like humans."

- **Large-scale and systematic model comparison.** Testing 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2) with variation in size, instruction-tuning, checkpoints, and modality is unusually thorough for this kind of cognitive-science-inspired LLM study. The English naming experiment (Section 4.1) provides a clear descriptive map of where different model classes lie relative to the English system and the IB bound.

- **The IICLL paradigm is a creative experimental adaptation.** Adapting iterated learning to LLMs via in-context learning (building on Zhu & Griffiths, 2024) is methodologically interesting and likely to be reused by other researchers. The design decision to present pseudo-labels without telling the model the stimuli are colors is a good control against simple label-matching, and the parallel to human iterated language learning experiments provides a strong baseline for comparison.

- **Rotation analysis provides a non-trivial sanity check.** The rotation analysis (Section 4.2, referencing Appendix H) — showing that rotating hue assignments away from the emergent system degrades efficiency and alignment for Gemini — strengthens the case that the evolved systems are genuinely structured rather than artifacts of the evaluation metric.

- **Surprising and informative negative results.** The finding that many prominent LLMs (including very large ones like Llama 3.3 70B) struggle to capture the English color naming system, and that Olmo 2 32B produces systems resembling low-resource WCS languages rather than English, are genuine surprises that speak to the paper's thoroughness and provide useful directions for future research.

## Weaknesses

### Fatal

None.

### Major

- **The central claim about "inductive bias" vs. training-data mimicry is not convincingly separated from the evidence.** The paper's strongest advertised finding — stated in the abstract, introduction, and discussion — is that LLMs exhibit an intrinsic inductive bias toward IB-efficiency, "not merely mimicking patterns in their training data." However, the IICLL experiment uses color stimuli (sRGB coordinates) drawn from the same domain the models were extensively trained on. When IICLL presents pseudo-labels alongside sRGB coordinates, the model could be using its pre-learned representations of color similarity — learned from human data — and simply relabeling pre-existing clusters with the provided pseudo-words. The convergence to IB-efficient systems would then reflect the fact that human color categories are IB-efficient, not that the model has an intrinsic bias. The iterated learning framework (Griffiths & Kalish, 2007) shows that chains converge to the learners' prior, but an LLM's "prior" over color category systems is the posterior from training on human language data — not a clean inductive prior. The paper acknowledges this ambiguity partially in the Discussion ("the precise origins of the bias we observe... are unclear") but the abstract and introduction frame the results as demonstrating a human-like inductive bias, overstating what the evidence cleanly separates. This is an evidential gap, not a fatal flaw — the descriptive contributions stand — but the interpretation goes beyond what the experimental design can differentiate.

- **The paper's strongest results depend on a single proprietary model (Gemini 2.0).** Gemini is the only model that recapitulates the wide range of near-optimal IB-tradeoffs observed in humans; the other three large instruction-tuned models (Gemma 3 27B, Qwen 2.5 32B, Llama 3.3 70B) all converge to low-complexity solutions. The rotation analysis finds "significant" results only for Gemini. The Shepard circles experiment only tests Gemini. This means the paper's headline result — that LLMs can evolve human-aligned semantic categories via IB-efficiency — effectively rests on one model whose training data and architecture are not fully disclosed. The paper is transparent about this in the results sections, but the abstract and conclusions do not adequately caveat it. A reader could come away thinking this is a general property of LLMs when the evidence shows it is a property of one LLM under specific prompting conditions.

### Minor

- **Statistical reporting is incomplete for key comparisons.** The rotation analysis (line 145) reports a "significant decrease" without specifying the test used, test statistic, or p-value. The claim that "Gemini's efficiency and alignment over generations are higher than the human IL trajectories" lacks quantification of how much higher and whether this comparison controls for the different numbers of chains and generations. Given the small number of human IL chains (20 chains across 4 conditions), proper statistical treatment is essential.

- **The controlled-generation vs. log-probability scoring confound is noted but not discussed as a potential explanation for Gemini's superior IICLL performance.** The paper mentions the difference in inference method (line 81) but does not address whether this could systematically advantage Gemini in the IICLL task, which requires integrating dozens of in-context examples.

- **The Shepard circles experiment (Section 4.3) is presented as a main result but is too preliminary to support the domain-generality claim.** Only Gemini is tested with k=4, only 4 chains are shown, no IB-efficiency analysis is performed (the paper explicitly defers this to future work), and results are described only qualitatively. The paper's own language is appropriately cautious ("preliminary investigation," "potentially have a domain-general bias"), but including this as a standalone subsection (4.3) rather than a preliminary observation in the Discussion gives it more weight than the evidence supports.

- **The human-to-LLM comparison in IICLL has unacknowledged asymmetries.** Human participants in Xu et al. (2013) learned from limited training examples and generalized to all 330 WCS chips — a genuine inductive learning task. In IICLL, the model performs few-shot pattern matching within its context window, drawing on pre-learned representations of color space. Human chains used different participants per generation; LLM chains reuse the same model. The paper acknowledges that the task "requires very strong in-context learning" but does not discuss how these fundamental differences affect the interpretation of the inductive bias claim.

### Trivial

None.

## Nice-to-Haves

- An analysis of *why* instruction-tuning improves color naming performance (is it improved color representations, better instruction-following, or something else?) would strengthen the paper.
- The CIELAB finding (all models struggle) is intriguing but unexplored; a brief discussion of why this asymmetry between LLMs and humans exists would be valuable.
- A control experiment where models undergo IICLL with systematically anti-efficient labels (rather than random initialization) would help distinguish whether the bias is directional toward efficiency or simply away from randomness.

## Removed Points

These points are flagged to be removed; treat them with caution:

- Criticisms about missing related works: REMOVED per hard rules (cannot confirm existence or non-existence of unmentioned works without external sources).
- Criticisms about missing appendix content, proofs, or references: REMOVED — the parser strips these sections; they exist in the original submission.
- Formatting/style nitpicks: REMOVED — parser artifacts.
- Generic criticisms about evaluation lacking rigor without concrete anchors: REMOVED per filtering discipline.
- The critic's claim that the Shepard circles experiment "was meant to address" the inductive-bias concern specifically: The paper frames Shepard circles as about domain generality, not as a direct test of the inductive-bias claim. This framing was slightly inaccurate, so the corresponding criticism was reframed.
- The critic's "missing analysis of why instruction tuning matters" was moved to Nice-to-Haves.

## Novel Insights

The harsh critic's key insight is that the paper's central interpretive claim conflates two distinct explanations — an intrinsic inductive bias toward IB-efficiency versus the propagation of training-data statistics that happen to be IB-efficient — and that the current experimental design cannot cleanly separate them. This is a useful framing for interpreting the paper's contribution, but it is a critique of the paper's framing rather than a novel positive insight.

## Suggestions

1. **Temper the inductive-bias claim throughout the paper.** Reframe the central finding descriptively: LLMs can evolve IB-efficient category systems through cultural transmission when the model has strong in-context learning capabilities. Label the "inductive bias" interpretation as one possible explanation and clearly acknowledge the confound with training-data statistics.
2. **Add statistical details** (test name, test statistic, p-value, effect size) to the rotation analysis and all group comparisons.
3. **Discuss the controlled-generation vs. log-probability scoring confound** explicitly — ideally with a control experiment showing that the inference method does not drive the main result, or at minimum a paragraph explaining why this is unlikely to explain Gemini's superior performance.
4. **Either strengthen the Shepard circles evidence** (run more models, perform IB-efficiency analysis) or move it to the Discussion as a preliminary observation rather than a standalone result section.
5. **Add an explicit caveat to the abstract and conclusion** that the full range of near-optimal IB tradeoffs was observed only in Gemini 2.0, not in LLMs generally.

## Score and Decision

**Calibration anchors considered:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fN8yLc3eA7.md` (avg 6.00, Round 1 & 2, itemized): "When LLMs Play the Telephone Game" — similar topic (iterated cultural transmission in LLMs), but that paper has much more severe weaknesses (very small sample size, no theoretical grounding, -6.74 weighted weakness items) than the current paper. This paper has stronger theory grounding and more thorough experimentation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XrsOu4KgDE.md` (avg 7.00, Round 2, itemized): "Attributing Culture-Conditioned Generations to Pretraining Corpora" — similar in studying LLM cultural knowledge, but that paper introduces a novel framework (MEMOED) while being limited to one model (OLMo-7B). The -2.54 weighted weakness severity is comparable to this paper's -2.40, but that paper's strengths peak higher (+6.35 vs +5.58).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nyuaoVnVCa.md` (avg 2.33, Round 1, itemized): Emergent spatial language paper — much weaker contribution with poorly written presentation, extremely negative weights.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YcML3rJl0N.md` (avg 7.00, Round 1, itemized): IB-EDL calibration paper — more technical/theoretical contribution with very strong experimental results but also a -11.00 weakness item about computational overhead.

**Round 1 bracket:** Between 5.5 and 7.5 based on topic similarity to the telephone game paper (6.00) and the culture attribution paper (7.00).

**Narrowing rationale:** My draft's weighted items show strengths peaking at +5.58 and weaknesses bottoming at -2.40. Compared to the 6.00 telephone game anchor (strength peak +6.13, weakness bottom -6.74), this paper has much milder weaknesses (no "originality: none" or "sample size too small" complaints). Compared to the 7.00 culture attribution anchor (strength peak +6.35, weakness bottom -2.54), this paper has slightly weaker strength peaks but comparable weakness severity. This places the paper above 6.0 (since its weaknesses are far milder than the 6.00 anchor) but below 7.0 (since its strongest strengths don't reach the novel-framework level of the 7.00 anchor). The shared heavy-weight items with the 6.00 anchor are the iterated-transmission methodology (positive in both cases); the missing heavy-weight items from the 7.00 anchor are a novel formal framework or causal analysis method (this paper adapts existing frameworks rather than introducing a new one).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>