## Summary
# Final Review Report

## Summary

This paper presents a self-evolution framework where a single language model acts as both generator and verifier in a simple game-theoretic setup (GV games) to produce preference data for DPO fine-tuning without external supervision. The authors propose two main variants: SimpleGV (single-turn verification with thresholded majority voting) and RevisionGV (multi-turn iterative refinement with verifier feedback). Experiments on the Knights and Knaves (KK) logical reasoning benchmark and four mathematical reasoning datasets (GSM8K, MATH500, MATHHard, TabMWP) show consistent improvements over base models, with KK accuracy rising from 31.0% to 44.8% under curriculum training. The paper also explores iterative DPO, curriculum learning, and model/data scaling effects. 

**Core claims (C1-C3):**
- **C1:** A simple yet general self-evolution framework using the same model for generation and verification, without external labels or environments.
- **C2:** Key principles for reliable self-evolution: thresholded majority voting and multi-turn generator-verifier interaction (RevisionGV).
- **C3:** Bootstrapping and easy-to-hard generalization via iterative training and curriculum learning.

**Overall assessment:** The paper addresses an important question (self-evolution without external signals) and provides a clean, well-structured framework with systematic experiments. The main strengths are the simplicity and generality of the approach and the thorough ablation studies on KK. However, the claims of "easy-to-hard generalization" and "general framework" are somewhat overstated given that the deep analysis is confined to a single synthetic benchmark (KK), the improvements on math benchmarks are modest, and the within-distribution nature of the easy-to-hard transfer limits its scope. Novelty verification is deferred due to external literature search being unavailable in this run.

## Strengths
**1. Well-motivated research question.** The paper tackles the important and timely problem of enabling language models to self-improve without external supervision. The framing around the limitations of human annotation and verifiable rewards is clear and compelling.

**2. Clean and simple framework.** The generator-verifier game abstraction is elegant and easy to understand. Separating the problem into SimpleGV and RevisionGV variants allows the paper to isolate the contribution of multi-turn interaction. The thresholded majority voting method for extracting reliable signals from noisy self-verification is a practical and well-motivated contribution.

**3. Thorough ablation on the KK benchmark.** The paper provides a systematic analysis on the synthetic KK dataset, covering: (a) single-turn vs. multi-turn verification, (b) iterative DPO across multiple rounds, (c) curriculum learning with difficulty scheduling, (d) model size scaling (1B, 4B, 12B, 27B), (e) data scaling (5K-40K samples), and (f) cost-performance trade-offs. This level of ablation depth is commendable and provides useful practical insights.

**4. Easy-to-hard transfer demonstration.** The finding that training on 2-3 person KK puzzles improves accuracy on 4-8 person puzzles by 13+ percentage points is a clean and interesting result. While limited to within-distribution scaling, it convincingly shows that the method can generalize along a difficulty dimension.

**5. Open and honest limitations.** The limitations section is well-written and acknowledges the key weaknesses: computational cost, threshold sensitivity, and the fundamental knowledge boundary. This transparency strengthens the paper's credibility.

**6. Reproducibility-oriented reporting.** The evaluation protocol (exact-match accuracy, temperature 0.7, 4 seeds, mean+std) is clearly specified. The use of open-source models (Gemma, Qwen) and publicly available datasets supports reproducibility.

## Weaknesses
**W1. Overclaimed "easy-to-hard generalization" (Major).** The paper frames the size-generalization on KK (2-3 → 4-8 people) as "emergent easy-to-hard generalization." However, larger KK instances share the identical logical structure with smaller ones — only the search space grows. This is within-distribution scaling, not cross-distribution or out-of-domain generalization as typically studied in the curriculum learning literature. No cross-benchmark transfer experiment is provided (e.g., training on KK and testing on GSM8K or TabMWP). The claim should be toned down to "size generalization" or "within-distribution scaling," and the limitations of this generalization type should be explicitly discussed. *(See annotations on Abstract, Section 3.4, and Conclusion.)*

**W2. Baseline comparisons are not controlled (Major).** Table 1 compares SimpleGV against INUITOR, Absolute Zero, and GRPO using scores from their original papers. These methods differ in training data, compute budget, and protocol. The paper does not control for these variables. For instance, SimpleGV uses 20K samples from OpenThoughts3; INUITOR and GRPO may use entirely different data sources. The comparison is informative as context but does not establish SimpleGV's superiority. Moreover, for gemma-3-4b-it on GSM8K, SimpleGV (89.0) is actually below the base model (89.2*). The "co-evolution" claim (verification accuracy improving alongside generation) is supported only on KK, not on math benchmarks. *(See annotations on Section 3.1/Table 1.)*

