## Summary

This paper investigates how architectural choices—hidden size, MLP-to-attention ratio, and grouped-query attention (GQA)—affect both inference efficiency and model accuracy in decoder-only transformers. The authors propose a conditional scaling law that extends the Chinchilla framework by incorporating architectural parameters, enabling the search for architectures that balance inference throughput and training loss. Through training over 200 models from 80M to 3B parameters, they validate that their framework can identify architectures that outperform LLaMA-3.2 baselines by up to 2.1% in accuracy and 42% in inference throughput.

## Strengths

- **Practical and timely research question**: The paper addresses the underexplored trade-off between model accuracy and inference efficiency, which is a critical concern for deploying LLMs at scale. This fills a genuine gap in the scaling law literature that has predominantly focused on training compute.

- **Comprehensive empirical study**: The authors train over 200 models across multiple scales (80M to 3B) and token budgets (8B to 100B), providing a rich dataset for fitting and validating their conditional scaling law. The progressive evaluation strategy (Task 1-3) demonstrates systematic validation.

- **Clear and actionable framework**: The two-step conditional approach (reference Chinchilla loss + multiplicative/additive calibration) is simple, transparent, and practically useful. The search framework (Algorithm 1) provides a concrete recipe for practitioners to identify inference-efficient architectures.

- **Strong empirical validation**: The fitted scaling laws achieve low MSE and high Spearman correlations across model scales. The resulting Panda and Surefire models consistently outperform LLaMA-3.2 baselines in both accuracy and throughput, with the efficiency gains transferring across serving stacks (vLLM, SGLang) and hardware (A100, H200).

## Weaknesses

### Major

- **Limited scope of architectural factors**: The paper fixes the number of layers and studies only hidden size, MLP-to-attention ratio, and GQA. While the authors justify this by noting that layer count strongly impacts accuracy, this is a significant limitation. The aspect ratio (hidden size / layers) has been shown to be a critical architectural parameter, and fixing layers may miss important trade-offs. The paper would be stronger if it included layer count as a variable or provided a more thorough justification for why it is excluded.

- **The conditional scaling law assumes separability of architectural effects**: The multiplicative and additive formulations (Eq. 3) assume that the effects of hidden size and MLP-to-attention ratio on loss are separable. While the authors ablate joint formulations in the appendix and find they do not improve performance, this assumption is not theoretically justified and may break down at larger scales or for different architectural configurations.

- **GQA handling is ad-hoc**: The paper acknowledges that GQA does not exhibit a consistent continuous relationship with loss and resorts to a local search with early stopping. This is a significant gap in the framework—GQA is a critical architectural choice for inference efficiency, yet the scaling law cannot predict its effect on accuracy. The paper would benefit from a more principled treatment of GQA.

- **Limited scale of validation**: The largest models trained are 3B parameters, and the paper acknowledges that evaluation does not extend to 7B models. While the progressive fitting strategy is reasonable, it remains unclear whether the findings generalize to the scales where inference efficiency is most critical (e.g., 7B-70B models). The ablation of fitting data strategy (Figure 8) suggests that coefficients shift with model size, raising questions about extrapolation reliability.

### Minor

- **The inference efficiency metric is hardware and framework dependent**: The paper uses vLLM on A100 GPUs as the primary evaluation setup. While the authors ablate with SGLang and H200, the search framework (Eq. 4) requires specifying inference efficiency \(I_N(P)\), which is not analytically defined and must be empirically measured. This limits the generalizability of the Pareto-optimal architectures found.

- **The paper does not compare against other architecture search methods**: The proposed framework is compared only against LLaMA-3.2 baselines. It would be stronger to compare against other systematic architecture search approaches (e.g., neural architecture search, Bayesian optimization) to demonstrate the advantage of the scaling law approach.

### Trivial

- The paper uses "Panda" and "Surefire" as model names without clear explanation of the naming convention.

## Nice-to-Haves

- Extending the analysis to include layer count as a variable would significantly strengthen the framework.
- A theoretical analysis of why the U-shaped curves for hidden size and MLP-to-attention ratio arise would deepen understanding.
- Providing the fitted scaling law coefficients for all tasks would aid reproducibility.
- Including downstream task performance breakdowns (not just averages) in the main paper would be informative.

## Novel Insights

The paper's key insight is that the relationship between architectural parameters (hidden size, MLP-to-attention ratio) and training loss follows a consistent U-shaped curve that can be captured by a simple parametric form (\(c_0 + c_1 \log x + c_2/x\)). This observation enables a conditional scaling law that decouples architectural effects from the standard Chinchilla scaling with respect to parameters and tokens. The finding that optimal MLP-to-attention ratios are often much lower than those used in popular open-weight models (e.g., LLaMA-3.2 uses \(r=4.8\) while the optimal is around \(r=1.0\)) is practically significant and challenges current design conventions.

## Suggestions

- Consider incorporating layer count as an additional architectural variable in the conditional scaling law, even if only for a subset of experiments, to demonstrate the framework's flexibility.
- Provide a more rigorous treatment of GQA, perhaps by modeling its effect on loss through a discrete correction term or by collecting more data points to characterize its relationship with accuracy.
- Include a comparison against a simple baseline (e.g., random architecture search or grid search) to quantify the value added by the scaling law predictions.
- Discuss the practical implications of the finding that optimal MLP-to-attention ratios are around 1.0, which is significantly lower than many current models.

## Score and Decision

The paper addresses a timely and important problem with a well-designed empirical study and a practical framework. The conditional scaling law is simple yet effective, and the validation across multiple scales is thorough. However, the limited scope of architectural factors (excluding layer count) and the ad-hoc treatment of GQA are notable weaknesses. The paper makes a solid contribution but falls short of the transformative impact expected for a top-tier venue.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>