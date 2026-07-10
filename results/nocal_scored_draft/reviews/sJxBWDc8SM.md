Now let me write the final consolidated review based on these signals.

## Summary

This paper conducts an extensive empirical comparison of modern SSMs (Mamba, Hyena, Mamba2, DeltaNet) against Transformers on multi-query associative recall (MQAR) and copying tasks. Through over 3,000 training runs, it documents that SSMs succeed only within a narrow learning rate window while Transformers are robust across roughly two orders of magnitude, demonstrates opposing width-vs-depth scaling preferences, and uses ablations to identify the 1D convolution as the critical component enabling 1-layer SSM expressivity. The core empirical contribution — that optimization instability is a substantial confound in SSM-vs-Transformer comparisons — is well-supported and practically important.

## Strengths

- **Figure 1's LR sweep is a clear and impactful finding.** Mamba and Hyena achieve high accuracy only within a narrow LR window (~1e-4 to ~3e-4 for Mamba), while Attention remains near-perfect across roughly two orders of magnitude. The contrast with Arora et al. (2023)'s grid makes it vivid that prior comparisons may have missed the optimal LR entirely.

- **The scaling analysis (Section 4, Figures 3–4) revealing opposite width/depth preferences is informative.** 1-layer SSMs benefit from width scaling while 1-layer Transformers do not (and cannot solve MQAR at any width); 2-layer Transformers solve the task at the smallest tested width while SSMs need width to match. This cleanly documents a genuine architectural difference.

- **The convolution ablation (Section 7, Table 2) is clean and mechanistically illuminating.** Removing the 1D convolution from 1-layer Mamba drops accuracy to 2% (matching the 1-layer Transformer); adding a convolution to 1-layer Attention raises it to 99%. This provides a crisp empirical identification of the conv1d as the critical component enabling 1-layer expressivity.

- **The DeltaNet comparison (Figure 7) provides concrete evidence that LR instability is not inherent to all recurrent formulations.** DeltaNet achieves Transformer-like LR robustness on MQAR, which is both practically relevant and theoretically informative.

## Weaknesses

### Major

- **The paper's central thesis is framed inconsistently.** Line 39 states: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics."* However, the paper's own evidence reveals genuine expressivity differences that this framing obscures: (a) 1-layer Transformers cannot solve MQAR at any width while 1-layer SSMs can (Section 4, Figure 3) — this is an expressivity difference; (b) Mamba without conv1d performs identically to the 1-layer Transformer (2%, Table 2) yet retains its narrow LR window, showing LR sensitivity and task-failure are partially decoupled rather than the gap being "mainly" about optimization; (c) 2-layer SSMs at small widths still underperform 2-layer Transformers even with optimal LR (Figure 2). The abstract's phrasing (*"not just in their expressivity but in their fundamental learnability"*) is more accurate. The claim that the gap is *mainly* about optimization is not consistently supported by the evidence, and the introduction should be revised to match the more nuanced framing used elsewhere in the paper.

### Minor

- **The induction head interpretation (Section 6) is supported only by a loss-curve bump.** In Olsson et al. (2022), induction head formation was diagnosed through converging signals: sharp loss drop, attention pattern analysis showing prefix-matching, head importance analysis, and logit-lens inspection. None of this is provided here. A loss bump without any attention-mechanism analysis could equally arise from optimization escaping a saddle point, feature competition, or other causes. The paper does use hedging language ("resembles," "hypothesize"), but presenting this as a contribution finding that "a 1-layer Transformer also exhibits a loss drop reminiscent of induction head formation" overstates the evidence. Either add mechanistic evidence or reframe as a tentative observation.

- **The vanishing-gradients explanation for SSM instability is hypothesized but never directly tested.** The paper attributes SSM optimization difficulty to vanishing/exploding gradients (lines 23, 221–222) and specifically points to the decay rate in the A matrix causing off-diagonal terms to vanish, yet provides no gradient norm plots, no spectral analysis of transition matrices, and no comparison of gradient magnitudes between Mamba and DeltaNet. Given that optimization dynamics are the paper's central focus, this missing evidence weakens the explanatory narrative. The paper frames this as a hypothesis, but the gap between the asserted mechanism and the evidence is noticeable.

### Trivial

None.

## Nice-to-Haves

- A small-scale language modeling experiment (e.g., perplexity on a held-out corpus at fixed compute budget) would broaden the evidential base for the claim that LR instability drives real-world performance gaps. The paper acknowledges this limitation.
- Adding gradient diagnostic measurements (gradient norms per layer, spectral radius of A matrices across training steps) would directly test the vanishing-gradients hypothesis.
- A more precise specification of Arora et al. (2023)'s LR grid (exactly what values, how many points) and how the authors' finer grid compares would strengthen the comparison.

## Removed Points

- *"The entire analysis is on synthetic benchmarks, limiting scope"* — REMOVED because the paper explicitly acknowledges this limitation and scopes its contribution accordingly. Moved to Nice-to-Haves.
- *"Parameter matching asymmetry (Mamba 12×1024 = 80M vs. Attention 12×1024 = 150M)"* — REMOVED because the paper provides a proper parameter-matched comparison (Mamba 12×1408 = 150M achieves 100%), and any asymmetry here favors the baseline (Transformer has more parameters).
- *"Missing gradient diagnostics"* — already covered under Minor weakness on vanishing gradients.
- *"Statistical reporting (relative max-min errors)"* — REMOVED as a minor presentation preference, not a substantive weakness.
- *"Pure formatting/style nitpicks"* — REMOVED as parser artifacts.
- *"Missing related works"* — REMOVED per policy (no external sources to confirm).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Revise the central thesis statement.** Replace the "not in terms of expressive power but mainly" framing (line 39) with the more accurate "not just in their expressivity but in their fundamental learnability" framing already used in the abstract.
2. **Either support the induction head claim** with attention-pattern visualizations and head-ablation experiments (following Olsson et al. 2022's methodology), or reframe the observation neutrally as "a loss bump whose timing coincides with where induction heads would form in deeper models."
3. **Add basic gradient diagnostic measurements** (e.g., gradient norm trajectories, spectral radius of A matrices) to support or qualify the vanishing-gradients hypothesis.

## Score and Decision

Paper: Revisiting Associative Recall in Modern Recurrent Models

This paper makes a solid empirical contribution by documenting that modern SSMs exhibit severe learning-rate sensitivity on associative recall and copying tasks, a phenomenon that can confound prior expressivity comparisons. The scaling analysis and convolution ablation are clean and informative. However, the paper's central thesis is stated too strongly in the introduction (claiming the gap is "mainly" about optimization when the paper's own evidence shows genuine expressivity differences), and two key interpretations (induction head formation, vanishing-gradients mechanism) are asserted without sufficient direct evidence. These are addressable issues that do not undermine the core empirical findings.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>