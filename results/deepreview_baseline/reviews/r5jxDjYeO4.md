## Summary

This paper proposes Adaptive Serial-Parallel Decoding (ASPD), a framework that accelerates LLM inference by exploiting intrinsic parallelism in autoregressive outputs. The approach consists of: (1) a non-invasive data pipeline that automatically extracts parallelizable structures from model responses using LLM rewriting and verification, (2) architectural modifications with branch-invisible attention masks and shared position IDs that enable parallel decoding within a single sequence, and (3) a Hybrid Decoding Engine that seamlessly switches between serial and parallel modes. Evaluations on general tasks, RAG, and mathematical reasoning show speedups of 1.04-1.82× with minimal quality degradation.

## Strengths

1. **Novel exploitation of intrinsic parallelism in LLM outputs.** The observation that many autoregressive responses contain segments that can be generated in parallel is well-motivated and supported by empirical analysis across multiple datasets (Figure 1). This insight is a genuine contribution that opens a new direction for accelerating inference beyond speculative decoding.

2. **Clean architectural design for parallel decoding within a single sequence.** The branch-invisible attention masks and shared position IDs (Section 3.2) elegantly enable parallel decoding without batching, threading, or external overhead. The authors correctly identify and resolve key issues faced by prior work (APAR’s KV-cache discarding, PASTA’s position encoding mismatches) through principled visibility and position encoding strategies.

3. **Comprehensive and rigorous evaluation.** The paper evaluates across diverse domains (general QA, RAG, mathematical reasoning), multiple model architectures (Vicuna-7B, Qwen2.5-7B, Qwen2.5-32B), and includes ablation studies on data pipeline, attention masks, and position encoding. The speed-quality trade-off analysis (Figure 4) clearly demonstrates that ASPD outperforms prior methods like APAR and SoT in maintaining quality while achieving competitive speedups.

4. **Practical non-invasive data transformation pipeline.** The automated pipeline for extracting parallel structures (Section 3.1) is well-designed with four stages that ensure semantic integrity, independence, and quality. The use of preference-based selection over multiple candidates is a pragmatic choice that improves data quality.

## Weaknesses

### Major
1. **Modest acceleration and limited speedup on reasoning tasks.** The average speedup on Vicuna Bench is 1.82×, but on MT Bench it is 1.30× and on RAG 1.46×, while mathematical reasoning achieves only 1.04–1.17× TPS (Table 3). This suggests that the method’s benefit is task-dependent and may be modest for complex reasoning where parallelism is limited. The paper claims “up to 3.10×” but this appears to be on a single subtask (Coding) and the average is far lower.

2. **Fine-tuning requirement limits practical adoption.** ASPD requires fine-tuning the base model with parallelized data and special tokens. This is a significant barrier compared to speculative decoding or prompt-based methods that work with frozen models. The paper does not discuss the training cost (compute, time) or the generalization to larger models (70B+) where fine-tuning is expensive.

3. **Data pipeline relies on a large LLM for data construction.** The parallel rewriting and verification stages use a powerful LLM (Qwen3-235B-A22B) for each training example. While this is one-time preprocessing, the computational cost is nontrivial and the method’s effectiveness depends on the quality of this auxiliary model. The paper does not analyze the scalability of data construction or the impact of using smaller/worse verifiers.

4. **Comparison with baselines could be stronger.** APAR* is a retrained version with improved data quality, but the original APAR (which uses rule-based data) is also presented. However, a direct comparison of ASPD against the original APAR’s codebase without the data quality improvement would better isolate the benefits of the architecture. Additionally, the paper does not compare against other concurrent works (e.g., Multiverse) quantitatively, though they are discussed in related work.

### Minor
5. **No analysis of attention mask computational overhead.** The branch-invisible mask described in Eq. 2 modifies the attention pattern during parallel decoding. The paper claims “without batching or threading overhead” but does not quantify the additional cost of computing visibility masks or the potential impact on inference latency for models with large hidden dimensions.

6. **Lack of statistical significance or variance for scores.** The main quality scores (Tables 1, 2) are reported as single numbers without confidence intervals or multiple runs. Given that LLM-as-judge evaluations can be noisy, reporting variance would strengthen the claims, especially for the marginal differences (e.g., Q-ASPD 9.03 vs Q-Seq 9.11).

7. **Special token overhead not fully characterized.** The Hybrid Decoding Engine introduces six special tokens and switching logic. The paper reports TPS but does not break down the time spent on switching, token generation overhead, or the effect of unequal branch lengths on decoding efficiency.

### Trivial
None.

## Nice-to-Haves
- Analysis of how the proportion of parallelizable data (PPD) in the training corpus correlates with downstream speedup.
- Comparison with speculative decoding methods (e.g., Medusa, draft models) that are also designed for single-sequence acceleration.
- Discussion of the minimum length or complexity of responses where the method becomes worthwhile.

## Novel Insights
The paper’s key insight is that autoregressive LLM outputs contain intrinsic parallelism—segments that are semantically independent and can be generated concurrently—and that this property can be systematically extracted and exploited without changing the output distribution. The branch-invisible attention mask with shared position IDs is a simple yet effective solution that allows each parallel branch to behave as if it were decoding in isolation while maintaining compatibility with the main branch. This avoids the complexity of batched decoding or external verifiers used in speculative decoding, and it correctly handles the position encoding problem that plagued PASTA. The ablation studies provide clear evidence that (1) independent (invisible) attention masks outperform visible masks for this task, and (2) shared position IDs with sequential ordering upon merging (Same-Seq) is superior to alternative position encoding strategies.

## Suggestions
1. Report speedups relative to the sequential fine-tuned baseline (V-Seq) in addition to the original model, as this better isolates the benefit of parallel decoding from fine-tuning effects.
2. Provide variance estimates (e.g., standard deviation across multiple seeds or runs) for the LLM-as-judge scores in Tables 1 and 2.
3. Add a small-scale analysis of the data construction pipeline cost (number of API calls or compute hours) to help practitioners assess feasibility.
4. Evaluate on a larger model (e.g., 70B) to demonstrate scalability, or at least discuss expected challenges.

## Score and Decision
**Score: 7.5**  
**Decision: Accept**

The paper makes a solid contribution to the important problem of LLM inference acceleration. The core idea of exploiting intrinsic parallelism is novel and well-executed, with thorough experiments across multiple domains and model sizes. The limitations (modest acceleration on some tasks, fine-tuning requirement, reliance on a strong LLM for data construction) are clearly presented and do not invalidate the contribution. The paper is well-written, the methodology is sound, and the ablation studies convincingly support the design choices. This is a quality submission that deserves acceptance at ICLR.

MY FINAL SCORE: 7.5
MY FINAL DECISION: Accept