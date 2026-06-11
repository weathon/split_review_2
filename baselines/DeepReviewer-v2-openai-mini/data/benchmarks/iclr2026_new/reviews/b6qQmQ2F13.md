## Summary
# Final Review Report

## Summary

This paper presents an empirical study of memory-accuracy trade-offs for deploying large reasoning models under fixed memory budgets. The authors systematically vary model size (0.6B--32B parameters), weight precision (4/8/16-bit), test-time token budget (2k--30k tokens), parallel scaling via majority voting (group sizes up to 16), and KV cache compression (eviction vs. quantization) across four benchmarks (AIME25, GPQA-Diamond, LiveCodeBench, MATH500) and three model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron). The core thesis is that the optimal memory allocation strategy is scale-dependent, with a threshold at approximately 4.2 GB of weight memory (equivalent to an 8-bit 4B model): below this threshold, allocating memory to larger or higher-precision weights is more efficient, while above it, extending the token budget or using parallel scaling yields better returns. The paper also finds that task type modulates the optimal weight precision (4-bit suffices for knowledge tasks but degrades math/code reasoning) and that KV cache compression universally improves the Pareto frontier, with eviction favored for smaller models and quantization competitive for larger ones.

The paper addresses a timely and practical problem — the deployment of reasoning models under memory constraints — and provides actionable, scale-dependent guidelines. The experimental coverage (1,700+ configurations) is impressive in breadth. However, the central threshold claims depend on a single architectural family (dense transformers), the task-dependent conclusions rest on limited benchmark evidence per category, and the absence of statistical uncertainty quantification limits the strength of the claims. Novelty attribution is deferred to manual literature verification because external retrieval was unavailable in this review run.

## Strengths
1. **Timely and practical problem formulation.** The paper correctly identifies that reasoning models shift the memory bottleneck from model weights to the KV cache, and that existing weight-focused quantization guidelines (e.g., "4-bit is always optimal") do not transfer. This reframing of test-time scaling around memory constraints rather than FLOPs is a useful perspective that addresses a genuine deployment challenge.

2. **Broad and systematic experimental coverage.** The study spans over 1,700 configurations across six model sizes, three weight precisions, multiple token budgets, parallel scaling up to 16 samples, two KV compression strategies, and three model families. This scale of systematic investigation is a major strength, enabling the authors to identify reliable, replicated patterns rather than anecdotal observations.

3. **Clear, actionable findings with explicit thresholds.** The paper distills complex multi-dimensional trade-offs into five compact, actionable findings organized around an intuitive scale-dependent threshold. This makes the results directly usable by practitioners deciding how to allocate hardware budgets for model deployment. The Finding-based structure (Finding 1--5) is reader-friendly and memorable.

4. **Verification across multiple model families.** By replicating key experiments on DeepSeek-R1-Distill and OpenReasoning-Nemotron in addition to the primary Qwen3 analysis, the paper demonstrates that the observed scale-dependent patterns are not artifacts of a single model family. The cross-family consistency strengthens the generality claims.

5. **Honest and specific limitations section.** Unlike many papers that relegate limitations to a perfunctory paragraph, this manuscript provides a detailed, specific account of its scope constraints (single verifier tested, limited quantization schemes, Qwen3-centered analysis) and explicitly identifies avenues for future work. This transparency is commendable.

## Weaknesses
### Major Weaknesses

**W1. Central threshold lacks architectural generalization evidence.** The paper's primary findings hinge on an "effective size" threshold (8-bit 4B ~ 4.2 GB weight memory), but all tested models are dense transformers from the Qwen/Llama architectural family. The paper claims generalization via DeepSeek-R1-Distill and OpenReasoning-Nemotron, but these share the same dense transformer paradigm. Mixture-of-experts (MoE) models, sparse transformers, or non-transformer architectures would have different KV cache proportionality and potentially different optimal thresholds. Since many state-of-the-art reasoning models (e.g., DeepSeek-V2, Mixtral) use MoE architectures, the practical applicability of the threshold to these models is unknown. *(Evidence: pages {1}-{2}, Finding 1 and test-time scaling analysis)*

