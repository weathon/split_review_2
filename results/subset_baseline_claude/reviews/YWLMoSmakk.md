## Summary

This paper addresses the problem of redundant transformations in middle-to-deep layers of Pre-Norm Transformer-based language models. The authors propose a Coherence-based Redundancy (CR) measure using characteristic functions and Fourier transforms to quantify the degree of redundancy between a layer's input and output feature distributions. Guided by CR analysis, they propose two complementary techniques: (1) a tree-structured residual path to improve cross-layer information flow from shallow to deep layers, and (2) a coherence-based redundancy regularization loss (plus a channel orthogonality loss) to explicitly penalize redundant transformations during training. Experiments on a 130M-parameter LLaMA3 model show evaluation perplexity improvements, with the 12-layer model surpassing a 14-layer baseline.

## Strengths

- **Theoretically motivated metric**: The use of characteristic functions and Fourier transforms to measure distributional differences between layer inputs and outputs is more principled than simple cosine similarity; it exploits complex-valued structure (magnitude and phase) and can in principle capture higher-order statistics beyond directional alignment.
- **Coherent analysis motivating design**: The paper systematically links the observed high cosine similarity in middle-to-deep layers to gradient analysis of Pre-Norm, providing a clear chain of reasoning from phenomenon to root cause to remedy.
- **Practical accessibility of the regularization**: The CR loss and orthogonality loss are add-ons to standard training that require no architectural redesign beyond residual path rewiring; the ablation studies (Figure 3) justify the hyperparameter choices (target, scaling, sharpening) in a structured way.

## Weaknesses

### Fatal
None.

### Major

1. **Experimentally under-validated at scale**: The entirety of quantitative validation rests on a single 130M-parameter model trained on 11B tokens. The main headline result — a 0.1 perplexity advantage over the 14-layer baseline (13.18 vs. 13.28) — is marginal in magnitude and measured only on next-token perplexity. There is no evidence this would hold at 1B, 7B, or larger scales, and prior work on representation collapse (which motivated this paper) is documented in models an order of magnitude larger.

2. **No downstream task evaluation**: Perplexity is the sole reported metric. A 0.1-point perplexity improvement does not establish practical utility. Without evaluation on standard benchmarks (HellaSwag, MMLU, ARC, etc.), the claim that redundancy reduction translates to improved model capability remains unsubstantiated.

3. **The CR measure's supposed advantage over cosine similarity is contradicted by the paper itself**: Section 3.1 states the paper employs CR because cosine similarity "struggles to capture higher-order statistical differences inherent in nonlinear transformations." Yet Section 3.1 also states: "the input–output coherence and the cosine similarity exhibit the same trend from 1 to 10 attention sub-layers. This proves the effectiveness of coherence." The paper uses the two metrics trending identically as proof CR is valid, but this simultaneously undermines the claim that CR provides information beyond cosine similarity. No experiment demonstrates that CR-guided design choices differ from what cosine-similarity guidance would produce.

4. **Architecture-specific hardcoding throughout**: The tree-structured residual path assumes exactly 12 transformer layers (binary tree of height 3, `N = 2^h - 1 = 7` nodes). The CR loss scaling factor `sqrt(12-L)` and `(12-L)*0.1` are hardcoded to a 12-layer model. Specific layer indices (2,4,6,8 for CR loss; 3,5,7,9,10 for orthogonality loss) are hand-selected from a single model run. It is entirely unclear how this methodology extends to models of different depths, and no generalization principle is given.

### Minor

- The paper claims the tree-structured residual path is "simpler and more easily implementable" than Hyper-connections, but provides no direct empirical comparison between them; the baseline is the default serial residual, leaving the claim about relative merit unverified.
- The ablation in Figure 3 compares hyperparameter variants (target = 0.3 vs 0.35 vs 0.4) but not the core component contributions individually (CR loss alone, orthogonality loss alone, tree path alone) vs. the combined system, making it hard to assess each component's independent value.
- The "target" coherence of 0.35 is chosen empirically with no principled justification for why the mid-range should be exactly this value rather than, e.g., 0.5.

### Trivial
None.

## Nice-to-Haves

- An experiment showing how the tree path topology (e.g., layer selection) should be adapted for 24-layer or 32-layer models, along with a general design principle.
- A head-to-head comparison with Hyper-connections under identical training budgets and model sizes.
- A direct experiment comparing a CR-guided model vs. a cosine-similarity-guided model to determine if the more complex CR actually changes design decisions.

## Novel Insights

The notion of measuring layer-wise transformation quality via frequency-domain coherence of empirical characteristic functions — treating the sequence dimension as a discrete probability distribution — is a genuinely novel framing. It opens the door to using classical signal-processing diagnostics (power spectra, cross-coherence) to analyze neural network layer behavior. However, the paper does not exploit this richness beyond a scalar summary statistic, and fails to demonstrate that this richer representation leads to meaningfully different or better guidance than cosine similarity.

## Suggestions

- Extend validation to at least one 1B-scale model with standard downstream benchmarks; a marginal perplexity difference at 130M scale is insufficient to substantiate the claims.
- Disentangle the contributions of the tree-structured path and the regularization losses with a clean ablation table (not just hyperparameter sweeps within CR loss).
- Provide a principled, depth-agnostic formulation of the tree path and scaling factors (e.g., express constants as functions of model depth fraction `L/L_max` rather than absolute layer indices).
- Directly compare CR and cosine similarity as diagnostic tools: show at least one case where CR reveals a redundancy that cosine similarity misses, to justify the additional complexity.

## Score and Decision

The paper addresses a real and well-observed problem in transformer training. The CR measure is an intellectually interesting tool, and the tree-structured residual path is a practical idea. However, the validation is limited to one tiny model and one metric, the flagship CR measure is not convincingly shown to exceed simpler alternatives, and the methodology is heavily hardcoded to the specific 12-layer experimental setup. Taken together, these constitute major unresolved concerns that prevent confident acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>