## Summary

This paper develops a theoretical framework for data curation in high-dimensional binary classification. Using random matrix theory, it derives exact test-error formulas under label-agnostic and label-aware pruning rules (Theorems 1–3). The key result (Theorem 2) predicts that optimal pruning flips from "keep hard" when the data generator is strong to "keep easy" when the generator is weak. The authors validate the theory on synthetic data, present ImageNet experiments, and interpret recent LLM reasoning results (LIMO, s1) through the theory's lens.

## Strengths

1. **Crisp, interpretable theoretical result.** Theorem 2 is a clean formalization: when the labeling generator is already excellent, focus on hard examples; when it is poor, focus on easy ones. This matches practitioner intuition and gives a principled condition for when "less is more" applies.

2. **Unified framework extending prior work.** The label-aware curation rule (Eqn 6) subsumes the label-checking oracle models of Feng et al. and Firdoussi et al. as a special case (Remark 1), while adding difficulty-based selection. This generalization captures how real pipelines like LIMO/s1 combine correctness filters with difficulty filters.

3. **Timely, well-posed question.** The apparent tension between "less is more" (LIMO, s1) and "more is more" (scaling laws) is a live debate, and the paper correctly targets a theory that explains when each regime applies.

## Weaknesses

### Fatal
None.

### Major

1. **ImageNet experiments are critically underspecified in the main paper.** Section 4.3 spans roughly 15 lines. The text never states what model architecture was used (only "a pre-trained model" with references to MMPreTrain and Dosovitskiy et al. in the bibliography, but no explicit architecture in the main text). It does not explain how margin-based "keep easy" / "keep hard" pruning was operationalized for 1000-class ImageNet images — the theory is for binary classification with margin defined by projection onto an oracle vector. Training hyperparameters, data subsets, and number of runs are absent. The rightmost panel of Figure 2 shows error rates around 30% even for ground-truth labels, which is unusually high for modern ImageNet classifiers; no explanation is given. The text references Appendix B ("For a comprehensive set of validations..."), which may contain these details in the full submission, but the main paper as presented cannot be evaluated on its own. This matters because the abstract and contributions list ImageNet validation as a main pillar of the paper.

2. **Synthetic experiments omit the direct comparison needed to test Theorem 2.** Figure 1 compares "keep hard" against random pruning. But Theorem 2 predicts *which strategy is optimal* — keep-hard for strong generators, keep-easy for weak generators. Testing this requires comparing keep-hard against keep-easy in each regime. The current design (keep-hard vs. random) shows that informed pruning beats uninformed pruning, but does not discriminate between the two strategies the theory distinguishes. (The ImageNet experiments in Figure 2 do make this comparison, partially mitigating this gap, but the controlled synthetic setting — where theory and practice can be directly matched — is where it matters most.)

3. **LLM reasoning section (4.2) is post-hoc narrative, not a test of the theory.** The paper presents two tables from prior work and asserts that the theory "resolves" the paradox. However: (a) no attempt is made to measure ρ (generator quality) for the Qwen models on the relevant AIME subsets; (b) no predictions are derived and tested against held-out data; (c) the "explanation" — that the base LLM is a strong generator for average problems but a weak generator for hard problems — is essentially restating the observation and labeling it with ρ. The paper's own limitations paragraph notes that real-world data is far from Gaussian binary classification, yet Section 4.2 is presented as supporting evidence rather than speculative interpretation. The contributions list says the paper "provides a rigorous justification for why methods like LIMO and s1 succeed"; this overstates what Section 4.2 can support.

### Minor

4. **Model collapse experiment lacks a "keep easy" baseline.** Figure 3 compares "keep hard" against "train on all data" but does not test whether "keep easy" also stabilizes training. Since Theorem 2(B) predicts that keep-easy is optimal for weak generators (which an iteratively retrained model becomes), this missing condition weakens the empirical case.

5. **Model collapse experiment uses a changing model but the theory assumes a fixed oracle wₒ.** The flow diagram shows that at each round, a new model f⁽ⁱ⁾ generates labels and presumably determines the pruning direction. The theory (Theorem 2) assumes a fixed pruning direction wₒ, but in iterative self-training the model — and hence any margin-based difficulty score — changes each round. The paper does not discuss how this affects the validity of applying the theory to the iterative setting.

