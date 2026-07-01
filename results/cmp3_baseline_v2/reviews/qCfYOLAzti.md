## Summary

This paper identifies a critical failure mode in LLM unlearning—*spurious unlearning*—where gradient-ascent-based methods suppress target responses but shift probability mass into semantically related rephrasings (the *squeezing effect*), making models appear unlearned under standard metrics while still leaking knowledge. To address this, the authors propose a bootstrapping framework that jointly suppresses both the original targets and the model’s own high-confidence predictions (its “beliefs”), instantiated at the token level (BS-T) and sequence level (BS-S). Theoretical analysis within the AKG learning dynamics framework explains how bootstrapping reshapes gradient residuals to mitigate the squeezing effect. Experiments on TOFU, MUSE, and WMDP with multiple model families (Llama 3 1B/3B/8B, Llama 2 7B, Zephyr-7B) show consistent improvements over strong baselines like NPO and RMU, particularly in aggregate forget-retention trade-offs.

## Strengths

- **Important problem identification**: The paper clearly reveals that spurious unlearning is a systematic failure of existing GA/NPO-based methods, not just a corner case. The empirical evidence (probability dynamics, LLM-based evaluation) convincingly demonstrates that probability mass gets squeezed into semantically similar rephrasings, a phenomenon that standard metrics (ROUGE, perplexity) fail to capture.
- **Principled and well-motivated method**: The bootstrapping framework is a clean, intuitive idea: use the model’s own high-confidence predictions as additional forgetting targets. Both token-level (BS-T) and sequence-level (BS-S) instantiations are natural, and the method is compatible with existing unlearning losses and regularizations.
- **Theoretical grounding**: The AKG-based analysis (Thms. 5.2 and 5.3) provides a formal understanding of how BS-T reshapes the gradient residual to spread forgetting pressure over the target and its belief neighborhood, and how off-policy BS-S aggregates these residuals across multiple high-likelihood continuations. This goes beyond pure heuristics.
- **Strong experimental results**: The empirical evaluation is extensive—three benchmarks (TOFU, MUSE, WMDP), multiple model scales and families, and comparison with six strong baselines (GradDiff, NPO, RMU, SimNPO, WGA). BS-S consistently achieves the best aggregate scores, and BS-T is a strong runner-up. The paper also includes qualitative analysis via LLM-based evaluation that aligns with the theoretical claims.
- **Code release**: Code is merged to OpenUnlearning, facilitating reproducibility and community adoption.

## Weaknesses

### Fatal
None.

### Major
- **Validation of LLM-based evaluation (LaaJ)**: The paper relies on LaaJ as an auxiliary metric to detect spurious unlearning, especially for the naturalness and similarity dimensions. While the authors cite prior work (Zheng et al., 2023) for alignment with human judgment, the specific prompts and rating scales (described only in Appendix F.2) are not validated against human annotations in this paper. Given that LaaJ is used to draw key conclusions (e.g., Fig. 4c), a small-scale human validation study or cross-check with multiple LLM judges would substantially strengthen the claims.

### Minor
- **Hyperparameter sensitivity**: The method introduces three key hyperparameters without in-depth analysis in the main text: λ_BST, λ_BSS, and the top-k size. The ablation study is relegated to Appendix F.5, and even there the sensitivity to k and λ is not exhaustively explored. A reader may question how robust the performance is to these choices across different benchmarks and models.
- **Theoretical assumptions**: The AKG analysis relies on the lazy eNTK (neural tangent kernel) approximation and teacher forcing, which are strong simplifications for LLM fine-tuning dynamics. The paper acknowledges this but does not discuss how violations (e.g., feature learning, non-linear dynamics) might affect the conclusions. The theory is thus more suggestive than definitive, which is acceptable but should be caveated more clearly.
- **Computational overhead not highlighted**: BS-S requires sampling N additional sequences per forget example, which adds non-negligible cost. The training time comparison in Appendix F.6 is helpful, but the main paper would benefit from a brief discussion of the trade-off between performance gain and computational budget.
- **Presentation density**: The paper is packed with content, but some transitions (e.g., from the empirical observation in §3.2 to the method in §4.1) could be smoother. The theoretical section (§5) is quite compressed; a more accessible exposition would help readers not familiar with the AKG framework.

### Trivial
None.

## Nice-to-Haves

- Human evaluation to validate the LaaJ metric on a subset of TOFU responses.
- Additional experiments on more diverse unlearning scenarios (e.g., copyrighted content, safety harms beyond WMDP) to test generality.
- A discussion of potential failure cases of the bootstrapping approach itself—e.g., when model beliefs are themselves unreliable or when the squeezing effect is not the dominant failure mode.

## Novel Insights

Beyond the paper’s own contributions, the work offers a subtle insight: that successful unlearning should target the model’s *internal belief regions* rather than just the training labels. This reframes the unlearning problem from “erase a specific (x,y) pair” to “erase the knowledge encoded in the high-probability manifold of the model’s own distribution.” The bootstrapping mechanism is a practical instantiation of this reframing, and the theoretical residual analysis shows how the gradient update can be explicitly steered away from that manifold. This perspective may inspire future work that uses model-internal signals (e.g., hidden representations, attention patterns) for more targeted forgetting.

## Suggestions

- Add a small human evaluation (e.g., 50 samples) to validate the LaaJ naturalness and similarity scores used in Fig. 4c, and report agreement rates.
- Include a sensitivity plot for λ_BST, λ_BSS, and top-k in the main paper, or at least a summary sentence stating the range of values over which BS-T/BS-S remain competitive.
- Modify the presentation of the theoretical section to first state the intuition in plain language, then provide the formal derivation, to improve accessibility.
- For reproducibility, specify the exact LLM judge prompts and rating criteria in the main paper or cite the appendix more prominently.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>