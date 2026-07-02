## Summary
This paper proposes **Thoughtbubbles**, a transformer variant that learns to dynamically allocate parallel computation by forking and pruning residual streams during standard language model pretraining. The core mechanism uses learned cumulative scores per stream to decide which residuals to duplicate (fork) or delete, with attention and residual updates attenuated by these scores. Outputs from multiple forked streams are averaged weighted by cumulative scores. Experiments at 150M–772M scales on OpenWebText and peS2o show consistent perplexity improvements (0.7–1.5 points) over parameter-matched baselines and a computation-matched Copy-N baseline, with gains on zero-shot LAMBADA and HellaSwag. Analysis reveals fork count correlates with output entropy, suggesting interpretable adaptive behavior.

**Overall assessment:** The paper introduces a genuinely novel mechanism for latent-space adaptive computation trained with only LM loss—a promising direction. However, the experimental validation has several weaknesses: the Copy-N baseline is structurally disadvantaged, comparisons conflate parameter efficiency with FLOPs, causal attribution for gains over baselines is unconfirmed, novelty claims are over-reaching, and key reproducibility details in the forking formulas need clarification. With substantial revisions to claims, baselines, and analyses, this work could make a meaningful contribution to efficient transformer architectures.

## Strengths
1. **Novel conceptual direction.** The idea of learning to dynamically fork residual streams during standard LM pretraining—without auxiliary supervision, special tokens, or prompting—is a genuinely fresh approach to adaptive computation. It moves beyond test-time CoT prompting and hand-designed pause tokens by making adaptivity a learned, training-native property.

2. **Clean, self-contained mechanism.** The forking + cumulative scoring + top-k pruning + score-attenuated computation forms a coherent end-to-end architecture. The use of cumulative scores to simultaneously control forking decisions, attention, and residual updates is elegant and avoids separate optimization loops.

3. **Consistent perplexity improvements.** The results show Thoughtbubbles improves perplexity over both the baseline transformer and the Copy-N baselines across all model sizes (150M, 319M, 772M) and both datasets (OpenWebText, peS2o). The improvement is monotonic with larger κ, which suggests the mechanism scales as expected.

4. **Interpretable allocation analysis.** The correlation between fork count and output entropy (Figure 5) provides a plausible signal that the model allocates computation where it is most needed—a valuable interpretability result that goes beyond "our model is better" to show *how* it allocates resources.

5. **Open Science commitment.** The authors commit to releasing pretrained models and PyTorch implementation, which is essential for reproducibility and community adoption given the architectural novelty.

## Weaknesses
### W1. Overclaimed novelty and "first" assertions (High severity)
The paper repeatedly uses strong novelty language—"first-known architecture" (Contribution 1), "unlocks the previously missing input-adaptivity" (Conclusion)—without rigorous literature verification. The related work itself cites pause-token methods (Herel & Mikolov, 2024; Goyal et al., 2024; Sun et al., 2025) as "most similar" to Thoughtbubbles, explicitly acknowledging that additional residual stream insertion has been explored before. The paper also cites adaptive computation methods (Graves, 2016; Dehghani et al., 2019) that learn when to allocate extra compute. The *specific combination* (forking + cumulative scores + score-attenuation) may be novel, but the broad category claims are not credible without a thorough literature search, which is unavailable in this run (Retrieval-Disabled Mode).

**Required action:** Replace "first-known" with precisely scoped claims. Qualify "previously missing" to reflect that prior pause-token methods exist but use a different mechanism. All novelty statements should be bounded to the specific mechanism combination, not the general problem. External literature verification is needed before final publication.

### W2. Weak Copy-N baseline undermines empirical comparison (High severity)
The primary computation-matched baseline copies input residuals N times and runs them through the same transformer. This baseline is structurally disadvantaged because (a) it adds uniform computation to *all* tokens rather than adaptively allocating, (b) it introduces redundant positions that increase sequence length and dilute attention, and (c) it has no learnable gating mechanism. Any method that selectively allocates computation would likely outperform it. Comparing against this baseline does not demonstrate the superiority of *adaptive* computation—it only shows that non-uniform allocation is better than blindly duplicating tokens.

**Required action:** Add at least one stronger baseline that also learns adaptive computation: e.g., Universal Transformer with adaptive depth, early-exit transformers, or a mixture-of-experts variant that learns to route to more experts for harder tokens. Report actual FLOP counts (not "roughly matched") for all methods.

### W3. 319M vs 772M comparison conflates parameter efficiency with compute budget (High severity)
The paper highlights that "our approach at a 319M parameter scale has lower perplexity on OpenWebText than the baseline approach at the 772M scale." This is misleading because the 319M Thoughtbubbles model with κ=4L uses significantly more per-token computation than a standard 319M forward pass—the forked streams and top-κ expansion create more FLOPs per token. The comparison confounds parameter count with compute budget. A 319M model with 4× compute per token will naturally outperform a 772M model with 1× compute per token on perplexity, which measures quality per token, not efficiency.

**Required action:** Report FLOP-matched comparisons: compare Thoughtbubbles at a given FLOP budget against a standard transformer that uses the same total FLOPs per sequence. Restate the 319M vs 772M claim with explicit qualification that the comparison involves different per-token compute budgets.

### W4. Causal attribution for gains is unconfirmed (Medium severity)
The paper implicitly attributes performance gains to the adaptive forking mechanism, but there is no ablation that controls for the extra parameters introduced by the forking layers (decision functions, fork embeddings). A matched-parameter baseline that uses the same number of layers and parameters but with uniform (non-adaptive) scores would isolate the effect of adaptivity. Without this control, gains could plausibly come from the additional learned parameters rather than the adaptive allocation itself.

