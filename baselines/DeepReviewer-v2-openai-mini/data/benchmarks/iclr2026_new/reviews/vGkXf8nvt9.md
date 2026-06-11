## Summary
This paper proposes Forget-to-Focus (F2F), a two-stage protocol that inserts a targeted unlearning step between pretraining and fine-tuning to improve domain specialization of LLMs. The unlearning phase uses gradient ascent on a "forget set" (general-domain data) and optionally gradient descent on a "retain set" (domain-specific data) to suppress irrelevant pretraining features, followed by standard fine-tuning on the target domain. Experiments across 5 model families (0.6B–72B parameters) and 3 domains (coding, medical, mathematics) suggest that F2F can improve performance over standard fine-tuning, DAPT, and LoRA baselines. The paper also provides a theoretical analysis using a convex surrogate model and a representational analysis using CKA and SVCCA to characterize how unlearning alters internal representations.

**Core strengths:** (1) The research question—whether unlearning can serve as a preparatory stage for domain specialization rather than only a privacy tool—is timely and potentially impactful. (2) The experimental scope is broad, covering multiple architectures (Qwen, LLaMA, Gemma) and scales (0.6B to 72B). (3) The representational analysis adds a useful layer of mechanistic understanding beyond accuracy comparisons.

**Core weaknesses:** (1) Statistical significance and variance are completely absent—all results are single-point estimates, preventing assessment of reliability. (2) The retain set overlaps with fine-tuning data, creating a confound that is not controlled for. (3) The number of unlearning steps (T_u) is never specified, undermining reproducibility. (4) The theoretical analysis rests on strong assumptions (orthogonal decomposition, convexity) that are not satisfied by LLMs, and no quantitative bridge is offered between theory and experiments. (5) Several claims (e.g., "stabler optimization," "reduced spurious correlations," "direct evidence") exceed what the evidence supports. (6) External novelty verification is deferred (retrieval-disabled mode).

## Strengths
1. **Timely and well-motivated research direction.** The question of whether unlearning can serve as a preparatory step for domain specialization—rather than only a privacy compliance tool—is novel and practically relevant. The paper identifies a genuine gap in the fine-tuning literature: the assumption that all pretrained knowledge is equally useful during adaptation may not hold, and active forgetting could be beneficial.

2. **Broad empirical scope.** Experiments span five model families (Qwen 0.6B–72B, LLaMA 8B, 13B, Gemma 2B) across three different domains (coding, medical, mathematics) with multiple benchmarks per domain. This breadth lends credibility to the main empirical finding that unlearning can improve downstream fine-tuning across diverse settings.

3. **Multiple unlearning algorithms benchmarked.** Beyond simple GA+GD, the paper evaluates GA-only, GA+KL, and NPO, providing insight into which unlearning strategies work best. The finding that GA+GD (balancing forgetting and retention) outperforms GA-only is practically useful for practitioners.

4. **Representational analysis adds depth.** The use of CKA, SVCCA, Fisher information, and PCA to characterize representational drift goes beyond standard accuracy comparisons. These analyses provide a mechanistic perspective, showing that F2F representations diverge more from the base model than standard fine-tuning, which is consistent with the intended suppression of irrelevant features.

5. **Forget-set quality investigation.** The systematic comparison of BC-Select, BC-Mixed, and BC-Cosine forget sets provides actionable guidance: curated, domain-disjoint forget sets yield better results. This is a practical contribution for anyone wanting to apply F2F.

6. **Calibration analysis on medical QA.** The observation that F2F improves calibration (reduces overconfidence) on medical question answering adds an important safety-relevant dimension beyond raw accuracy, especially for high-stakes domains.

## Weaknesses
### W1. Missing statistical significance and variance reporting (Major, Validity)

All reported results (Tables 1, 2, 3) are single-point estimates with no standard deviations, confidence intervals, or significance tests. For a paper whose central claim is "consistently outperforms standard fine-tuning," the lack of any variance information is a critical gap. Without multi-seed runs, the reader cannot assess whether the observed gaps (e.g., Qwen 0.6B HumanEval: 42.07 vs 31.71) are robust or could flip with a different random seed. This is especially concerning for smaller models where performance is more variable. **Fix:** Report mean ± std over at least 3 seeds, add significance tests (e.g., paired bootstrap), and mark statistically significant improvements in all tables. *(See annotation 8: Page 1 - 4.1 Effect of F2F on Coding Performance)*

### W2. Data leakage confound from retain set (Major, Validity)

The retain set R is described as "a small subset of the fine-tuning data" (Section 3.3). This means the model sees a portion of the target-domain data during the unlearning phase before formal fine-tuning, creating a confound: F2F's gains could partially reflect additional exposure to domain data rather than the unlearning mechanism itself. The paper does not control for this by comparing against SFT trained on D∪R. **Fix:** Add a control experiment where standard SFT is trained on D extended with R. If this matches F2F performance, the unlearning component is not the driver of gains. Also, explicitly state whether R is a strict subset of D or disjoint. *(See annotation 7: Page 1 - Section 3.3 Models and Datasets)*

### W3. Critical hyperparameter T_u (unlearning steps) never specified (Major, Reproducibility)

The method description (Section 2) defines T_u as the number of unlearning steps, but no numeric value is reported anywhere in the paper. The effectiveness of unlearning is highly sensitive to this parameter: too few steps leaves irrelevant knowledge intact, too many causes catastrophic forgetting. The performance collapse of Gemma 2B (0.00 after unlearning) could reflect a suboptimal T_u rather than inherent model limitations. **Fix:** Report exact T_u for each model, or equivalently the number of epochs and forget-set size. Add a sensitivity analysis of T_u for at least one model-benchmark pair. *(See annotation 10: Page 1 - Section 3.4 Hyperparameter Configuration)*

