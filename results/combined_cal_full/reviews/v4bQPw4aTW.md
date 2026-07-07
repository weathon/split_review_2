Now let me finalize my review by writing the complete output.

## Summary

This paper tackles the practical problem of inefficient uniform budget allocation in Best-of-N inference-time alignment. It proposes AdaBoN, a two-stage prompt-adaptive allocation policy: first, a uniform exploration phase estimates per-prompt reward distributions via Gaussian KDE, then a greedy algorithm allocates the remaining budget based on estimated marginal gains. The method requires no auxiliary model training, limits latency to two serial LM calls, and is evaluated across 12 LM-RM pairs, 3 datasets, and 50 batches per setting.

## Strengths

- **Clean formalization of a practical problem.** Section 2.3 and Equation 1 provide a well-posed mathematical framing of the inference allocation problem for Best-of-N, making precise the notion that per-prompt budgets should vary with difficulty. (weight: +4.50)

- **Simplicity and model-agnostic design.** AdaBoN requires no auxiliary model training, works out-of-the-box for any LM-RM pair by estimating reward distributions via Gaussian KDE at test time, and is validated across 12 LM-RM pairs and 3 datasets. This contrasts favorably with training-based approaches. (weight: +4.25)

- **Latency-conscious two-stage design.** The method limits serial LM calls to two rounds (one exploration, one allocation), which is a pragmatic design choice compared to more sequential adaptive policies. (weight: +3.54)

- **Broad empirical evaluation.** The paper evaluates across 12 LM-RM pairs (4 LMs × 3 RMs), 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF), 50 batches per setting, and 100 runs per batch, consistently showing BWRs > 0.50 and ESTs around 148–156 against B=120. (weight: +5.86)

- **Well-motivated evaluation metrics.** BWR and EST appropriately handle the fact that RM scores are only meaningful comparatively, and quartiles are reported alongside medians. (weight: +2.80)

- **Honest limitations discussion.** Section 5 openly acknowledges the KDE assumption, lack of dynamic refinement, and batch setting restriction. (weight: +2.79)

## Weaknesses

### Major

- **The exploration budget d=0.75B means 75% of total compute is still allocated uniformly, severely limiting adaptivity.** With B=120, K=5, exploration consumes 450 of 600 total LM calls uniformly across prompts; only the remaining 150 calls (25%) are distributed adaptively. The paper tunes d only over {0.60B, 0.70B, 0.75B, 0.80B} (line 242) and never tests smaller values like 0.1B or 0.2B. This undercuts the claim that reward distributions are "smooth and easy to learn" (line 27) — if they were easy to learn from small samples, a much smaller d should suffice. Calling 75% a "small exploration budget" (abstract) is misleading. (weight: -3.82)

- **No empirical comparison against the most closely related prior work (Damani et al., 2024).** The paper explicitly declines comparison (line 188) citing unavailable implementation and computational cost (claiming 216,000 MLPs). The cost argument appears miscalculated: BK=600, so 600 × 12 × 3 = 21,600 (not 216,000). While the implementation availability concern is legitimate, even a limited comparison on a subset of settings would provide an informative point of reference. Without it, the paper can only claim superiority over uniform allocation, not over existing adaptive approaches. (weight: -5.95)

### Minor

- **The gains, while real, are modest relative to the paper's framing.** Median BWRs of 0.54–0.62 represent 8–12 percentage points above the 0.50 baseline, and ESTs of ~148–156 represent 23–30% effective savings, but these come from only the 25% adaptive portion. The language ("consistently and often significantly outperforms", "BWRs as high as 0.70") somewhat overstates practical significance. (weight: -0.12)

- **The Bernoulli reward example (Section 2.3) assumes a reward ceiling at 1**, making the adaptive allocation problem qualitatively different from the continuous-reward setting actually studied (FsfairX, ArmoRM, etc.) where there is no such ceiling and marginal value diminishes but never reaches zero. The intuition from the Bernoulli example does not cleanly transfer, and the paper does not acknowledge this distinction. Moreover, the example uses d=0.4B (40% exploration), while the actual method uses d=0.75B, making the gap even larger. (weight: -4.13)

- **No oracle upper bound reported.** Computing how close AdaBoN gets to the optimal allocation (knowing true reward distributions) would contextualize the BWR and EST values and show whether the remaining gap is due to estimation error or the greedy heuristic. Without this, it is unclear how much room for improvement remains. (weight: +0.28)

### Trivial

None.

## Nice-to-Haves

- An ablation isolating the contribution of the greedy allocation phase (e.g., comparing AdaBoN against a version that uses the same two-stage structure but allocates remaining budget uniformly) would quantify how much the adaptive step matters beyond simply having two stages.
- A per-prompt qualitative analysis (e.g., which prompt characteristics predict wider reward distributions that benefit from extra samples) would strengthen the practical contribution.
- Testing smaller d values (e.g., 0.1B, 0.2B, 0.3B) would help validate or refute the claim that reward distributions are "easy to learn from small samples."

## Removed Points

- **Section-by-section editorial notes and formatting nitpicks** — Removed as editorial noise (e.g., "figures not in vector format", "two decimal places").
- **Request for confidence intervals / standard errors** — The paper reports Q1/Q3 quartiles, which is standard; this is a presentation preference, not a weakness.
- **Generic strengths (e.g., "important problem")** — Removed per filtering rules; the formalization strength covers this.
- **Complaints about results being relegated to appendix** — The parser strips appendices; these placement claims cannot be verified against the available content.
- **The critic's alternative calculation of 4,320 MLPs for Damani comparison** — The critic used B=120 instead of BK=600; this miscalculation is also incorrect, though less wrong than the paper's 216,000.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Show results with substantially smaller d values (e.g., d ∈ {0.1B, 0.2B, 0.3B}) to validate the "easy to learn" claim and demonstrate that the method is genuinely adaptive rather than mostly uniform.
- Provide at least a limited comparison against Damani et al. (2024) — training even a single MLP for one LM-RM pair on one dataset would be informative.
- Recalibrate the language in the abstract and introduction to accurately reflect that 75% of the budget is spent uniformly, and frame the contribution as "a small amount of adaptivity on top of a mostly-uniform allocation" rather than a fully adaptive scheme.

## Score and Decision

**Bracket analysis:** Round 1 bracketing placed this paper between 4.0 and 6.5. The most directly relevant anchor is Damani et al. (2024) (avg 6.50, file: 6qUUgw9bAZ), which addresses the same allocation problem. Comparing weighted items: AdaBoN's strongest positive (+5.86 for broad evaluation) exceeds Damani's strongest (+4.62), but AdaBoN's strongest negative (-5.95 for no comparison against Damani) is more severe than Damani's most negative item (-5.62). The d=0.75B structural concern (-3.82) is an issue Damani et al. does not face because their approach is fully adaptive. The 5.0–6.0 range anchors (C2MAB-V at 5.50, BoN-aware FT at 5.67) exhibit similar patterns: real contributions tempered by significant weaknesses. Overall, AdaBoN offers a simpler, training-free method with broader evaluation than Damani et al., but the 75% uniform exploration and missing direct comparison prevent it from reaching the 6.50 level of its predecessor. Score 5.0 appropriately reflects a borderline-accept contribution that is real but structurally limited.

**MY FINAL SCORE: <score>5.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**