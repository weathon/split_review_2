Now let me produce the final consolidated review.

## Summary

This paper adapts n-gram induction heads (originally from NLP) to in-context reinforcement learning (ICRL), specifically within the Algorithm Distillation (AD) framework. The core idea is to replace one transformer attention layer with an n-gram attention layer that explicitly computes n-gram statistics over the input sequence, providing an inductive bias that the authors argue reduces data requirements and speeds up hyperparameter search. The method is evaluated on Dark Room, Key-to-Door, and Miniworld environments (both discrete and pixel-based, the latter via vector quantization), consistently outperforming the AD baseline.

## Strengths

1. **Clean architectural adaptation.** The n-gram induction head from Akyürek et al. is integrated as a drop-in modification of a transformer attention layer, with a sensible VQ-based quantization scheme to handle image observations. The approach is straightforward to implement on top of existing AD pipelines.

2. **Honest sanity check (Section 4.5).** The permuted-mask experiment — shuffling the n-gram attention matrix to simulate a broken matching mechanism — tests whether a malfunctioning n-gram layer harms performance. The result (no significant difference from baseline) provides useful evidence that the added component does not degrade performance even when its matching signal is meaningless.

3. **Ablation on n-gram hyperparameters (Section 4.4).** Tables 1(a) and 1(b) show that n-gram length and layer position have little impact on final EMP, suggesting the method does not introduce expensive new hyperparameter tuning overhead. This is a genuinely helpful result for practitioners.

4. **Consistently positive results across diverse environments.** The n-gram variant outperforms AD across three environment families (Dark Room, Key-to-Door, Miniworld) with both discrete and visual observations, in both low-data and full-data regimes. The improvement is directionally robust.

## Weaknesses

### Fatal

None.

### Major

1. **Single baseline (AD, 2022) against acknowledged alternative approaches.** The paper cites Lee et al. (2023), retrieval-augmented ICRL (Schmied et al., 2024), data augmentation (Kirsch et al., 2023), and noise-curriculum methods (Zisman et al., 2024) as prior work addressing the same data-efficiency bottleneck in ICRL. Despite this, the *only* baseline in every experiment is the original 2022 AD method. The paper distinguishes its approach as "model-centric" versus data-centric, but since the stated goal — reducing data requirements for ICRL — is shared, comparison against at least one of these alternative approaches is necessary for the reader to assess the method's relative value. Without it, the contribution is evaluated against a 3-year-old baseline that the paper itself agrees is known to have data efficiency problems.

2. **Hyperparameter "sensitivity" claim conflated with performance ceiling.** The paper claims n-gram heads "make the search for optimal hyperparameters quicker" (Section 4.1 title) and "mitigate hyperparameter sensitivity" (abstract, contributions). The supporting evidence (Figure 2, EMP curves) shows that the n-gram model reaches a higher expected max return with fewer hyperparameter assignments. This is equally consistent with the n-gram model having a higher performance ceiling at any reasonable hyperparameter setting. A model that is genuinely *less sensitive* to hyperparameters should exhibit lower variance across the hyperparameter sweep, or maintain good performance across a wider range of values relative to its peak. The paper reports neither. The EMP metric primarily reflects how quickly a good configuration is found and how high the ceiling is — it does not isolate sensitivity. The faster-convergence claim is supported; the reduced-sensitivity claim is asserted without corresponding evidence.

### Minor

3. **The 27× data reduction figure cannot be cross-checked from the numbers given in the main text.** The paper states that AD requires 2048 goals and 2048 learning histories, while the n-gram method uses 100 goals and (in Figure 4) 500–1000 histories. Computing 2048/100 = 20.48×, not 27×; computing (2048×2048)/(100×500) ≈ 83.9×. The paper defers the arithmetic to Appendix B. Whatever the correct computation (episode lengths likely differ), a headline efficiency factor that cannot be roughly verified from the paper's own stated numbers is a presentation weakness that undermines trust in the claim.

4. **Parameter count is not controlled.** The n-gram layer adds learnable parameters (W₁, W₂, MLP) that the baseline transformer does not have. The paper explicitly searches over hyperparameters that "do not change the parameter count of the model," but this means the n-gram model has more total parameters at every search point. Any improvement could partly reflect increased model capacity rather than the inductive bias of n-gram matching. A matched-parameter-count augmentation (e.g., an additional standard transformer layer or expanded MLP) would be a stronger control.

5. **The n-gram matching mechanism for RL trajectories is underspecified.** Equation (1) defines matching over raw input tokens, but the RL input is a heterogeneous sequence (s₀, a₀, r₀, s₁, a₁, r₁, ...). Section 2.3 describes two matching approaches (full-transition matching and state-only matching), but does not formally connect these to Equation (1) or explain how the n-gram indicator function handles tokens of different types (states vs. actions vs. rewards). The adaptation from homogeneous text tokens to heterogeneous RL sequences needs a clearer formal treatment.

6. **The two matching variants ("states" vs. "[s, a, r]") are not analyzed or discussed.** The paper shows that state-only matching consistently outperforms full-transition matching across Figures 2 and 4, but never discusses why this might be the case or what the different matching strategies imply mechanistically. This is a missed opportunity for insight.

7. **Permuted-mask experiment conditions differ from ablation experiments.** Table 1(c) reports EMP values of 0.51–0.52, while Tables 1(a) and 1(b) report 0.67–0.76 for different n-gram configurations in the same Miniworld-Dark environment. The paper does not explain this discrepancy, making it unclear whether the permuted experiment was run under different data regimes or HP budgets than the ablations it is meant to complement.

### Trivial

None.

## Nice-to-Haves

- **Attention pattern analysis.** Visualizing what the n-gram attention heads actually capture in RL trajectories (e.g., revisiting the same state after looping, visiting the goal state repeatedly after finding it) would ground the mechanism in evidence rather than speculation.
- **Impact of data-generating algorithm on n-gram usefulness.** The paper uses table Q-learning for grid-world and a decaying-noise oracle for image environments, but does not discuss whether the type of data-generating algorithm affects the utility of n-gram matching. Given AD's known sensitivity to the learning pace of the data source, this connection merits exploration.

## Removed Points

These were flagged in the input review but are not included as weaknesses per the filtering rules:

- **"Abstract's claim stated before method is introduced":** This is a style nitpick about abstract conventions, not a substantive weakness.
- **"Transitivity should be transience":** Word-level/typographical issue of the type the parser may introduce; not authorial content error.
- **"27x computation deferred to Appendix B (stripped)":** The appendix exists in the original submission; the weakness is reframed as the arithmetic not being checkable from main-text numbers (point 3 above), not as the appendix being absent.
- **"No parameter-matched baseline even though augmentation would be straightforward":** Already covered by point 4 above; the removed framing was about missing experimental detail rather than the core concern about capacity vs. inductive bias.
- **"Section 3.3 does not discuss whether data-generating algorithm affects n-gram usefulness":** Scope creep beyond what is standard for an empirical demonstration paper.
- **"Section 4.1 vs 4.2 structurally identical":** Both use EMP curves but test different hypotheses (HP search efficiency vs. data efficiency); the metric is shared but the independent variables differ.
- **Generic strengths claimed about problem importance:** Removed because they are not specific to this paper's execution.
- **Strength about "addresses a genuine bottleneck":** Generic; applies to any paper working on data-efficient ICRL.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one alternative ICRL efficiency method as a baseline (e.g., noise-curriculum AD [33] or retrieval-augmented ICRL [26]) to enable relative assessment.
2. Clarify the hyperparameter claim: report variance or IQR across the hyperparameter sweep, or frame the contribution as "faster convergence to good hyperparameters" rather than "reduced sensitivity."
3. Provide the 27× computation transparently in the main text. Show the total transition counts for both methods with the assumptions stated.
4. Add a parameter-matched baseline by increasing the baseline transformer's capacity (e.g., adding a layer or widening the MLP) to match the n-gram model's parameter count.
5. Formally define how the n-gram indicator function in Equation (1) operates on the heterogeneous RL sequence, and discuss why state-only matching consistently outperforms full-transition matching.

## Score and Decision

The paper tackles a real problem with a clean architectural idea, produces consistently positive results across multiple environments, and includes thoughtful ablations. However, the single-baseline comparison against only the 2022 AD method — while multiple more recent approaches to the same problem are cited — is a significant limitation that prevents the reader from assessing the method's relative value. The hyperparameter sensitivity claim is also overstated relative to the evidence (EMP curves alone do not isolate sensitivity from ceiling effects). The core idea is sound and the results are directionally clear, but the evidence as presented is not strong enough to fully justify the paper's stronger claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>