**Required action:** Add an ablation experiment: "Thoughtbubbles-Uniform" where keep/fork scores are fixed to 1.0 (no adaptivity) but the extra forking-layer parameters are retained. Compare its performance against full Thoughtbubbles to quantify the benefit of adaptivity alone.

### W5. Forking mechanism has ambiguities affecting reproducibility (Medium severity)
The forking formulas (Section 2.3) contain several ambiguities: (a) Eq (1) produces scalar scores p_fork and p_keep without clarifying whether they are broadcast across the d_model dimension; (b) the top-k operation over the interleaved fork/keep score list leaves unclear whether a stream can be both kept and forked simultaneously; (c) there is a direct contradiction between Eq (4), which forces the rightmost token's keep score to 1, and the text on line 57, which says "the rightmost token does not have forced-maximum score of 1, allowing the model to ignore the rightmost token." These issues must be resolved before the method can be reliably reimplemented.

**Required action:** Resolve the Eq (4)/text contradiction definitively. Specify the dimensionality and broadcasting semantics of fork/keep scores. Clarify whether fork and keep scores compete in the same top-k selection or are applied sequentially.

### W6. Related Work lacks structured comparison (Medium severity)
The Related Work section reads as three independent literature summaries (CoT, Adaptive Computation, Latent Computation Analysis) without comparison axes or explicit differentiation between Thoughtbubbles and the most related methods. The "most similar to our approach" claim in the Adaptive Computation paragraph does not state what exactly overlaps and what is different, leaving the novelty position unclear.

**Required action:** Reorganize Related Work around 2-3 comparison axes (e.g., explicit vs implicit token insertion, serial vs parallel, fixed vs dynamic budget). For each axis, state where prior methods fall and where Thoughtbubbles differs.

### W7. Incomplete limitation disclosure (Medium severity)
The Limitations section acknowledges three issues but omits critical threats to validity: (a) lack of ablation for causal attribution (related to W4); (b) training-inference distribution mismatch (forking decisions during training see broader context within the block); (c) no analysis of fork quality under varying sequence lengths. Adding these improves scientific transparency.

**Required action:** Add the missing limitations discussed in the annotation at Page 9 - Limitations.

### W8. Abstract introduces speculation not supported by experiments (Low severity)
The abstract concludes with "paving the way to unify train-time and test-time scaling behaviors," which is a speculative statement not supported by any experiment in the paper. No scaling law analysis is conducted, and no evidence links Thoughtbubbles' behavior to any unification of train/test scaling.

**Required action:** Remove this sentence or replace with a grounded version: "enabling adaptive computation to be learned during pretraining without auxiliary supervision."

### W9. Entropy-allocation analysis confounds correlation with causation (Medium severity)
The analysis showing fork count correlates with output entropy is interpreted causally ("learned to allocate more computation at regions of higher uncertainty"). However, the fork scoring function is a learned projection of the residual stream, and residual norm also correlates with token difficulty. The observed entropy correlation could be an indirect effect of activation magnitude rather than a calibrated uncertainty signal. A control analysis (partial correlation with residual norm held constant) is needed to support the causal interpretation.

**Required action:** Add a control analysis: report the correlation between fork count and residual norm alongside the entropy correlation. If both are similarly strong, revise the interpretive language to reflect uncertainty-driven *or* magnitude-driven allocation.

### W10. Absence of variance reporting and significance tests (Low severity)
Table 1 reports single-point estimates without standard deviations or significance tests. Given the small improvement margins (perplexity differences of 0.3–1.5 points), statistical noise could affect rankings. Multi-seed experiments (at least 3) with confidence intervals are standard practice for LM pretraining comparisons.

**Required action:** Add multi-seed variance estimates for at least the 150M and 319M configurations. Report significance for the key comparison (Thoughtbubbles vs baseline at each scale).

## Score
**Final Score: 5/10**

**Rationale:** The paper introduces a genuinely novel architectural mechanism (forking + cumulative scoring + score-attenuated computation) for learning adaptive computation during standard LM pretraining—this is a promising research direction with conceptual merit. However, the current validation has significant weaknesses that substantially limit the confidence in the claimed contributions:

- **Research value (primary dimension):** The core idea is interesting and could influence future architecture design, which is valuable. Score contribution: +2.5 (moderate-high value).
- **Novelty (primary dimension):** The specific mechanism combination appears novel, but the broad "first-known" claims are overreaching and unsupported by literature verification (deferred). The paper's own related work acknowledges closely related pause-token methods. Score contribution: +1.0 (moderate novelty with scope overclaim).
- **Validity/soundness:** Key empirical claims are undermined by weak baselines (Copy-N), confounded comparisons (319M vs 772M conflating parameters with FLOPs), missing ablation for causal attribution, ambiguous formulas affecting reproducibility, and no variance reporting. Score contribution: +0.5 (substantial validity concerns).
- **Reproducibility:** The forking formulas contain contradictions and ambiguities that would hinder reimplementation. Score contribution: +0.5.
- **Presentation/clarity:** The writing is generally clear and the figures are informative, though the introduction storyline could better establish stakes and the related work lacks structured comparison. Score contribution: +0.5.

**Total: 5/10** — This is a borderline paper. The core idea is interesting enough to warrant further development, but the current experimental validation does not meet the standard for acceptance at a top venue. With major revisions addressing the baseline fairness, causal attribution, claim calibration, formula clean-up, and addition of a stronger adaptive baseline, the paper could become a solid contribution (target post-revision: 6-7/10).

**Deferred novelty verification:** Due to Retrieval-Disabled Mode in this run, all novelty/comparison conclusions are marked for manual verification. The "first-known" claims should be treated as unverified until a proper literature search is conducted.