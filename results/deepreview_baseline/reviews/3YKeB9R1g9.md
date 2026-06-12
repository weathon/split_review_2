## Summary

This paper demonstrates that training loss curves (TLCs) from LLMs of different sizes collapse onto a universal trajectory when three controls are matched: the AdamW timescale τ, the tokens-per-parameter ratio (TPP), and the learning-rate schedule. The authors identify τ as a key modulator of TLC shape through its control of the bias-variance trade-off, and show that when τ is set optimally for a given TPP (following recent scaling laws), collapse emerges naturally as a signature of compute-efficient training. They introduce the Celerity model family trained under this collapse regime, demonstrate that deviations from collapse serve as early diagnostics for training pathologies, and propose a method for early stopping in hyperparameter tuning by aligning partial training curves to predicted normalized TLCs.

## Strengths

- **Novel and practically valuable insight**: The paper identifies that collapse of training loss curves is not merely a theoretical curiosity but a practical signature of well-tuned, compute-efficient training. The connection between optimal τ scaling and collapse is a genuine contribution that bridges scaling law theory with practical LLM training.

- **Strong empirical validation at meaningful scale**: The experiments span from 111M to 3.9B parameters across multiple TPP bands (20, 80, 234), demonstrating that the phenomenon holds at scales relevant to modern LLM development. The Celerity models are shown to lie on the compute-efficiency frontier, validating that collapse coincides with good training outcomes.

- **Actionable diagnostic tool**: The demonstration that collapse residuals can detect training issues (numerical instability in the 1.8B run) earlier than raw loss curves is compelling and practically useful. The ability to pinpoint the onset of divergence (~60% of training) rather than just noticing symptoms late (~90%) is a concrete benefit for large-scale training teams.

- **Principled early stopping method**: The proposed procedure for early stopping in hyperparameter tuning—fitting a parametric surrogate for normalized TLCs at small scale, then aligning partial large-scale curves to predict final loss—is well-motivated and shows strong results (near-zero loss gap after 10-30% of training).

## Weaknesses

### Major

- **Limited evaluation of Celerity models**: The paper claims Celerity is "competitive" and on the "compute-efficiency frontier," but the evaluation is limited to 7 common downstream tasks (ARC-c, ARC-e, BoolQ, HellaSwag, PIQA, SIQA, WinoGrande). Modern LLM evaluation typically includes many more benchmarks (MMLU, GSM8K, HumanEval, etc.). Without broader evaluation, it's difficult to assess whether the collapse-guided training actually produces models with general capabilities or if the results are specific to these particular tasks.

- **The parametric surrogate model (Eq. 4-5) is under-validated**: The proposed functional form for normalized TLCs is fit on 111M-scale data and evaluated on 3.3B-scale data, but the paper only shows one example prediction (Figure 8) and reports aggregate MAE in the appendix. It's unclear how robust this surrogate is across different architectures, data distributions, or hyperparameter ranges. The alternating fitting procedure for b and q parameters, while computationally efficient, may not converge to the global optimum.

- **The "early-align" normalization strategy is somewhat ad-hoc**: For using collapse as a diagnostic during training (when final loss is unknown), the paper proposes aligning partial curves with the smallest-scale curve over 25-50% of training. This requires having already completed a small-scale reference run and assumes the alignment window is sufficient, which may not hold if the divergence occurs early.

### Minor

- **The theoretical justification (noisy quadratic model in Appendix B.3) is somewhat disconnected from the empirical results**: While the quadratic model provides intuition for how τ controls bias-variance trade-off, the paper doesn't rigorously validate that real LLM loss landscapes approximate this model. The derivation that normalized TLC depends only on τ and t̂ relies on assumptions (negligible residual bias, curvature factor cancellation) that are stated but not empirically verified.

- **The comparison with Llama-2 (Figure 1, left) is somewhat unfair**: Llama-2 models were trained with varying TPP and τ across sizes, so it's expected that curves don't collapse. The paper frames this as a limitation of prior work, but Llama-2 was not designed to achieve collapse. A more informative comparison would be to show that collapse fails when τ is deliberately mis-scaled in the Celerity setup.

- **The paper doesn't fully address when collapse might break down**: The 234 TPP band shows "divergences appear late in training for larger models" (Section 4), which the authors attribute to loss improving disproportionately on training data. This suggests collapse may not hold under distribution shift or memorization, which are common concerns in LLM training.

## Nice-to-Haves

- A more thorough ablation of the "early-align" normalization strategy, including sensitivity to the alignment window size and the choice of reference model
- Investigation of whether collapse holds for validation loss curves, not just training loss
- Analysis of how collapse behaves under different learning rate schedules (cosine, cosine with restarts) beyond linear decay-to-zero
- Discussion of whether the findings extend to other optimizers (Adam, AdamW with different β settings, Sophia)

## Novel Insights

Beyond the paper's own contributions, the key insight is that the AdamW timescale τ serves as a unifying control variable that explains why seemingly different hyperparameter choices (learning rate, weight decay, batch size) produce similar training dynamics when τ is matched. This reframes hyperparameter tuning: rather than searching over η, λ, and B independently, practitioners can target a specific τ and adjust the individual hyperparameters accordingly. The paper also reveals that collapse is not just a descriptive phenomenon but a prescriptive one—it provides a quantitative target for training quality that can be monitored in real-time, unlike final loss which is only known after completion.

## Suggestions

- Expand the evaluation of Celerity models to include standard benchmarks (MMLU, GSM8K, HumanEval, etc.) to strengthen the claim that collapse-guided training produces generally capable models.
- Provide more systematic validation of the parametric surrogate model, including error bars across multiple random seeds and hyperparameter settings, and test its extrapolation to unseen τ and TPP combinations.
- Include an ablation where τ is deliberately mis-scaled in the Celerity setup to demonstrate that collapse breaks down, strengthening the causal link between optimal τ and collapse.
- Clarify the practical limitations: under what conditions (data distribution shifts, curriculum learning, multi-epoch training) would collapse be expected to fail?

## Score and Decision

The paper makes a solid contribution by bridging theoretical insights about loss curve collapse with practical LLM training. The identification of τ as a key control variable and the demonstration that collapse serves as both a diagnostic tool and enabler of early stopping are valuable. However, the limited evaluation of the Celerity models and the under-validated parametric surrogate prevent the paper from being a definitive demonstration of the approach's utility. The core ideas are sound and the experiments at meaningful scale are commendable, but the paper would benefit from broader validation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>