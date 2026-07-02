## Summary
This paper proposes High-Entropy Sum (HES), a metric for selecting high-quality training data for LLM reasoning. HES sums the per-token entropy of only the top 0.5% highest-entropy tokens in each reasoning trajectory, motivated by the hypothesis that these tokens correspond to critical "forking points" where the model makes non-trivial decisions. The authors validate HES across three training paradigms (SFT, RFT, RL) on math, code, and STEM benchmarks using Qwen3-8B and DeepSeek-R1-distilled models. In SFT, training on the top 20% HES-ranked data matches full-dataset performance, while pruning the lowest-HES 20% consistently improves over using all data. In RFT, HES outperforms random and heuristic baselines. In RL, an asymmetric sampling strategy (highest-HES positive trajectories paired with random negative ones) surpasses the full-batch baseline using half the updates.

The paper is clearly written and addresses a practical problem—efficient data selection for reasoning—with a simple, intuitive metric. The experimental evaluation is broad, covering multiple benchmarks, models, and domains. However, several weaknesses limit the strength of the conclusions: (1) no statistical significance or variance reporting throughout, (2) overclaiming in the framing ("unified," "training-free," "obviates reward models"), (3) a confound between data pruning and data selection that is not explicitly discussed, (4) a duplicated paragraph and minor grammatical errors, and (5) notably thin related-work positioning relative to the forking-tokens work that inspired it. Novelty assessment is deferred due to external literature search being unavailable in this run.

## Strengths
1. **Simple and intuitive metric.** HES is conceptually elegant: it identifies "forking tokens" via per-token entropy and uses their cumulative value as a quality signal. This simplicity makes the approach easy to understand, implement, and adopt by practitioners. Unlike methods that require training separate reward models or running expensive gradient computations, HES requires only a single forward pass, making it computationally practical for large-scale data curation.

2. **Broad empirical validation.** The paper evaluates HES across three distinct training paradigms (SFT, RFT, RL) on seven math benchmarks plus code and STEM tasks, using two different model families (Qwen3 and DeepSeek-R1-distilled). This breadth of evaluation strengthens the claim that HES captures a generalizable signal rather than a setting-specific artifact.

3. **Useful ablation design.** The experimental design includes a comprehensive set of baselines (length, difficulty, average entropy, total entropy sum, average high-entropy entropy, forking-only) and two HES variants (relative and absolute threshold). This allows readers to isolate the contribution of HES's specific design choices (relative threshold, top-0.5% selection) from generic entropy-based selection.

4. **Small-to-large model transfer.** The demonstration that a 0.6B proxy model can select data for 8B model training with comparable effectiveness is practically valuable. If robust, this could substantially reduce the computational cost of data curation at scale.

5. **Explicit negative result analysis.** The paper honestly reports that constraining negative samples (Lowest-HES) in RL hurts performance and that per-query selection outperforms global pool selection. These analyses provide actionable guidance for practitioners beyond the core HES metric.

## Weaknesses
### W1: No statistical significance or variance reporting (Major)

**Evidence**: All results in Tables 1–6 are reported as single numbers without standard deviations, confidence intervals, or significance tests. The paper uses phrases like "significantly outperforms" and "consistently surpasses" throughout the results sections (Page 5–8), but no statistical test is performed.

**Impact**: The reported gains are typically 1–4 average percentage points (e.g., Full-Dataset 32.61 vs. Highest-HES 80% 35.36 in Table 1; Pos-High, Neg-Rand 21.30 vs. Full-Batch 20.63 in Table 6). Without variance estimates, readers cannot assess whether these differences are robust across training seeds or dataset splits. The GPQA anomaly (Random-20% scores 40.09 while Full-Dataset scores 38.04 in Table 1) further suggests that some of the observed variation may be due to noise rather than treatment effects.

**Recommended fix**: Report mean ± std over at least 3 random seeds for all key conditions. Add bootstrap-based significance tests comparing HES-selected subsets against random subsets of the same size. Discuss the GPQA anomaly explicitly.

### W2: Overclaiming in contributions framing (Major)

**Evidence**: (a) "Training-free" — HES requires a complete forward pass with per-token log-probability computation, which costs roughly 1x inference per sample. This is not "free," though it is cheaper than training a separate model. (b) "Unified data selection framework" — tested on only three paradigms (SFT, RFT, RL) in math-dominated domains; "unified" implies broader coverage. (c) "Obviates the need for costly external reward models" (Conclusion) — HES replaces data *selection*, not reward modeling. The RL experiments still rely on correctness-based rewards for GRPO; HES only selects which trajectories to include in the update.

**Impact**: These overstatements may mislead readers about the method's generality and may attract reviewer criticism that detracts from the paper's genuine contributions.

**Recommended fix**: Replace "training-free" with "model-intrinsic" or "forward-pass-only." Replace "unified" with "effective across three tested paradigms." In the conclusion, clarify: "HES reduces reliance on external selection models by leveraging the model's own per-token uncertainty."

### W3: Confound between data pruning and data selection (Major)

