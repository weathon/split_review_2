## Summary

This paper proposes AdaSVD, an adaptive SVD-based compression method for large language models. The method introduces two key components: **adaComp**, which adaptively compensates for SVD truncation errors by alternately updating the singular matrices U and V^T using Moore-Penrose pseudoinverse, and **adaCR**, which assigns layer-specific compression ratios based on the relative importance of each layer. Experiments across multiple LLM/VLM families demonstrate that AdaSVD consistently outperforms existing SVD-based compression methods (FWSVD, ASVD, SVD-LLM) across various compression ratios.

## Strengths

- **Clear and well-motivated problem formulation**: The paper correctly identifies two key limitations of existing SVD-based LLM compression methods: (1) insufficient compensation for truncation errors, and (2) uniform compression ratios across layers. Both issues are practically relevant and well-justified through empirical observations (e.g., Figure 4 showing varying layer importance).

- **Technically sound approach for adaComp**: The use of Moore-Penrose pseudoinverse to solve the least squares estimation problem for updating U and V matrices is a principled way to handle numerical instability. The alternating update scheme is well-motivated and the stack-of-batch strategy for handling limited GPU memory is a practical contribution.

- **Comprehensive experimental evaluation**: The paper evaluates AdaSVD across multiple LLM families (LLaMA2, OPT, Mistral, Vicuna), multiple compression ratios (40%-80%), multiple datasets (language modeling and reasoning), and even extends to VLMs. The ablation studies (Table 3) systematically validate each component.

- **Orthogonality to quantization**: The demonstration that AdaSVD can be combined with GPTQ (Table 4) shows practical value, as SVD compression is often used alongside other compression techniques in deployment scenarios.

## Weaknesses

### Fatal
None.

### Major

- **Incomplete and potentially misleading experimental comparisons**: The main results (Table 1) show that FWSVD and ASVD produce perplexity values in the thousands or tens of thousands at 40-60% compression ratios on LLaMA2-7B, while SVD-LLM and AdaSVD produce much lower perplexity. This raises a serious concern: either the baselines are not properly tuned/reproduced, or the comparison is unfair. The paper states "We reproduce FWSVD, ASVD, and SVD-LLM using their official GitHub repositories" but does not specify whether the same calibration data, preprocessing steps (e.g., data whitening), and evaluation pipeline were used consistently. Given that SVD-LLM already dramatically outperforms FWSVD and ASVD (e.g., perplexity 16.11 vs. 1,609.32 at 40% ratio), the comparison seems to be between methods at very different maturity levels. The paper should clarify whether the data whitening technique from SVD-LLM was applied to all methods or only to SVD-LLM and AdaSVD.

- **Limited novelty of adaCR**: The idea of assigning different compression ratios to different layers based on importance is not new. Prior work in pruning (e.g., layer-wise pruning ratios) and quantization (e.g., mixed-precision quantization) has extensively explored this concept. The specific implementation using cosine similarity between input and output activations is straightforward and lacks theoretical justification for why this particular metric is optimal for SVD compression. The paper does not compare against alternative importance metrics (e.g., sensitivity to perturbation, gradient-based metrics, or Hessian-based metrics).

- **The stack-of-batch strategy is essentially averaging calibration samples**: The stack-of-batch strategy described in Equations 14-15 simply averages groups of calibration samples to fit within GPU memory constraints. This is a practical engineering trick but not a novel algorithmic contribution. The paper does not analyze the information loss from averaging samples or compare against alternative memory-efficient strategies (e.g., gradient accumulation, random subsampling).

- **Lack of theoretical analysis for convergence**: The alternating update scheme for U and V is presented without any convergence guarantees or analysis. While the empirical results show improvement, it is unclear whether the procedure converges to a stationary point, how many iterations are needed, or whether the procedure is guaranteed to reduce the loss monotonically. The ablation study (Table 3c) shows that more iterations can sometimes hurt performance (e.g., at 40% ratio, 1 iteration gives 14.76 perplexity while 15 iterations give 15.84), suggesting potential overfitting or instability.

### Minor

- **The paper claims "state-of-the-art" but comparisons are limited to SVD-based methods only**: The paper only compares against other SVD-based compression methods. While this is acceptable given the paper's focus, the claim of "state-of-the-art" should be qualified as "state-of-the-art among SVD-based methods." The paper does not compare against pruning or quantization methods that may achieve better performance at similar compression ratios.

- **The stack-of-batch strategy is not clearly explained**: The notation in Equations 14-15 is confusing. The variable `mini_bsz` is defined as `ceil(N/M)` but then used as a divisor in the averaging. The indexing in Equation 15 is ambiguous. The paper should clarify how the averaging works and whether this is equivalent to simply using fewer calibration samples.

- **Missing details on the whitening step**: The paper mentions using data whitening from SVD-LLM but does not explain how it is applied or whether it is applied consistently across all baselines. The whitening step is critical for the SVD-LLM method and its inclusion in AdaSVD makes the comparison less clean.

### Trivial

- The caption in Figure 1 is duplicated three times in the text.
- The paper states "We will release all the code and models" but this is not verifiable.
- The ethics statement and LLM usage statement are boilerplate.

## Nice-to-Haves

- A comparison against non-SVD compression methods (e.g., pruning, quantization) at similar compression ratios would strengthen the paper's claims about practical utility.
- An analysis of the computational overhead of adaComp (time and memory) compared to baselines would help practitioners understand the trade-offs.
- A discussion of why the first layer is consistently the most important (Figure 4) and whether this is a general property of LLMs or specific to the evaluated models.

## Novel Insights

None beyond the paper's own contributions. The key insight—that alternating updates of U and V using Moore-Penrose pseudoinverse can compensate for SVD truncation errors—is a reasonable engineering contribution but does not represent a fundamentally new theoretical understanding of SVD compression or LLM behavior.

## Suggestions

- Clarify whether data whitening was applied to all baseline methods or only to SVD-LLM and AdaSVD. If whitening was only applied to SVD-LLM and AdaSVD, the comparison is unfair and should be corrected.
- Provide a theoretical or empirical analysis of the convergence properties of the alternating update scheme. At minimum, show that the loss decreases monotonically or provide a stopping criterion.
- Compare adaCR against alternative importance metrics (e.g., sensitivity to weight perturbation, gradient-based importance, or the importance metric used in pruning methods) to justify the choice of cosine similarity.
- Report the computational cost (time and memory) of AdaSVD relative to baselines, as the alternating update and pseudoinverse computation add overhead.

## Score and Decision

The paper presents a solid engineering contribution to SVD-based LLM compression with two well-motivated components (adaComp and adaCR). The experimental results show consistent improvements over existing SVD-based methods. However, the paper has significant weaknesses: the comparison against baselines may be unfair due to inconsistent application of data whitening, the novelty of adaCR is limited, and the stack-of-batch strategy is a minor engineering trick. The paper is technically sound but the contribution is incremental rather than transformative. I recommend borderline reject.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>