6. **No quantitative goodness-of-fit for synthetic theory-experiment comparison.** Figure 1 shows dashed empirical curves matching solid theoretical curves qualitatively, but no numeric metric (e.g., RMSE, correlation) is reported. The number of synthetic runs and parameter values (d, λ, etc.) are not stated in the main text.

7. **Theorem 2 is derived in the double limit φ→0 (data-rich), λ→0 (unregularized).** This is the interpolating regime. The paper does not discuss how robust the optimal-pruning conclusions are to finite φ and λ, even though practical settings (including the motivating LLM examples) may be far from interpolation. A brief discussion of expected deviations would strengthen the connection to practice.

### Trivial
None.

## Nice-to-Haves

- **Quantitative prediction testing of Theorem 1.** The exact formula in Theorem 1 could be tested by measuring the constants in Eqn (8) from synthetic data and comparing predicted vs. observed error numerically, rather than only through qualitative curve shapes.
- **Comparison with Sorscher et al. (2022).** Since Sorscher et al. empirically showed that margin-based pruning bends neural scaling curves, a direct comparison — e.g., checking whether the theory reproduces their observed scaling exponents — would be a natural validation.
- **Test the LLM interpretation more rigorously.** A controlled experiment using a small transformer on a synthetic math-like task with known label quality would demonstrate that the theory makes testable predictions.

## Removed Points

These points were flagged by the harsh reviewer but are removed for the following reasons:

- **"Scaling law framing overclaims"** — Removed. The paper's Theorem 1 provides exact functional forms for test error as a function of data dimensions and pruning, which is a scaling law in the precise sense. Showing that pruned data can outperform full data is a legitimate "bending" of the monotonic-improvement prediction. The reviewer's complaint that this doesn't match the Kaplan/Hoffmann empirical paradigm is a framing preference, not an error.
- **Missing architecture / detail about ImageNet experiments** — This is kept in Major Weakness #1 above but rebalanced: the paper references Appendix B for details, so the issue is insufficient main-text exposition rather than total absence.
- **"Theorem 2 requires ρ_* → 1 (excellent pruner)"** — Removed as a standalone point. This is part of the theorem's stated assumption; every theorem has assumptions. The reviewer's implied request for robustness to imperfect oracles is reasonable but captured indirectly by the acknowledgment that the theory's setting is idealized.
- **"Model collapse prevention in ImageNet is remarkable but unsupported"** — Merged into Major Weakness #1 rather than kept as a separate point.
- **"Section 4.1 footnote: for strong generator, ρ_* = ρ = 1 means perfect pruner"** — This matches Theorem 2's assumption. Not a weakness.
- **Pure reproducibility complaints** (undisclosed hyperparameters, missing training logs) — Removed per policy; these are standard expectations for appendix placement.
- **Related work comparisons / missing references** — Removed per policy; cannot verify.

## Novel Insights

None beyond the paper's own contributions. The harsh review's main insight is that the empirical sections do not match the strength of the theoretical contribution, and that the paper would be more credible if it either supplied full experimental details or scaled back the empirical claims. This is accurate but does not constitute a novel observation about the paper itself beyond what the weaknesses already convey.

## Suggestions

1. **Add the keep-easy curve to Figure 1.** Directly compare keep-hard vs. keep-easy vs. random in the synthetic experiments. This would directly test Theorem 2's distinctive two-sided prediction.
2. **Provide full experimental details for ImageNet** in the main text (or a clearly referenced appendix): architecture, how margin-based pruning was adapted for 1000 classes, training hyperparameters, data splits, and the significance of the ~30% error baseline.
3. **Reframe Section 4.2** as interpretive speculation rather than validation. The phrase "rigorous justification" in the contributions list should be tempered to match what the evidence supports.
4. **Add a "keep easy" baseline to the model collapse experiment** and discuss how the changing model relates to the fixed-oracle assumption in the theory.

## Score and Decision

The paper presents a genuinely valuable theoretical contribution (Theorem 2 is crisp, well-motivated, and fills a gap in the literature). However, the empirical validation — which the paper prominently features as a main contribution — is substantially weaker than claimed. The ImageNet experiments lack essential detail, the synthetic experiments omit the most informative comparison, and the LLM section offers interpretation rather than evidence. These gaps can be addressed with a major revision, but in the current form the empirical claims are not adequately supported.

**Score: 6** (borderline accept)

**Decision: Accept**

<score>6</score>
<decision>Accept</decision>