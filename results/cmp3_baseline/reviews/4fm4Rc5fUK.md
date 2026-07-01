## Summary

This paper presents Autoformalizer with Tool Feedback (ATF), a framework that integrates syntactic (Lean 4 compiler) and semantic consistency (multi-LLM-as-judge) tools into the autoformalization process. The model is trained via a three-stage pipeline—cold-start on synthetic tool-calling data, expert iteration, and DPO—to iteratively refine generated formal statements based on tool feedback. ATF achieves substantial improvements over existing formalizers across three benchmarks (e.g., 29.13% relative gain in semantic consistency on CombiBench), demonstrates favorable inference-time scaling, and the authors release a 750K formal statement dataset.

## Strengths

- **Novel and well-motivated approach**: The paper identifies two concrete bottlenecks in autoformalization—lack of formal knowledge and unreliable consistency validation—and addresses them by incorporating tool feedback directly into the generation process. This is a principled extension of tool-integrated reasoning to the autoformalization setting.
- **Strong empirical results**: ATF-32B consistently outperforms all baselines (including Goedel-V2-Formalizer-32B) on both syntax and consistency metrics across all three benchmarks, with particularly large margins on the out-of-distribution CombiBench. The gains are validated by human evaluation, and the consistency check tool shows high correlation with human judgments (Pearson r=0.746).
- **Comprehensive and well-designed experiments**: The paper includes thorough ablations (tool components, training stages), scaling analysis (revision attempts and parallel sampling), and detailed tool usage analysis. The training pipeline is clearly described, and the open-source dataset is a valuable community resource.
- **Clear exposition and strong empirical methodology**: The problem is clearly framed, the method is explained with sufficient detail, and the evaluation is rigorous (decontamination, multiple metrics, human evaluation, unbiased pass@k).

## Weaknesses

### Major

- **Consistency check reliability remains a concern despite benchmarking**: The multi-LLM-as-judge approach achieves an FPR of 5.79% and FNR of 40.33% on the constructed benchmark. While the ensemble reduces false positives, the high false negative rate means many semantically correct statements may be incorrectly rejected during training and inference. The paper does not fully discuss how this affects the quality of the training data or the final model's behavior. The human evaluation correlation is strong, but the benchmark itself is synthetic and may not capture all failure modes.

- **DPO phase provides only marginal improvements**: The ablation shows that DPO adds only 1–2% absolute gain on most metrics (e.g., CombiBench consistency from 63.88% to 65.38%). Given the complexity of collecting preference pairs and the risk of instability, the contribution of this phase is somewhat incremental. The paper could have explored alternative methods (e.g., simply filtering out long trajectories) or provided more analysis on when DPO helps.

### Minor

- **Limited novelty in tool-integrated reasoning**: The idea of using external tools (compilers, LLM judges) for iterative refinement is well-established in theorem proving (e.g., Lean verifier loops) and other domains. The paper's main novelty lies in applying this to autoformalization with a dedicated training pipeline, but the individual components (syntax check, consistency check) are relatively straightforward. The paper would benefit from a clearer discussion of what is specifically new beyond the combination.

- **Reproducibility concerns**: Training requires 128 NPUs and uses Claude-4-Sonnet for cold-start data synthesis, which is a proprietary model. While the authors open-source the final dataset, the exact training recipe may be difficult to reproduce without access to the same compute and API.

### Trivial

- Figure 1 caption is duplicated and the third failure example is not explained. The figure quality is adequate but the caption could be more informative.

## Nice-to-Haves

- An analysis of the types of syntax errors that persist after tool feedback (e.g., missing imports vs. type mismatches) would deepen understanding of the model's limitations.
- A comparison with a simpler baseline that uses only syntax feedback (without consistency check) but with more revision attempts would help isolate the value of the consistency tool.
- The paper could discuss the computational cost of the multi-LLM-as-judge approach and whether cheaper alternatives (e.g., a single strong model with calibrated confidence) could achieve similar FPR.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide a more detailed analysis of the false negative cases in the consistency check benchmark and discuss how they might affect the training data quality. Consider releasing the consistency benchmark to facilitate future work.
- Clarify whether the DPO phase could be replaced by a simpler filtering strategy (e.g., discarding trajectories with >N revisions) and whether the gains are statistically significant.
- Include a discussion of the limitations of the consistency check tool, especially its high FNR, and potential mitigations (e.g., using a stronger judge model or incorporating proof search feedback).

## Score and Decision

**Score**: 8  
**Decision**: Accept

The paper makes a clear and significant contribution to autoformalization by demonstrating that tool feedback can be effectively integrated into the generation process, leading to large empirical gains. The methodology is sound, the experiments are thorough, and the released dataset is a valuable resource. The weaknesses (consistency check reliability, marginal DPO gains) are not fatal and are partially addressed by the human evaluation and ablation studies. The paper is well within the acceptance range for ICLR.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>