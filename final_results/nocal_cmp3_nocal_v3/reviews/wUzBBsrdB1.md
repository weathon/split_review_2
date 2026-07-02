## Summary

This paper studies the effect of $L_0$ (average number of active latents per token) on Sparse Autoencoder (SAE) quality. Using a toy model with known ground-truth features, the authors show that too-low $L_0$ causes SAEs to "hedge" by mixing correlated features into individual latents, producing better MSE than the correct SAE despite having corrupted latents. This demonstrates that sparsity-reconstruction Pareto fronts are an unreliable evaluation criterion. The authors propose $c_{\text{dec}}$ (pairwise decoder cosine similarity) as a diagnostic metric and validate it on Gemma-2-2b and Llama-3.2-1b, showing that the $c_{\text{dec}}$ elbow region coincides with peak sparse probing performance.

## Strengths

1. **Clean toy model with ground truth — the core demonstration is convincing.**  
   Sections 3.1–3.3 construct a toy model where features are known and a ground-truth SAE can be built. The paper concretely shows that a trained SAE at $L_0=5$ achieves *better* MSE (2.73) than the ground-truth SAE (4.88) despite learning corrupted, polysemantic latents (Section 3.3). This clearly demonstrates that MSE minimization actively incentivizes feature hedging when $L_0$ is too low.

2. **The sparsity-reconstruction tradeoff critique is important and well-targeted.**  
   The paper identifies a genuine blind spot: the widespread practice of using sparsity-reconstruction Pareto fronts to compare SAE architectures implicitly assumes that better reconstruction at fixed sparsity means a better SAE. Section 3.4 shows this fails even in a simple toy model, where the ground-truth SAE scores *worse* than a cheating low-$L_0$ SAE. This is a real methodological contribution that is supported by the evidence.

3. **The $c_{\text{dec}}$ metric is simple, interpretable, and grounded in the observed failure mode.**  
   The intuition (Section 3.5) is clear: if latents mix components of correlated features, they become less orthogonal to each other. In toy models $c_{\text{dec}}$ has a clean minimum at the true $L_0$ (Figure 6). The metric is straightforward to compute and provides a useful diagnostic signal even if, as the authors acknowledge, it is not a perfect guide.

## Weaknesses

### Fatal
None.

### Major
- **LLM validation is limited in scope and lacks basic statistical rigor.**  
  The key LLM result is that the $c_{\text{dec}}$ elbow region coincides with peak sparse probing F1. However: (1) Only two models (Gemma-2-2b, Llama-3.2-1b), two layers from one model (layers 5 and 12) and one from the other (layer 7), and two SAE architectures are tested. (2) The probing F1 variation is small ($\sim0.78$ to $\sim0.82$, a $\sim0.04$ range across $L_0$ values), yet *no error bars or confidence intervals are shown for the probing results* — the paper reports "3 seeds per $L_0$" (Figure 8 caption) but does not visualize the variance, unlike the toy model experiments which show standard deviations (Figure 6). Without this, it is unclear whether the probing peak is statistically distinguishable from the surrounding region. (3) The relationship between $c_{\text{dec}}$ and probing F1 is correlational; the paper does not establish why $c_{\text{dec}}$ should track probing performance beyond both being consequences of feature mixing. The claims about LLM SAEs would benefit from broader and more rigorous empirical support.

### Minor
- **The $c_{\text{dec}}$ metric does not independently identify the correct $L_0$ in real LLM settings; it requires a sweep and external validation.**  
  In the toy model, $c_{\text{dec}}$ has a sharp global minimum at the true $L_0$. But in the LLM experiments, the pattern is less clean: for Gemma-2-2b layer 5 (Figure 8), the metric has "a long shallow region with the global minimum actually appearing in that shallow region," and the authors resort to using the "elbow" before the low-$L_0$ jump. For Gemma-2-2b layer 12 (Figure 9), BatchTopK and JumpReLU SAEs have minima at different $L_0$ values ($\sim200$ vs $\sim250-300$). The paper acknowledges these limitations (Section 6), but the gap between the framing ("a proxy metric that can help guide the search") and the operational burden — training many SAEs and cross-validating with a separate benchmark — is worth noting.

