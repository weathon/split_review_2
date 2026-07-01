## Summary

The paper proposes AUTO-RT, a reinforcement learning framework for automatically discovering jailbreak strategies against large language models. It introduces two techniques—Dynamic Strategy Pruning (DSP) to eliminate redundant exploration paths and Progressive Reward Tracking (PRT) with a First Inverse Rate (FIR) metric to smooth sparse rewards via a downgraded target model. Experiments on 16 white-box and 2 black-box LLMs show improvements in attack success rate, diversity, and efficiency compared to simple baselines.

## Strengths

- **Novel formulation of strategy-level exploration**: Decomposing the attack model into a strategy generator and a rephraser, and treating prompt generation as a sequential decision process, is a principled step beyond fixed-template or intent-specific attacks.
- **Introduction of DSP and PRT with FIR**: The dynamic pruning mechanism and the reward shaping via a carefully selected downgrade model are technically interesting and address real challenges in sparse-reward RL for red-teaming.
- **Extensive model coverage**: The evaluation spans 18 models from multiple families (Llama, Mistral, Yi, Gemma, Qwen, etc.), demonstrating the method’s applicability across diverse safety alignments.

## Weaknesses

### Fatal
None.

### Major

1. **Insufficient comparison with state-of-the-art automated red-teaming methods.** The baselines (Few-Shot, Imitate Learning, RL, Direct Attack) are weak and do not represent the current frontier. Methods such as PAIR, TAP, AutoDAN-turbo, GCG, and Rainbow-Teaming are mentioned in the related work but are not compared in the main experiments. The separate human-based comparison (Table 3) shows that AUTO-RT’s ASR_rst (38.38) is far below AutoDAN (55.23), undermining the claim of superior effectiveness. Without a head-to-head comparison against strong automated baselines, the paper’s core claims are not convincingly supported.

2. **Misleading claim about improvement magnitude.** The abstract states “improving success rates (by up to 16.63%)”, yet the results in Table 1 show much larger absolute gains (e.g., Vicuna 7B: RL 31.95 → AUTO-RT 56.40, a 24.45% absolute increase). This inconsistency suggests either a misstatement or a lack of clarity about whether the figure is relative or absolute. The claim should be precisely stated and verified against the data.

3. **Lack of theoretical or strong empirical justification for the reward shaping in PRT.** The paper acknowledges that the shaped reward does not follow potential-based shaping, making the choice of downgrade model critical. The FIR metric is heuristic, and the paper does not provide theoretical guarantees or a rigorous analysis of when the shaped reward preserves the optimal policy. The ablation study (Table 2) shows PRT helps, but the mechanism is not deeply understood.

4. **Incomplete ablation of the diversity and consistency judges.** The paper introduces two judges (diversity and consistency) as part of DSP, but their individual contributions are not ablated. It is unclear how much of the improvement comes from pruning versus the judges themselves, and whether the penalty values are well-tuned.

### Minor

- The notation is sometimes confusing (e.g., AM^g, AM^r, TM'^d, multiple subscripts and superscripts), and Figure 1 is dense and hard to parse without careful study.
- The paper does not report computational cost (e.g., training time, number of queries) for AUTO-RT versus baselines, making it difficult to assess efficiency trade-offs.
- The black-box experiments (Table 4) use in-context learning to construct the downgrade model, but the results are much lower than white-box, and the comparison with baselines is still limited to the same weak set.

### Trivial
None.

## Nice-to-Haves

- A direct comparison with PAIR, TAP, AutoDAN-turbo, or GCG in the main experimental table would greatly strengthen the paper.
- Qualitative examples of generated strategies and how they differ across methods would help illustrate the diversity claim.
- A discussion of limitations (e.g., when the downgrade model assumption fails, or when FIR selection is ambiguous) would improve completeness.

## Novel Insights

The paper’s key insight is that strategy-level exploration, combined with a downgrade model that broadens the “dangerous subspace” and a metric (FIR) to select the right level of weakening, can make sparse-reward RL for red-teaming more efficient. This idea of using a weaker model as a reward-shaping guide is conceptually clean and could be applied beyond jailbreak discovery.

## Suggestions

1. Include comparisons with at least two strong automated red-teaming baselines (e.g., PAIR and AutoDAN-turbo) in the main results.
2. Clarify the “up to 16.63%” claim: specify whether it is relative or absolute, and ensure it matches the reported numbers.
3. Provide an ablation that isolates the effect of the diversity and consistency judges from the pruning mechanism itself.
4. Add a brief theoretical discussion or additional experiments (e.g., on synthetic reward landscapes) to justify why the FIR-based selection works.

## Score and Decision

**Score**: 4  
**Decision**: Reject

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>