Now I have all the information needed to write the final merged review. Let me compose it.

## Summary

This paper proposes AdaBoN, a two-stage adaptive Best-of-N alignment method. Given a batch of K prompts and a per-prompt budget B, Stage 1 allocates d samples per prompt to estimate reward distributions via Gaussian KDE; Stage 2 uses the estimated distributions to greedily allocate the remaining budget across prompts. The method is training-free, model-agnostic, and latency-friendly (only two rounds of LM calls). Experiments on AlpacaEval, HH-RLHF, and PKU-SafeRLHF with 12 LM-RM pairs and 50 batches per setting show that AdaBoN consistently achieves BWR > 0.50 against the uniform baseline.

## Strengths

1. **Well-motivated and clearly framed problem.** The paper correctly identifies the inefficiency of uniform BoN allocation and grounds its two-stage design in practical latency constraints (Section 2.3, lines 92–96). The framing around small-batch, large-budget regimes for on-device inference is explicit and defensible.

2. **Simple, principled, and practical method.** AdaBoN uses only off-the-shelf components (Gaussian KDE with Scott's rule, greedy allocation with a concavity guarantee via Proposition 3.1). It requires no training, works with any LM-RM pair out of the box, and has a single hyperparameter (d). The latency advantage (two rounds of LM calls) is a genuine strength over more adaptive but sequential approaches.

3. **Comprehensive evaluation scope.** The evaluation covers 12 LM-RM pairs × 3 datasets × 50 batches with multiple batch sizes (K ∈ {3,5,10,15,20}) and budgets (B ∈ {80,100,120,140,160}). This is substantially more extensive than the closest prior work (Damani et al., 2024), which uses a single LM-RM pair and a single batch.

4. **Well-designed evaluation metrics.** BWR (Eq. 3) correctly handles the ordinal nature of reward model outputs using pairwise comparison with tie-weighting, and EST (Eq. 5) provides an interpretable computational-savings measure. These improve over raw expected reward comparisons.

5. **Honest limitations section.** Section 5 (lines 244–247) explicitly acknowledges the KDE assumption, the lack of dynamic refinement, and the batch assumption, without overclaiming.

## Weaknesses

### Fatal
None.

### Major

- **No comparison against any adaptive baseline.** The paper compares AdaBoN only against the uniform allocation — the minimax-optimal *non-adaptive* baseline (line 82). While beating uniform is a necessary first check, the paper does not compare against any alternative adaptive strategy (e.g., allocating extra samples to the prompt with the lowest current max reward, or a thresholding heuristic motivated by the paper's own Bernoulli example in lines 84–86). Without such comparisons, the evidence does not distinguish whether AdaBoN's specific KDE+greedy machinery is beneficial or whether *any* reasonable adaptive rule would achieve similar gains. This limits the strength of the paper's central claim about the method itself.

### Minor

- **Exploration budget consumes 75% of the per-prompt budget, which limits the practical significance of the adaptive allocation.** With d = 0.75B (e.g., d=90, B=120), only 25% of the budget is available for adaptive reallocation. The median BWRs of 0.54–0.62 (Table 1) represent 4–12 percentage points above uniform, and the ESTs of 148–156 (Table 2a) suggest competitiveness with ~23–30% larger budgets. These are positive but modest results. The paper emphasizes upper-end framing ("win rates as high as 70%," "33% larger"), but the typical gains are smaller, and the large exploration commitment leaves limited room for adaptivity to matter. The key ablation suggested by the reviewer (replacing Stage 2 with uniform allocation) would reproduce the uniform baseline and thus is already tested — but the fact remains that the adaptive handle is relatively small.

- **Numerical error in the justification for not comparing against Damani et al. (2024).** The paper states (line 188) that comparing against Damani et al. would require training "216,000 MLPs" (12 LM-RM pairs × 3 datasets × BK=600). The correct figure is 12 × 600 = 7,200 MLPs (one per LM-RM pair per budget value, not per dataset). Even 7,200 is computationally heavy, but the order-of-magnitude error suggests the calculation was not carefully checked and weakens the paper's stated justification.

- **The motivating Bernoulli example (binary rewards, lines 84–86) differs qualitatively from the experimental setting (real-valued, continuous rewards).** In the Bernoulli case, a single exploration sample can reveal the exact prompt difficulty (p=0.95 vs p=0.05). For continuous reward distributions, the signal from the exploration phase is much weaker. The paper does not acknowledge this gap.

- **EST estimates are truncated at 2B (line 215), but the paper does not report what fraction of runs hit this truncation bound.** If a non-negligible fraction of runs have survival times ≥ 2B, the reported ESTs are biased downward, and the "20% larger budget" claim may be conservative in an uncontrolled way.

- **The claim that reward distributions are "smooth and easy to learn" (line 27) is supported only by visual inspection of histograms (Figure 1).** No quantitative measure of smoothness or learnability is provided. This is a minor overclaim in the listing of contributions.

### Trivial
None.

## Nice-to-Haves

- Adding even a single simple adaptive baseline (e.g., "allocate remaining samples to the prompt with the lowest current max reward") would substantially strengthen the empirical evaluation. A comparison against a thresholding heuristic (stop allocating to prompts whose max reward exceeds a quantile) would also be informative and could connect the experimental evaluation to the Bernoulli motivation.

- A partial comparison against a simplified version of Damani et al. (2024) — e.g., on a single LM-RM pair and a single dataset — would better position the contribution relative to the closest prior work, even if a full reproduction is impractical.

- An analysis of how KDE estimation error (from d samples) and Monte Carlo estimation error (from m=1024 samples per V_{i,j}) compound would help understand the robustness of the method. This is acknowledged as a limitation but not analyzed.

## Removed Points

- **Issue from Harsh Critic: "The ablation replacing Stage 2 with uniform allocation would isolate the effect of adaptivity."** REMOVED — this critique misunderstands the paper's setup. In AdaBoN, exploration samples (R_{i,1:d}) are included in the final max (Eq. 2, line 104). A uniform allocation in Stage 2 would give each prompt 90+30 = 120 total i.i.d. samples, which is statistically identical to the uniform baseline. The paper already tests AdaBoN vs. uniform, which IS a test of whether adaptive Stage 2 allocation helps. The critic's suggested ablation would not provide new information.

- **Issue from Harsh Critic: "Gains are modest in absolute terms — median BWR 0.54–0.62 is only 4–12 points above 0.50."** REMOVED — this is about framing, not evidence. The paper's claim is that AdaBoN "outperforms" uniform, which is supported. BWR > 0.50 on every LM-RM pair is a clear positive result. The paper does include the full distribution (medians with Q1, Q3) and also reports the high end, which is standard practice.

- **Section-by-section notes** about missing confidence intervals, the smoothness overclaim, missing discussion of error compounding, and the "small batch, large budget" regime justification — these are either too minor to list separately, or likely addressed in the now-stripped appendix. The smoothness overclaim is retained above as a minor point; the rest are subsumed into other issues or are nice-to-haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add at least one simple adaptive baseline** (e.g., allocate remaining budget to the prompt with the lowest current maximum reward, or a thresholding rule along the lines of the Bernoulli example). This directly addresses the main evaluative gap.
2. **Correct the MLP count** (line 188) from 216,000 to the proper figure (7,200 or 21,600) and, if possible, include a limited comparison against Damani et al. (2024) on a representative subset.
3. **Report the fraction of runs hitting the 2B truncation bound** for the EST, so readers can assess whether the truncation bias is material.
4. **Acknowledge the gap** between the Bernoulli motivating example (where a single draw reveals difficulty) and the continuous reward setting where signal is weaker.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>