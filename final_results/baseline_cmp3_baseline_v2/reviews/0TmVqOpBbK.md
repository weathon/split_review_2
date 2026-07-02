## Summary

This paper investigates how architectural choices—hidden size, MLP-to-attention ratio, and grouped-query attention (GQA)—affect both inference efficiency and model accuracy in decoder-only transformers. The authors propose a conditional scaling law that extends the Chinchilla framework by incorporating architectural parameters, enabling the prediction of training loss for different architectural configurations. They validate their approach by training over 200 models (80M to 3B parameters) and demonstrate that architectures optimized using their framework achieve up to 42% higher inference throughput and 2.1% better accuracy compared to LLaMA-3.2 baselines under the same training budget.

## Strengths

- **Practical and timely research question**: The paper addresses a critical gap in scaling law research by explicitly modeling the trade-off between inference efficiency and accuracy, which is highly relevant given the deployment costs of large language models. The focus on inference efficiency is well-motivated and practically important.

- **Comprehensive empirical study**: The authors train over 200 models across multiple scales (80M to 3B) with systematic variation of architectural factors, providing a rich dataset for fitting and validating their scaling laws. The progressive evaluation strategy (Task 1-3) demonstrates careful experimental design.

- **Novel conditional scaling law formulation**: The two-step approach of using Chinchilla's optimal loss as a reference point and then calibrating architectural effects via multiplicative/additive corrections is elegant and practical. The U-shaped relationships identified for both hidden size and MLP-to-attention ratio are empirically well-supported and provide actionable insights.

- **Clear practical impact**: The resulting Surefire models demonstrate meaningful improvements in both accuracy (up to 2.1%) and inference throughput (up to 42%) over LLaMA-3.2 baselines, with consistent results across different serving frameworks (vLLM, SGLang) and hardware (A100, H200).

## Weaknesses

### Major

- **Limited validation at larger scales**: The paper's primary validation is at 1B and 3B parameters, with the largest model being 3B. While the authors acknowledge this limitation, the practical utility of the scaling law for predicting optimal architectures at 7B+ scales (where inference costs are most pressing) remains unvalidated. The observation that fitting on closer-size-range models (1B for predicting 3B) works better than fitting on smaller models (80M-297M) raises questions about how well the law extrapolates to significantly larger scales.

- **Fixed number of layers assumption**: The paper fixes the number of layers and studies hidden size and MLP-to-attention ratio, but this is a significant restriction. The authors acknowledge that layer count strongly influences accuracy, yet they do not provide a principled justification for fixing it rather than incorporating it into the scaling law. This limits the generality of the framework, as optimal layer count likely interacts with the other architectural factors studied.

- **Separability assumption not fully justified**: The conditional scaling law assumes that the effects of hidden size and MLP-to-attention ratio on loss are separable (multiplicative or additive). While the authors ablate non-separable formulations and find they don't improve performance, the theoretical justification for separability is weak. The U-shaped curves in Figures 4 and 5 are shown conditioned on the other factor being fixed, but this doesn't demonstrate that the effects are independent.

### Minor

- **GQA treatment is ad-hoc**: Unlike hidden size and MLP-to-attention ratio, GQA is handled via a local search with early stopping rather than being incorporated into the scaling law. The authors note that GQA doesn't exhibit a consistent continuous relationship with loss, but this limits the completeness of the framework and makes the search procedure less principled.

- **Training token budget is relatively small**: Models are trained on 100× parameter count tokens (e.g., 3B models on 100B tokens), which is only about 5× the Chinchilla-optimal ratio. While this is stated as ensuring convergence, it's unclear whether the scaling law predictions would hold at the much larger token budgets used in practice (e.g., LLaMA-3.2-3B was trained on ~2T tokens).

- **Limited downstream evaluation**: The evaluation uses nine benchmarks, but these are relatively standard and may not capture the full range of capabilities where architectural differences matter. The 2.1% average improvement for Panda-1B over LLaMA-3.2-1B is notable, but the improvement for Panda-3B is only 0.6%, suggesting diminishing returns.

### Trivial

- The paper could benefit from more explicit discussion of how practitioners should choose between the multiplicative and additive calibration forms.

## Nice-to-Haves

- Extending the analysis to include layer count as a variable in the scaling law would significantly increase the framework's generality.
- Validation at 7B+ scales would substantially strengthen the practical claims.
- Analysis of how the optimal architecture changes with different inference hardware (e.g., memory-bandwidth-bound vs. compute-bound regimes) would be valuable.

## Novel Insights

The paper's key insight is that architectural factors like hidden size and MLP-to-attention ratio exhibit U-shaped relationships with training loss, with optimal values that can be predicted via a conditional scaling law. This challenges the common practice of simply scaling up existing architectures without considering these trade-offs. The finding that larger hidden sizes and higher MLP-to-attention ratios can simultaneously improve both inference throughput and accuracy (up to a point) is non-trivial and practically valuable. The observation that fitting the scaling law on models within a closer size range to the target (e.g., 1B for predicting 3B) yields better predictions than fitting on much smaller models is an important practical consideration for practitioners.

## Suggestions

- Provide guidance on how to determine the appropriate size range of fitting models for a given target scale, as the paper shows that fitting on 1B models works better than fitting on 80M-297M models for predicting 3B behavior.
- Consider incorporating layer count into the scaling law or providing a principled justification for fixing it, as this is a significant architectural degree of freedom in practice.
- Validate the framework at 7B+ scales or provide stronger theoretical guarantees about extrapolation to larger scales.

## Score and Decision

The paper makes a solid contribution to an important and timely problem. The empirical work is thorough, the conditional scaling law formulation is novel and practical, and the results demonstrate clear improvements over strong baselines. However, the limited scale of validation (max 3B parameters) and the fixed layer count assumption temper the strength of the claims. The paper is well within the acceptance range for ICLR but falls short of the highest tier due to these limitations.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>