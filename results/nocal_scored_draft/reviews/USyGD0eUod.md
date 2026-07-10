Now I have all the data I need. Let me synthesize the final consolidated review.

---

## Summary

This paper applies a sanity check — inspired by Adebayo et al. (2020) — to SAE evaluation metrics: do commonly used auto-interpretability measures (fuzzing/detection AUROC) distinguish SAEs trained on real transformers from those trained on randomly initialized ones? Testing across Pythia models (70M–6.9B) with multiple randomization schemes, the paper finds that aggregate AUROC scores for trained and randomized models are often surprisingly similar, especially at larger scales, and can even reverse direction. The paper also identifies token distribution entropy as a metric that *does* separate the two settings. The core finding — that standard automated interpretability metrics can be insufficient on their own — is a timely and important signal for the interpretability community.

## Strengths

- **Timely and well-motivated sanity check.** Drawing an explicit parallel to Adebayo et al. (2020)'s influential sanity checks for saliency maps, the paper applies the same logic to SAE evaluation — a natural and valuable move given the rapid growth of the SAE literature and relatively thin validation of its metrics. (Favorability: 0.81–1.00)

- **Broad experimental scope.** The paper tests five Pythia model sizes (70M to 6.9B), multiple layers per model, and four randomization schemes (Step-0, re-randomized incl./excl. embeddings, Gaussian-embedding control). This breadth makes the core observation — that the trained/randomized gap narrows at larger scales — substantially more credible than a single-model study would be. (Favorability: 1.00)

- **Constructive finding: token distribution entropy.** The last row of Figure 2 identifies a metric that does distinguish trained from random models: trained models show increasing token entropy with layer depth, while randomized variants do not. This goes beyond a purely negative result and points toward a concrete alternative that captures feature "abstractness." (Favorability: 0.92–0.97)

## Weaknesses

### Fatal
None.

### Major

- **The title overstates the paper's own evidence.** The title reads "Automated Interpretability Metrics Do Not Distinguish Trained and Random Transformers," which is too categorical. The paper's data shows a more nuanced picture: (a) for Pythia-70m, auto-interpretability AUROC *does* distinguish trained from random — the paper acknowledges this at line 49; (b) for Pythia-6.9b, randomized variants score *higher* (AUC 0.87–0.88) than the trained model (AUC 0.79), a reversal the paper reports but does not analyze; (c) the paper's own token distribution entropy metric successfully distinguishes the two settings. The abstract and conclusion are appropriately qualified ("in many settings," "under certain conditions"), but the title communicates a broader claim than the evidence sustains. (Favorability: 0.15)

- **No direct comparison of what SAEs actually learn across settings.** The paper never quantitatively compares the feature dictionaries themselves (decoder weight matrices) across trained vs. randomized conditions. This is the most important missing analysis: without knowing whether the learned features are similar or different, the paper cannot distinguish two very different interpretations — (i) the SAEs learn genuinely different features but the metrics miss this (the alarming interpretation), vs. (ii) the SAEs learn similar features across settings, in which case metric similarity would be less concerning. Cosine similarity between dictionaries, overlap in top-activating tokens, or comparisons of maximal-activation token IDs would all be straightforward to compute from data the authors already have. Qualitative examples are deferred to Appendix J, but quantitative dictionary comparison belongs in the main text. (Favorability: 0.20)

### Minor

- **No uncertainty quantification on core AUROC estimates.** The paper samples 100 features per SAE (line 77) and reports point estimates of AUROC (e.g., 0.79 vs. 0.87) without confidence intervals, error bars, or standard deviations in the main figures. Appendix E is referenced for multiple random seeds, but the reader cannot assess whether the observed differences (or lack thereof) are statistically meaningful from the main presentation. (Favorability: 0.31)

- **The Pythia-6.9b AUROC reversal is reported but unanalyzed.** That randomized models achieve *higher* AUROC (0.87–0.88) than the trained model (0.79) is arguably the paper's most surprising finding. The paper describes the curves as "overlapping" and moves on. This merits its own analysis — is it because trained models learn more abstract features that resist concise description? The token entropy result is consistent with this hypothesis but the link is not made explicitly. (Favorability: 0.24)

- **The toy model section (Section 4.1) is mathematically thin.** Showing that linear transformations preserve superposition (Section 4.1) is linear-algebra basics that does not add insight. The more interesting material is in Sections 4.2–4.3, but their connection to the main transformer experiments remains loose. The paper could be tightened by cutting Section 4.1 and expanding the discussion of why random MLP outputs show consistent sparsity regardless of input. (No favorability score explicitly — this is my own judgment from the text.)

### Trivial
None.

## Nice-to-Haves

- The CE loss score limitation (lines 89–90) is already transparently acknowledged — a reader looking for a weakness here should note that the paper handles this honestly rather than hiding it.
- The "we speculate" pattern (lines 85, 87, 127) is common and acceptable in empirical work, but testing even one of these conjectures would strengthen the explanatory contribution. This is a minor presentation point, not a core flaw.

## Removed Points

- **Control condition "not informative" (from Harsh Critic Issue 4).** The reviewer argued the control was used to draw a non sequitur. In fact, the paper uses the Gaussian-embedding control as a standard floor to verify the metrics are not completely degenerate (AUROC ≈ 0.50). The main comparison is directly between trained and randomized variants. This criticism misreads the paper's experimental design and is removed.
- **CE loss score limitation (from Harsh Critic Issue 5).** The paper explicitly states at lines 89–90: "Importantly, the CE loss score only makes sense for the trained variant." The paper acknowledges this limitation; flagging it as a weakness is redundant.
- **Generic framing concerns.** Claims about "the evaluation lacks rigor" or "could be measuring a proxy" without a specific anchor in the paper are removed as category-driven noise.
- **Untested speculations criticism.** While the paper does use "we speculate" three times, this is normal practice in empirical work. The criticism was kept as a "nice-to-have" rather than a retained weakness. The 0.00 favorability from the scoring model confirms this item has low utility in the final review.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no observation about the paper that the paper does not already state or imply.

## Suggestions

1. **Revise the title** to reflect the nuanced finding, e.g., "Aggregate Auto-Interpretability AUROC May Not Reliably Distinguish Trained from Random Transformers at Scale."
2. **Add direct quantitative comparison of SAE feature dictionaries** across trained vs. randomized conditions — cosine similarity between decoder weight matrices, overlap in top-activating tokens, or similar analyses.
3. **Report confidence intervals or bootstrapped error bars** on AUROC estimates in the main figures.
4. **Explicitly analyze the Pythia-6.9b reversal** — why do randomized models achieve higher AUROC than trained? Connect this observation to the token distribution entropy finding.
5. **Tighten the toy model section** by cutting Section 4.1 (mathematically trivial) and expanding the discussion of why random MLP outputs exhibit consistent sparsity regardless of input (the finding at line 153).

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>