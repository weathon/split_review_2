Now let me construct the final consolidated review.

---

## Summary

This paper proposes **Regression-based Test-time Adaptation (RTA)** for vision-language models. The key idea is to train a LightGBM decision tree offline on high-confidence pseudo-labeled ImageNet images to regress from CLIP logits to cross-entropy loss, then use the trained tree at test time to select the most confident augmented views for any downstream dataset without per-instance updates. The paper includes a motivating oracle analysis ("Ceiling TTA") showing that label cross-entropy dramatically outperforms Shannon entropy for view selection, and evaluates RTA across single-label, cross-domain, and multi-label benchmarks with two CLIP backbones.

---

## Strengths

- **The "Ceiling TTA" oracle experiment (Tables 1–2) is genuinely informative.** The paper cleanly demonstrates that if ground-truth labels were available for view selection, label cross-entropy (LCE) overwhelmingly outperforms Shannon entropy — e.g., ViT-B/16 with 64 views achieves 90.2% on ImageNet-A vs. SE's 64.3%. This is a well-executed empirical observation that provides principled motivation for pursuing regression-based view selection.

- **Broad and systematic evaluation.** The paper tests on 5 ImageNet-scale single-label datasets, 10 cross-domain datasets, and 3 multi-label datasets, with two CLIP backbones (RN50 and ViT-B/16). RTA achieves the top average accuracy in nearly every main table, demonstrating consistent positive results across diverse settings.

- **Computationally light at test time.** Once the LightGBM tree is trained offline, RTA's inference requires only CLIP forward passes per view, a tree lookup, and averaging top-k views. No per-instance prompt updates, memory banks, or diffusion steps are needed, making the method practical and easy to reproduce.

---

## Weaknesses

### Fatal
None.

### Major

- **The paper does not explain how the regression tree handles datasets with different label spaces.** Algorithm 1 trains the tree on logit vectors of length 1,000 (ImageVal-12k uses ImageNet's 1,000 classes). Algorithm 2 at test time computes logit vectors whose length equals the target dataset's number of classes — 37 for Pets, 102 for Flowers, 10 for EuroSAT, 80 for MSCOCO, etc. A LightGBM decision tree expects fixed-dimensional input; the paper provides no description of dimensionality reduction, feature alignment, retraining per dataset, or any other mechanism that would allow a tree trained on 1,000-dimensional features to accept inputs of other dimensionalities. This gap directly affects the paper's central claim that the regression model is "trained once, applied anywhere" to "arbitrary test distributions." The cross-domain and multi-label results in Tables 4–6 cannot be properly evaluated without this clarification.

### Minor

- **The regression tree is trained exclusively on high-confidence samples.** The training data is filtered to CLIP confidence ≥ 0.8 (line 332). During OOD test-time adaptation, many augmented views will fall into low-confidence regions that the tree never observed during training. The paper provides no analysis of how reliably the tree's predictions extrapolate beyond its training distribution, or whether the learned logit-loss relationship holds in low-confidence regimes.

- **No uncertainty quantification is reported.** The paper does not include error bars, confidence intervals, or statistical significance tests for any result. This is especially relevant for ViT-B/16 where margins over the strongest baseline (Zero) are often small: +0.24% on IN-1k, +0.32% on IN-V2, +0.23% on IN-R, and only +0.11 average on cross-domain (68.70 vs. BCA's 68.59). Without variance estimates it is unclear whether these differences are statistically reliable.

### Trivial

- **Eq. (8) and Eq. (9) use the superscript `x_i^{reg}`** when the context describes test-time augmented views. This notation error makes the test-time procedure harder to follow than necessary.

---

## Nice-to-Haves

- A controlled ablation comparing regression-based view selection vs. entropy-based selection using the *same* augmentation configuration and filtering ratio, to isolate the contribution of the regression model more directly than the current comparison against published baseline numbers.
- An analysis of when RTA underperforms simple entropy selection, and whether the regression model's predicted losses correlate with actual pseudo-label CE on low-confidence OOD views.

---

## Removed Points

- **Gap between ceiling LCE and RTA performance (24.6pp on IN-A) "undermines the claimed mechanism."** Removed because the paper uses the ceiling exclusively as motivation and an oracle bound — it never claims RTA would approach that bound. The gap between an oracle and a practical approximation is expected, not contradictory.
- **"The regression model learns a slightly transformed version of CLIP's confidence, not true correctness."** Removed because pseudo-label CE is mathematically distinct from confidence/entropy, and the paper's claim is that regression on pseudo-label CE provides better view selection than entropy. This is an interpretation dispute, not a concrete error in the paper.
- **t-SNE visualization does not demonstrate joint structure.** Removed as speculative; the paper uses t-SNE only as qualitative illustration and relies on experiments as the actual evidence.
- **Criticism about the "paradigm" not being novel (Kim et al. 2020).** Removed because the paper clearly distinguishes its design choices (tree-based, pseudo-labels, offline, cross-domain) from the closest prior work. The criticism is a subjective assessment of degree of novelty, not a factual error.

---

## Novel Insights

None beyond the paper's own contributions. The most incisive observation from the review process — the unexplained dimensionality mismatch — is surfaced as the Major weakness above. Other reviewer observations either restate the paper's own content or fail to hold up against the actual text.

---

## Suggestions

1. **Clarify how the regression tree trained on 1,000-class ImageNet logits is applied to datasets with different label spaces.** If the authors always compute 1,000 ImageNet-class logits at test time (while using target-class logits for the final prediction), state this explicitly. If a different mechanism is used, describe it in full.
2. **Report results with variance estimates** (multiple random seeds or bootstrapped confidence intervals), particularly for ViT-B/16 where margins over strong baselines are often <1%.
3. **Analyze the regression tree's behavior on low-confidence views**, e.g., by comparing predicted vs. actual pseudo-label CE on a held-out OOD validation set, to assess whether the tree trained on high-confidence samples generalizes reliably.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>