**W3. Uneven experimental depth across benchmarks (Major).** The in-depth analysis (model scaling, data scaling, iterative DPO, curriculum learning, cost analysis) is conducted almost exclusively on the KK synthetic benchmark. The mathematical reasoning benchmarks (GSM8K, MATH500, MATHHard, TabMWP) receive only a single table entry and a data-scaling plot. This asymmetry means that the paper's strongest conclusions (easy-to-hard generalization, curriculum benefits, iterative improvement) are validated only on one synthetic task. The "general framework" claim is weakened by this narrow evaluation scope. *(See annotations on Contribution listing and Section 3.2-3.5.)*

**W4. Missing statistical significance testing (Medium).** All results are reported as mean ± std over 4 seeds, but the paper makes comparative claims ("improves over," "outperforms," "approaches") without any formal significance testing. Some improvements (e.g., RevisionGV vs. SimpleGV on 4B: 42.2% vs. 40.7%) have overlapping standard deviations. Without confidence intervals or p-values, the reader cannot assess whether reported gains are statistically reliable. *(See annotation on Section 2.1 Evaluation Protocol.)*

**W5. Confounded curriculum vs. random mixing comparison (Medium).** The curriculum learning experiment (Section 3.5) compares curriculum (train on KK23 then KK45) against random mixing (train on KK2345 once). The curriculum approach sees KK23 data twice (once in each stage), while random mixing sees each instance once. This confounds curriculum ordering with total data volume. A controlled experiment matching total training steps is needed to isolate the effect of ordering. *(See annotation on Section 3.5.)*

**W6. RevisionGV mechanism is under-analyzed (Medium).** The paper attributes RevisionGV's improvement to "more detailed verifier feedback" and "better incorporation" without providing any analysis of actual feedback content. No examples, no categorization of feedback types, and no correlation between feedback quality and model size are provided. The mechanism explanation remains speculative. *(See annotation on Section 4, Discussion.)*

**W7. Threshold sensitivity and discard rate not analyzed (Minor).** The thresholded majority voting method discards candidates with correctness rates between (1-τ, τ). The discard rate directly affects dataset size and downstream performance, but no statistics on discard rate are reported. The paper's data scaling analysis (Section 3.3) may be partially confounded by varying discard rates across thresholds. *(See annotation on thresholded voting description.)*

**W8. Related work is a flat list (Minor).** The Related Work section (Section 5) lists methods without organizing them by comparison axes. The paper's key distinctions (no external verifier, offline training, single-model self-play) are not explicitly contrasted with each prior work cluster. A structured comparison would strengthen novelty positioning. *(See annotation on Section 5.)*

**W9. Cost analysis lacks a formal model (Minor).** The claim that "verifier computation is more cost-effective" (Section 3.6) is based on a single model and benchmark. No formal cost model (e.g., total FLOPs = n₁·C_gen + n₁·n₂·C_ver) is provided, and the analysis does not account for the multiplicative interaction between n₁ and n₂. *(See annotation on Section 3.6.)*

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and important question (self-evolution without external supervision) with a clean, well-motivated framework and thorough ablations on the KK benchmark. The generator-verifier game abstraction is elegant, and the easy-to-hard transfer result on KK is a solid empirical contribution. However, the score is constrained by several factors:

1. **Overclaimed generalization (research value impact):** The central claims of "emergent easy-to-hard generalization" and a "general framework" are not fully supported by the evidence. The deep analysis is confined to a single synthetic benchmark, and the easy-to-hard transfer is within-distribution scaling, not cross-domain generalization.

2. **Uncontrolled baselines (validity risk):** The comparisons against prior methods in Table 1 are not controlled for training data or compute budget, weakening the paper's competitive claims.

3. **Narrow experimental scope (novelty impact):** Only the KK benchmark receives deep analysis; the math benchmarks show modest improvements and lack the detailed ablation that would support the framework's claimed generality.

4. **Missing statistical rigor:** No significance testing is provided for comparative claims, and some improvements have overlapping error bars.

The paper has a solid empirical core and the framework is genuinely useful, but the contributions would be strengthened by more measured claims and broader validation. Novelty verification is deferred due to external literature search being unavailable in this run; manual verification is recommended before final acceptance decisions.