- **The claim that "most commonly used SAEs have an $L_0$ that is too low" is asserted without sufficient substantiation.**  
  The abstract (line 37) and discussion (line 240) present this as a key finding. The only support offered is "a cursory search of open source SAEs on Neuronpedia" deferred to Appendix A.13. Even with solid appendix evidence that $L_0<100$ is common, the claim would require establishing the *correct* $L_0$ for each of those SAEs, which the paper does not do. This specific claim is more speculative than the rest of the paper's contributions.

- **The toy model assumes exact feature orthogonality while real features are only "nearly orthogonal," and this gap is not discussed.**  
  The paper correctly states that the Linear Representation Hypothesis posits *nearly* orthogonal features (lines 13, 59), but the toy model uses exactly orthogonal feature directions (line 65). The core mechanism (hedging via firing correlations) likely persists under approximate orthogonality, but the paper does not discuss how much non-orthogonality the phenomenon tolerates or whether it could change the optimization landscape. Adding a sweep over a noise parameter on feature directions would strengthen confidence in the transfer to real LLMs.

- **Contribution relative to the closest related work (Chanin et al., 2025) is incremental, though the paper correctly acknowledges this.**  
  The paper positions itself as "a version of feature hedging due to low $L_0$" (Section 5), while Chanin et al. focused on narrow SAE width. The additional contributions — the low-$L_0$ mechanism, the sparsity-reconstruction critique, and the $c_{\text{dec}}$ metric — are real but incremental. This does not diminish the paper's value, but the framing ("Sparse But Wrong") implies a more sweeping finding than the incremental advance relative to the cited prior work.

### Trivial
None.

## Nice-to-Haves
- **Test robustness to approximate feature orthogonality in the toy model.** Adding a simple sweep over a noise parameter controlling feature direction cosine similarity would directly test whether the hedging phenomenon transfers to settings closer to real LLMs.
- **Make the $c_{\text{dec}}$ metric operational with a specific decision rule.** Currently $c_{\text{dec}}$ identifies a qualitative elbow region; the paper would be strengthened by proposing and validating a concrete rule (e.g., "pick the $L_0$ at the knee of the $c_{\text{dec}}$ curve").
- **Report error bars for LLM probing results.** The probing F1 differences are small ($\sim0.04$); visualizing the variance across the 3 seeds per $L_0$ would clarify whether the observed peaks are meaningful.
- **Test whether $c_{\text{dec}}$ is sensitive to SAE width ($h$).** The toy model uses $h=g$; real SAEs use vastly overcomplete dictionaries (e.g., $h=32768$ for $d\sim2048$), which could change hedging dynamics.

## Removed Points
These points are flagged to be removed; treat them with caution.
- *"JumpReLU automatically finding the right L0 undermines the paper's message"* — REMOVED: The paper reports this as a positive feature of JumpReLU training ("a testament to Anthropic's JumpReLU SAE training method," line 187). This does not undermine the core message (that $L_0$ matters) — it simply shows one architecture handles it better.
- *"The paper does not test random initialization"* — REMOVED: The paper explicitly initializes the $L_0=1.8$ SAE to the ground-truth solution "ensuring that the result of training is due to gradient pressure rather than just being a local minimum" (line 77). Testing random initialization would be a nice additional experiment but is not a weakness of the current design, which deliberately isolates the gradient effect.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add error bars or confidence intervals to the LLM probing F1 plots (Figures 8 and 9).
2. Expand the LLM validation to cover more layers, at least one larger model, and report whether the $c_{\text{dec}}$ elbow consistently predicts the probing peak.
3. Tone down or more carefully qualify the claim that "most commonly used SAEs have too low an $L_0$" — the paper's actual evidence supports the claim that $L_0$ must be set correctly, but the claim about the state of practice is not directly tested.
4. Add a brief discussion of how relaxing the exact orthogonality assumption in the toy model might affect the findings, and ideally add a robustness experiment with nearly-orthogonal features.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>