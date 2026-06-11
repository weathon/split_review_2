## Summary
This paper investigates the effect of the sparsity hyperparameter L0 (average number of active latents per token) on Sparse Autoencoders (SAEs) for LLM interpretability. The authors demonstrate that L0 is not a free parameter and that setting it incorrectly leads to SAEs learning incorrect, polysemantic features rather than the true monosemantic features of the underlying LLM. 

**Core contributions:**

1. **Mechanism identification:** Using toy models with ground-truth features, the paper shows that when L0 is too low, SAEs "cheat" by mixing correlated (and anti-correlated) feature components into the same latent, achieving better reconstruction at the cost of monosemanticity. When L0 is too high, SAEs learn degenerate solutions that also mix features.

2. **Sparsity-reconstruction tradeoff critique:** The paper demonstrates that the standard sparsity-reconstruction tradeoff evaluation (variance explained vs. L0) is misleading: a ground-truth correct SAE can score *worse* on reconstruction than a cheating SAE at low L0, meaning this evaluation metric would reject perfectly correct features.

3. **Proxy metric (c_dec):** The authors propose decoder pairwise cosine similarity as a diagnostic to detect when L0 is too low. In toy models, c_dec is minimized at the correct L0. On Gemma-2-2b and Llama-3.2-1b, the L0 corresponding to the elbow in the c_dec curve coincides with peak sparse probing performance (L0 ≈ 200), suggesting the metric has practical utility.

The paper is clearly written, tackles an important and timely problem, and makes a convincing case that L0 deserves more careful attention than it currently receives. However, the LLM validation is limited to two models and relies on sparse probing as a proxy for feature quality, and the c_dec metric requires training a full L0 sweep, which is computationally expensive. The strong practical claim that "most commonly used SAEs have an L0 that is too low" is supported by suggestive evidence but warrants broader verification across more models, layers, and evaluation paradigms.

## Strengths
1. **Timely and practically important problem.** The question of how to set L0 in SAEs is directly relevant to the growing community using SAEs for LLM interpretability. Current practice treats L0 as a free parameter in sparsity-reconstruction tradeoffs, and this paper provides compelling evidence that this practice is flawed. The potential impact on the field is substantial.

2. **Clear toy model demonstration.** The controlled experiments with synthetic data provide a clean, reproducible demonstration of the core mechanism. The use of ground-truth features, ground-truth SAE baselines, and controlled correlation structures makes the causal chain (low L0 → feature mixing) highly interpretable and convincing. The initialization of the L0=1.8 SAE from the ground-truth solution (ensuring the result comes from gradient pressure, not local minima) is a particularly nice experimental design choice.

3. **Critical insight about sparsity-reconstruction tradeoffs.** The demonstration that a ground-truth correct SAE can be *outperformed* on variance explained by a cheating SAE at low L0 (Section 3.4, Figure 4) is a significant and non-obvious finding. This has direct implications for how SAE architectures should be evaluated, challenging a widespread assumption in the literature.

4. **Practical diagnostic metric.** The c_dec metric (decoder pairwise cosine similarity) is simple, intuitive, and grounded in the paper's theoretical analysis. The fact that its minimum (or elbow) correlates with peak sparse probing performance on two different LLM families provides preliminary validation that the toy model insights transfer to real models.

5. **Intellectually honest about limitations.** The paper acknowledges that c_dec can be flat across wide L0 ranges, that it requires a sweep to apply, and that the JumpReLU vs. BatchTopK differences need further investigation. This balanced tone increases confidence in the claims that are supported.

6. **Well-written and structured.** The paper is clearly organized, with a logical flow from background to toy experiments to LLM validation. The prose is concise and accessible, making the technical content easy to follow.

## Weaknesses
### W1. Limited LLM validation breadth (Major)
The paper's central practical claim is that "most commonly used SAEs have an L0 that is too low." Yet the LLM experiments cover only two models (Gemma-2-2b and Llama-3.2-1b) at selected layers, with detailed evaluation on only one layer per model. This is insufficient to support a claim about "most SAEs" in the field. The relationship between c_dec and L0 differs qualitatively between the two tested models (Gemma shows a flat region, Llama a clear minimum), suggesting that model architecture, scale, and training data all affect the optimal L0. Broader validation across more model families (e.g., Pythia, GPT-2, larger Llama variants) and multiple layers per model is needed before drawing general conclusions. Additionally, the evaluation relies entirely on the sparse probing benchmark (Kantamneni et al., 2025) as a proxy for feature quality — direct interpretability evaluations (e.g., manual inspection, automated interpretability scores) would strengthen the claims.

