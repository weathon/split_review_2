## Summary

This paper proposes AdaSVD, an adaptive SVD-based compression method for LLMs with two key components: **adaComp**, which compensates for SVD truncation errors by alternately updating the left and right singular matrices using Moore-Penrose pseudoinverse solutions, and **adaCR**, which assigns layer-specific compression ratios based on the cosine similarity between layer inputs and outputs. The method also introduces a stack-of-batch technique to use more calibration data under memory constraints. Experiments on several LLMs and VLMs show that AdaSVD consistently outperforms prior SVD-based compression methods (FWSVD, ASVD, SVD-LLM) across a range of compression ratios.

## Strengths

- **Novel adaptive compensation (adaComp)** provides a principled post-truncation adjustment of the singular matrices, reducing the objective \(\|\widehat{\mathcal{W}}\mathcal{X} - \mathcal{W}\mathcal{X}\|_F^2\) more effectively than prior methods that stop after truncation. The use of Moore-Penrose pseudoinverse for the update steps is a practical fix for numerical instability.
- **Stack-of-batch strategy** is a simple yet effective technique to aggregate calibration samples, enabling the use of more data under fixed GPU memory without increasing matrix sizes. The ablation demonstrates clear MSE reduction.
- **Adaptive per-layer compression ratio (adaCR)** based on input–output similarity is well motivated by the observation that layer importance varies significantly (e.g., first layer is always most important). The assignment formula is straightforward and leads to consistent perplexity improvements over uniform compression ratios.
- **Thorough empirical evaluation** across multiple LLM families (LLaMA2, OPT, Mistral, Vicuna) and a VLM (LLaVA), at compression ratios ranging from 40% to 80%, with comparisons to three SOTA SVD methods. AdaSVD achieves the best perplexity and zero-shot accuracy in nearly all settings.
- **Orthogonality to quantization** is demonstrated by combining AdaSVD with GPTQ-INT4, showing further gains over SVD-LLM+GPTQ.

## Weaknesses

### Fatal
None.

### Major
- **Computational cost of adaComp is not discussed.** Each alternating iteration requires two SVDs (on matrices of size \(\mathcal{X}^\top \mathcal{V}_k^\sigma\) and \(\mathcal{U}_k^\sigma\)) plus matrix multiplications. The paper does not report wall-clock time, FLOPs, or the trade-off between cost and the added performance. This makes it hard to judge practical viability, especially since some gains come from multiple alternating iterations.
- **The layer importance metric in adaCR is ad-hoc.** Using cosine similarity between \(\mathcal{X}\) and \(\mathcal{Y}\) is one of many possible choices, and the paper provides no justification or comparison with other metrics (e.g., output sensitivity, gradient-based importance, singular value entropy). The linear interpolation to assign compression ratios (Eq. 19) is also arbitrary; the sensitivity analysis in Table 3d only varies the minimum retention ratio, not the functional form.

### Minor
- **Gains at moderate compression ratios (40%) are modest.** On LLaMA2-7B WikiText-2, AdaSVD improves perplexity from 16.11 (SVD-LLM) to 14.76—an 8% relative improvement. While consistent, this is not a dramatic leap. The paper’s claim of “significantly outperforming” is more justified at higher ratios (e.g., 60%: 89.90 → 50.33).
- **No convergence guarantee or analysis for the alternating update.** The approach is a block coordinate descent on a non-convex objective; the paper does not discuss whether it converges to a stationary point or how the number of iterations should be selected in general (ablation shows overfitting at low compression ratios with many iterations).
- **Stack-of-batch is simply sample averaging**; while effective, it is a straightforward workaround without theoretical insight. The paper does not explore alternative strategies (e.g., gradient accumulation, randomized SVD) that might achieve similar benefits.
- **Reproducibility details are incomplete.** The paper states the code will be released, but the exact hyperparameters for adaCR (mrr, trr) per experiment and the number of alternating iterations used in the main results are not fully specified (the ablation suggests 1 iteration at 40%, but the main results may use different values). The pseudocode in Algorithm 1 leaves some details vague (e.g., the WHITENING function, SOB details).

### Trivial
None.

## Nice-to-Haves
- A comparison with “fine-tuning” only the low-rank matrices via gradient descent (with the same calibration data) would strengthen the claim that the closed-form pseudoinverse update is beneficial.
- Reporting the end-to-end time for AdaSVD versus SVD-LLM for a given compression ratio would help practitioners assess the overhead.
- An analysis of the cosine similarity metric’s correlation with layer-wise performance loss would add depth to adaCR.

## Novel Insights
None beyond the paper’s own contributions: the demonstration that post-truncation alternating updates of singular matrices can reduce SVD compression error more effectively than prior preprocessing-only methods, and that layer importance measured by input-output similarity provides a useful signal for allocating compression budgets.

## Suggestions
- Add a table comparing the runtime (seconds) of AdaSVD (including adaComp iterations) with SVD-LLM and other baselines for at least one model and compression ratio.
- Explicitly state the number of alternating iterations used in all main experiments (e.g., Table 1) and justify the choice. The ablation shows 1 iteration is best at 40%, but the main results might use 1 iteration as well—clarify.
- For adaCR, consider comparing the cosine-similarity metric with alternatives (e.g., norm ratio, Fisher information) on a small model to justify the design choice.
- Provide a brief discussion on the convergence of the alternating update (e.g., it is a Gauss-Seidel-like solver for a linear least squares problem when the objective is bilinear?).

## Score and Decision
**Score**: 8.0  
**Decision**: Accept

I assess that the paper makes a clear, well-supported contribution to LLM compression. The adaptive compensation and per-layer ratio are both effective and the experiments are thorough. The weaknesses (lack of cost analysis and ad-hoc importance metric) are manageable and do not invalidate the core claims. The paper is above the borderline and merits acceptance.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>