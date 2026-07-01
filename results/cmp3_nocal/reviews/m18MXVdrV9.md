Now I have all the information needed to write the final consolidated review.

## Summary

This paper introduces INFO-SEDD, a method for estimating mutual information (MI) and entropy on high-dimensional discrete data using Continuous Time Markov Chains (CTMCs) and discrete diffusion models. The key idea is to express KL divergences via Dynkin's formula, substituting intractable probability ratios with learned score functions from discrete diffusion models. The method supports two variants (Joint and Conditional) and leverages absorbing-state diffusion to compute marginal scores from a single joint model. Experiments on synthetic benchmarks, text summarization, and genomics demonstrate that INFO-SEDD outperforms "embedding trick" baselines.

## Strengths

- **Novel and principled methodology.** The connection between CTMCs, Dynkin's formula, and KL divergence (Equations 2–5) is a genuine contribution that bridges two previously separate literatures. The absorbing-state trick (Equation 6) enabling marginal scores from a single joint model is elegant and makes the method practical.

- **Strong theoretical foundation.** The derivation from time-reversal properties of CTMCs to a tractable KL estimator is mathematically sound. The error bound (Equation 7) provides a concrete characterization of the bias-variance tradeoff, establishing consistency up to an exponentially decaying truncation bias.

- **Impressive synthetic results.** In Table 1, INFO-SEDD achieves near-perfect estimates across all five MI/dimensionality settings (9.92±0.12 for true MI=10, up to 47.77±1.18 for MI=50), while all eight competitors degrade substantially — many producing estimates off by a factor of 2–8×. Standard deviations are also much lower.

- **Real-world applicability across two domains.** The SUMMEVAL model selection experiment (Table 2) and the TATA-box motif discovery (Figure 5) demonstrate concrete uses for MI estimates in NLP and genomics. The TATA-box result — where the MI peak aligns with the known biological target region around position −35 — is a compelling qualitative demonstration.

## Weaknesses

### Fatal
None.

### Major

- **Pretraining asymmetry in text summarization experiments.** INFO-SEDD uses a pretrained MDLM-SMALL model (Sahoo et al., 2024) as its backbone (line 130), which already encodes rich distributional information about language. Competitors, by contrast, must "project text tokens into an embedding space of fixed dimension, by jointly learning an embedding look-up table" (line 134) — i.e., learning from scratch. This gives INFO-SEDD a significant head start that is independent of the method's core contribution. The stated goal of using "the same backbone" is admirable, but the execution is asymmetric: INFO-SEDD inherits pretrained weights while competitors receive randomly initialized embeddings. A fairer comparison would give competitors access to the same pretrained representations, or train INFO-SEDD from scratch in at least one setting. (Note: this concern primarily applies to the text domain; the genomics experiments use a pretrained CADUCEUS model for "all methods" (line 182), which is fairer.)

### Minor

- **Real-world evaluation relies on consistency, not ground-truth accuracy.** The paper explicitly calls these "consistency tests" (lines 128, 130, 182) and acknowledges that "we cannot establish an exact ground truth for these experiments" (line 130). The text experiment uses entropy-rate-derived reference values (256–303 nats) that span a 20% range. The genomics experiment's reference is itself an estimate from a classifier's accuracy via binary entropy. The paper is transparent about this, but there is tension with broader claims (abstract, conclusion) that INFO-SEDD is "accurate." The real-world evidence shows that INFO-SEDD behaves *sensibly* — which is meaningful — but does not demonstrate that it estimates the *correct numerical value* of MI in real settings. A clearer distinction between consistency and accuracy would strengthen the paper.

- **No computational cost analysis despite "lightweight" claim.** The paper claims INFO-SEDD is "lightweight and scalable" (line 9) but provides no runtime, parameter count, FLOPs, or GPU-hour comparisons against competitors. The method requires training a discrete diffusion model via the DWDSE loss (involving sampling time steps and computing score estimates) and evaluating an integral over time with sums over O(D·|χ|) terms. Competing variational methods (MINE, NWJ, SMILE) typically use a single forward pass per sample. Without efficiency data, the "lightweight" claim is unsubstantiated.

- **Error bound scaling with D·|χ| is not discussed in context of high-dimensional claims.** The bound in Equation (7) contains a factor of D·|χ|·(ε_p + ε_q), meaning the estimation error grows linearly with both dimensionality and support size for fixed score approximation error. The paper presents this bound as a positive consistency result but does not discuss what it implies for high-D, high-|χ| regimes where INFO-SEDD claims superiority. If score errors ε_p, ε_q are themselves large in high dimensions, the bound may be vacuous. A discussion of the bound's tightness would be valuable.

### Trivial
None.

## Nice-to-Haves

- An analysis of the relationship between DWDSE training loss and MI estimation accuracy — i.e., does minimizing the generative modeling loss minimize MI estimation error?
- A study of sensitivity to the finite time horizon T.
- A quantitative comparison against another MI estimator on the TATA-box motif-finding task (e.g., comparing MI profiles or using AUC for motif detection).
- A discussion of failure modes: e.g., when a good pretrained discrete diffusion model is unavailable, or when support size |χ| is very large.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Critical Issue 1 (synthetic benchmark circularity)** — The critic argued that the synthetic data generation is not described in the main text and is only in Appendix C.1 (stripped by the parser). Per Hard Rules, weaknesses about missing appendix content (which exists in the original submission) are removed. The paper explicitly states "full details are in Appendix C.1" (line 102). The synthetic data generation exists in the original submission and cannot be judged absent from this parsed extract.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the pretraining asymmetry as the most significant unresolved issue. The reviewer's observation that INFO-SEDD uses pretrained models while competitors learn from scratch is the key insight that the authors should address. The remaining criticisms (consistency vs. accuracy framing, missing runtime analysis, error bound scaling) are secondary and do not change the core assessment.

## Suggestions

- **Address the pretraining asymmetry in the text experiments directly.** Either: (a) fine-tune the pretrained MDLM-SMALL model and use its internal representations (e.g., the encoder hidden states) as input features for the competing estimators, so all methods benefit from the same pretrained knowledge; or (b) train INFO-SEDD from scratch (without pretrained weights) in at least one setting to demonstrate that the method's advantage does not depend on pretraining. Even a single ablation showing this would substantially strengthen the paper.

- **Acknowledge the consistency-vs.-accuracy distinction explicitly.** The real-world experiments use carefully constructed consistency tests, which is reasonable. But the conclusion should clearly state that these experiments show *plausible behavior* consistent with MI estimates, not that INFO-SEDD recovers the true unknown MI in real settings.

- **Provide basic computational cost information.** Report wall-clock time per MI estimate (or training time), number of parameters, and GPU hours for at least one representative experiment (e.g., the D=50 synthetic benchmark).

## Score and Decision

The paper presents a genuinely novel and theoretically well-motivated method for an important problem. The synthetic results are strong, and the real-world applications demonstrate useful behavior. The primary concern is the pretraining asymmetry in the text experiments, which weakens the empirical comparison. This is addressable and does not invalidate the core contribution. With the synthetic data generation described in the appendix (present in the original submission) and the pretraining asymmetry acknowledged or repaired, this is a solid contribution to the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>