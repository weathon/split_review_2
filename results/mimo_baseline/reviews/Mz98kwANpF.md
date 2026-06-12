## Summary

This paper challenges the prevailing paradigm in multi-task LoRA that architectural diversity (multiple adapters/heads with routing) is essential for effective multi-task learning. The authors show that a simplified multi-head variant (M-LoRA) with high inter-head similarity outperforms complex diversity-focused methods, and that simply increasing the rank of a standard single-adapter LoRA matches multi-component architectures. Based on these findings, they propose Align-LoRA, which adds a KL-divergence or MMD-based alignment loss to encourage task-shared representations in the low-rank space, achieving superior performance with zero additional inference overhead.

## Strengths

- **Genuinely counter-intuitive and well-supported empirical finding**: The "paradox of diversity" (Section 3.2) is compelling — M-LoRA, which removes the router and exhibits the highest inter-head similarity (~0.85), consistently outperforms R-LoRA and HydraLoRA across all five tasks (Table 1: 75.45 vs 74.67 vs 74.04 average). This directly challenges a core assumption in recent multi-task LoRA work.

- **Practical and impactful method**: Align-LoRA introduces zero inference overhead (weights remain mergeable), uses fewer trainable parameters than multi-component baselines (0.20% vs 0.25-0.38% in Table 4), and achieves consistent improvements across three model families (Qwen2.5, LLaMA3) and scales (3B-14B). This is a meaningful practical contribution.

- **Well-structured narrative with progressive evidence**: The paper builds its case methodically — first showing M-LoRA's superiority, then showing rank-scaling suffices, then proposing Align-LoRA to validate the shared-representation hypothesis. Each step motivates the next, making the argument coherent and persuasive.

- **Comprehensive evaluation breadth**: Experiments span multiple base models (LLaMA2, LLaMA3, Qwen2.5), model scales (3B-14B), evaluation paradigms (in-domain multi-task and out-of-domain generalization to BBH), and two alignment loss instantiations (KL and MMD), providing robust evidence.

## Weaknesses

### Fatal

None.

### Major

- **MMD variant inconsistency undermines the generality claim**: In Table 4, A-LoRA-M (MMD) actually underperforms M-LoRA on Qwen2.5-7B (47.53 vs 48.44) and Qwen2.5-14B (52.24 vs 53.78). The paper claims "both KL and MMD-based alignment strategies elevate performance above the standard LoRA baseline," but the more important comparison is against M-LoRA and other strong baselines, where MMD fails. This weakens the claim that representation alignment is a robust, general principle rather than a property specific to KL divergence.

- **The "task-shared vs. task-specific" dichotomy is overstated**: The paper repeatedly frames its contribution as demonstrating that task-shared learning is superior to task-specific isolation. However, the evidence is more nuanced. M-LoRA's success could be attributed to the specific interaction between multi-head dropout and summation (an implicit regularization effect), not necessarily to "shared representations" per se. The alignment loss works, but the paper doesn't disentangle whether it succeeds because of genuine shared-representation learning or because it acts as an effective regularizer that prevents overfitting to task-specific noise.

- **Rank-scaling comparison is not fully controlled**: In Tables 2-3, the high-rank LoRA (rank=30 or 10) is compared against multi-head variants at rank 4. While parameter-matched, the paper doesn't explore whether multi-head variants would also benefit from higher rank per head. The claim that "architectural complexity is unnecessary" would be stronger with this ablation.

### Minor

- **Unnamed tasks in Table 5**: The 8-task benchmark uses generic labels (Task1-8) without identifying the actual tasks, making it difficult for readers to assess the diversity and difficulty of the evaluation. This hinders reproducibility and interpretability.

- **Theoretical analysis is high-level**: The generalization bound in Section 5.3 is a relatively standard application of domain adaptation bounds (resembling Ben-David et al., 2006 style results). The key claim that alignment "actively minimizes Δ(Di, Dj)" during training is asserted but not formally connected to the empirical KL/MMD losses used. The bound's practical tightness is not discussed.

- **Sensitivity to λ is narrow**: Figure 3 shows Align-LoRA peaks at λ=0.10 and the improvement window is relatively narrow (75.10-75.75%). While the method is "robust" in the sense of always beating baselines, the gains are modest for suboptimal λ values, suggesting the method requires careful tuning.

### Trivial

None.

## Nice-to-Haves

- An ablation studying whether multi-head variants also benefit from increased per-head rank would strengthen the claim about architectural complexity being unnecessary.
- Identifying the 8 tasks in Table 5 and providing per-task analysis would improve interpretability.
- A comparison of Align-LoRA applied to full fine-tuning or other PEFT methods would help establish whether the alignment principle is LoRA-specific or more general.

## Novel Insights

The paper's most genuinely novel insight is the empirical demonstration that removing the router from a multi-head LoRA architecture (creating M-LoRA) paradoxically improves performance despite increasing head redundancy. This finding, combined with the observation that high-rank single-adapter LoRA matches multi-component architectures, provides a compelling case that the field's focus on architectural diversity for multi-task LoRA may be misguided. The alignment loss itself, while drawing from domain adaptation literature, is a novel and practical application to the LoRA multi-task setting that hadn't been explored before.

## Suggestions

- Add an ablation where multi-head variants (HydraLoRA, R-LoRA) are given proportionally higher per-head rank to match the total parameter budget of high-rank LoRA, directly testing whether architecture or capacity drives performance.
- Provide the MMD variant with its own hyperparameter tuning (it may require different λ values than KL) before concluding that KL is superior, or discuss why MMD underperforms.
- Name the 8 tasks in Table 5 and provide a brief analysis of which task types benefit most from alignment.

## Score and Decision

The paper presents a well-motivated challenge to existing multi-task LoRA paradigms, supported by solid empirical evidence across multiple models and scales. The core findings (M-LoRA's superiority, rank-scaling sufficiency) are genuinely interesting and the proposed Align-LoRA is practical and effective. However, the MMD variant's inconsistency, the somewhat overstated framing around "shared vs. specific" representations, and the incomplete rank-scaling ablation prevent a stronger score. The paper is above the median for ICLR submissions and makes a clear contribution, but the claims occasionally outpace the evidence.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept