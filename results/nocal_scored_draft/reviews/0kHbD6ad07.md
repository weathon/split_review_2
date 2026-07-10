Now I have the favorability-calibrated assessment. Let me write the final consolidated review.

## Summary

This paper proves that decoder-only Transformers are almost surely injective — distinct prompts map to distinct last-token hidden states — using a real-analyticity argument (Theorems 2.1–2.3). The proof strategy is elegant: each Transformer component is real-analytic, the difference function for two prompts is therefore real-analytic, and a fundamental dichotomy forces its zero set to be measure-zero unless it is identically zero (which a constructive witness rules out). Injectivity is further argued to persist under GD-family training. The paper introduces SIFT/SIPIT, a sequential algorithm that exploits this injectivity to reconstruct the exact input from per-position hidden states, with a worst-case O(T|V|) guarantee and practical efficiency via a gradient-based candidate heuristic. Experiments include a large-scale collision search (100k prompts, ~5B comparisons) and small-scale inversion tests.

## Strengths

- **Genuinely surprising theoretical result.** The paper proves that decoder-only Transformers are almost surely injective — distinct prompts map to distinct last-token hidden states — which is counterintuitive given that individual components (LayerNorm, softmax, residual connections) appear many-to-one in isolation. The result revises a widely held intuition.
- **Elegant proof strategy.** The approach is well-conceived: (1) establish real-analyticity of all Transformer components, (2) use the dichotomy of real-analytic functions (either identically zero or measure-zero zero set), (3) construct a witness parameter setting that separates any two distinct prompts (Theorem 2.2's proof). The construction — freezing the network to embedding-plus-position for prompts differing at the last position, and having a single attention head attend to the first differing position otherwise — is clean and non-trivial.
- **Clean logical chain from theory to algorithm.** The paper connects the injectivity guarantee to a concrete algorithmic consequence: because representations uniquely identify the input, exact recovery reduces to sequential search. The SIFT/SIPIT algorithm is a natural operationalization of this insight, and the robustness bound (Theorem 3.2) is a nice addition.

## Weaknesses

### Fatal
None.

### Major

- **Training-preservation theorem covers only GD-family optimizers, while all evaluated models were trained with adaptive optimizers.** Theorem 2.3 and Corollary 2.3.1 are proved only for gradient descent (GD), SGD, and mini-batch GD with step sizes in (0,1). Adaptive optimizers such as Adam, AdamW, and Adafactor — which were used to train every model tested in Section 4 — are not addressed. The paper offers no argument that the absolute-continuity preservation proof carries over to optimizers with per-parameter adaptive learning rates. While the theorem statement is precise, the abstract and broader narrative ("preserved during training") imply a more general scope that is not yet supported. This does not invalidate the initialization result (Theorem 2.2), which is independent, but it does mean the training-preservation claim is narrower than the paper's framing suggests.

- **Inversion experiments are conducted on a very small sample.** The paper reports results on 100 prompts (20 tokens each) for GPT-2 Small and 50 prompts (10 tokens each) for quantized models. The standard deviation for SiPT in Table 5 (28.01 ± 35.87 s) exceeds the mean, indicating extreme variability that is not analyzed. No per-prompt success rates, per-token difficulty analysis, or systematic study of when the gradient heuristic performs well versus poorly are provided. For a paper claiming 100% exact recovery with practical efficiency, this sample is insufficient to establish robustness.

### Minor

- **The collision-search experiments (Section 4.1) are better described as illustrations than validations.** The theoretical claim is that collisions occur on a measure-zero set of *parameters*; showing that a finite sample of prompts yields no collisions in a fixed set of pre-trained models is consistent with the theory but does not provide additional confirmation. This experimental design is not misleading, but its evidential value is limited.

- **The HARDPROMPTS comparison in Table 5 is not informative.** HARDPROMPTS is designed for soft-prompt optimization for downstream task performance, not for exact input inversion from hidden states. Its 0% accuracy on this task is expected and provides no useful signal. The only meaningful comparison in the table is between SiPT and its BRUTEFORCE ablation.

- **The gradient-based candidate policy is underspecified in the main text.** Algorithm 1 calls `POLICY` with references to Algorithms 2 and 3 (in the appendix), but the main text provides no description of how the gradient heuristic works — what gradient is computed, with respect to what, or how it ranks candidates. Since the algorithm's practical efficiency (0.19–0.22% vocabulary explored) depends entirely on this heuristic, the reader cannot assess its soundness from the main paper alone.

- **No discussion of floating-point arithmetic.** The theoretical result concerns exact equality in ℝ^d, but rounding in standard floating-point formats (FP16, BF16, FP32) could cause analytically distinct representations to collide numerically. The quantization experiments partially address this for extreme low-precision settings, but standard floating-point inference is the more common scenario.

- **The legal/policy discussion overreaches.** Section 6 claims that "any system that stores, caches, or transmits hidden states is effectively handling the user's verbatim text," but this conflates the last-token state (whose injectivity is proved) with per-position intermediate states (which the inversion algorithm requires full access to). Production systems typically cache KV states, not full hidden-state matrices, and the paper has no result about invertibility from KV caches alone.

- **Lack of discussion of causal masking and real-analyticity.** The paper asserts that causal attention is real-analytic (Theorem 2.1) without discussing the subtlety of causal masking with -∞ values. In practice implementations use large finite negative values, so the function is real-analytic, but the theoretical treatment would benefit from explicit acknowledgment.

### Trivial

- **Inconsistent algorithm naming.** The algorithm is called SIFT (abstract), SIPIT (Sections 1 and 3), SIpIT (Algorithm 1), and SiPT (Tables 4–5, Section 4). This does not affect technical content but undermines readability.

## Nice-to-Haves

- Extend the training-preservation proof to cover adaptive optimizers (Adam/AdamW), or clearly bound the claim to GD and add a discussion of why the result is expected to hold more broadly.
- Replace or remove the HARDPROMPTS comparison; include a more informative baseline (e.g., random search without injectivity guarantees, or the method of Thomas et al. 2025).
- Add a prose description of the gradient heuristic in the main text (ideally with a summary of the loss, differentiation target, and ranking mechanism).
- Discuss floating-point arithmetic and its implications for practical injectivity.
- Expand the inversion experiments with per-prompt statistics and failure-case analysis.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"SIFT does not use the property the paper proves"**: REMOVED. The paper correctly argues (Section 3, line 143) that last-token injectivity implies full hidden-matrix injectivity, since the last-token state is a deterministic function of the hidden matrix at any layer. The algorithm is a valid operationalization of this property. The critic's characterization that the algorithm exploits a "different (and weaker) property" is inaccurate.
- **"Jacobian-determinant gap in Theorem 2.3 proof"**: REMOVED. The critic claimed the set where det Dφ = 0 "could still be large." This is incorrect for real-analytic functions: if det Dφ is real-analytic and not identically zero, its zero set has Lebesgue measure zero (by the same dichotomy used in Theorem 2.2). The proof sketch is sound on this point.
- **"Linear-time guarantee is misleading"**: REMOVED. O(T|V|) is standard worst-case analysis linear in each variable; the critic's characterization as "linear in the *product*" is a nitpick that does not identify a substantive flaw.

## Novel Insights

The reviews surface a key gap: the training-preservation proof is limited to GD-family optimizers while the paper's broader narrative ("preserved during training") and all its experiments involve models trained with adaptive optimizers. This is a genuine scope limitation that the authors should address. The thinness of the inversion experiments (100–150 total prompts) and the resulting high variance (σ > μ in Table 5) are also surfaced, indicating that the empirical demonstration lags behind the theoretical claim.

## Suggestions

1. Clearly qualify the "preserved during training" claim to specify GD-family optimizers, or extend the proof to cover adaptive optimizers.
2. Substantially expand the inversion experiments (1000+ prompts, per-prompt statistics, failure-case analysis).
3. Remove the HARDPROMPTS comparison or explicitly state it is a different-task reference point.
4. Add a prose explanation of the gradient heuristic in the main text.
5. Discuss floating-point arithmetic's effect on the injectivity guarantee in practice.
6. Use a single consistent name for the algorithm throughout.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>