Here is the final consolidated review.

---

## Summary

This paper investigates whether translating evaluation benchmarks into Arabic can mask data contamination in LLMs. The authors fine-tune four open-weight models on varying proportions of Arabic-translated test items and evaluate on English benchmarks, using a choice-reordering extension of TS-Guessing as a memorization probe. The core claim is that Arabic translations conceal contamination signals while models still benefit from exposure, creating a blind spot in multilingual evaluation.

## Strengths

- **Novel and timely research question.** The paper identifies a genuine gap in the contamination literature — whether translation into lower-resource languages can obscure contamination signals — which has not been systematically studied before (Section 1, Abstract).
- **Choice-reordering extension of TS-Guessing.** Adapting TS-Guessing for multiple-choice questions by shuffling options and masking incorrect choices is a sensible probe design for detecting memorization of index patterns (Section 3.3, Figure 1).
- **Cross-model scope.** The study includes four models spanning three families and a range of sizes (1B–7B), providing some breadth for observing whether effects are consistent or scale-dependent (Table 2, Table 3).

## Weaknesses

### Fatal
None.

### Major

1. **The p=0 baseline is itself contaminated, and the design conflates contamination with data augmentation.** The training set `D_EN^d` uses English *test items* at every contamination level including p=0 (Section 3.1, Eq. 1, lines 128–142). This means the "clean" condition already fine-tunes on the exact evaluation data. Adding Arabic translations (p>0) increases total training data, so any accuracy gains (e.g., Mistral MMLU: 0.577→0.690) could reflect straightforward data augmentation benefits rather than contamination-specific effects. No English-only control is run at matched data quantities, making it impossible to attribute any observed pattern — flat or otherwise — to translation specifically. Without both a genuinely clean baseline and an English-only contamination control, the paper's central claim that translation "masks" contamination is not supported by the experimental design.

2. **TS-Guessing results contradict the paper's interpretation.** The paper states that TS-Guessing scores are "broadly stable" and "approximately equal" across contamination levels, interpreting this flatness as evidence that translation masks detection (Section 4.2, lines 201–208, 216–218). However, Table 3a shows substantial variation that is inconsistent with this claim:
   - **Gemma-3-1B-it IDR**: 0.350 → 0.029 → 0.005 (drops by two orders of magnitude)
   - **LLaMA-3.2-1B-Instruct IDR**: 0.287 → 0.643 → 0.410 (more than doubles then drops)
   - **Qwen3-1.7B IDR**: 0.261 → 0.251 → 0.208 (monotonically decreasing)
   
   For Gemma and Qwen, IDR *decreases* as contamination increases — the opposite of what the contamination hypothesis predicts. Mistral IDR is essentially zero at all levels (0.000→0.000→0.001), suggesting no detectable memorization. The paper does not discuss these patterns. A near-zero or decreasing TS-Guessing signal is better interpreted as *no detectable contamination* rather than "contamination masked by translation."

3. **The paper claims translation "conceals traditional contamination signals" but never tests existing detection methods on Arabic data.** The paper surveys methods like Min-K% Prob, guided prompting, and BM25 search (Section 2.3) but runs none of them on the Arabic-translated data to demonstrate their failure. The central claim that translation creates a "blind spot" for existing detection tools is asserted without empirical evidence.

4. **Unsupported claim about "stronger Arabic capabilities."** The abstract and introduction claim that models benefit "particularly those with stronger Arabic capabilities" (lines 9, 17). Arabic proficiency is never measured — no Arabic perplexity, Arabic benchmark scores, tokenizer coverage, or any other metric is reported. This claim is asserted without evidence.

### Minor

1. **TACD framework is claimed as a contribution but not implemented or validated.** The abstract presents TACD as a contribution ("we propose a Translation-Aware Contamination Detection framework"), but Section 5.3 explicitly states it is "a forward-looking blueprint rather than a complete implementation." No experiments, metrics, baselines, or comparisons evaluate TACD. It should either be implemented or moved to a "Future Work" paragraph.

2. **No measures of variance reported.** All results in Tables 2 and 3 are single values without confidence intervals, standard deviations, or multi-seed runs. Given modest effect sizes (e.g., Qwen MMLU: 0.553→0.581) and the small model sizes where fine-tuning outcomes can be sensitive to initialization, it is impossible to assess whether observed differences reflect real signals or random variation.

3. **Embedding similarity analysis is referenced but not shown in the main text.** Section 4.3 (line 224) mentions an "embedding figure" showing high cosine similarity between Arabic→English translations and their English originals, but no quantitative values or figure appear in the main text. This analysis is central to the argument that translation preserves semantics while perturbing surface form.

### Trivial
None.

## Nice-to-Haves

- **Clean p=0 baseline.** The English test items should not be in the fine-tuning data at any level. A genuinely clean baseline would use only training splits or task-format-matched non-benchmark data.
- **English-only contamination condition at matched data quantities.** To directly test whether translation masks contamination, compare fine-tuning on p% of English test items vs. p% of Arabic-translated test items at the same data quantity. If the English condition yields detectable TS-Guessing signals while the Arabic condition does not (despite both producing accuracy gains), that would directly support the masking claim.
- **Test existing detection methods on Arabic data.** Applying Min-K% Prob or guided prompting to the Arabic-translated data and showing they fail to flag contamination would empirically ground the paper's qualitative claim about blind spots.
- **Address the contradictory TS-Guessing trends.** The decreasing IDR for Gemma and Qwen needs explanation. If TS-Guessing is the paper's primary memorization probe, these results undermine rather than support the narrative.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Critic's claim that the literature review is disproportionately long.* — Removed as a structural/style nitpick; it does not affect the paper's empirical validity.
- *Critic's claim about missing LoRA hyperparameters (rank, alpha, target modules) in the main text.* — Removed per the reproducibility-nitpick rule; the paper defers these to Appendix A (Section 7), which was stripped by the parser.
- *Critic's claim that the "embedding figure" analysis should have been in the main paper rather than the appendix.* — The appendix was stripped by the parser, so we cannot verify whether this analysis exists there. The remaining minor point about the analysis being absent from the main text is preserved above.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no observation that recasts the paper's results or identifies an unexamined implication that the authors themselves missed.

## Suggestions

1. Rerun the experiment with a genuinely clean baseline (no English test items in training) and an English-only contamination control at matched data quantities. This is the minimum needed to support claims about translation specifically.
2. Report TS-Guessing results with variance estimates across multiple fine-tuning seeds, and explicitly address why Gemma and Qwen IDR decrease with more contamination.
3. Apply at least one existing detection method (e.g., Min-K% Prob) to the Arabic-translated data to empirically demonstrate the claimed blind spot.
4. Either implement and evaluate TACD, or reframe it as future work and remove it from the abstract's list of contributions.
5. Measure or remove the unsupported claim about "stronger Arabic capabilities" from the abstract and introduction.

## Score and Decision

This paper asks a genuinely novel and important question, but its experimental design contains a critical confound: the p=0 baseline is already contaminated with English test items, and there is no English-only control at matched data quantities. The TS-Guessing results — the paper's primary evidence for the "masking" interpretation — are in several cases inconsistent with the paper's own narrative. Additional claims (that existing methods fail on Arabic data, that models with stronger Arabic capabilities benefit more) are asserted without empirical support. The underlying research direction is promising, but the current evidence does not support the headline conclusions. The paper requires substantial redesign before it can meet the bar for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>