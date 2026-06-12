## Summary

This paper investigates whether a single language model can self-improve by acting as both generator and verifier in preference-based games, without requiring external labels or reward signals. The authors propose SimpleGV (single-turn verifier-as-a-judge with thresholded majority voting) and RevisionGV (multi-turn game where the model critiques and revises its own outputs), and demonstrate modest improvements across logical reasoning (Knights and Knaves) and mathematical reasoning benchmarks (GSM8K, MATH, TabMWP), with particularly interesting findings on easy-to-hard generalization.

## Strengths

- **Clear and systematic framework.** The paper rigorously maps out generator-verifier game variants (single-turn SimpleGV, multi-turn RevisionGV) with well-defined formalism, making it easy to understand and reproduce. The progression from simple to complex (thresholded voting → multi-turn → iterative training → curriculum learning) is logical and well-organized.

- **Interesting easy-to-hard generalization finding.** Models trained only on KK instances with 2–3 people show meaningful improvement on 4–8 person instances where the search space grows exponentially. This is a genuinely interesting empirical finding suggesting the model learns transferable reasoning patterns rather than memorizing solutions (Table 2: 31.0% → 44.1% across all difficulty levels with iterative training).

- **RevisionGV provides stronger signal than SimpleGV.** On KK, RevisionGV consistently outperforms SimpleGV across all model scales (4B, 12B) and all difficulty levels (Table 4: 42.2% vs 40.7% for 4B; 52.8% vs 51.1% for 12B), and approaches oracle verification performance for the 12B model (52.8% vs 53.6%). This demonstrates that the model can not only identify but also correct its own errors—a more sophisticated form of self-improvement.

- **Thorough ablation studies.** The paper provides systematic analysis of model size effects (Figure 3), data scaling (Figure 3.3), cost-performance trade-offs (Figure 5 with heatmaps across generator/verifier configurations), and threshold sensitivity, providing practical guidance for deployment.

- **Transparent reporting of limitations and negative results.** The authors honestly report that SimpleGV performs worse than the base Qwen model on KK (17.6% vs 18.1%, Table 1), that 1B models show limited gains (Table 4), and that performance plateaus at larger data sizes (Figure 4). This transparency strengthens credibility.

## Weaknesses

### Fatal
None.

### Major

- **Very modest improvements on standard math benchmarks.** On Qwen2.5-7B, SimpleGV yields essentially zero gain on GSM8K (90.2→90.6, +0.4) and TabMWP (91.9→92.3, +0.4). On MATH500 and MATHHard, gains are 2.5 and 1.8 points respectively. For Gemma-3-4b-it, gains are similarly modest (1.4–2.9 points). These improvements are small enough that they could be within normal experimental variance, especially given 4-seed averaging. This significantly limits the paper's claim of general applicability across reasoning benchmarks.

- **Inconsistent cross-model-family results undermine generalizability claims.** SimpleGV improves Gemma-3-4b-it on KK from 31.0% to 40.7% (+9.7 points) but *degrades* Qwen-7B-Instruct from 18.1% to 17.6% (-0.5 points). While the paper reports both numbers, it does not adequately discuss why the method fails on one model family, weakening the central claim that generator-verifier games are a general self-evolution framework.

- **Comparison methodology against baselines is uneven.** Table 1 mixes self-evaluated base numbers ("89.2*" from Gemma's report), reproduced numbers, and original report numbers ("84.0 (0.4)" for AZR). Some baselines (GRPO, INTUITOR) have "/" on multiple benchmarks, suggesting incomplete evaluation. A more controlled comparison—where all methods are evaluated with the same pipeline—would strengthen the results.

### Minor

- **Threshold sensitivity requires task-specific tuning.** The paper acknowledges that thresholds between 0.6–0.7 are "reliable," but the optimal threshold varies by benchmark (e.g., 0.6 for KK but 0.7 for cost analysis in Figure 5), and the practical guidance for choosing thresholds in new domains is limited.

- **KK training set size is very small.** Training on KK uses ~120–285 unique prompts (2–3 people, 4–5 people), which seems small for DPO training. While multiple samples per prompt create more preference pairs, the paper does not clarify how many unique prompts vs. augmented samples contribute to the effective training set, making the KK results harder to contextualize.

- **Only DPO is explored as the preference learning objective.** Other methods like KTO, IPO, or online RL approaches could potentially yield different results. The paper does not compare against simpler self-training baselines (e.g., self-consistency + SFT on majority-voted solutions).

### Trivial
- Some tables are dense with many rows, making comparison across configurations difficult. The iterative DPO table (Table 2) with its chain of arrows could benefit from clearer visual grouping.

## Nice-to-Haves

- A comparison against self-training with ground-truth labels (e.g., standard SFT on human-annotated solutions) would help quantify the gap between unsupervised and supervised approaches more precisely, beyond the oracle verifier numbers.
- Analysis of what types of problems SimpleGV helps vs. hurts (e.g., error analysis on where self-verification succeeds or fails on GSM8K).
- Comparison against simpler baselines like self-consistency decoding at inference time, to isolate whether the benefit comes from training-time preference learning or from verification/computation at scale.

## Novel Insights

The finding that easy-to-hard generalization emerges from generator-verifier self-training on the KK benchmark is genuinely novel and worth highlighting. When a 4B model trained only on 2–3 person KK instances is evaluated on 4–8 person instances, accuracy improves substantially across all difficulty ranges (Table 2: 4–5 people from 31.0% to 46.9%; 6–8 people from 10.3% to 20.8% after iterative training). This suggests the model learns reasoning strategies that compose and generalize, rather than memorizing solutions to specific problem instances. This is distinct from typical curriculum learning results because the test-time problems are genuinely harder, with exponentially larger search spaces.

## Suggestions

- Add a controlled comparison where the same training data and evaluation pipeline is used for all methods, ideally re-running AZR/GRPO on the same benchmarks to ensure fair comparison.
- Investigate and discuss the model-family discrepancy (Gemma vs. Qwen on KK) more thoroughly—this could reveal important insights about when self-verification works.
- Include a breakdown of SimpleGV performance by problem difficulty on math benchmarks, to understand whether gains concentrate on easy or hard problems.

## Score and Decision

The paper presents a systematic and well-executed empirical study of self-evolution through generator-verifier games. The easy-to-hard generalization result and the RevisionGV approach are genuinely interesting contributions. However, the improvements on standard math benchmarks are very modest (often < 2 points), the results are inconsistent across model families (SimpleGV degrades Qwen on KK), and the comparison methodology against baselines is uneven. As an empirical study, the experiments are thorough and the ablations are useful, but the practical significance is limited by the small magnitude of improvements and the high computational cost of multi-sample generation and verification.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept