## Summary
# Final Review Report

## Summary

This paper proposes EPAR (Explicit Position-Attention Relationship), a parametric framework for modeling position information in Transformer attention. Instead of encoding positions at the vector representation level (as in RoPE, absolute/relative position embeddings), EPAR directly modulates attention scores via an explicit exponential function $P_{\text{effect}}(i,j,L) = \alpha \cdot e^{-\beta |i-j|/L}$ with three parameters: position influence intensity $\alpha$, spatial decay rate $\beta$, and long-range enhancement coefficient $\gamma$. The authors prove basic analytic properties (continuity, differentiability, monotonicity), introduce an enhanced formulation with a $\gamma$-controlled baseline to mitigate attention decay at long distances, and develop a triple-attention architecture with task-aware and content-aware modules. Experiments on five NLP benchmarks (WikiText-103, WMT'14 En-De, SQuAD 2.0, GLUE, ArXiv) with a standard 110M-parameter Transformer show 1.8%-8.9% improvements over strong baselines including RoPE and ALiBi. The visible main text presents the core equations and empirical results, but the complete mathematical analysis (Theorems 2-5, information-theoretic derivations, detailed ablation studies) is in the removed appendix and cannot be verified in this review. The paper makes an interesting conceptual contribution by reframing position encoding as an explicit parametric function at the score level, but this contribution is weakened by inflated claims about mathematical novelty (basic calculus properties presented as theoretical guarantees), incomplete reproducibility details, and a factual error in the central framing dichotomy (ALiBi already operates at the attention score level).

## Strengths
1. **Clear conceptual reframing.** The core idea of modeling the position-attention relationship as an explicit parametric function at the attention score level is conceptually clean and distinct from the dominant approach of encoding positions at the representation level. This reframing opens up analytical possibilities (closed-form optimal position derivation, explicit parameter control) that are not straightforward with implicit methods.

2. **Interpretable parameter design.** The three-parameter family ($\alpha$, $\beta$, $\gamma$) provides intuitive, interpretable control over positional effects: $\alpha$ controls overall intensity, $\beta$ controls how quickly attention decays with distance, and $\gamma$ controls the long-range baseline. This is a practical improvement over black-box learned embeddings whose parameters have no clear semantic interpretation.

3. **Comprehensive benchmark coverage.** The experiments span five diverse task types (language modeling, machine translation, question answering, classification, long-document understanding) with multiple strong baselines (RoPE, ALiBi, Relative PE, Transformer-XL). This breadth strengthens the claim of general applicability.

4. **Statistical rigor.** The reporting of 5-run means with standard deviations, 95% confidence intervals, Cohen's d effect sizes, and Bonferroni-corrected p-values is a methodological strength that many position encoding papers lack. The effect sizes (medium to large: d=0.45-1.85) suggest the improvements are practically meaningful rather than incidental.

5. **Acknowledgment of limitations.** The paper includes a dedicated Limitations section (9.1) and a Failure Cases section (9.2), which demonstrate awareness of boundary conditions. The discussion of diminishing returns beyond 2048 tokens and sensitivity to extreme parameter values is honest and helpful for practitioners.

## Weaknesses
### W1. Core framing contradiction and factual inaccuracy (Major)
The paper's central motivation rests on a dichotomy: existing methods operate at the "vector representation level" while the proposed method operates at the "attention score level." However, ALiBi (Press et al., 2021) explicitly operates at the attention score level by adding a linear bias directly to pre-softmax scores. The paper's own Table 2 confirms this. This factual inconsistency between the text (Section 1: "Core Problem") and the table undermines the claimed "fundamental shift." The paper would be more credible by acknowledging that ALiBi already works at the score level and positioning EPAR as a generalization (parametric exponential vs. fixed linear bias) rather than a paradigm shift. 

**Fix:** Correct the Introduction to say "Most existing methods (RoPE, relative position encoding) operate at the vector representation level, while ALiBi operates at the score level but uses a fixed linear bias without parametric flexibility. EPAR generalizes this with a learnable exponential parametric function."

### W2. Overclaiming standard calculus as theoretical novelty (Major)
The paper repeatedly claims that proving continuity, differentiability, and monotonicity of $P_{\text{effect}}(i,j,L) = \alpha e^{-\beta |i-j|/L}$ constitutes "theoretical guarantees that are not possible with implicit encodings" (Section 4.2). These are basic properties of the exponential function — a standard calculus fact. Moreover, RoPE also uses continuous and differentiable functions (rotations), and learned embeddings produce continuous representations. Presenting these as a distinguishing theoretical contribution will face strong reviewer pushback.

**Fix:** Acknowledge that these properties are elementary and shared with most parametric methods. Reposition the theoretical novelty as the closed-form optimal parameter derivation (Theorem 2) and convergence analysis (Theorems 3-5), which are genuinely enabled by the explicit parametric form.

### W3. Unanalyzed consequences of multiplicative score modulation (Major)
Equation (2) places $P_{\text{effect}}$ as a multiplicative factor inside softmax. The paper does not analyze two critical consequences:
(a) When $P_{\text{effect}}$ is very small (distant positions), all scaled scores approach zero, causing softmax to output a near-uniform distribution — the opposite of selective attention suppression.
(b) Because softmax renormalizes globally, independent control over individual position pairs is impossible in principle; changing $\alpha$ for one pair affects attention weights for all pairs through the denominator.

**Fix:** Add an analysis paragraph discussing the multiplicative vs. additive modulation trade-off and acknowledge that the "fine-grained control" is relative (not independent) due to softmax normalization.

### W4. Mathematically incorrect claim about the $\gamma$ enhancement (Major)
Section 7.1 claims that the enhanced function ensures "a non-zero lower bound $\frac{\alpha}{1+\gamma}$ for attention weights." This is incorrect because $P_{\text{effect}}$ is a multiplicative factor on pre-softmax scores, not the attention weight itself. After softmax normalization, individual attention weights $A_{ij}$ can still be arbitrarily close to zero. The enhancement guarantees a minimum score factor, not a minimum attention weight.

**Fix:** Correct to: "ensures a minimum multiplicative factor of $\frac{\alpha}{1+\gamma}$ on pre-softmax scores, preventing complete score vanishing and improving gradient flow at long distances."

### W5. Unverifiable results from removed appendix (Major)
Multiple key results are only in the removed appendix: (a) Theorems 2-5, (b) Mutual information estimates ($I(P;A)=0.78\cdot H(P)$), (c) Detailed ablation studies, (d) TaskWeight and ContentImportance definitions. Without these, the main text's claims are unverifiable. The mutual information numbers (52% for RoPE, 61% for ALiBi, 48% for Shaw, 78% for EPAR) are presented as precise facts with no methodological description in the main text. The evaluation protocol (binning, estimator, input distribution) is entirely missing.

**Fix:** Move at least one representative theorem proof sketch and the information-theoretic estimation methodology into the main text. If this is not possible, remove or heavily caveat the specific numbers.

### W6. Insufficient reproducibility information (Major)
The experimental setup (Section 6.1) provides model architecture but omits: learning rate, optimizer, schedule, warmup steps, batch size, training epochs, GPU hardware, training time, hyperparameter tuning protocol for baselines, and which GLUE subtasks are included. Without these details, the experiments cannot be reproduced, and the reported gains could reflect suboptimal baseline tuning rather than genuine improvement.

**Fix:** Add a hyperparameter table and describe the tuning protocol for each baseline. State: "Baselines were tuned over [grid description] on validation sets."

### W7. Underdeveloped Related Work (Moderate)
The Related Work section (Section 3) is only two paragraphs covering four methods. Several relevant score-level methods (KERPLE, FIRE, xPOS, Sandwich Transformers) are not discussed. This makes it difficult to assess the novelty of EPAR's score-level parametric modulation.

**Fix:** Expand to include head-to-head comparison with ALiBi on the score-level axis and survey other score-level position methods.

### W8. Conclusion does not add synthesis (Minor)
The Conclusion (Section 10) repeats the three contribution bullet points nearly verbatim from the Introduction. It should summarize validated findings, acknowledge remaining gaps (scaling, length extrapolation), and propose a concrete next experiment.

**Fix:** Restructure as: validated findings $\rightarrow$ strongest limitation $\rightarrow$ one concrete next-step experiment.

## Score
**Final Score: 5/10**

**Rationale:** The paper introduces a conceptually interesting approach to position-aware attention through an explicit parametric function at the attention score level, which provides interpretability and analytical potential that implicit methods lack. The empirical evaluation covers diverse tasks with statistical rigor (multiple seeds, effect sizes, confidence intervals). However, the score is constrained by several significant concerns: (1) The central framing contains a factual inaccuracy (ALiBi already operates at the attention score level, contradicting the claimed dichotomy). (2) Core mathematical properties (continuity, differentiability, monotonicity) are presented as novel theoretical guarantees when they are standard calculus facts. (3) A mathematically incorrect claim about the γ-enhanced function guaranteeing a non-zero lower bound for attention weights (the bound applies to pre-softmax scores, not attention weights). (4) Many essential results (Theorems 2-5, information-theoretic analysis, key definitions) are in the removed appendix and cannot be verified. (5) Reproducibility details are insufficient. The paper would benefit from a major revision that corrects the mathematical accuracy, verifiably presents the theoretical contributions, and tempers the novelty claims to match what is actually demonstrated. The core idea has merit and the empirical results are encouragingly consistent, but the presentational overreach and factual issues prevent a higher score at this stage.