### W2. MSE comparison lacks proper controls (Major)
The central evidence in Section 3.3 (trained SAE MSE 2.73 vs. ground-truth SAE MSE 4.88) compares a *trained* SAE with a *fixed, untrained* ground-truth SAE. The ground-truth SAE is not optimized for reconstruction — it simply projects onto true feature directions without training. A fairer comparison would train the ground-truth-initialized SAE at the same L0 and observe whether gradient descent degrades feature alignment to improve MSE. This would directly test whether MSE optimization *causes* feature corruption, rather than merely showing that an untrained correct SAE has higher MSE than a trained incorrect one. Without this control, the causal claim that "MSE loss actively incentivizes low L0 SAEs to learn incorrect latents" is partially supported but not fully verified.

### W3. Ground-truth SAE evaluation in sparsity-reconstruction tradeoff (Major)
In Section 3.4, the ground-truth SAE's L0 is varied by changing k (BatchTopK) while keeping the encoder and decoder fixed at true feature directions. This is a valid comparison for demonstrating the existence of the problem, but it conflates two factors: (a) the true feature directions may inherently be suboptimal under tight sparsity budgets, and (b) the encoder (which determines which latents activate) is not adapted to the k constraint. An adapted encoder operating on the same true feature directions might achieve better reconstruction at low L0, narrowing the gap shown in Figure 4. The paper's conclusion that sparsity-reconstruction tradeoffs are misleading is likely correct, but the strength of this claim could be further verified by training the ground-truth-initialized SAE at each L0.

### W4. c_dec metric limitations (Moderate)
The c_dec metric relies on the assumption that correct features are orthogonal (as in the toy model). In real LLMs, features may not be perfectly orthogonal, which would increase baseline decoder cosine similarity and potentially obscure the c_dec minimum. The paper acknowledges this partially (Discussion) but does not quantify how sensitive c_dec is to violations of the orthogonality assumption. Additionally, c_dec requires training a full sweep of SAEs across L0 values, which is computationally expensive (each SAE on 500M-1B tokens). The practical utility of the metric is thus limited by compute budget. The paper mentions automatic optimization during training (Appendix A.11) but provides no details in the main text.

### W5. Insufficient statistical rigor (Moderate)
While the toy model experiments include standard deviations across 5 seeds (Figure 6), the LLM experiments show only 3 seeds per L0 (Figure 8). The sparse probing F1 differences between L0 values are small (e.g., ~0.04 F1 range in Figure 8, bottom). Without formal significance testing or confidence intervals, it is unclear whether the observed trends are statistically reliable. The paper would benefit from paired significance tests (e.g., comparing each L0 against the null of random feature assignment) and reporting effect sizes.

### W6. Speculative mechanisms without direct verification (Minor)
Several mechanistic claims in Sections 4.1-4.2 are presented as plausible hypotheses without direct evidence:
- The explanation that JumpReLU SAEs perform better at high L0 because they "stick" near the correct threshold per latent is indirect (based on L0 vs. λ_s curves, not per-latent threshold analysis).
- The suggestion that at L0=750, some latents have L0 too high while others have it too low is a plausible interpretation of histogram shapes but is not verified by individual latent analysis.
These claims are appropriately hedged ("we suspect"), but the paper would be strengthened by even simple per-latent analyses (e.g., sorting latents by firing frequency and examining their c_dec contributions).

### W7. Missing discussion of alternative approaches to L0 selection (Minor)
The Related Work section covers MDL SAEs and AFA SAEs, but the paper does not compare c_dec against existing heuristics for L0 selection. For example, the common practice of choosing L0 based on the "knee" of the reconstruction loss curve or based on downstream probing performance is mentioned only implicitly. A direct comparison showing that c_dec identifies a different (and better) L0 than these heuristics would strengthen the paper's contribution.

### W8. Overclaiming in abstract and conclusion (Minor)
The abstract states that "most commonly used SAEs have an L0 that is too low" as a finding, but this is supported only by a "cursory search of open source SAEs on Neuronpedia" (Discussion) and two LLM experiments. This should be presented as a hypothesis or preliminary observation rather than an established result. Similarly, the claim that "our work shows that L0 must be set correctly to train SAEs with correct features" is accurate within the scope of the toy model experiments, but the LLM evidence is correlational (sparse probing performance) rather than directly demonstrating that correct features are learned at the optimal L0.

## Score
**Final Score: 6/10**

This score reflects the paper's clear conceptual contribution and well-executed toy model experiments, weighed against the limited breadth of LLM validation and the practical limitations of the proposed diagnostic metric. The paper identifies a genuine and important problem in SAE training (the misleading nature of sparsity-reconstruction tradeoffs and the danger of too-low L0) and provides convincing proof-of-concept through synthetic experiments. However, the evidence base is too narrow to fully support the strong practical claims about SAEs in widespread use, and several key experiments lack proper controls. With expanded validation across more models, layers, and evaluation paradigms, and with stronger causal evidence for the claimed mechanism, the paper could make a substantially stronger contribution. The idea is worthy of further development.