### W4. Theoretical analysis has limited applicability to actual LLMs (Major, Soundness)

The Proposition and Corollary in Section 2 analyze a convex linear surrogate model under assumptions of orthogonal feature decomposition, strong convexity, and smoothness. None of these assumptions hold for LLM training (non-convex, features are entangled, no orthogonal decomposition). The paper acknowledges this ("While LLM training objective is non-convex") but does not bridge the gap: it never measures µ_F, β, or G_R for the actual models, so the bounds remain purely qualitative. **Fix:** (a) Add explicit caveats about the gap between the surrogate and actual LLMs; (b) measure empirical proxies (e.g., gradient norms, Hessian curvature estimates on forget vs retain sets) to validate the qualitative predictions; (c) position the analysis as intuitive motivation rather than formal proof. *(See annotation 6: Page 1 - Section 2 Forget-to-Focus)*

### W5. Unsupported and overreaching claims (Major, Objectivity)

Several claims in the abstract, introduction, and conclusion exceed what the evidence supports:
- "More stable optimization dynamics" — no direct optimization measurements are provided.
- "Reduced spurious correlations" — no test for spurious correlations is conducted.
- "Direct evidence that unlearning reduces negative transfer" — CKA/SVCCA show representational drift, but this is correlational, not direct evidence of negative transfer reduction.
- "Consistently outperforms" — some conditions show small or mixed gains (e.g., MedMCQA on Qwen 0.6B with BC-Mixed).
- "First comprehensive study" — the "first" claim cannot be verified in retrieval-disabled mode; "comprehensive" is subjective with only 4 unlearning methods. **Fix:** Qualify each claim to match the evidence. Replace "direct evidence" with "evidence consistent with," remove "stabler optimization" unless directly measured, and replace "first" with "to the best of our knowledge." *(See annotations 1, 5, 9: Page 1 - Abstract, Contributions, Conclusion)*

### W6. Abstract calibration claim over-extends evidence (Major, Objectivity)

The abstract states that F2F "helps improved calibration on medical QA tasks, reducing overconfidence and mitigating reliability issues." Calibration is only evaluated on medical QA; the paper does not report calibration results for coding or math domains. The phrase "reliability issues that persist under standard fine-tuning" implies a general problem, but only one domain is tested. **Fix:** Qualify: "On medical QA, F2F improves calibration; calibration behavior in other domains remains to be studied." *(See annotation 1: Page 1 - Abstract)*

### W7. Inconsistent fine-tuning conditions across models (Minor, Fairness)

The fine-tuning setup varies across models in ways that complicate fair comparison:
- Qwen 0.6B fine-tuned for 8 epochs, larger models for only 1 epoch.
- Qwen 72B uses QLoRA with 4-bit quantization and only 50% of the dataset.
- LLaMA-8B, LLaMA-13B, Qwen-72B use LoRA-based SFT with FP16, while Qwen 0.6B uses full SFT.
- The effective batch size of 128 (via gradient accumulation with step 32) means actual micro-batch sizes differ: batch 8 (Qwen 0.6B) vs batch 2 (others), leading to different gradient noise characteristics.

These differences make cross-model comparisons difficult. **Fix:** Either standardize the fine-tuning protocol across models or explicitly discuss how each choice might affect the observed F2F gains.

### W8. Missing novelty verification against external literature (Deferred)

Because this run operates in Retrieval-Disabled Mode, the novelty claims (especially "first comprehensive study" and the comparison against DAPT/LoRA baselines) cannot be verified against external literature. The paper's positioning relative to prior work on unlearning for domain adaptation (e.g., active forgetting during pretraining [Chen et al. 2023a], parameter-efficient unlearning [Cha et al. 2024]) remains an open question that requires manual literature check. **Fix:** Authors should strengthen the related-work section with explicit overlap analysis against the closest prior methods, clearly stating what is new and what is incremental.

### W9. Grammar and writing quality issues (Minor)

Several grammatical errors reduce readability:
- "This helps us analyze of how domain overlap" (Section 3.3) — should be "analyze how."
- "F2F a simple two-stage pipeline : unlearns" (Conclusion) — colon misuse and missing comma.
- "causing the model align better" (Section 4.1) — missing "to."
- "the less dependency on stability-preserving corrections" (Section 4.3) — awkward phrasing.

These are minor but suggest the paper would benefit from a careful language revision pass.

## Score
**Final Score: 6.0/10**

**Score rationale:** The paper tackles a timely and well-motivated research question with a broad empirical scope (5 model families, 3 domains) and includes useful representational analysis. However, the score is tempered by several critical issues that affect validity and reproducibility: (1) no variance or significance testing anywhere in the empirical results, which undermines the central claim of consistent improvement; (2) a data leakage confound from the retain set overlapping with fine-tuning data that is not controlled for; (3) missing specification of the critical hyperparameter T_u (unlearning steps), which prevents reproducibility; (4) a theoretical analysis whose strong assumptions limit relevance to actual LLMs; and (5) several claims that overreach the evidence (e.g., "stabler optimization," "direct evidence," "reduced spurious correlations"). The novelty of the core idea (using unlearning as a preparatory stage) is promising but cannot be fully verified against external literature in this run. The paper has a solid empirical foundation but requires major revisions—especially in statistical rigor, confound control, and claim calibration—before it can be considered for publication at a competitive venue.