**Fix:** Add an explicit architecture scoping statement: "All evaluated models use dense transformer architectures. The effective size thresholds may differ for mixture-of-experts or attention-alternative architectures. Practitioners deploying non-dense architectures should treat the reported thresholds as approximate starting points." Additionally, if feasible, include at least one MoE-based reasoning model in the evaluation.

**W2. Task-dependent findings rest on limited benchmark coverage.** The paper divides tasks into "knowledge-intensive" (GPQA-Diamond alone) and "mathematical reasoning" (AIME25, MATH500) and "code generation" (LiveCodeBench). The knowledge-intensive conclusion that "4-bit is broadly memory-optimal" relies on a single benchmark that uses a multiple-choice format (4-option QA). Multiple-choice evaluation may be less sensitive to quantization degradation than generation-based evaluation, and GPQA-Diamond's 198-question size raises statistical power concerns. Similarly, the code benchmark is a single corpus (LiveCodeBench). The paper does not evaluate other common knowledge tasks (MMLU, long-form QA, summarization) or code tasks (HumanEval+, Codeforces). *(Evidence: Page {5}, Finding 2 and the task comparison section)*

**Fix:** (i) Qualify all task-dependent claims with the specific benchmarks used. (ii) Add at least one generation-form knowledge benchmark (e.g., MMLU-Pro with CoT prompting) to validate that the 4-bit tolerance extends beyond multiple-choice formats. (iii) Report explicit accuracy deltas (4-bit vs 8-bit) per benchmark in a compact table rather than relying solely on visual comparison of overlapping curves.

**W3. No statistical uncertainty quantification for accuracy estimates.** Throughout the paper, accuracy is reported as a single point estimate (averaged over 32 generations). No confidence intervals, standard deviations, or significance tests are provided. Given that many comparisons show small accuracy differences (e.g., 2-5 percentage points), the absence of uncertainty bounds makes it impossible to judge whether observed differences are statistically reliable or due to random variation. This is particularly concerning for the Pareto frontier analysis, where a configuration being "on the frontier" could be influenced by noise in individual point estimates. *(Evidence: Page {3}, Inference details; all Figures)*

