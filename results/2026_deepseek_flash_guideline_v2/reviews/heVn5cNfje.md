Now I have all the content I need from the initial read. Let me compile the final review with careful verification of each claim.

---

## Final Consolidated Review

## Summary
This paper proposes High-Entropy Sum (HES), a training-free metric that sums the entropy of only the highest-entropy tokens (top ~0.5%) in reasoning traces, motivated by the observation that critical "forking tokens" get diluted when averaging over all tokens. The metric is validated across three training paradigms (SFT, RFT, RL) on multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B, Qwen3-0.6B) and seven benchmarks spanning math, code, and STEM. The core finding—that selecting or pruning data based on HES consistently improves over the full dataset, random selection, length, difficulty, average entropy, and entropy sum baselines—is well-supported across the board.

## Strengths

1. **Comprehensive validation across three training paradigms with consistent outperformance.** HES is evaluated on SFT (Tables 1–4), RFT (Table 5), and RL (Table 6) using multiple model families and seven benchmarks. In SFT on Qwen3-8B (Table 1), Highest-HES-80% achieves 35.36% avg vs. Full-Dataset 32.61%—a 2.75-point gain from *removing* 20% of the data. This pattern replicates on DeepSeek-R1-Distilled-7B (Table 2: 34.61% vs. 30.22%). In RL (Table 6), Pos-High, Neg-Rand reaches 21.30% vs. Full-Batch 20.63%.

2. **Pruning low-HES data improves over full-dataset training—a non-obvious, concrete finding.** Training on the highest-HES 80% of data consistently surpasses the full dataset, while Lowest-HES-20% collapses to 14.90% (Table 1)—far below even Random-20% at 25.89%. This provides strong evidence that HES identifies genuinely harmful training data, not just lower-value samples.

3. **Generalization to code and STEM domains with strong gains.** On code (Table 3), Highest-HES-20% achieves 39.54% vs. Fullset 36.28%. On STEM (Table 4), it achieves 49.56% vs. Fullset 44.42%. These relative gains are larger than in math, extending HES's validity beyond its primary domain.

4. **Small-to-large model transfer reduces inference cost while matching performance.** Using Qwen3-0.6B as a proxy scorer for Qwen3-8B training achieves 32.12% avg, comparable to the 8B self-selection at 31.14% (Table 1). This reduces cost by an order of magnitude and suggests HES captures data-intrinsic properties rather than model-specific artifacts.

5. **Systematic ablation against 12 baselines** (Section 4.1.1), including random, difficulty, length, average entropy, average HE, entropy sum, and HES_absolute. HES outperforms all at matching ratios.

6. **The asymmetric RL design yields a nuanced finding about negative diversity.** Pos-High, Neg-Rand (21.30%) outperforms Pos-High, Neg-Low (19.50%) and Pos-Rand, Neg-Low (19.76%) in Table 6, showing that while HES is useful for identifying high-quality positive signals, negative diversity must be preserved.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **HES-based selection has no effect on MMLU STEM and LiveCodeBench in the sensitivity analysis (Figure 4).** On MMLU STEM, all token ratios (0.005, 0.05, 0.5, 1.0) and all data selection ratios produce an identical score of 0.855. LiveCodeBench is similarly flat at 0.544. The paper claims HES "captures intrinsic reasoning quality signals common across diverse logic-intensive tasks" but does not discuss these plateaus, which could indicate domain-dependent discriminative power or saturated baselines. This limits the universality claim.

2. **The RL comparison between Pos-High, Neg-Rand (16 trajectories/step) and Full-Batch (32 trajectories/step) is partially confounded by training data quantity.** Both are trained for the same 628 steps, so Pos-High, Neg-Rand sees half the total trajectories. The comparison to Pos-Rand, Neg-Rand (also 16 trajectories) partially controls for this—Pos-High, Neg-Rand (21.30%) beats Pos-Rand, Neg-Rand (19.88%)—but the headline claim of surpassing Full-Batch should be qualified as "with half the compute per step" rather than as pure evidence of selection quality.

3. **No variance or confidence intervals reported.** Several key gains are modest (e.g., RFT k=8 per-query: Highest-HES 31.13% vs. Random 30.16%, a +0.97-point gain; RL: Pos-High, Neg-Rand 21.30% vs. Full-Batch 20.63%, a +0.67-point gain). Benchmarks like AIME 2025 have only 30 problems, and while pass@1 is averaged over 16 sampling paths, the lack of multiple seeds or standard errors makes it unclear whether the smaller gains are robust. This is a common omission in LLM training papers but noteworthy given the strength of some claims.

4. **No qualitative analysis of high- vs. low-HES samples.** The dramatic performance crash on Lowest-HES-20% (14.90% in Table 1) is attributed to "training noise" (line 206), but the paper never shows examples of what low-HES vs. high-HES solutions look like. Are they short/templatic, incorrect but slipped through, or genuinely noisy? Such analysis would strengthen the mechanistic understanding and help distinguish whether HES measures "reasoning quality" or "reasoning complexity"—both are directionally consistent with the results.

5. **The framing of HES as a "reasoning quality" metric could be sharpened.** The paper explicitly states HES "quantifies the complexity of a reasoning path" (line 36) and "a higher HES score signifies a greater diversity and complexity of reasoning patterns, indicating a higher learning value" (lines 36–37). These are two different interpretations (quality vs. complexity) that happen to align in these experiments. A brief acknowledgment of this distinction would improve precision without weakening the claims.

### Trivial

- **"Forking-Only" baseline label in Table 1** applies a different intervention (token-level gradient masking, not sample selection) and could be more clearly distinguished from the sample-level selection methods.

## Nice-to-Haves

- **Qualitative examples** comparing high- and low-HES reasoning traces (e.g., from Open-Math-Reasoning or Open-R1) would make the mechanism tangible.
- **A control experiment** in the RL setting (Full-Batch trained for proportionally fewer steps to match the total trajectory count of Pos-High, Neg-Rand) would isolate the selection benefit.
- **A brief discussion** of why MMLU STEM and LiveCodeBench show flat sensitivity profiles, and what this means for the scope of HES's applicability.

## Removed Points

- **"Highest-Difficulty baseline uses a different model, making comparison unfair."** Removed per rule: the asymmetry favors the baseline (72B model for difficulty vs. 0.6B for HES). The paper also explicitly states the source of difficulty scores; there is no unfairness to the authors.
- **"No discussion of data contamination."** Removed: speculative concern, not verifiable from the paper.
- **"No limitations section."** Removed: the appendix was stripped by the parser; the original submission may contain one.
- **Generic criticisms with no concrete anchor** (e.g., "the evaluation lacks rigor", "evidence is weak for the claims")—removed as noise.
- **Strength Finder items that are generic/delusional:** None found; all listed strengths were concrete and evidence-grounded.

## Novel Insights

The RL asymmetric sampling result (Section 4.3) is the paper's most nuanced finding. The comparison of Pos-High, Neg-Rand (21.30%) vs. Pos-High, Neg-Low (19.50%) reveals that HES's discriminative power on *positive* trajectories does not transfer to *negative* trajectories—in fact, constraining negatives to low-HES samples harms performance compared to random negatives. This suggests that learning from diverse failure modes is independently important, a more subtle result than a simple "higher HES = better" story.

## Suggestions

1. Add a brief discussion of the flat sensitivity profiles on MMLU STEM and LiveCodeBench, acknowledging that HES's effect may be domain-dependent.
2. Qualify the RL claim about surpassing Full-Batch with explicit mention of the compute-per-step reduction.
3. Consider adding a small set of qualitative examples (a high-HES correct solution vs. a low-HES correct solution) to make the mechanism concrete.
4. Report standard errors or multiple-seed results for at least the main SFT and RL comparisons.

## Score and Decision

**MY FINAL SCORE:** <score>7.5</score>
**MY FINAL DECISION:** <decision>Accept</decision>