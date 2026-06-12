## Summary

This paper empirically compares SSMs (Mamba, Hyena, Mamba2, DeltaNet) and Transformers on multi-query associative recall (MQAR) and copying tasks, demonstrating that SSMs have a much narrower optimal learning-rate window than Transformers. Through over 3,000 runs, it shows LR sensitivity is a critical confounder in architectural comparisons, that width-vs-depth scaling strategies differ fundamentally between the two families, and that the 1D convolution is the key component enabling single-layer Mamba to solve recall. The paper does not propose a new method but documents a practically important phenomenon.

## Strengths

- **Figure 1 is a striking and immediately useful finding.** The contrast between Attention's broad LR plateau (near-perfect accuracy across two orders of magnitude) and the narrow, needle-like peaks of Mamba and Hyena is visually unambiguous and directly communicates the paper's core thesis. This provides a clear caution that reported SSM-vs-Transformer performance gaps may be artifacts of incomplete LR tuning — a genuine service to the community.

- **The convolution ablation (Table 2) is clean, symmetric, and mechanistically informative.** Removing the 1D convolution from a 1-layer Mamba drops accuracy from 99% to 2% — matching the 1-layer Attention failure point. Adding a convolution to 1-layer Attention boosts it from 2% to 99%. This bidirectional result isolates the 1D convolution as the critical architectural component for single-layer recall and establishes a concrete mechanistic link between Mamba and Attention.

- **The width-vs-depth scaling analysis provides practical guidance.** Table 1 cleanly demonstrates that parameter-matched comparisons are only fair if the scaling axis matches each architecture's preferred direction (width for SSMs, depth for Transformers). A 12-layer width-1024 Mamba (80M params) scores 0%, while a 12-layer width-1408 Mamba (150M params) scores 100% — compared to 16% for a deeper-but-narrower configuration with the same parameter count.

- **Substantial experimental effort.** Over 3,000 runs and approximately 20,000 GPU hours across multiple models, learning rates, widths, depths, and sequence lengths — an unusually broad empirical scope for an analysis paper at this scale.

## Weaknesses

### Fatal
None.

### Major

- **The central claim overreaches the evidence.** The paper's strongest framing (line 39: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics"*) is contradicted by the paper's own results. 1-layer Attention *cannot* solve MQAR regardless of LR tuning (Figure 3, Table 2: 2% accuracy) — this is a structural/expressivity limitation, not an optimization one. 1-layer Mamba *can* solve the task but only with careful tuning. The actual pattern in the data is more nuanced: *in 2-layer settings, optimization is the primary differentiator; in 1-layer settings, expressivity and optimization trade off differently (SSMs win on expressivity, Attention wins on stability).* The conclusion (line 235) partially walks this back to "a crucial differentiator lies not just in their theoretical expressivity, but in their fundamental learnability," which is more defensible but conflicts with the stronger abstract/intro claims. The paper would be more credible if it stratified its thesis by depth from the outset.

### Minor

- **No direct evidence for the hypothesized optimization mechanism.** The paper attributes SSM LR brittleness to "vanishing and exploding gradients" (lines 13, 23, 221) inherited from classical RNNs, but presents no direct optimization measurements — no gradient norm trajectories, no loss-landscape visualizations, no Hessian estimates. A narrow LR window is a symptom, not a diagnosis; many phenomena (sharp minima, gradient noise amplification, ill-conditioned Hessians) produce similar symptoms with different causes. The vanishing-gradient explanation is circumstantial, inferred from architectural similarity to classical RNNs. While the core empirical finding (LR sensitivity exists) does not require a mechanistic diagnosis, the paper's causal framing of *why* SSMs are brittle is unsupported without these measurements.

- **The induction head analysis (Section 6) is too thin for the weight it carries.** The paper observes a loss bump in 1-layer Attention and concludes it "resembles the formation of an induction head circuit" (line 188). This claim is based solely on superficial similarity of loss curves to prior work (Olsson et al., 2022). No attention-pattern analysis, head-by-head attribution, or circuit-level analysis is performed. The paper also acknowledges that induction heads require two layers to function (Section 2), yet invokes them to explain a 1-layer phenomenon — the tension is noted but not resolved with evidence. This section would benefit from either mechanistic evidence or being scaled back to a brief observation.

- **The generalization from synthetic tasks to language modeling is asserted rather than quantified.** The paper states that MQAR and copying are "highly correlated with language modeling performance" (abstract, line 23) and uses this to justify "re-contextualiz[ing] prior performance evaluations" of SSMs vs. Transformers on LMs. While the cited references (Arora et al., 2023; Jelassi et al., 2024) support a qualitative link, the correlation strength is not quantified, and the paper acknowledges this limitation only in the conclusion (line 235). This creates a tension between the paper's strong "re-contextualizing" claims and its synthetic-only experimental scope.

- **The DeltaNet comparison is preliminary.** Testing is limited to model dimension ≤ 256 due to implementation constraints (line 231), and no discussion of computational cost or expressivity trade-offs is provided. The claim that Householder matrices avoid gradient decay (line 221) is a hypothesis, not a demonstrated mechanism.

### Trivial
- Figure 2 does not specify which LR value from the finer grid was used for the "Our" results — whether it was the best per-configuration LR or a single fixed LR per model class. This matters for exact reproducibility.

## Nice-to-Haves
- Adding gradient norm measurements (trajectories for one LR near the optimal peak and one LR outside it) would transform the speculative mechanistic claims into actual evidence.
- Testing whether modern LR schedulers (cosine decay, warmup) mitigate SSM LR sensitivity would substantially strengthen the practical relevance.
- Studying whether tuning Adam hyperparameters (β₂, ε) could broaden the SSM LR window would be informative, even as a negative result.
- A brief study of batch size effects, since batch size interacts with LR sensitivity.

## Removed Points
- *"The LR grid methodology is under-specified for the main paper"* — REMOVED: The paper states that grid specifics are in Appendix A.2. Per policy, criticisms of appendix content stripped by the parser are not valid.
- *"Reproducibility concerns about undisclosed hyperparameters"* — REMOVED: Code is released and hyperparameters are documented in the (stripped) appendix per the reproducibility statement.
- *"No study of batch size effects"* and *"No baseline with modern LR schedulers"* — MOVED to Nice-to-Haves (these are extensions, not core flaws).
- *"The paper does not discuss optimizer hyperparameters"* — MOVED to Nice-to-Haves.
- *Generic strengths about addressing an important problem* — REMOVED: Not specific to the paper's evidence.

## Novel Insights
The most valuable insight emerging from the meta-review is the stratification of the paper's own findings: the SSM-vs-Transformer comparison is not a single story but two distinct regimes — an expressivity-limited regime at 1 layer (where SSMs can succeed and Attention cannot, regardless of LR tuning) and an optimization-limited regime at 2 layers (where both can succeed but SSMs require precise LR tuning). The paper's framing attempts to collapse this into a single "optimization is the main driver" narrative, but the data actually tell a richer story. The convolution ablation (Table 2) is the strongest individual result and deserves more emphasis, as it directly mechanistically links the architectures via a single architectural component. The DeltaNet result, while preliminary, hints at a promising architectural direction that decouples recurrent expressivity from optimization brittleness — a finding whose importance is somewhat understated in the paper's own discussion.

## Suggestions
1. **Resolve the framing mismatch.** Restate the core finding precisely: *in 2-layer settings, optimization is the primary differentiator; in 1-layer settings, expressivity and optimization trade off differently.* This matches the data and is a more interesting result than the blanket claim.
2. **Add gradient norm measurements** for at least one representative configuration to test the vanishing-gradient hypothesis directly.
3. **Either strengthen or downsize the induction head analysis** — add attention-pattern visualizations or reduce it to a brief qualitative observation.
4. **Acknowledge the synthetic-to-real limitation earlier** (abstract/intro, not just the conclusion) to avoid overclaiming about re-contextualizing LM evaluations.

## Score and Decision
Score: 6.5  
Decision: Accept

**Round 1 bracket:** 5.5–7.5. The paper's core findings (Figure 1, Table 2) are solid and well-supported, placing it significantly above the 3–5 range where papers have weak or disconnected experiments. The framing overreach and the absence of gradient measurements prevent it from reaching the 7.5+ tier where execution is near-flawless. Final score 6.5 reflects a clear accept with substantive but addressable weaknesses.

**Calibration anchors used** (all rounds):
- StableSSM (BwG8hwohU4, 5.33, Round 1 band 3.5–5.5): Weaker experimental validation; current paper has much stronger empirical work.
- Deconstructing Good Optimizer (zfeso8ceqr, 6.00, Round 1 band 5.5–7.5): Similar empirical-analysis scope; current paper has more striking core finding but more framing issues.
- Scaling Optimal LR (WYL4eFLcxG, 6.00, Round 1 band 5.5–7.5): Empirical LR study at LLM scale; current paper less computationally intensive but cleaner ablations.
- MambaPEFT (UAKnJMIBwf, 6.00, Round 1 band 5.5–7.5): Application paper with limited novelty; current paper has stronger conceptual contribution.
- Small-scale proxies (d8w0pmvXbZ, 8.00, Round 1 band 7.5–8.5): Near-flawless empirical paper; current paper's framing issues and thin sections keep it below this tier.
- Transformers Learn Higher-Order Optimization (YKzGrt3m2g, 4.25, Round 1 band 3.5–5.5): Theory paper with mixed reviews; current paper has stronger empirical grounding.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>