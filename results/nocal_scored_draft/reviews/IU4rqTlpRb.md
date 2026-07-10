## Summary

This paper challenges the prevailing view that benign relearning (recovery of forgotten information from benign fine-tuning data) is primarily driven by topical relevance. Through controlled experiments on TOFU with carefully constructed relearn sets, the authors show that **syntactic/surface-form similarity predicts relearning better than topical relevance**, and provide a mechanism (template-vs.-keyword imbalance) to explain why. They propose **syntactic diversification**—paraphrasing forget-set queries before unlearning—as a practical remedy that demonstrably suppresses benign relearning and improves the unlearning-utility trade-off on the TOFU benchmark.

## Strengths

- **Cleanly separated experimental design on TOFU (Section 5.2).** The paper constructs topically relevant and syntactically similar relearn sets that carefully disentangle topicality from syntactic structure: the topically relevant set shares entities but not syntax, while the syntactically similar set shares syntax but not entities. This isolation of syntactic similarity as a causal factor is the paper's strongest analytical contribution, and it convincingly shows that syntactic similarity predicts relearning better than topical relevance across three unlearning methods (GA, NPO, SCRUB).

- **Non-obvious mechanism analysis (Section 6, Figure 6).** The loss-ratio analysis showing that unlearning disproportionately suppresses template tokens while leaving keyword tokens relatively intact provides a concrete, testable mechanistic explanation for benign relearning. The observation that the loss ratio balloons during unlearning but collapses during relearning is direct evidence for the proposed structural pathway.

- **The core insight is genuinely novel and practically relevant.** The claim that syntactic/surface-form structure—not topical content—can dominate benign relearning challenges the prevailing view established by BLUR and has practical implications for how unlearning robustness should be evaluated and how forget sets should be constructed.

- **Syntactic diversification (Section 7) is a simple, motivated intervention** that shows clear empirical benefit on TOFU: it suppresses benign relearning, accelerates forgetting, and improves model utility (Table 2), all while being straightforward to implement.

## Weaknesses

### Fatal
None.

### Major

1. **BLUR re-analysis is oversold relative to the evidence shown (Section 4).** The paper claims that under a fairer evaluation "the advantage of topically relevant datasets largely disappears," but: (a) Figure 3 — the only per-step trajectory shown — covers just one benchmark (WMDP) under one method (NPO); no equivalent trajectories are shown for WHP, RWKU, or the other methods. (b) The bar charts in Figure 2 still show D_hi > D_mid > D_low ordering for WMDP and RWKU across most methods; the compression pattern is clearest only on WHP. (c) The claim that D_low (Lorem Ipsum) on WHP "achieves recovery similar to D_hi and D_mid" is stated in prose without explicit numerical support. Since the paper uses this re-analysis to motivate its central thesis, the gap between the strong "largely disappears" claim and the partial evidence weakens the paper's foundation. The paper would be stronger if it acknowledged these nuances and positioned the BLUR re-analysis as suggestive rather than conclusive.

2. **Core experimental evidence is limited to a single synthetic, templated dataset (TOFU).** TOFU consists of 4,000 highly templated QA pairs with rigid syntactic structure ("What is the full name of the author born in X on Y?"). The syntactic similarity between target and relearn sets is *by construction* very high (0.4513 vs. 0.2349), making this the ideal scenario for the paper's hypothesis. The paper references additional experiments on Phi models (Appendix B.3) and a "more realistic unlearning scenario" (Appendix C), but these are not presented in the main text. The central claim that syntactic similarity is the *primary* driver of benign relearning rests predominantly on a single dataset whose artificial structure maximally favors the hypothesis. This limits the demonstrated generality, especially for natural-language scenarios (e.g., copyrighted prose, toxic comments) where syntactic structure is less rigid and less cleanly separable from topical content.

### Minor

3. **No statistical reporting.** All quantitative results (Figures 4, 5, Table 2, etc.) are presented as point estimates with no error bars, confidence intervals, standard deviations, or significance tests. While single-run evaluation is a common convention in this subfield, the paper's comparative claims about which factor is the "primary driver" would benefit from at least some characterization of variability (e.g., bootstrapped intervals or results across multiple random seeds).

4. **Levenshtein distance conflates surface form with syntax (Section 5.1).** The paper uses character-level Levenshtein distance to quantify "syntactic similarity," but this metric measures surface-form overlap (lexical overlap + edit distance), not syntactic structure in a linguistically meaningful sense. The paper acknowledges alternative metrics (parse-tree similarity, template-mining) in a footnote referencing Appendix I, but the main text's systematic use of "syntactic" for what is actually a surface-form measure conflates the two concepts. Given that the central contribution is about *syntax*, this terminology gap matters.

5. **Loss-ratio analysis (Figure 6) is presented without method specification.** The paper does not state which unlearning method produced the shown dynamics, how representative this single trajectory is, or whether the pattern holds consistently across GA, NPO, and SCRUB. Variance is also unreported for this analysis.

6. **The "max ROUGE-L across steps" criterion (Section 4)** selects the best-performing checkpoint per condition, which could differentially benefit conditions with higher variance and inflate recovery estimates. Reporting full trajectories with a fair per-step budget would be more informative.

### Trivial
None.

## Nice-to-Haves

- Show per-step trajectories for **all BLUR benchmarks and methods**, not just WMDP under NPO, to substantiate the generality of the re-analysis.
- Add at least **one non-templated, natural-language forgetting scenario** (e.g., copyrighted prose, private emails) to demonstrate generality beyond TOFU's rigid QA templates.
- Supplement or replace the Levenshtein metric with a **properly syntactic measure** (e.g., constituency tree edit distance or dependency parse similarity).
- Report **variance** (bootstrapped confidence intervals or multiple random seeds) for the key quantitative comparisons.

## Removed Points

These points from the harsh critic review were filtered after cross-checking against the paper:

- **"The 'primary driver' claim is not commensurate with the evidence"** — This concern is already fully addressed by the two Major weaknesses above (BLUR re-analysis oversold + TOFU scope limitation). No separate weakness is needed.
- **"Figure 5 comparison is asymmetric"** — This is a methodological suggestion (add random baselines for similarity), not a concrete weakness that undermines any specific claim.
- **"Syntactic diversification is simple paraphrasing"** — The paper correctly frames the novelty in the *motivation and application context*, not in the paraphrasing technique itself. This is not a weakness.
- **"No dedicated limitations section"** and **"DPO/LoRA claims without main-text data"** — These are common formatting conventions (pointers to appendices) and do not constitute substantive weaknesses.
- **Any formatting, typos, or appendix-missing complaints** — Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a pattern or contradiction that the paper itself does not already discuss or acknowledge.

## Suggestions

1. Tone down the BLUR re-analysis claim from "largely disappears" to a more measured characterization (e.g., "the advantage is reduced and varies across benchmarks"), and show per-step trajectories for all benchmarks.
2. Explicitly acknowledge that the main experimental evidence comes from a single synthetic templated dataset, and position the "primary driver" claim as applying most clearly to structurally rigid settings.
3. Supplement the Levenshtein metric with at least one properly syntactic measure to align measurement with the claimed construct.
4. Add variance estimates (even bootstrapped CIs from a single run or results over 2–3 seeds) to the key quantitative comparisons.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>