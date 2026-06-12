## Summary

This paper identifies a critical failure mode in LLM unlearning—the *squeezing effect*—where gradient ascent and its variants suppress target responses but redistribute probability mass to semantically related paraphrases, yielding only spurious forgetting. To address this, the authors propose a bootstrapping framework (BS-T and BS-S) that explicitly incorporates the model’s own high-confidence predictions (its “beliefs”) into the unlearning objective, jointly suppressing both original targets and high-likelihood alternatives. The method is supported by a theoretical analysis within the AKG learning dynamics framework and demonstrates strong empirical results across TOFU, MUSE, and WMDP benchmarks with multiple model families.

## Strengths

- **Clear identification and mechanistic analysis of an overlooked problem.** The paper systematically demonstrates the squeezing effect via both qualitative case studies and quantitative probability dynamics, showing that existing methods (GA, NPO) produce superficially convincing metrics while models still generate semantically rephrased harmful content. This is a valuable contribution to the LLM unlearning literature.
- **Principled and practical solution.** The bootstrapping framework is conceptually simple yet grounded in the observed failure mode. The token-level (BS-T) and sequence-level (BS-S) instantiations are well-motivated, compatible with existing loss functions, and require minimal architectural changes. The theoretical connection to gradient dynamics (Thm. 5.2 and 5.3) provides rigour.
- **Strong and consistent empirical results.** The experiments cover multiple benchmarks (TOFU, MUSE, WMDP), model scales (1B to 8B), and forget ratios. BS-T and BS-S consistently outperform strong baselines (NPO, WGA, RMU, SimNPO) on aggregate metrics while maintaining competitive utility. The LLM-based evaluation (Fig. 4c) directly confirms that the method genuinely mitigates spurious unlearning.
- **Reproducibility and integration.** The code is merged into the OpenUnlearning framework, lowering the barrier for adoption and comparison.

## Weaknesses

### Fatal

No fatal errors are present.

### Major

No major issues invalidate the paper’s core claims.

### Minor

- **Theoretical assumptions are limiting.** The AKG decomposition (Lem. 5.1) relies on a lazy eNTK approximation and teacher forcing. While the analysis provides useful intuition, real-world training dynamics with auto-regressive sampling may deviate from these simplifications. The paper does not discuss how violations of these assumptions might affect the conclusions.
- **LLM-as-a-judge evaluation is used without human validation.** The paper introduces a novel LaaJ evaluation for naturalness and similarity but does not report correlation with human judgments. While the authors cite prior work supporting LaaJ alignment, a small-scale human study would strengthen confidence in the metric, especially given the paper’s own critique of existing metrics.
- **Notation inconsistency in GA formulation.** The paper defines gradient ascent as $\min_{\theta} \mathbb{E}[\log \pi_\theta]$, which is mathematically equivalent to maximizing the NLL but is confusing from a naming perspective (standard GA typically maximizes $-\log \pi_\theta$). This does not affect correctness but hurts readability.
- **Hyperparameter and computational costs are deferred to appendix.** The main text omits discussion of sensitivity to $\lambda_{\text{BST}}$, $k$, $N$, and training overhead. While these details are promised in the appendix, their absence in the main body makes it harder to judge practical deployment costs from the core paper.

### Trivial

- Some figure captions (e.g., Fig. 2) include redundant auto-generated text that could be trimmed for clarity.
- The abbreviation “LaaJ” (LLM-as-a-Judge) is occasionally used in a way that may confuse readers unfamiliar with the term.

## Nice-to-Haves

- A small human evaluation to validate the proposed LaaJ metrics would further increase trust in the qualitative results.
- Ablation on the number of bootstrapped sequences $N$ (currently in appendix) could be briefly summarized in the main text to illustrate the trade-off between forgetting thoroughness and computational cost.
- A discussion on the limitation of the AKG framework (linearization) and empirical validation that the derived residuals indeed correlate with final token-level changes would strengthen the theoretical claims.

## Novel Insights

None beyond the paper’s own contributions. The core insight—that unlearning must counteract the redistribution of probability mass into model beliefs—is a new and useful perspective for the field, and the connection to the squeezing effect in fine-tuning (Ren & Sutherland, 2025) is a well-adapted transfer.

## Suggestions

- Clarify the GA objective formulation in §2.2 by either explicitly stating the gradient ascent direction or using the more standard notation $\max_{\theta} \mathbb{E}[-\log \pi_\theta]$ to avoid confusion.
- Report the correlation between LaaJ scores and human judgment on a small sample of responses to strengthen the evaluation, or at least discuss the expected alignment.
- Include a brief discussion of how the key hyperparameters ($\lambda_{\text{BST}}$, $k$, $N$) affect the forget-vs-retain trade-off in the main paper, even if full results are in the appendix.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>