**Fix:** (i) Report accuracy with 95% confidence intervals (bootstrapped over instances or generations) for all main result figures. (ii) Add a paired significance test (e.g., McNemar's test) when comparing two configurations on the same set of benchmark instances. (iii) Mark Pareto frontier points with uncertainty bands rather than single curves.

---

### Minor Weaknesses

**W4. Threshold inconsistency across findings.** Finding 1 and 3 use "8-bit 4B" (~4.2 GB) as the threshold for serial/parallel scaling strategy, while Finding 5 uses "8-bit 8B" (~8.9 GB) for the eviction-vs-quantization decision. The paper does not explain why the threshold differs between these two decisions, nor does it give the threshold in GB units for cross-architecture applicability. This can confuse practitioners who may apply the wrong threshold to their problem. *(Evidence: Pages {2}, {5}, {9})*

**Fix:** Add a unified threshold table converting model+precision references to GB weight memory for all findings. Explicitly note that the KV compression crossover occurs at a different (approximately 2x larger) threshold than the serial-scaling strategy crossover, and discuss why this might be the case (e.g., KV cache eviction preserves full precision of selected tokens, which is more beneficial when weight memory is small relative to KV memory).

**W5. Memory cost model underspecified for precise reproducibility.** The memory equation (Eq. 1) states M is roughly proportional to N·P_W and N·G·T, but the exact functional forms and constants are deferred to Appendix B (not included in the provided manuscript). The term "roughly proportional" leaves ambiguity: for transformers, KV cache memory is proportional to the number of KV heads × head dimension × layers × 2 × precision, which correlates with but is not identical to total parameters N. Without the exact equations in the main text, practitioners cannot compute exact memory for their own models. *(Evidence: Page {3}, Equation 1 and surrounding text)*

**Fix:** Include the exact memory formulas from Appendix B in the main text, or at minimum provide a footnote with the precise architectural dependency. Add a worked example calculation for the Qwen3-4B model at 8-bit with 30k tokens to illustrate the formula.

**W6. No variance reporting for KV compression experiments.** Section 5 reports results averaged over 8 generations per instance (compared to 32 for the main experiments), further reducing statistical reliability. The paper mentions averaging over 8 generations but does not justify why fewer generations are sufficient for the compression experiments. *(Evidence: Page {7}, Section 5 first paragraph)*

**Fix:** Either increase generations to 32 for KV compression experiments, or provide a power analysis showing that 8 generations are sufficient for the observed effect sizes. At minimum, report bootstrap confidence intervals to quantify the increased uncertainty.

**W7. Calibration data for GPTQ quantization not specified.** The paper uses GPTQ for weight quantization but does not report the calibration dataset size, source, or sequence length. Since GPTQ's quantization quality is calibration-dependent, missing these details hinders reproducibility. A mismatch between calibration data and evaluation data could partially explain the observed task-dependent quantization sensitivity. *(Evidence: Page {2}, Background -- Weight-only quantization)*

**Fix:** Add one sentence: "GPTQ calibration uses 128 samples of 2048 tokens from [dataset], consistent with prior work [Frantar et al., 2022]."

**W8. External verifier evaluation limited to a single verifier at a single scale.** The conclusion that external verifiers are memory-inefficient is based on ActPRM-X (7B, 13.28 GB). A smaller verifier (0.5B--2B parameters) could produce different trade-offs, especially under tight memory budgets. The paper's language ("external verifier is consistently memory-inefficient") overgeneralizes from this single data point. *(Evidence: Page {7}, Section 4.1)*

**Fix:** Qualify: "At the 7B verifier scale tested, external verification is memory-inefficient. Smaller verifiers may shift this trade-off."

**W9. Conclusion introduces unsupported speculation.** The conclusion states "the inflection point where extra KV cache beats extra model weight may change as models become more sophisticated." This is speculative and unsupported by the paper's experimental evidence, which only evaluates current-generation models. Speculative claims in the conclusion can undermine reader confidence in the robustness of core findings. *(Evidence: Page {9}, Conclusion)*

**Fix:** Replace with an evidence-grounded statement: "Across the three model families tested, the threshold behavior remained consistent, suggesting the scale-dependent principle is robust to moderate architectural differences. Verification on future model generations is an important next step."

**W10. No ablation of budget forcing prompt effect.** The paper uses "Wait" as the budget-forcing prompt to extend generation. The choice of this specific prompt may affect generation quality and accuracy compared to alternative prompts (e.g., "Continue," "Keep thinking," or a learned trigger token). Without an ablation, readers cannot assess whether the observed serial-scaling gains are specific to the "Wait" prompt or generalize to other budget-forcing methods. *(Evidence: Page {3}, Inference details)*

**Fix:** Add a brief ablation comparing 2-3 alternative budget-forcing prompts (e.g., "Wait," "Continue," "") on a single model+benchmark combination, or acknowledge this as a limitation and cite prompt sensitivity as a potential confound.

## Score
**Final Score: 7/10**

**Rationale:** The paper addresses a well-motivated and practically important problem with impressive experimental breadth (1,700+ configurations across multiple model families). Its core findings — scale-dependent memory allocation, task-dependent weight precision sensitivity, and the complementary role of KV cache compression — are clearly articulated and supported by consistent evidence across benchmarks. The threshold-based framework provides actionable guidance for practitioners.

However, the score is moderated by three key factors. First, the central threshold claims depend on a single architectural family (dense transformers), limiting generalization to MoE and non-transformer reasoning models that are increasingly common in practice. Second, the task-dependent findings rely on limited benchmark coverage per category (one benchmark for knowledge tasks, one for code), and the knowledge-task benchmark uses a multiple-choice format that may mask quantization sensitivity. Third, the absence of statistical uncertainty quantification throughout the paper weakens the reliability of fine-grained comparisons (e.g., which configuration lies on the Pareto frontier). These limitations are fixable and do not invalidate the core contributions, but they bound the strength of the claims that can be made in the current version.

The novelty assessment is deferred because external literature retrieval was unavailable during this review. A final score may shift after manual literature verification determines how much of the observed scale-dependent findings overlap with existing work.