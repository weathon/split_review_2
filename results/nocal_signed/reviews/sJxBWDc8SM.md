Now let me write the final consolidated review.

## Summary

This paper systematically compares SSMs (Mamba, Hyena) and Transformers on multi-query associative recall (MQAR) and copying tasks. It demonstrates that SSMs exhibit a critical optimization instability — their success is confined to a narrow learning rate window — while Transformers are robust across orders of magnitude. It further shows SSMs favor scaling in width while Transformers favor depth, identifies the 1D convolution as the source of 1-layer Mamba's expressivity advantage over 1-layer Transformers, and demonstrates that DeltaNet (a newer SSM architecture) achieves Transformer-like LR robustness.

## Strengths

- **Well-motivated and timely question (Section 1).** The paper cleanly identifies the unresolved tension between theoretical expressivity analyses and empirical scaling studies on whether SSM-Transformer performance gaps are due to expressivity or optimization, and designs experiments to address it.

- **Striking and well-visualized LR sensitivity finding (Figure 1).** The log-scale LR sweep shows a dramatic contrast: Attention maintains near-perfect accuracy across two orders of magnitude of LR, while Mamba and Hyena succeed only at a single specific value. The dashed lines marking prior work's LR choices (missing the optimal region) make the practical implication concrete.

- **Scalability insight (Figures 3, 4; Table 1).** The finding that SSMs favor width over depth while Transformers favor depth over width is practically useful for fair comparisons. The demonstration that 1-layer Mamba can solve MQAR while 1-layer Transformer cannot (Figure 3), and that this reverses at 2 layers, is a clean result with implications for architectural comparisons.

- **Concise ablation locating the source of 1-layer expressivity (Table 2).** Removing the 1D convolution from 1-layer Mamba collapses accuracy to 2% (matching 1-layer Transformer failure), and adding a convolution before QKV raises 1-layer Transformer accuracy to 99%. This cleanly identifies a specific architectural component as the root cause.

- **DeltaNet as constructive existence proof (Figure 7).** Showing DeltaNet achieves Transformer-like LR robustness demonstrates the instability is not inherent to all recurrent formulations and provides a concrete architectural clue (Householder-based updates avoiding vanishing off-diagonal terms) for future work.

## Weaknesses

### Major

- **The central thesis is overclaimed relative to the evidence.** The paper states (line 39): *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics."* However, the paper's own results show clear practical expressivity differences: 1-layer Transformers cannot solve MQAR at any LR or width (Figure 3), while properly-tuned 1-layer Mamba can. The paper itself acknowledges "a sizable gap with Transformers can still be observed at low widths" (line 140) and earlier says "while fundamental expressivity issues exist between such model classes" (line 31) before pivoting to the stronger claim. The evidence better supports the weaker claim that both expressivity (through architecture-specific scaling requirements) and optimization difficulty matter, with their relative importance depending on configuration. The empirical contributions stand on their own and would be stronger with a framing that honestly characterizes both factors rather than asserting optimization is the primary differentiator.

- **The induction head analysis (Section 6, Figure 6) is presented as a contribution but lacks mechanistic evidence.** The paper claims a 1-layer Transformer's loss bump "resembles the formation of an induction head circuit" (line 188) and lists this as a key finding (line 45). The only evidence is the shape of a loss curve. No attention map visualizations, head-wise analysis, probing, or causal interventions are provided to verify the well-characterized induction head signatures from Olsson et al. (2022). While the paper uses cautious language ("resembles," "hypothesize"), this is listed as a central contribution and the evidence does not support the specificity of the claim. The paper should either provide mechanistic evidence or reframe this as a loss-dynamics observation without the induction head framing.

### Minor

- **The abstract overgeneralizes the instability claim.** The abstract states "the performance of modern recurrent models suffers from critical instabilities: success is confined to an extremely narrow window of learning rates" — but Section 7 and Figure 7 show that DeltaNet (a modern recurrent model) achieves Transformer-level LR robustness across two orders of magnitude. The paper discusses this nuance in Section 7 (noting Householder-based updates avoid gradient pathology), so the evidence is not hidden, but the abstract and high-level framing present the instability as a universal property of "modern recurrent models" when the paper's own data show it is architecture-dependent.

### Trivial

None.

## Nice-to-Haves

- **Gradient analysis.** The paper invokes vanishing/exploding gradients (lines 13, 23, 221) as the hypothesized mechanism for LR instability but never measures gradient norms. Reporting gradient statistics throughout training would substantially strengthen the explanatory link between architecture and instability.
- **Learning rate schedule investigation.** The paper treats LR as a static hyperparameter; it is possible that SSMs require a specific schedule (warmup, cosine decay) more than a specific initial LR.
- **Optimizer hyperparameter ablation.** A sensitivity analysis over Adam betas, epsilon, or weight decay could determine whether the narrow LR window can be widened through other optimizer choices.
- **Downstream language modeling validation.** The paper acknowledges this as future work (line 235). Showing the LR instability generalizes to perplexity-based training would significantly strengthen the broader claims.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about Table 1 "confounding width and total parameters" (Critic's point 3b).** REMOVED: The critic claimed the paper compares 12L/w=1408 to 12L/w=1024 as a width-vs-depth tradeoff while confounding parameters. In fact, the paper's explicit claim (line 159) compares 24L/w=1024 (150M, 16%) vs 12L/w=1408 (150M, 100%) — a clean same-parameter-count comparison. The 12L/w=1024 (80M) row is an additional baseline. This criticism is factually wrong about the paper's framing.

- **Criticism about 16% being called "fails to copy."** REMOVED: On a copy task where perfect accuracy is expected, 16% is essentially failure. This is a quibble, not a substantive weakness.

- **Generic reproducibility nitpicks about undisclosed hyperparameters, missing appendix content, missing related works.** REMOVED per policy (appendix sections are stripped by the PDF parser; related works speculation is not grounded; hyperparameter details are in Appendix A.2).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the central thesis.** Acknowledge that both expressivity (divergent width/depth scaling preferences) and optimization difficulty (narrow LR windows) differentiate SSMs from Transformers, with their relative importance depending on configuration. The current "not expressive power but optimization" framing is contradicted by the paper's own 1-layer results.
2. **Either strengthen or de-emphasize the induction head claim.** Add mechanistic evidence (attention maps, head probing, causal interventions) for the induction head interpretation in Section 6, or reframe the observation as a loss-dynamics curiosity without the induction head terminology.
3. **Make the abstract's claims conditional on architecture family.** The abstract should acknowledge that the instability characterizes Mamba/Hyena but not DeltaNet, rather than presenting it as a universal property of "modern recurrent models."

## Score and Decision

The paper makes several genuinely useful empirical contributions: documenting LR sensitivity, identifying opposing scaling preferences, localizing the convolution's role, and demonstrating DeltaNet's stability. These contributions are well-supported by clean experiments. The two main weaknesses are (a) an overclaimed central thesis that the evidence doesn't fully support, and (b) a thin induction head claim presented as a contribution. Both are fixable in revision and do not undermine the core empirical findings. The paper would benefit from more precise framing but the experimental work is sound and provides actionable guidance for practitioners working with recurrent models.

**Score:** 7.0  
**Decision:** Accept

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>