**Evidence**: The paper's strongest result (Highest-HES 80% surpasses Full-Dataset) is framed as evidence that HES identifies high-quality data. However, pruning the 20% lowest-HES data improves performance, while using only the top 20% roughly matches full-dataset performance. This pattern is equally consistent with a *pruning* effect: removing a small fraction of systematically harmful data improves training regardless of what quality signal is used. The paper does not control for this by comparing against random pruning or other pruning-based baselines.

**Impact**: The central claim—that HES captures "reasoning quality"—is not cleanly separable from the simpler claim that "removing the lowest-entropy trajectories helps." This distinction matters for understanding why HES works.

**Recommended fix**: Add a control experiment that prunes 20% of data at random and compares with HES-based pruning. Explicitly discuss the pruning vs. selection distinction in the results section.

### W4: Duplicated paragraph and grammatical errors (Minor)

**Evidence**: The paragraph "HES shows robust performance in both Per-Query and Global Pool settings" (Page 7, lines 188–189) appears twice verbatim, with the second instance truncated. Additionally: "the model, trained the 80% highest-HES" (Page 5, line 175) should be "trained on the"; "It average score" (Page 5, line 176) should be "Its average score"; "different from AvgHE" (Page 3, line 121) is self-referential (should be "different from AvgE").

**Impact**: These errors reduce the manuscript's professional polish and may distract reviewers from the technical content.

**Recommended fix**: Remove the duplicated paragraph. Proofread for grammatical errors.

### W5: Related Work positioning is too thin (Minor)

**Evidence**: The Related Work section (Section 5) consists of two brief paragraphs that do not adequately differentiate HES from the most directly relevant prior work—specifically Wang et al. (2025) on "forking tokens," which the paper repeatedly cites as inspiration. The "Forking-Only" baseline (gradient masking on high-entropy tokens) used in Table 1 is not discussed in the related work section, leaving readers without a clear understanding of how HES's *selection* approach differs from Forking-Only's *gradient-masking* approach.

**Impact**: Without proper positioning, the novelty of HES relative to existing entropy-based methods is unclear to readers unfamiliar with the literature.

**Recommended fix**: Expand Related Work to include a dedicated paragraph on entropy-based selection and forking-token methods, explicitly articulating the differences (selection vs. masking, sum vs. average, relative vs. absolute threshold).

### W6: Conclusion introduces unsupported claims (Minor)

**Evidence**: The conclusion states HES "enables efficiently training more robust models" without any robustness experiments (OOD evaluation, perturbation tests, or adversarial settings). It also claims to "obviate the need for costly external reward models," which conflates data selection with reward modeling as noted above.

**Impact**: These claims extend beyond the paper's evidence base and may be challenged during review.

**Recommended fix**: Restructure the conclusion to: (1) summarize validated findings, (2) state bounded limitations, (3) outline future work. Remove or rebrand the "robust" and "reward model" claims.

### W7: Missing discussion of the "correctness ≈ quality" assumption (Major)

**Evidence**: Figure 1 analysis treats correct responses as "high-quality" and incorrect ones as "low-quality," but this conflates answer correctness with reasoning quality. A correct answer can arise from lucky guessing or flawed reasoning, while an incorrect answer can follow sophisticated logic with one subtle error. HES could be tracking problem difficulty (harder problems produce more high-entropy tokens) rather than reasoning quality per se.

**Impact**: The foundational assumption of the analysis is not defended. If HES primarily identifies problem difficulty, the data selection benefits may reflect curriculum learning (training on harder examples) rather than quality filtering.

**Recommended fix**: Add an analysis comparing HES distributions among *only correct* answers to isolate reasoning complexity from correctness. Acknowledge the assumption explicitly and discuss potential confounds.

## Score
**Final Score: 6/10**

**Rationale**: The paper addresses a practical and timely problem—efficient data selection for LLM reasoning training—with a simple, intuitive metric (HES) that is well-motivated. The empirical evaluation is broad across benchmarks, models, and training paradigms. However, the score is weighed down by several significant weaknesses:

- **Validity risk (no statistical significance)**: Without variance reporting or significance tests, the claimed improvements (typically 1–4 average points) cannot be reliably distinguished from noise. This is a fundamental evidentiary gap.
- **Construct overclaiming**: "Training-free," "unified," and "obviates reward models" overstate the method's scope and novelty, which undercuts the credibility of the contribution framing.
- **Confounded interpretation**: The paper does not cleanly separate data *pruning* from data *selection* effects, weakening the central claim that HES captures reasoning quality.
- **Novelty verification unavailable**: External literature search was not possible in this run, so novelty relative to concurrent entropy-based selection methods (forking tokens, perplexity-based selection) cannot be independently verified.
- **Editorial issues**: Duplicated paragraph and grammatical errors reduce professionalism.

The paper has genuine strengths (simplicity, broad validation, practical small-to-large transfer) and the core HES idea is likely to be useful to the community. The recommended revision path (adding statistical rigor, toning down claims, expanding related work, and addressing the pruning/selection confound) is feasible and would substantially strengthen the paper.